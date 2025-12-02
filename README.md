<h1 align="center">GBAS GUI</h1>
A local graphical user interface (GUI) application which enables a user-friendly handling of the GABS-pipeline from https://github.com/mcurto/SSR-GBS-pipeline


<h2 align="center"> Introduction</h2>
The GBAS pipeline as described in Curto et al. (2019) and Tibihika et al (2019) has been used for genotyping Microsatellites using amplicon sequencing being able to incorporate length and SNP (Single Nucleotide Polymorphism) variation in the allele call. However it also produces genotype data for other marker types, such as from amplicons covering parts of the mitochondrial and chloroplast genomes, nuclear coding regions, and exon primed intron-crossing (EPIC) markers. In all cases the process is done in two steps. First  amplicon sequences resulting from the merging of paired sequences are fused to call genotypes based on length information, mimeking traditional SSR genotyping. Second, the reads corresponding to defined lengths and the most abundant variants considering whole sequence information are used to call alleles. The pipeline is designed to allow a user quality control between both steps. The pipeline consists of multiple parts which need to be executed sequentially one after another to achieve the final high quality genotype call. The final result is a matrix containing codominant genotype information. The consensus sequences of the final alleles are also made available.<br><br>

This manual refers to an updated version of the GBAS pipeline integrating a GUI. The GUI allows easy usage of the GBAS pipeline by detecting errors in the necessary inputs, the possibility of running individual pipeline parts on their own and the option to store detected alleles in a local database using the SQLite3 module. Furthermore in the process of integrating the SSR-GBAS pipeline into the GUI application parts of the original scripts have been rewritten and enhanced to give the user more insight into the intermediate results of pipeline parts and allow a faster processing time while not changing the basic procedure and goal of each script part.

<h2 align="center"> Installation</h2>
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

Furthermore in order to run the pipeline the user needs to install Python (>3.10) and Java. All other dependencies are downloaded through the installation process.

<h2 align="center"> Bin</h2>
The bin folder contains all the necessary external executables in order to run the GBAS pipeline. This folder must be in the same location as the starting point of the GUI application in order to be recognized. The bin folder will contain the executables for Trimmomatic (REF) and Usearch (REF). The first part of the pipeline calls upon these executables; therefore, they are necessary for the pipeline to proceed.
Below is a graphical view of the bin folder structure.
<br><br>
The bin can be either downloaded through the command as described above.
If users however wish to set up their own bin folder they can follow the next few steps.
<br><br>

&rarr; Download the Trimmomatic binary (http://www.usadellab.org/cms/?page=trimmomatic), unzip the downloaded folder and add it to the bin folder. This folder also contains the adapters subfolder which has multiple FASTA files containing the different illumina adapters. For our purpose of processing pair-end amplicons adapters are used from the TrueSeqAdaptersInUsage.fa file and thus these adapters are used by default. Users have the option to select different adapters.<br><br>
 
&rarr; Next download Usearch (https://drive5.com/usearch/download.html). Choose the correct binary file depending on your Operating System (Windows, Linux, Mac). These binary files are of filetype GZ and as described on the website, you will need gunzip to decompress the GZ file and get the executable (EXE). Put the executable in the bin folder.<br><br>

Once the bin folder is ready the user can proceed with starting the GUI as described above. <br><br>

<h2 align="center"> GUI overview</h2>

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

<h2 align="center"> Preparation</h2>
<h3 align="center"> Pipeline Parameters</h3>

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

By clicking on Save Params all your set values will be saved in a paramterfile with the name given in parameterfilepath. Every time the GUI is opened the user is asked to input the filepath of the parameterfilepath. If the user chooses just clicks Enter without choosing anything the GUI will try to parse the inputs from a default _parameters.txt_ file. Failing to do so will result in the GUI not able to parse any inputs. Update Params is useful in case the user wants to make a test run with different  parameters settings. This option saves the parameters but only for the current run and the changes are lost once the GUI is closed. Below is an example for a parameterfile:<br>
 


