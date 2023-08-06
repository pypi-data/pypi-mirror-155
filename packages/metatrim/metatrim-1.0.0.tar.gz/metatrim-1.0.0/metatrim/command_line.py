#!/usr/bin/env python3

from metatrim.metatrim import Primer, out_dir, validate_fastqDir, create_logger, \
metatrim_driver
import argparse
import os
import sys


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-V', '--version', action='version', 
	    version='metatrim v2.0.0')
	parser.add_argument('-I', '--fastqDir', help='Quoted input glob for '
	    'fastq.gz files. Use wildcards. Paths to R1 and R2 reads '
	    'expected to differ only by "_R1_" and "_R2_". No lane splitting')
	parser.add_argument('-O', '--outDir', help='Output dir path and name for '
	    'trimmed fastq.gz files. Created if does not exist.')
	parser.add_argument('-FP', '--forwardPrimer', help='Forward primer '
	    'sequence or partial for faster trimming. Recommend >=8 bases. More bases '
	    'decreases speed. Supports IUPAC ambiguity')
	parser.add_argument('-RP', '--reversePrimer', help='Reverse primer '
	    'sequence or partial for faster trimming. Recommend >=8 bases. More bases '
	    'decreases speed. Supports IUPAC ambiguity')
	parser.add_argument('-FD', '--forwardDegeneracy', default=0, 
	    help='Proportion allowable error in the forward primer. Recommended: 0 '
	    '- 0.33')
	parser.add_argument('-RD', '--reverseDegeneracy', default=0, 
	    help='Proportion allowable error in the reverse primer. Recommended: 0 '
	    '- 0.33')
	parser.add_argument('-TL', '--targetLength', default=None, help='Length of '
	    'target region. If length is variable, omit and metatrim will trim '
	    'primers from both ends of both reads.')
	parser.add_argument('-ML', '--minLength', default=0, help='OPTIONAL: '
	    'Minimum trimmed read length. Sequences shorter than this length are '
	    'considered primer dimers and removed.')
	parser.add_argument('-R1I', '--r1Indices', nargs="+", default=None, 
	    help='OPTIONAL: Space delimited R1 1st stage PCR indices. Indices must '
	    'be at the very beginning of the read.')
	parser.add_argument('-R2I', '--r2Indices', nargs="+", default=None, 
	    help='OPTIONAL: Space delimited R2 1st stage PCR indices. Indices must '
	    'be at the very beginning of the read.')
	parser.add_argument('-DI', '--degenerateIndices', action='store_true', 
	    help='RECOMENDED: Allow 1 base mismatch in 1st stage indices. Indices '
	    'must have more than 1 base difference or this will cause problems.')
	args = parser.parse_args()

	out_dir(args.outDir)

	dt_string, logger = create_logger(args)

	try:
	    # get input files from glob
	    fastq_tups = validate_fastqDir(args.fastqDir, logger)

	    # validate primers and get regex
	    f_primer = Primer(args.forwardPrimer, float(args.forwardDegeneracy), 
	    	logger)
	    f_primer.validate_primers()
	    f_regex = f_primer.make_regex_list()
	    r_primer = Primer(args.reversePrimer, float(args.reverseDegeneracy), 
	    	logger)
	    r_primer.validate_primers()
	    r_regex = r_primer.make_regex_list()

	    # time to metatrim!
	    indices = [args.r1Indices, args.r2Indices]
	    metatrim_driver(indices, args.degenerateIndices, f_regex, r_regex, 
	        args.targetLength, int(args.minLength), fastq_tups, args.outDir, 
	        dt_string, logger)
	except:
	    # we want the traceback in the log
	    logger.critical('An error occurred during processing. Aborting')
	    logger.exception('Exception raised')
	    raise