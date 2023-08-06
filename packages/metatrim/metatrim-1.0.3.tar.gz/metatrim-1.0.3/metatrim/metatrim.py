# M. R. Snyder 2022
# This is really just an example to show I know how to code in python.
# It does not show all of my skills, but since the work I do is proprietary, 
# I cannot post any of it publicly. See my resume for additional details of
# my other skills.

from datetime import datetime
from glob import glob
from itertools import zip_longest
from sympy.utilities.iterables import multiset_permutations
import gzip
import logging
import os
import re
import os

# create a logger
def create_logger(args):
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(args.outDir, f'metatrim_{dt_string}.log')
    # make a logger
    logger = logging.getLogger('metatrim')
    logger.setLevel(logging.DEBUG)
    # different level to stream vs file
    ch = logging.StreamHandler()
    fh = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    ch.setLevel(logging.INFO)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt='%(asctime)s %(name)s [%(levelname)s] %(message)s', 
        datefmt='%d-%b-%y %H:%M:%S')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)

    # let's do this!
    logger.info('Alright, we are metatrimming!')
    logger.info('Here are the inputs:')
    logger.info(args)
    return dt_string, logger


# class for creating primer regex list.
# this really doesn't have to be a class, but now you know I've got class(es).
# also shows some fancy list comprehension
class Primer:
    def __init__(self, seq, deg, logger):
        self.seq = seq
        self.deg = deg
        self.len_seq = len(seq)
        self.num_deg = round(self.len_seq * deg)
        self.logger = logger

    # ensures all bases in primers are in ambiguity dict
    def validate_primers(self):
        err = False
        invalid = []
        for base in self.seq:
            if base.upper() not in iupac_amb:
                invalid.append(base)
                err = True
        if err == True:
            self.logger.error(f'Primer {seq} has invalid base(s) '
                '{", ".join(invalid)}. Aborting.')
            exit()

    # make a list of all permutations of degeneracy in primer sequence for regex
    def make_regex_list(self):
        num_lists = [[1 if bp <= e else 0 for bp in range(0, self.len_seq)] 
            for e in range(0, self.num_deg)]
        num_perms = [[n for n in list(multiset_permutations(i))] for i in num_lists]
        deg_regex_list = ['|'.join(''.join([iupac_amb[self.seq[i].upper()] 
            if n == 0 else '[ATCG]' for i, n in enumerate(perm)]) 
            for perm in perm_list) for perm_list in num_perms]
        return [''.join([iupac_amb[base] for base in self.seq])] + deg_regex_list

# create outDir
def out_dir(out):
    # make output dir if not exists
    if not os.path.exists(out):
        os.makedirs(out)

    # check if this dir is empty
    if len(os.listdir(out)) > 0:
        print(f'{out} is not empty. Aborting')
        exit()

# validate fastqDir input
def validate_fastqDir(in_path, logger):
    if re.search('\*.fastq.gz$', in_path) == None:
        in_path = in_path + '*.fastq.gz'
    in_files = sorted(glob(in_path))
    if len(in_files) == 0:
        logger.error('No fastq.gz input files in glob. Aborting')
        print('No fastq.gz input files in glob. Aborting')
        exit()
    else:
        logger.info(f'{len(in_files)} input files found.')
    if len(in_files) % 2 != 0:
        logger.error('Uneven number of input files. Aborting')
        print('Uneven number of input files. Aborting')
        exit()
    it = iter(in_files)
    in_tuples = [*zip(it, it)]
    if any(re.sub('_R1_', '', f[0]) != re.sub('_R2_', '', f[1]) for f in in_tuples):
        logger.error('At least one sample is not paired end or file names '
            'differ by a pattern other than "_R[12]_". Aborting')
        print('At least one sample is not paired end or file names differ by '
            'a pattern other than "_R[12]_". Aborting')
        exit()
    else:
        logger.info('All input files are paired.')
    return in_tuples

# driver function
def metatrim_driver(indices, deg, forward, reverse, length, min_length, 
    fastq_tups, out_dir, dt_string, logger):
    # write header of summary file
    summary_empty = {'Sample': None, 'total_reads': 0,
                   'r1_index': None, 'i_in_r1': 0,
                   'p1_in_r1': 0, 'p2_in_r1': 0, 'dimers_r1': 0,
                   'r2_index': None, 'i_in_r2': 0,
                   'p1_in_r2': 0, 'p2_in_r2': 0, 'dimers_r2': 0,
                   'metatrimmed': 0
                   }
    with open(os.path.join(out_dir, f'metatrim_summary_{dt_string}.txt'),
        'wt') as summary_file:
        header = "\t".join(i for i in summary_empty.keys())
        summary_file.write(f'{header}\n')
    
    # cycle through input files as sorted paired tuples
    for tup in fastq_tups:
        metatrimmer(indices, deg, forward, reverse, length, min_length, tup, 
            out_dir, dt_string, logger, summary_empty)
    logger.info('That\'s all! Thanks for metatrimming! BYE BYE!')

# this is the meat and potatoes
def metatrimmer(indices, deg, forward, reverse, length, min_length, tup, 
    out_dir, dt_string, logger, summary_empty):
        # empty summary dict
        summary = summary_empty
        # get the sample name
        sample = re.sub('_R[12]_.*', '', os.path.basename(tup[0]))
        summary['Sample'] = sample
        logger.info(f'Processing {sample}')

        # determine index if provided
        if indices[0] is not None:
            index_r1 = index_count(tup[0], indices[0], 1000, deg, logger)
            summary['r1_index'] = index_r1[0]
        if indices[1] is not None:
            index_r2 = index_count(tup[1], indices[1], 1000, deg, logger)
            summary['r2_index'] = index_r2[0]

        # time to open some output files to write to. not using 'with' so they
        # DO NOT close if there is an exception not caught.
        r1_name = os.path.basename(tup[0])
        r2_name = os.path.basename(tup[1])
        out_r1_name = re.sub('fastq.gz', 'metatrimmed.fastq.gz', r1_name)
        out_r2_name = re.sub('fastq.gz', 'metatrimmed.fastq.gz', r2_name)
        out_path = os.path.join(out_dir, os.path.basename(os.path.dirname(tup[0])))
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        out_r1_path = os.path.join(out_path, out_r1_name)
        out_r2_path = os.path.join(out_path, out_r2_name)
        out_r1 = gzip.open(out_r1_path, 'wt')
        out_r2 = gzip.open(out_r2_path, 'wt')

        # trim the reads
        read_buffer_r1 = []
        read_buffer_r2 = []
        with gzip.open(tup[0], 'rt') as infile_r1, \
        gzip.open(tup[1], 'rt') as infile_r2:
            for line_r1, line_r2 in zip_longest(infile_r1, infile_r2):
                read_buffer_r1.append(line_r1.strip())
                read_buffer_r2.append(line_r2.strip())
                if len(read_buffer_r1) + len(read_buffer_r2) == 8:
                    read_r1_name = read_buffer_r1[0].split()[0]
                    read_r2_name = read_buffer_r2[0].split()[0]

                    # check for read name match
                    if read_r1_name != read_r2_name:
                        logger.error(f'Reads in {sample} FASTQ files not '
                            'identically sorted. ABORTING.')
                        print(f'Reads in {sample} FASTQ files not '
                            'identically sorted. ABORTING.')
                        out_r1.close()
                        out_r2.close()
                        break

                    # trim r1
                    if indices[0] is None or re.match(index_r1[1], 
                        read_buffer_r1[1]):
                        summary['i_in_r1'] += 1
                        trim_r1 = trim_primers(forward, reverse, length, 
                            min_length, read_buffer_r1)
                        summary['p1_in_r1'] += trim_r1[2]
                        summary['p2_in_r1'] += trim_r1[3] 
                        summary['dimers_r1'] += trim_r1[4] 

                    # trim r2                      
                    if indices[1] is None or re.match(index_r2[1], 
                        read_buffer_r2[1]):
                        summary['i_in_r2'] += 1
                        trim_r2 = trim_primers(reverse, forward, length, 
                            min_length, read_buffer_r2)
                        summary['p1_in_r2'] += trim_r2[2]
                        summary['p2_in_r2'] += trim_r2[3]
                        summary['dimers_r2'] += trim_r2[4]   

                    # write to file if both reads trimmed                    
                    if trim_r1[0] is not None and trim_r2[0] is not None:
                        read_r1 = (f'{read_buffer_r1[0]}\n{trim_r1[0]}\n+\n'
                            f'{trim_r1[1]}\n')
                        out_r1.write(read_r1)
                        read_r2 = (f'{read_buffer_r2[0]}\n{trim_r2[0]}\n+\n'
                            f'{trim_r2[1]}\n')
                        out_r2.write(read_r2)
                        summary['metatrimmed'] += 1

                    # track total reads
                    summary['total_reads'] += 1
                    if summary['total_reads'] % 1000 == 0:
                        print (f'{sample} metatrimmed reads: '
                            f'{summary["total_reads"]}', end = '\r')
                    read_buffer_r1 = []
                    read_buffer_r2 = []

                # make sure one file is not shorter than the other
                elif len(read_buffer_r1) != len(read_buffer_r2):
                    logger.error(f'Unequal number of reads in {sample} '
                        'FASTQ files. ABORTING')
                    print(f'Unequal number of reads in {sample} '
                        'FASTQ files. ABORTING')
                    out_r1.close()
                    out_r2.close()
        out_r1.close()
        out_r2.close()

        # how many total reads?
        logger.info(f'{sample} total metatrimmed reads: '
            f'{summary["total_reads"]}')
        with open(os.path.join(out_dir, f'metatrim_summary_{dt_string}.txt'),
            'at') as summary_file:
            summary_line = '\t'.join(str(i) for i in summary.values())
            summary_file.write(f'{summary_line}\n')

# trim primers from (both ends of) sequence
def trim_primers(p1, p2, length, min_length, read_buffer):
    p1_end = find_primer(read_buffer[1], p1)
    if length is None:
        p2_end = py_end = find_primer(rev_comp(read_buffer[1]), p2)
        if p1_end is not None and p2_end is not None:
            seq = read_buffer[1][p1_end:len(read_buffer[1]) - p2_end]
            if len(seq) >= min_length:
                qual = read_buffer[3][p1_end:len(read_buffer[1]) - p2_end]
                return [seq, qual, 1, 1, 0]
            else:
                return [None, None, 1, 1, 1]
        elif p1_end is not None and p2_end is None:
            if len(read_buffer[1][p1_end:]) >= min_length:
                return [read_buffer[1][p1_end:], read_buffer[3][p1_end:],
                        1, 0, 0]
            else: 
                return [None, None, 1, 0, 1]
        elif p1_end is None and p2_end is not None:
            return [None, None, 0, 1, 0]
        else:
            return [None, None, 0, 0, 0]
    else:
        if p1_end is not None:
            if len(read_buffer[1][p1_end:]) >= min_length:
                return [read_buffer[1][p1_end:p1_end + int(length)], 
                    read_buffer[3][p1_end:p1_end + int(length)], 1, 0, 0]
            else:
                return [None, None, 1, 0, 1]
        else:
            return [None, None, 0, 0, 0]

# find primer using list of degenerate (or not degenerate) primers
def find_primer(sequence, primer_list):
    for p in primer_list:
        try:
            p_end = re.search(p, sequence).end()
        except AttributeError:
            pass
        else:
            return p_end

# reverse compliment a sequence
def rev_comp(Seq):
    trans = str.maketrans('ATGCN', 'TACGN')
    seqRC = Seq[::-1].translate(trans)
    return seqRC

# count indices in 1st stage PCR to remove index hops and cross contamination
def index_count(fastq, indices, reads, deg, logger):
    logger.debug(f'Counting indices in {fastq}')
    if deg:
        logger.debug('Degeneracy allowed')
        count = {i:[0, '|'.join([i[:x].upper() + '[AGTCN]' + i[x+1:].upper() 
            for x in range(0, len(i))])] for i in indices}
    else:
        logger.debug('No degeneracy allowed')
        count = {i:[0, i] for i in indices}
    read_buffer = []
    processed = 0
    with gzip.open(fastq) as infile:
        for line in infile:
            read_buffer.append(line.strip().decode('ascii'))
            if len(read_buffer) == 4:
                processed += 1
                for i in count:
                    if re.match(count[i][1], read_buffer[1]):
                        count[i][0] += 1
                read_buffer = []
            if processed == reads:
                break
    logger.debug(f'Spacer counts in first {reads} sequences:')
    for i in count:
        logger.debug(f'{i} : {count[i][0]}')
    max_spacer = [i for i in count if count[i][0] == max([count[i][0] 
        for i in count])]
    if len(max_spacer) > 1:
        logger.debug(f'Spacers {max_spacer} both have the max number of counts.')
        if reads < 1000000:
            logger.debug('Counting more spacers...')
            index_count(fastq, indices, reads*10)
        else:
            logger.error('Could not determine proper index for '
                f'{os.path.basename(fastq)} in 1,000,000 reads. Remove this '
                'sample from glob path. Aborting')
            print('Could not determine proper index for '
                f'{os.path.basename(fastq)} in 1,000,000 reads. Remove this '
                'sample from glob path. Aborting')
            exit()
    else:
        logger.info(f'{fastq} has max index {max_spacer}')
        return max_spacer, count[max_spacer[0]][1]

# ambiguity dict
iupac_amb = {'A' : 'A',
            'T' : 'T',
            'C' : 'C',
            'G' : 'G',
            'R' : '[AG]', 
            'Y' : '[CT]', 
            'S' : '[GC]', 
            'W' : '[AT]', 
            'K' : '[GT]', 
            'M' : '[AC]', 
            'B' : '[CGT]', 
            'D' : '[AGT]', 
            'H' : '[ACT]', 
            'V' : '[ACG]', 
            'N' : '[ATCG]'
            }
