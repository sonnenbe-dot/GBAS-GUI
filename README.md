# GBAS GUI
A local graphical user interface (GUI) application which enables a user-friendly handling of the GABS-pipeline from https://github.com/mcurto/SSR-GBS-pipeline


## Introduction
The GBAS pipeline as described in Curto et al. (2019) and Tibihika et al (2019) has been used for genotyping Microsatellites using amplicon sequencing being able to incorporate length and SNP (Single Nucleotide Polymorphism) variation in the allele call. However it also produces genotype data for other marker types, such as from amplicons covering parts of the mitochondrial and chloroplast genomes, nuclear coding regions, and exon primed intron-crossing (EPIC) markers. In all cases the process is done in two steps. First  amplicon sequences resulting from the merging of paired sequences are fused to call genotypes based on length information, mimeking traditional SSR genotyping. Second, the reads corresponding to defined lengths and the most abundant variants considering whole sequence information are used to call alleles. The pipeline is designed to allow a user quality control between both steps. The pipeline consists of multiple parts which need to be executed sequentially one after another to achieve the final high quality genotype call. The final result is a matrix containing codominant genotype information. The consensus sequences of the final alleles are also made available.

This manual refers to an updated version of the GBAS pipeline integrating a GUI. The GUI allows easy usage of the GBAS pipeline by detecting errors in the necessary inputs, the possibility of running individual pipeline parts on their own and the option to store detected alleles in a local database using the SQLite3 module. Furthermore in the process of integrating the SSR-GBAS pipeline into the GUI application parts of the original scripts have been rewritten and enhanced to give the user more insight into the intermediate results of pipeline parts and allow a faster processing time while not changing the basic procedure and goal of each script part.

## Installation
Users can install the GUI application using PIP with the following command:
<br><br>
pip install --index-url https://test.pypi.org/simple/ --no-deps --upgrade GBAS-package-sonnenbe-vers2
<br><br>
After installing the GUI through PIP the user should download the bin folder with the the command:
<br><br>
gbas_get_bin_vers2
<br><br>
This will copy the folders and files of the bin into a local bin directory at the same location from where the GUI has been installed.
<br><br>
The GUI can be started with the command:
<br>
gbas_gui_vers2_start 
<br>

Furthermore in order to run the pipeline the user neers to install Python (>3.10) and Java. All other dependencies are downloaded through the installation process.

## Bin
The bin folder contains all the necessary external executables in order to run the GBAS pipeline. This folder must be in the same location as the starting point of the GUI application in order to be recognized. The bin folder will contain the executables for Trimmomatic (REF) and Usearch (REF). The first part of the pipeline calls upon these executables; therefore, they are necessary for the pipeline to proceed.
Below is a graphical view of the bin folder structure.
