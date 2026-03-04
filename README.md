<h1 align="center">GBAS GUI</h1>
A local graphical user interface (GUI) application which enables a user-friendly handling of the GABS-pipeline from https://github.com/mcurto/SSR-GBS-pipeline

## Table of contents
* [Introduction](#introduction)
* [Installation](#installation)
* [Bin](#bin)
* [GUI overview](#gui-overview)
  * [Preparation](#preparation)
    * [Pipeline Parameters](#pipeline-parameters)
    * [Workspace Status](#workspace-status)
    * [Data Preparation](#data-preparation)
    * [Instructions](#instructions)
  * [Pipeline](#pipeline)
    * [Pipeline Details](#pipeline-details)
    * [Length Detection](#length-detection)
    * [SNP Detection](#snp-detection)
  * [Database](#database)
    * [Allelelist Comparison](#allelelist-comparison)
    * [PIC Calculation](#pic-calculation)
    * [Add to Database](#add-to-database)
    * [Extract subset](#extract-subset)
* [Tutorial](#tutorial)
  * [Preparing the data](#preparing-the-data)
  * [Running the pipeline](#running-the-pipeline)
  * [Adding and extracting from database](#add-to-database)
  * [Calculating PIC values for all 4 markers](#pic-calculation)


<h2 align="center">Introduction</h2>
The GBAS pipeline as described in Curto et al. (2019) and Tibihika et al (2019) has been used for genotyping Microsatellites using amplicon sequencing being able to incorporate length and SNP (Single Nucleotide Polymorphism) variation in the allele call. However it also produces genotype data for other marker types, such as from amplicons covering parts of the mitochondrial and chloroplast genomes, nuclear coding regions, and exon primed intron-crossing (EPIC) markers. In all cases the process is done in two steps. First  amplicon sequences resulting from the merging of paired sequences are fused to call genotypes based on length information, mimeking traditional SSR genotyping. Second, the reads corresponding to defined lengths and the most abundant variants considering whole sequence information are used to call alleles. The pipeline is designed to allow a user quality control between both steps. The pipeline consists of multiple parts which need to be executed sequentially one after another to achieve the final high quality genotype call. The final result is a matrix containing codominant genotype information. The consensus sequences of the final alleles are also made available.<br><br>

This manual refers to an updated version of the GBAS pipeline integrating a GUI. The GUI allows easy usage of the GBAS pipeline by detecting errors in the necessary inputs, the possibility of running individual pipeline parts on their own and the option to store detected alleles in a local database using the SQLite3 module. Furthermore in the process of integrating the SSR-GBAS pipeline into the GUI application parts of the original scripts have been rewritten and enhanced to give the user more insight into the intermediate results of pipeline parts and allow a faster processing time while not changing the basic procedure and goal of each script part.<br><br>

To get a quick hands-on overview we refer to the step-by-step tutorial in the [Tutorial](#tutorial) section.<br>

<h2 align="center">Installation</h2>
Users can install the GUI application using Pip with the following command:
<br>

```
pip install --index-url https://test.pypi.org/simple/ --no-deps --upgrade GBAS-package-sonnenbe-vers2
```
<br><br>
After installing the GUI through PIP the user should download the bin folder with the the command:

```
gbas_get_bin_vers2
```


This will copy the folders and files of the bin into a local bin directory at the same location from where the GUI has been installed.
<br><br>

The GUI can be started with the command:

```
gbas_gui_vers2_start
```

<br>

Furthermore in order to run the pipeline the user needs to install Python (>3.10) and Java. All other dependencies are downloaded through the installation process.

<h2 align="center">Bin</h2>
The bin folder contains all the necessary external executables in order to run the GBAS pipeline. This folder must be in the same location as the starting point of the GUI application in order to be recognized. The bin folder will contain the executables for Trimmomatic (REF) and Usearch (REF). The first part of the pipeline calls upon these executables; therefore, they are necessary for the pipeline to proceed.
Below is a graphical view of the bin folder structure.
<br><br>
The bin can be either downloaded through the command as described above.
If users however wish to set up their own bin folder they can follow the next few steps.
<br><br>

&rarr; Download the Trimmomatic binary (http://www.usadellab.org/cms/?page=trimmomatic), unzip the downloaded folder and add it to the bin folder. This folder also contains the adapters subfolder which has multiple FASTA files containing the different illumina adapters. For our purpose of processing pair-end amplicons adapters are used from the TrueSeqAdaptersInUsage.fa file and thus these adapters are used by default. Users have the option to select different adapters.<br><br>
 
&rarr; Next download Usearch (https://drive5.com/usearch/download.html). Choose the correct binary file depending on your Operating System (Windows, Linux, Mac). These binary files are of filetype GZ and as described on the website, you will need gunzip to decompress the GZ file and get the executable (EXE). Put the executable in the bin folder.<br><br>

Once the bin folder is ready the user can proceed with starting the GUI as described above. <br><br>

<h2 align="center">GUI overview</h2>

When first executing the GUI a main window separated into 3 columns will pop up:
**Preparation**, **Pipeline** and **Database**

<br>
<p align="center">
<img width="743" height="468" alt="main_window" src="https://github.com/user-attachments/assets/263fa82d-1092-426e-87f4-eaaf3d48b0c5" />
</p>

**Preparation**: User defined settings necessary to run the pipeline. This includes locations of input and output files and parameters to be used by each step of the pipeline. Here the following options can be found.<br><br>

_Pipeline Parameters_: Add settings required to run the pipeline<br>
_Workspace status_: Checkpoint to evaluate if all the parameters required were added and if they are in conformity<br>
_Data Preparation_: Import necessary samples into another folder to avoid copy pasting all samples<br>
_Instructions_: Short version of the manual<br><br>

**Database**: Option for storing results in a local database, generating filtered outputs and additional utilities <br><br>
_Advance Mode_: Run individual pipeline components on their own provided the necessary input folders are in the same folder as the GUI application.<br>
_Individual Mode_: Run individual pipeline components of the first script on their own. Input folders do not need to be in the same folder as the GUI application.<br>
_Run Length Detection_: Run first part of the pipeline focused on allele call based on amplicon length.<br>
_Run SNP Detection_: Run the second part of the pipeline that takes the outputs from Run Length Detection to call alleles based on whole sequence information.<br><br>

**Pipeline**: Options to actually run the different components of the pipeline <br><br>
_Allelelist Comparison_: Shows differences between 2 Allelists.<br>
_PIC Calculation_: Calculates the PIC value per marker for length-based and sequence-baded allele-matrices per project.<br>
_Add to Database_: Adding genotyping results into a local database incorporating metainformation regarding markers used and individuals genotypes. The necessary inputs are: matrix output from the final pipeline step (JSON), a file with samples metadata information, and the primerfile used for generating the matrix output.<br>
_Database Status_: Shows all alleles currently stored in the local database.<br>
_Extract Subset_: Filtering the stored genotypes and corresponding allele information according to the metadata parameters Project, the metadata parameter and Loci used. Users can generate the matrix output in both CSV and JSON format based on the filtering parameters.<br><br>

<h2 align="center">Preparation</h2>
<h3 align="center">Pipeline Parameters</h3>

The **Pipeline Parameters** button opens a window separated into 4 subwindows: **Folders**, **Files**, **Calculation Params** and **Additional Params**. <br>

<p align="center">
<img width="450" height="496" alt="general_parameters_window" src="https://github.com/user-attachments/assets/1bb1ca89-2ac1-413c-9800-594407ffecdf" />
</p>
<br>

In order for the SSR-GBAS pipeline to start and process data correctly following parameters need to be set:<br>
* Outputfolder: Path to the Folder where all results will be stored. By default the path is set to a folder named “output” located in the user's home directory.
* Bin: Path to the folder named bin containing the necessary third party executables (Trimmomatic, Usearch, both R scripts). The program assumes by default that the bin folder is located at the user’s home directory.
* Rawdata: Path to a folder containing gunzipped FASTQ files of raw amplicon sequencing data (fileending must be fastq.gz!).
* Primerfile: A TXT or CSV file (without a header) containing all primers used for the amplification of the target DNA regions. The Primerfile contains 3 columns separated by comma corresponding to: Name of the marker, sequence of primer forward in 5' -> 3' direction, sequence of reverse primer in 5' -> 3' direction. Furthermore each marker name must have the following format: primername_repetitionmotif (eg. Tn1_ACT). The primer name should only be composed by alphanumeric characters. Non microsatellite markers (eg. EPIC) should have the following name structure: primername_. Below is an example of a primerfile.<br>
<p align="center">
 <img width="344" height="76" alt="primerfile_example_small" src="https://github.com/user-attachments/assets/b2bd7b9c-7144-4bd1-bb99-70ff3d0f40ac" />
</p>

* Samplefile: A TXT or CSV file providing the correspondence between the sample identifier present in the FASTQ files and the final sample name (SampleID). The sample identifier corresponds to the string before the first underscore “_” of the file name. For example, for the file name “P7CS35-P5CS25_S144_L001_R1_001.fastq.gz” the sample identifier would be “P7CS35-P5CS25”.<br>
The Samplefile contains 2 columns separated by ";" or "," : sample identifier, final sample name (SampleID). Below is an example for a samplesheet containing Oak Illumina data:<br>
<p align="center">
 <img width="167" height="113" alt="samplefile_example" src="https://github.com/user-attachments/assets/e7f42b5b-22ae-44f4-91f1-f8529c1d45fc" />
</p>

* Metadata: Path to an existing Metadata file which contains Metadata information per SampleID. The file has at minimum 2 columns SampleID and Project but the user can add up to 3 more columns for metadata, allowing a maximum of 4 different metadata values to be added for the final output of the matrix. The first row must contain headers sample, Project and additional headers if the user chooses to use add more metadata values. Below is an example for a  metadata file for Oak samples:<br>
<p align="center">
<img width="341" height="205" alt="metadata_example" src="https://github.com/user-attachments/assets/45d8aaa6-faba-4fbe-8ef2-5230f3a33c23" />
</p>

* Allelelist: Path to an existing Allelelist file where newly detected alleles will be added. If no path is given then a brand new Allelelist file will be generated at the end of the pipeline run. Allelelist is a file containing a catalog of all alleles called by the pipeline. This catalog allows for results from multiple runs to be combined into a single dataset, since the alleles in this catalog will be used to produce genotype calls of new runs. New alleles and markers are added to the existing allele list.
* Calculation Params: The right upper section of the window has multiple parameters which are all already set to default values and do not have to be changed for the pipeline to run. However they can be optimized depending on the type of amplicon sequencing data. These parameters will be referenced in the various script parts of the Pipeline section below. Further explanation on how they interact with the pipeline can be found in this section.
* Additional Params: These parameters also have default values that do not have to be changed. They will also be referenced in later sections of the manual.<br><br>
*  Databasefilepath: Path to an existing or new SQlite file (.db) for storing results. The default name is database.db and will be created in the same location from where the GUI was executed the first time the user clicks the button _Add to Database_
*  Parameterfilepath: Path to an existing or new parameter file (.txt) for storing all input values chosen. The default name is parameters.txt and will be created in the same location from where the GUI was executed the first time the user clicks the button _Save Params_ <br><br>

<p align="center">
 
***It is important to note that the ”_”separators are important in the filename structure of all intermediate and final output files, so under any circumstances do not add any additional ”_” in the samplenames, primernames and raw data FASTQ filenames besides the ones described above.***
 
</p>
<br><br>

By clicking on Save Params all your set values will be saved in a paramterfile with the name given in parameterfilepath. Every time the GUI is opened the user is asked to input the filepath of the parameterfilepath. If the user just clicks Enter without entering anything the GUI will try to parse the inputs from a default _parameters.txt_ filepath. Failing to do so will result in the GUI not able to parse any inputs. Update Params is useful in case the user wants to make a test run with different  parameters settings. This option saves the parameters but only for the current run and the changes are lost once the GUI is closed. Below is an example for a parameterfile:<br>

<p align="center">
 <img width="546" height="314" alt="paramterfile_example" src="https://github.com/user-attachments/assets/4470e4bf-31a6-43a3-a7ef-fc4a43790ff8" />
</p>
<br>
Lines starting with '#' will be ignored. The remaining lines containing text are of the following format: “parametername = value”. Only the “value” should be changed by the user. Modifying the parameter name will result in the parameter not being recognized by the GUI.<br><br>

A test dataset for the GBAS pipeline for a small set of individuals from oak species (2 samples and 4 markers)  can be  downloaded from the repository and used to test the GBAS workflow yourself.
This consists in a folder containing a samplefile, a primerfile, and the rawdata folder with the gunzipped FASTQ files.
<br><br>

<h3 align="center">Workspace Status</h3>
Clicking on the Workspace Status button allows the user to check if parameters were correctly set preventing to start runs with empty parameters or invalid paths.<br>
The user should also see if the bin folder has been correctly placed and if it contains all necessary executables and adapter files that are needed for parts of the pipeline to execute.<br>
The contents of the samplefile are checked for possible duplicates in both columns (sample identifiers and final sample names), which the user must eliminate or change the FASTQ file names to ensure they are different. Otherwise the GBAS pipeline will  overwrite the  results of the first duplicated entry with the results of the latter duplicate entry. The correct delimiter usage is ("," or ";").
The content and format of the Primerfile is also checked according to uniqueness and correct delimiter usage (","). Primers for Microsatellites have the name structure: primername_motif; while for remaining marker types: primername_ .<br><br>

The use of underscore as a delimiter plays an important role in the identification of the primername and samplename from the initial raw FASTQ files and all intermediate files produced by the different components of the pipeline. More specifically it is used to divide file names into fields that are read by the pipeline.<br>
If the user unknowingly used repeated sample names, the pipeline produces a  warning message. 
At the end of the Workspace Window a message will display if the pipeline is safe to start or not. If it is safe to start (no duplicates in sample file, there are no  missing files in bin, etc.) then the number of input FASTQ files is shown.<br><br>

<h3 align="center">Data Preparation</h3>
In many cases the raw gunzipped FASTQ files will be in an external folder. Copy pasting them all into local machine when the user plans to run the GBAS pipeline locally can be memory- and time intensive, especially since most of the time the user only requires the raw gunzipped FASTQ files corresponding to the Sample Identifiers in the samplesheet. Data Preparation will open a window with the input fields Rawdata, Samplesheet and Output.<br>
<p align="center">
 <img width="265" height="193" alt="data_preparation_window" src="https://github.com/user-attachments/assets/b48c400c-3b05-40d7-be73-698ad47d4ec7" />
</p>
Choosing the paths for Rawdata, Samplesheet and Output the user can import from Rawdata only the FASTQ files which correspond to the Sample Identifiers from the samplesheet into Output, saving memory and time.<br><br>

<h3 align="center">Instructions</h3>
Here the user has the option to see a shortened version of the manual and most important points summarized in a new window. <br><br>

<h2 align="center">Pipeline</h2>
<h3 align="center">Pipeline details</h3>
If all input parameters are set to valid values and no errors are detected by workspace status the GBAS pipeline can start. The middle column of the GUI allows the user to do so in three modes: default mode (each pipeline part runs sequentially one after the other), Advanced Mode (combinations of individual components of the pipeline) and Individual Run mode (run a specific part of the pipeline). The figure showcases the pipeline process.<br>

<p align="center">
<img width="457" height="394" alt="flowchart_pipeline_with_database" src="https://github.com/user-attachments/assets/508cdb3f-0456-4f6d-8229-6cc1c76736aa" />
</p>

<br>
As described above the user has to provide the following inputs in order to run the GBAS pipeline:  a Samplefile making the correspondence between fastq names and final samples IDs, a Primerfile providing information regarding primer sequences, and a folder containing all gunzipped FASTQ files of the raw data.<br><br>

The pipeline produces multiple outputs:
* Allelelist in TXT, JSON and FASTA format containing the catalog of all Allele names and corresponding Sequences per Marker
* Allelematrix in TXT format containing diploid genotype information where each row represents an individual and each pair of columns a marker. The genotypes are coded in two consecutive cells.  Each cell contains an Integer which represents an the Alleleindex whose sequence can be found in the Allele list. Thus the matrix assigns all found alleles to the corresponding samples and markers.
* A Combined Output in JSON format merging information from both Allelelist and Allelematrix. If a valid metadata filepath has been set in _Pipeline Parameters_ then the metadata (Project, etc.) will be added for each SampleID in the JSON output. If no valid metadata filepath has been set then the _Metadata_ field of the combined output will be empty.<br><br>

In order to run the pipeline in normal mode the user can click on the Run Length Detection button to start the first part of the pipeline getting the genotypes based on allele length.  Afterwards the Run SNP Detection can be run for the final allele call.<br><br>

The folders  **QC**, **MergedOut**, **SeparatOut**, **MarkerStatistics** and **MarkerPlots** are created when running Length Detection while the folders **AllelesOut**, **ConsensusOut**, **ConsensusTogether**, **Corrected** and **AlleleCall** when running SNP Detection. These are subfolders of the Outputfolder and will contain all outputs and intermediate files.
The following section explains in detail the main functions and parts of the pipeline.<br><br><br>

<h3 align="center">Length Detection</h3>

The first part of the pipeline runs in five steps: 1st raw reads are quality controlled, 2nd paired reads are merged, 3rd sequences are sorted according to maker, 4th amplicon lengths are counted per individual and marker, and 5th genotypes are defined based on amplicon length.<br><br> 

**Read quality control**:<br>
First raw FASTQ reads are quality controlled with Trimmomatic by removing 3’ low quality portions  (< 20) and trimming adapter sequences listed in the TrueSeqAdapterInUsage.fa adapterfile . More specifically the Trimmomatic is run with the following parameters:<br><br>
“ILLUMINACLIP:adapterfilename:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:20”
<br><br>
Per default the adaperfilename is set as TrueSeqAdaptersInUsage.fa but can be changed in the Pipeline Parameters window in the Files Section (**currently broken!**)<br><br>

More information about these parameters and the resulting output files can be found in the manual of Trimmomatic: http://www.usadellab.org/cms/index.php?page=trimmomatic <br><br>

The resulting FASTQ files are stored in the QC folder. The paired read files contain R1 and R2 in their names corresponding to the forward and reverse directions, respectively.<br><br>

**Merging paired end reads**:<br>
In a second step paired reads are merged into a consensus read covering the totality of the amplicon using Usearch. Usearch takes the paired reads in the QC folder as input and merges both forward and reverse reads storing resulting FASTQ files in the  MergedOUT folder. Usearch runs  with the minimum percentage identity parameter (-fastq_pctid) set to 80% and the maximum number of mismatches parameter (-fastq_maxdiffs) set to 40.<br><br>

**Demultiplexing**:<br>
The Demultiplexing process sorts reads into different markers defined according to the sequences of the amplification primers. Merged amplicon sequences should start and end with the sequences of the forward and reverse primers, respectively. The pipeline compares these parts of the merged read with the primer sequences provided by the user. If the number of mismatches between them is bellow the user defined threshold the read is saved into a new file for the matching marker. The mismatch threshold can be set in the Calculation Params subwindow of the Pipeline Parameters window. By default the mismatch parameter is set to 2.<br>
The pipeline takes the  FASTQ files from the MergedOut folder and saves reads into a FASTA file per marker within the SeparatOut folder. The FASTA files will have the following name structure: _samplename_primername_motif_ (FASTA). Demultiplexing yields a large number of fasta files (number of fasta files = number of primers*number of samples). The advanced pipeline mode (which will be described more in detail later) allows the user to start running the GBAS pipeline from this step if files are already trimmed and merged with other tools.<br><br>


**Calculating read counts per length**:<br>
In the next step the number of reads per amplicon length per sample and marker are counted. The pipeline uses the FASTA files from the SeparatOut folder and saves this information into a STATISTICS file (JSON). This file contains all unique lengths and corresponding counts. This file is stored in the MarkerStatistics folder.

**Length allele call**:<br>
The last step for the first part involves calling alleles based on the length count information saved previously generated STATISTICS file. The corresponding python function calls either diploid or haploid genotypes. The diploid genotype calling picks up to two different lengths as the potential alleles. The criteria is described in detail in Curto et al. (2019).  For haploid mode the most abundant length is chosen as the final allele. 
The resulting lengths are saved in matrix form in a CSV file (column headers representing the primers while row headers representing different individuals ). Alongside a markerplots.pdf is generated plotting amplicon length distribution per sample per marker. The x-axis stands for the length while the y-axis is the relative frequency of said length appearing in the STATISTICS file. The user can use the marker plots to manually control the automatic genotype calling and make changes in the matrix file accordingly. Both the matrix and markerplots files are stored in the Markerplots folder.


<h3 align="center">SNP Detection</h3>

The second part of the pipeline script handles calls to genotypes based on whole sequence information. To make this, possible potential SNP variants within each amplicon length are identified and if verified these are used to phase the data into two alleles per length. Finally, the resulting sequences are used to call alleles. This part runs in four steps.  

**Extracting sequences per length**:<br>
Sequences for  all amplicon lengths used as alleles in the previously generated matrix are extracted from the FASTA files saved in the Separatout folder. Kept reads are saved into a FASTA file per length, sample and marker in the  AllelesOut folder. The output file names contain the same structure as the files from Separatout with the added substring of "Al_Allelelength".

**Making a consensus sequence per length**:<br>
All sequences from each FASTA file in AllelesOut are summarized into a single Consensus sequence. Because all sequences of each AllelesOUT file are now of the same length we can look at each position and determine the frequency for each four possible nucleotides ( 'A', 'C', 'G', 'T'). If one of these reaches a frequency above the Consensus threshold, it is chosen as the most likely option for that position.  If no nucleotide meets this criterion, an “N” is output marking that position as a potential SNP. The consensus threshold is set by default to 0.7 (70%) and it can be changed in the Calculation Params subwindow. Afterwards all Consensus sequences from the same Locus will be grouped together and saved in a single file saved in the ConsensusTogether folder.

**SNP calling**:<br>
The  N’ nucleotides in the consensus sequences are assumed to represent potential heterozygous SNPs. A single consensus sequence can contain multiple “N”s, indicating multiple SNPs. These SNPs are linked, meaning that phased sequences can be inferred based on the frequency of linked nucleotides at the positions marked as “N” 
For example, considering two hypothetical SNPs, A/C and G/T, in different positions of an amplicon, the possible linked nucleotide variants would be AG, AT, CG, and CT. The two most abundant combinations are more likely to represent real variation. This step counts the occurrences of linked nucleotide variants and selects the two most frequent combinations to determine diploid genotypes. If an heterozygote length genotype was called in the first part of the pipeline only the most abundant linked nucleotide variant. The same is done for the haploid mode.
The chosen linked nucleotide variants are used to produce two sequences by replacing the “N” positions with the respective nucleotide combinations. In some cases, more than two (in case of diploid mode) or one (for haloid mode and length heterozygous genotypes) equally frequent most abundant variants are found making this process ambiguous. In this case the genotype is excluded.
The positions containing “N” nucleotides are extracted from the consensus sequences stored at the ConsensusTogether folder. The frequency of  linked nucleotide variants for each length, individual and marker is taken from the FASTA files in the AllelesOut folder. 
If the Consensus sequence contains no ‘N’ it will be considered the final variant.  This process is done for every Consensus sequence from the ConsensusTogether folder and results are saved in the Corrected folder.

**Whole sequence information allele calling**:<br>
The final step involves calling alleles based on whole sequence information. In short,  all sequence variants saved in the Corrected folder are compared with the sequences from the Allelelist, if available. If a match is found, the corresponding index is assigned to that variant. Otherwise, a new index is created and added to the Allelelist.
If an Allelelist is not available, a new index is assigned to every unique sequence while processing all sequence variants across all individuals. The final genotypes are determined based on the indices from the Allelelist. If two different sequence variants are found for a particular individual, the output genotype is a heterozygote, coded with the two different indices of the corresponding sequences. If only one variant is found, the genotype is homozygous and coded with a duplicate of the same index.

 All output files are saved in both TXT and JSON format with the Allelelist also being additionally saved in the FASTA format. If the user has chosen a previous Allelelist as an input, then new alleles will be saved into that Allelelist and the result is an updated Allelelist with both old and new results. 
All final results will be saved in the AlleleCall folder.




<h2 align="center">Database</h2>
Each full run of the pipeline results in an Allelematrix (TXT), an Allelelist (TXT, JSON, FASTA), and their combined output (JSON). The Allelelist contains all found sequence variants while the Allelematrix contains the final genotype table with allele call based on whole sequence information. The user can choose to use the obtained Allelelist as an input in a future run. The Allelelist will be  extended with newly found variants and data from additional individuals and markers. The combined output contains all found allele sequences per marker and per SampleID as well as Metadata information per sample if a metadata filepath has been given. The figure below shows an example for a combined output in JSON format. <br>
<p align="center">
<img width="638" height="457" alt="combined_output_example_oak" src="https://github.com/user-attachments/assets/206ca101-da93-4719-907c-a8838698c527" />
</p>
If no alleles are found per sample locus the _Alleles_ field will be left empty. This is to distinguish between loci which failed for a sample and those that did not. This combined output file can be stored in the local database which will be described in more detail down below. <br> <br>

<h3 align="center">Allelelist Comparison</h3>

<h3 align="center">PIC Calculation</h3>
The GUI offers the option to determine the absolue PIC (Polymorphism Information Content) per Marker for each Project. The button opens a window with fields to enter the paths for Input and Outputfolder.<br>
<p align="center">
 <img width="316" height="332" alt="PIC_calculation" src="https://github.com/user-attachments/assets/3d1d38e6-8047-4e97-9cca-e1f2eb23d9bf" />
</p>

The inputfolder needs to have a specific structure in order for the calculation to process. Below is example figure for the folder structure for PIC calculation of the projects **Spruce**, **Oak**, **Buvi** and **Micromeria**. <br>
<p align="center">
<img width="265" height="493" alt="PIC_folder_structure_4projects" src="https://github.com/user-attachments/assets/55c52a35-368f-4f10-a388-985636a91031" />
</p>
<br>

The inputfolder contains a subfolder per project. Each project folder must contain the 2 subfolders with the exact names **allele_matrices** and **length_matrices** as well as a primerfile with the name _primers.txt_ containing all primers used for the project. The subfolder length_matrices contains all **cleaned** matrices generated by the Length Detection part of the GBAS-pipeline while the allele_matrices subfolder contains all matrices generated by the SNP Detection part of the GBAS-pipeline. All matrices must be in EXCEL (.xlsx) or CSV (.csv) format.<br><br>
3 output files will be generated once the calculation is done:<br>
* _PIC_results.json_ contains the absolute PIC value (both length- and sequence based) for each marker per project, the absolute PIC difference as well as the individual frequencies of each allele appearing per marker (both length- and sequence based). A positive PIC difference indicates indicates an increase in the PIC value when identifying alleles from the length-based allele-matrix to identifying alles from the sequence-based allele-matrix.
* _PIC_additional_info.json_ shows for each project the 5 best performing markers based on absolute length-based and sequence-based PIC values as well as on absolute PIC increase from length-based to sequence-based.
* 1 plot (PNG) containing the boxplots for each project. Each project has 2 boxplots, one representing the PIC values calculated from amplicon-length–based genotypes (AL) and one representing the PIC values calculated from sequence-based genotypes derived from whole amplicon information (WAI).
* 1 plot (PNG) per project showing a histogramm for each marker representing the PIC value differences from length-based to sequence-based values.
* 1 plot (PNG) showing for each marker per project a bar representing the PIC value difference from length-based to sequence-based value and 1 plot (PNG) showing the same for the best 5 performing markers for each project based on the PIC value increase. A bar to the right indicates an increase from length-based to sequence-based while a bar going to the left indicates a PIC drop.<br><br>

Below is a figure showcasing the boxplots for the projects Spruce, Oak, Green Toad and Micromeria.<br>
<br>
<p align="center">
<img width="2000" height="1200" alt="ALL_PROJECTS_PIC_boxplot" src="https://github.com/user-attachments/assets/bd8dc210-bbd9-4b65-9248-fbdb02730769" />
 </p>
<br>
Below is a plot showcasing the PIC value differences for the best 5 performing markers for each of the 4 above mentioned projects.<br>
<p align="center">
<img width="2880" height="1920" alt="ALL_PROJECTS_PIC_diffs_horizontal_best" src="https://github.com/user-attachments/assets/a89c35ce-1461-49be-a6cc-1b36761072c4" />
</p>
<br>

<h3 align="center">Add to Database</h3>

This option allows the user to add alleles from the combined output generated by the last Pipeline part. The input field needed are the path to the combined output, the path to the primerfile used for generating that output and the path to the metadata file if the user has not set the path in _Pipeline Parameters_ yet. <br>
<p align="center">
 <img width="322" height="407" alt="add_to_database_window" src="https://github.com/user-attachments/assets/574d3150-0069-4eda-90b2-d244fc465734" />
</p>
<br>
Once all paths have been set, the content of the combined output will be stored in the database represented by the SQlite database file in the databasefilepath location. <br>
Before the storing process can happen all input paths are checked regarding their format. Furthermore samples with empty Metadata fields will not be added to the database. At the very least each sample needs to have information regarding it's project.<br><br>

A relational structure was chosen and implemented for the database and the figure below showcases the Entity Relationship Model used.<br>
<p align="center">
<img width="612" height="490" alt="relational_database_scheme_with_no_grid" src="https://github.com/user-attachments/assets/ca11b271-f975-4380-9bb6-b5c99ed28e81" />
</p>
<br>
Each rectangle represents a tabular table (entity) and the connected oval forms for each table's columns (attributes). For example the entity Locus contains 3 attributes representing the Locus name, and the used Forward and Reverse Primer sequence to amplify that Locus region. All entities are linked and the numbers above the links indicate the cardinalities, meaning the multiplicities. As an example, the link between Locus and Allele with corresponding cardinalities indicates that for Locus we can have multiple alleles but 1 allele can only belong to one Locus. Each entity has a primary column which uniquely identifies each row of the table.
<br><br>

If it is the first time adding data then a new SQlite database file will be created with the filename given in the databasefilepath field.<br>
Afterwards the content from the input filepaths will be parsed and correctly added to the respective tables of the database. With the _Check Status_ Button the current status of the database will be updated and the current number of alleles will be displayed.<br><br>
After adding the projects Spruce, Oak, Micromeria and Green Toad (for each project the respective matrix, primerlist and metadata) the window will show the number of stored alleles and loci.<br>
<p align="center">
<img width="313" height="436" alt="add_to_database_window_4projects_added" src="https://github.com/user-attachments/assets/d1630d01-8136-4f1b-9cb0-4baef64f7916" />
</p>
<br>

<h3 align="center">Extract subset</h3>
The Extract Subset feature can be used to filter final results. It is separated into 3 columns. Each column represents a different parameter for which we can filter our saved data. For now these parameters are the metadata field Project, the second metadata column (depending what the user put as the second metadata column in the metadata file)  Locus name taken from the primer file. In the future more parameters will be included to enhance the filtering options.<br>
<p align="center">
 <img width="653" height="407" alt="extract_subset_4projects" src="https://github.com/user-attachments/assets/062df2e8-6832-4b3d-add7-bdd4abcf025f" />
 </p>
<br>

<h2 align="center">Tutorial</h2>
This section gives the user a direct and quick hands-on rundown of a typical GBAS process using the GUI. This includes running the GBAS pipeline, adding the results into a local database and calculating PIC values.
For this a test folder containing data for Micromeria has been prepared in the repository.<br>

<h2 align="center">Preparing the data</h2>

First step is to download the content of this folder.<br>
The test folder has data for 4 samples and 4 primers and contains the following:<br>

- 1 samplefile containing the links between between the names of the zipped FASTQ files and the actual sample names
- 1 primerfile giving all the names of the primers used for the sequencing process along with the forward and reverse primer sequences
- 1 metadata file giving meta information (Project, Species, Island) for each sample
- 1 folder containing the raw zipped FASTQ files containing Micromeria sequences for each sample

Because the GBAS process is designed for processing pair-end amplicons each each sample has 2 raw zipped FASTQ files, one containing forward sequences (R1) and one containing reverse sequences (R2), thus in total 8 raw zipped FASTQ files.<br><br>

As a suggestion keep the following workspace structure as below.<br><br>

Next install the GUI application as described in the [Installation](#installation) section. For that make sure to have python (>=3.8) and Pip installed on your system. Furthermore make sure Java is installed.

In Bash

```
java -version
```

Next prepare the bin folder as described in the [Bin](#bin) section. <br><br>

In the end your workspace should have the following structure:<br>
<p align="center">
 <img width="331" height="468" alt="image" src="https://github.com/user-attachments/assets/97deaecd-277b-416c-bdb4-f410b18bb992" />
 </p>
<br><br>

Now that the workspace is ready we can start the GUI with the command:

```
gbas_gui_vers2_start
```

The GUI must be started from the same location as the Bin folder in order for the Bin's contents to be recognized by the GUI!<br><br>
Click on the **Pipeline Parameters** button and set up the mandatory input paths for Rawdata, Primerfile and Samplefile. Furthermore add the path to the Metadata file. All other parameters can be left at their default value. Since the samples are of diploid nature the ploidy entry field will also be left diploid. After this is done choose a name or path for the field Parameterfilepath. The input settings will be saved in a TXT parameterfile with your choosen name.<br><br>

Next click on the **Workspace Status** button to make sure inputs are correctly set. The window has to show the message: <br>
**Mandatory Inputfiles correctly set!** 
<br>
Only then the pipeline will be ready to start.<br><br>

Many processes in the pipeline by default run in parallel and will use all available cores on the system leaving one free. We can change the number of cores in the Pipeline Parameters window in the NumberCores entry field in case we want to leave more CPU processing power for other processes in the background.<br><br>

<h2 align="center">Running the pipeline</h2>

Start the first part of pipeline using the **Run Length Detection** button in the middle column.<br><br>

<p align="center">
<img width="738" height="463" alt="image" src="https://github.com/user-attachments/assets/9b9a7492-1ef4-4493-ac39-035fc89856b9" />
</p>
<br><br>

The first part of the pipeline will produce markerplots (PDF) and the codominant length matrix (in both CSV and JSON format). 
The markerplots file will open automatically once the first part of the pipeline is finished.
<p align="center">
<img width="553" height="485" alt="image" src="https://github.com/user-attachments/assets/a5ba23b9-e3dc-4e94-ade8-9dbd4e64e87a" />
</p>
<br><br>

Since we use 4 samples and 4 primers and our default value for the Ploidy entry field is diploid the dimension of the resulting matrix will be 4x8. If the samples were of haploid nature then the resulting length matrix will be of dimension 4x4.
<p align="center">
<img width="569" height="94" alt="image" src="https://github.com/user-attachments/assets/0ef1f9a6-7b17-427a-b64c-7b04e047ee22" />
</p>
<br><br>

In the next step the second part of the pipeline can be started by clicking on the **Run SNP Detection** button.
<p align="center">
<img width="741" height="464" alt="image" src="https://github.com/user-attachments/assets/fd185d0d-1808-4f2a-9bb9-978b5a9e1cdb" />
</p>
<br><br>

Once the second part finishes a new file (TXT) containing the allele matrix will open. This will be again a matrix of dimension 4x8. 
<p align="center">
<img width="427" height="70" alt="image" src="https://github.com/user-attachments/assets/b14ed42d-a68c-43b8-956d-31677f572332" />
</p>
<br><br>

Along with this an allelelist is produced which shows the actual allele sequences for each number per marker.
<p align="center">
<img width="689" height="266" alt="image" src="https://github.com/user-attachments/assets/2e66aa78-bba5-4bc3-ae28-e02e5f6d895f" />
</p>
<br><br>

Furtheremore a combination of matrix and allelelist will be outputted in a JSON file matrix.json. 
<p align="center">
<img width="521" height="398" alt="image" src="https://github.com/user-attachments/assets/9767772d-f4dc-41eb-b1be-c81bf9c06249" />
</p>
<br>

The metadata field in the above JSON output will be left empty if no metadata input was specified.

<br>
All final outputs will be stored in the folder AlleleCall in the output folder.
<br><br>

<h2 align="center">Adding and extracting from database</h2>

In the next part we will add this output along with the medata into a local SQLite database. We click on the **Add to Database** button in the right column and set the input fields to the primerfile, metadata file and the JSON output of the second pipeline part. If the GUI has not been closed after running the pipeline then the input fields will already be set automatically.
<p align="center">
<img width="355" height="448" alt="image" src="https://github.com/user-attachments/assets/8f004cf2-c67e-4893-baae-47b641e942e0" />
</p>
<br>

The button **Add to local Database** will generate a new SQLite file (DB) with the name choosen in the Pipeline Parameters window. By default this name will just be database. After clicking the button we should see the confirmation that all alleles have been stored.
<p align="center">
<img width="355" height="450" alt="image" src="https://github.com/user-attachments/assets/b77ddfe0-57e6-4436-a9b2-d923103b29bc" />
</p>
<br>
Because the allelelist contains 26 unique alleles we will get the message that all 26 alleles have been stored.<br><br>

Click on the **Update Database Status** to make sure that these database changes are now properly reflected.<br>
<p align="center">
<img width="358" height="446" alt="image" src="https://github.com/user-attachments/assets/9fbe8b8c-8c94-401f-89aa-65cc1e7e7e80" />
</p>
<br>
All 4 Markers yield allele results and we go from 9 amplicon-length–based genotypes (AL) to 26 sequence-based genotypes derived from whole amplicon information (WAI).<br><br>

Click next on the button **Database Status** to show a scrollable list of all currently stored WAI genotypes. 
<p align="center">
<img width="518" height="283" alt="image" src="https://github.com/user-attachments/assets/4ac47878-5f72-47fe-9f41-eaf48308c46d" />
</p>
<br>

Now we can use the **Extract subset** button to extract either the full content of the database or a subset based on the Metadata parameters Project or Metadata2. Metadata2 is a variable paramerter but will always represent the third column of the metadata file which can represent any metadata depending on the individual user. The third subset parameter is the Locus which is represented by the primernames used.
<p align="center">
<img width="521" height="313" alt="image" src="https://github.com/user-attachments/assets/c38904ff-d42c-4860-8c5e-7e73c2e5ff55" />
</p>
<br>

By default all fields are clicked and thus when using the **Download Subset** button the output will be the original matrix in both EXCEL and JSON format. Subset results will be stored in a folder called ***subset_output***.
<p align="center">
<img width="113" height="43" alt="image" src="https://github.com/user-attachments/assets/a7edd4f8-e957-4fc6-a4c6-59e83f59b3e7" />
</p>
<br>

Since we only have processed 1 project, namely Micromeria, our extracted subset will naturally only be a single matrix and in both EXCEL and JSON format. 
Keep in mind that outputs are directly linked to project metadata. Meaning if I were to unclick Micromeria in the Include Project column:
<p align="center">
<img width="521" height="313" alt="image" src="https://github.com/user-attachments/assets/1aa94f79-366b-4da1-b47c-7a8f97ca1a63" />
</p>
<br>

The output will then be an empty matrix since by unclicking the Micromeria field we keep all genotype outputs from Micromeria out from our subset. Remember that the metadata has each sample linked with a certain project name. Unclicking said project name eliminates all the samples from the subset output.<br><br>

<h2 align="center">Calculating PIC values for all 4 markers</h2>
To get a first overview for the performance of all 4 markers (which have the same name as the primers in the primerlist) we can calculate the absolute PIC values and gain some plots for them.<br><br>

First of all is to manually built a workspace with the following structure.<br>
<p align="center">
<img width="211" height="134" alt="image" src="https://github.com/user-attachments/assets/4de4b08b-184e-4412-937c-ed5ed52d2e9b" />
</p>
<br>

The outer foldername is the name of the project, here Micromeria. Then the 2 subfolders must be named _allele_matrices_ and _length_matrices_ . Subfolder _length_matrices_ contains the matrix results from the first part of the script in EXCEL format. This could be multiple matrices depending how many runs we have per project but for the test folder our project only contains 1 length-based matrix. Copy paste the matrix in excel format from the output folder Markerplots into _length_matrices_. We also added the substring "_AL" (Amplicon Length) to it's name to make identify it quickly as a length based allele matrix. Subfolder _allele_matrices_ contains the matrices from the second part of the pipeline in EXCEL format. Since the second part of the pipeline does so far not automatically output the matrix in EXCEL you have to do it manually. Here we also added a "_WAI" (Whole Amplicon Information) substring to the filename to clearly identify it as a matrix based on the whole Sequence Information. <br><br>
Of course the above naming conventions can be changed and are just a suggestion. Most important is that all matrices are in EXCEL format and that subfolder _length_matrices_ contains only length-based matrices and that subfolder _allele_matrices_ only contains allele matrices based on whole sequence information.<br><br>

Click on the **PIC Calculation** button in the GUI to open the window for the PIC calculation process. Set the Inputfolder entry field to the folder containing the above folder structure. Set the Outputfolder entry field to the output folder you wish to store the PIC calculation outputs into. Afterwards click on the **Check Inputs** button to make sure your folder structure is in the correct format. The window should show the message as below.

<p align="center">
<img width="335" height="362" alt="image" src="https://github.com/user-attachments/assets/d1b71037-9720-4900-8c23-41ff403607a7" />
</p>
<br>

Next click on the **Calculate PIC** button to start the PIC calculation process. The chosen output folder will contain multiple files.
<p align="center">
<img width="604" height="115" alt="image" src="https://github.com/user-attachments/assets/e65e0afb-c713-41a5-9cc6-5b9321fb63cc" />
</p>
<br>

The main file will be the boxplot with the name _all_projects_PIC_boxplot_. The plot shows 2 boxplots representing the absolute PIC values of all 4 markers. 1 boxplot represents the PIC values calculated from amplicon-length–based genotypes (AL) and the second boxplot represents the PIC values calculated from sequence-based genotypes derived from whole amplicon information (WAI). 
<p align="center">
<img width="545" height="325" alt="image" src="https://github.com/user-attachments/assets/e01dc0e6-8fa5-409d-b587-d2ade374b381" />
</p>
<br><br>
We can see from the boxplot the increase of PIC values from AL genotypes to WAI genotypes.
