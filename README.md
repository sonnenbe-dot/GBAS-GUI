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
_gbas_get_bin_vers2_
<br><br>
This will copy the folders and files of the bin into a local bin directory at the same location from where the GUI has been installed.
<br><br>
The GUI can be started with the command:
<br>
gbas_gui_vers2_start
<br>

Furthermore in order to run the pipeline the user needs to install Python (>3.10) and Java. All other dependencies are downloaded through the installation process.

## Bin
The bin folder contains all the necessary external executables in order to run the GBAS pipeline. This folder must be in the same location as the starting point of the GUI application in order to be recognized. The bin folder will contain the executables for Trimmomatic (REF) and Usearch (REF). The first part of the pipeline calls upon these executables; therefore, they are necessary for the pipeline to proceed.
Below is a graphical view of the bin folder structure.
<br><br>
The bin can be either downloaded through the command as described above.
If users however wish to set up their own bin folder they can follow the next few steps.
<br><br>

&rarr; Download the Trimmomatic binary (http://www.usadellab.org/cms/?page=trimmomatic), unzip the downloaded folder and add it to the bin folder. This folder also contains the adapters subfolder which has multiple FASTA files containing the different illumina adapters. For our purpose of processing pair-end amplicons adapters are used from the TrueSeqAdaptersInUsage.fa file and thus these adapters are used by default. Users have the option to select different adapters.<br><br>
 
&rarr; Next download Usearch (https://drive5.com/usearch/download.html). Choose the correct binary file depending on your Operating System (Windows, Linux, Mac). These binary files are of filetype GZ and as described on the website, you will need gunzip to decompress the GZ file and get the executable (EXE). Put the executable in the bin folder.<br><br>

Once the bin folder is ready the user can proceed with starting the GUI as described above. <br><br>

## GUI overview
When first executing the GUI a main window separated into 3 columns will pop up:
<br>
**Preparation**, **Pipeline** and **Database**
<br>

## Preparation:
User defined settings necessary to run the pipeline. This includes locations of input and output files and parameters to be used by each step of the pipeline. Here the following options can be found.


