# Megabarcoding Pipeline
This is a pipeline written in python to determine barcode sequences from zipped FASTQ files containing pair-end sequences.

The pipepline uses Trimmomatic for Quality Trimming and Usearch for Merging. Afterwards sequences are demultiplexed according to the primer used (COI, Mitochondrial).
Each file represents a single sample and the module determines the most abundant sequences per file and outputs them into a JSON and FASTA.

