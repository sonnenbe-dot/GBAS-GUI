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

By clicking on Save Params all your set values will be saved in a paramterfile with the name given in parameterfilepath. Every time the GUI is opened the user is asked to input the filepath of the parameterfilepath. If the user just clicks Enter without entering anything the GUI will try to parse the inputs from a default _parameters.txt_ filepath. Failing to do so will result in the GUI not able to parse any inputs. Update Params is useful in case the user wants to make a test run with different  parameters settings. This option saves the parameters but only for the current run and the changes are lost once the GUI is closed. Below is an example for a parameterfile:<br>

<p align="center">
 <img width="546" height="314" alt="paramterfile_example" src="https://github.com/user-attachments/assets/4470e4bf-31a6-43a3-a7ef-fc4a43790ff8" />
</p>
<br>
Lines starting with '#' will be ignored. The remaining lines containing text are of the following format: “parametername = value”. Only the “value” should be changed by the user. Modifying the parameter name will result in the parameter not being recognized by the GUI.<br><br>

A test dataset for the GBAS pipeline for a small set of individuals from oak species (2 samples and 4 markers)  can be  downloaded from the repository and used to test the GBAS workflow yourself.
This consists in a folder containing a samplefile, a primerfile, and the rawdata folder with the gunzipped FASTQ files.
<br><br>

<h3 align="center"> Workspace Status </h3>
Clicking on the Workspace Status button allows the user to check if parameters were correctly set preventing to start runs with empty parameters or invalid paths.<br>
The user should also see if the bin folder has been correctly placed and if it contains all necessary executables and adapter files that are needed for parts of the pipeline to execute.<br>
The contents of the samplefile are checked for possible duplicates in both columns (sample identifiers and final sample names), which the user must eliminate or change the FASTQ file names to ensure they are different. Otherwise the GBAS pipeline will  overwrite the  results of the first duplicated entry with the results of the latter duplicate entry. The correct delimiter usage is ("," or ";").
The content and format of the Primerfile is also checked according to uniqueness and correct delimiter usage (","). Primers for Microsatellites have the name structure: primername_motif; while for remaining marker types: primername_ .<br><br>

The use of underscore as a delimiter plays an important role in the identification of the primername and samplename from the initial raw FASTQ files and all intermediate files produced by the different components of the pipeline. More specifically it is used to divide file names into fields that are read by the pipeline.<br>
If the user unknowingly used repeated sample names, the pipeline produces a  warning message. 
At the end of the Workspace Window a message will display if the pipeline is safe to start or not. If it is safe to start (no duplicates in sample file, there are no  missing files in bin, etc.) then the number of input FASTQ files is shown.<br><br>

<h3 align="center"> Data Preparation </h3>
In many cases the raw gunzipped FASTQ files will be in an external folder. Copy pasting them all into local machine when the user plans to run the GBAS pipeline locally can be memory- and time intensive, especially since most of the time the user only requires the raw gunzipped FASTQ files corresponding to the Sample Identifiers in the samplesheet. Data Preparation will open a window with the input fields Rawdata, Samplesheet and Output.<br>
<p align="center">
 <img width="265" height="193" alt="data_preparation_window" src="https://github.com/user-attachments/assets/b48c400c-3b05-40d7-be73-698ad47d4ec7" />
</p>
Choosing the paths for Rawdata, Samplesheet and Output the user can import from Rawdata only the FASTQ files which correspond to the Sample Identifiers from the samplesheet into Output, saving memory and time.<br><br>

<h3 align="center"> Instructions </h3>
Here the user has the option to see a shortened version of the manual and most important points summarized in a new window. <br><br>

<h2 align="center"> Pipeline </h2>
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

<h3 align="center"> Pipeline details </h3>
In order to run the pipeline in normal mode the user can click on the Run Length Detection button to start the first part of the pipeline getting the genotypes based on allele length.  Afterwards the Run SNP Detection can be run for the final allele call.<br><br>

The folders  **QC**, **MergedOut**, **SeparatOut**, **MarkerStatistics** and **MarkerPlots** are created when running Length Detection while the folders **AllelesOut**, **ConsensusOut**, **ConsensusTogether**, **Corrected** and **AlleleCall** when running SNP Detection. These are subfolders of the Outputfolder and will contain all outputs and intermediate files.
The following section explains in detail the main functions and parts of the pipeline.<br><br><br>

The first part of the pipeline runs in five steps: 1st raw reads are quality controlled, 2nd paired reads are merged, 3rd sequences are sorted according to maker, 4th amplicon lengths are counted per individual and marker, and 5th genotypes are defined based on amplicon length.<br><br> 

**Read quality control**:
First raw FASTQ reads are quality controlled with Trimmomatic by removing 3’ low quality portions  (< 20) and trimming adapter sequences listed in the TrueSeqAdapterInUsage.fa adapterfile . More specifically the Trimmomatic is run with the following parameters:<br><br>
“ILLUMINACLIP:adapterfilename:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:20”
<br><br>
Per default the adaperfilename is set as TrueSeqAdaptersInUsage.fa but can be changed in the Pipeline Parameters window in the Files Section (**currently broken!**)<br><br>

More information about these parameters and the resulting output files can be found in the manual of Trimmomatic: http://www.usadellab.org/cms/index.php?page=trimmomatic <br><br>

The resulting FASTQ files are stored in the QC folder. The paired read files contain R1 and R2 in their names corresponding to the forward and reverse directions, respectively.<br><br>

**Merging paired end reads**:
In a second step paired reads are merged into a consensus read covering the totality of the amplicon using Usearch. Usearch takes the paired reads in the QC folder as input and merges both forward and reverse reads storing resulting FASTQ files in the  MergedOUT folder. Usearch runs  with the minimum percentage identity parameter (-fastq_pctid) set to 80% and the maximum number of mismatches parameter (-fastq_maxdiffs) set to 40.<br><br>

**Demultiplexing**:
The Demultiplexing process sorts reads into different markers defined according to the sequences of the amplification primers. Merged amplicon sequences should start and end with the sequences of the forward and reverse primers, respectively. The pipeline compares these parts of the merged read with the primer sequences provided by the user. If the number of mismatches between them is bellow the user defined threshold the read is saved into a new file for the matching marker. The mismatch threshold can be set in the Calculation Params subwindow of the Pipeline Parameters window. By default the mismatch parameter is set to 2.<br>
The pipeline takes the  FASTQ files from the MergedOut folder and saves reads into a FASTA file per marker within the SeparatOut folder. The FASTA files will have the following name structure: _samplename_primername_motif_ (FASTA). Demultiplexing yields a large number of fasta files (number of fasta files = number of primers*number of samples). The advanced pipeline mode (which will be described more in detail later) allows the user to start running the GBAS pipeline from this step if files are already trimmed and merged with other tools.<br><br>

<h2 align="center"> Database </h2>
Each full run of the pipeline results in an Allelematrix (TXT), an Allelelist (TXT, JSON, FASTA), and their combined output (JSON). The Allelelist contains all found sequence variants while the Allelematrix contains the final genotype table with allele call based on whole sequence information. The user can choose to use the obtained Allelelist as an input in a future run. The Allelelist will be  extended with newly found variants and data from additional individuals and markers. The combined output contains all found allele sequences per marker and per SampleID as well as Metadata information per sample if a metadata filepath has been given. The figure below shows an example for a combined output in JSON format. <br>
<p align="center">
<img width="638" height="457" alt="combined_output_example_oak" src="https://github.com/user-attachments/assets/206ca101-da93-4719-907c-a8838698c527" />
</p>
If no alleles are found per sample locus the _Alleles_ field will be left empty. This is to distinguish between loci which failed for a sample and those that did not. This combined output file can be stored in the local database which will be described in more detail down below. <br> <br>

<h3 align="center"> Allelelist Comparison </h3>

<h3 align="center"> PIC Calculation </h3>
The GUI offers the option to determine the absolue PIC (Polymorphism Information Content) per Marker for each Project. The button opens a window with fields to enter the paths for Input and Outputfolder.<br>
<p align="center">
 <img width="316" height="332" alt="PIC_calculation" src="https://github.com/user-attachments/assets/3d1d38e6-8047-4e97-9cca-e1f2eb23d9bf" />
</p>

The inputfolder needs to have a specific structure in order for the calculation to process. Below is example figure for the folder structure for PIC calculation of the projects **Oak**, **Buvi** and **Spruce**. <br>
<p align="center">
 <img width="268" height="368" alt="PIC_folder_structure_vers1" src="https://github.com/user-attachments/assets/75d72b43-dec1-4dd7-abac-c3862c268871" />
</p>
<br>

The inputfolder contains a subfolder per project. Each project folder must contain the 2 subfolders allele_matrices and length_matrices as well as a primerfile _primers.txt_ containing all primers used for the project. The subfolder length_matrices contains all cleaned matrices generated by the Length Detection part of the GBAS-pipeline while the allele_matrices subfolder contains all matrices generated by the Snips Detection part of the GBAS-pipeline. All matrices must be in EXCEL format (.xlsx).<br><br>
3 output files will be generated once the calculation is done:<br>
* _PIC_results.json_ contains the absolute PIC value (both length- and sequence based) for each marker per project, the absolute PIC difference as well as the individual frequencies of each allele appearing per marker (both length- and sequence based). A positive PIC difference indicates indicates an increase in the PIC value when identifying alleles from the length-based allele-matrix to identifying alles from the sequence-based allele-matrix.
* _PIC_additional_info.json_ shows for each project the 5 best performing markers based on absolute length-based and sequence-based PIC values as well as on absolute PIC increase from length-based to sequence-based.
* A plot (PNG) showing for each marker per project a bar representing the PIC value difference from length-based to sequence-based value. A bar to the right indicates an increase from length-based to sequence-based while a bar going to the left indicates a PIC drop.<br><br>
Below is a figure showcasing the Allele frequencies, PIC values and PIC differences for the Marker Bv1_AATA for the project Buvi.<br>
<p align="center">
 <img width="457" height="455" alt="PIC_values_example" src="https://github.com/user-attachments/assets/7457c2a4-8278-4928-9ff2-e6d109871449" />
</p>
<br>


