# metatrim
**v1.0.4**

**by M. R. Snyder 2022**

***Written for Python 3.6 or later***

***metatrim*** trims paired end metabarcoding reads in gzipped FASTQ files (\*.fastq.gz) for subsequent merging in other programs such as Dada2, Unoise, or OBITools. ***metatrim*** trims primers from reads allowing for user specified degeneracy (sequencing error in the primer region). ***metatrim*** will create trimmed FASTQ files with the same tree structure as the input files in a user specified output directory, which will be created if it does not exist, but the program will abort if this directory is not empty. Output files will end in "metatrimmed.fastq.gz". A log and summary file will be created in the top level of this output directory as well.  
  
First stage PCR indices may be used in metabarcoding experiments to detect index hops and/or cross contamination. A list of one or more of these indices used on the run (or for the sample) may be supplied, allowing metatrim to naively determine the appropriate index for a sample based on the most common present in the reads. Reads that do not possess this index will be removed from the results. Information about the number of reads with the index will be included in the summary file.  
  
A target length can be specified. If so, reads will be trimmed this number of bases from the end of each primer. Alternatively, omit this argument and ***metatrim*** will search for both primers in R1 and R2 reads and trim the intervening region. If the 3' primer in the read is not found the read will be trimmed from the end of the 5' primer to the end of the sequence. Information about the number of trimmed reads and those with the 5' (and 3') will be included in the summary file.  
  
A minimum length may also be supplied. If so, reads less than this length after trimming will be considered "primer dimers" and discarded. Information about the number of reads less than the minimum length will be included in the summary file.  
  
*Note: **metatrim** assumes your FASTQ files have uppercase sequences. Primer and index sequence inputs are case insensitive!*
  
## Installation
To install ***metatrim*** in your path:  
`pip3 install metatrim`  
***metatrim*** will be available as a standalone executable in your path.  
  
## Usage
***metatrim*** is a simple program to use. Issue `metatrim -h` to see the help menu.  
  
### Examples
*Trim 5' primers to target length from reads with no first stage indices:*  
```
metatrim -I "</quoted/input/fastq.gz/glob>" -O </output/dir> \  
-FP <forward_primer_sequence> -RP <reverse_primer_sequence> \  
-FD <forward_primer_error> -RD <reverse_primer_error> \  
-TL <target_length>
```
  
*Trim 5' and 3' primers from reads with no first stage indices. Keep reads >= 50 bp:*  
```
metatrim -I "</quoted/input/fastq.gz/glob>" -O </output/dir> \  
-FP <forward_primer_sequence> -RP <reverse_primer_sequence> \  
-FD <forward_primer_error> -RD <reverse_primer_error> \  
-ML 50
```
  
*Trim 5' primers to target length from reads with first stage indices. Keep reads >= 50 bp:*  
```
metatrim -I "</quoted/input/fastq.gz/glob>" -O </output/dir> \  
-FP <forward_primer_sequence> -RP <reverse_primer_sequence> \  
-FD <forward_primer_error> -RD <reverse_primer_error> \  
-R1I <R1_index1> <R1_index2> ... <R1_indexN> \  
-R2I <R2_index2> <R2_index2> ... <R2_indexN> \  
-TL <target_length> \
-ML 50
```
  
*Trim 5' and 3' primers from reads with first stage indices. Keep reads >= 50 bp:*  
```
metatrim -I "</quoted/input/fastq.gz/glob>" -O </output/dir> \  
-FP <forward_primer_sequence> -RP <reverse_primer_sequence> \  
-FD <forward_primer_error> -RD <reverse_primer_error> \  
-R1I <R1_index1> <R1_index2> ... <R1_indexN> \  
-R2I <R2_index2> <R2_index2> ... <R2_indexN> \
-ML 50
```

## HAVE FUN, *METATRIMMING*!
  
***Note: this program is really just an example that shows that I know how to code and create packages in Python. The work I do is entirely proprietary and so I cannot share any of it publicly. For more information on my other skills, see my resume, email me (msnyder424@gmail.com), or message me on [my LinkedIn](https://www.linkedin.com/in/matt-snyder-phd-03779572/).***