#! /bin/env python3

"""
Fetching the raw RNAseq data.
=============================

Author: Andrés García García @ Sept 2018

About the project
-----------------
We are trying to detect if there are changes in the expression of
long non-coding RNAs between the left and right hemisphere of a mouse's
brain (telencephalon). For this, 3 samples where taken and sequenced using
RNAseq. For more information about RNAseq, see: 
https://galaxyproject.org/tutorials/rb_rnaseq/


The data
--------

The data belongs to Dr. Alfredo Varela Echávarri and comes
from telencephalus tissue extracted by Brenda (INB Lab A03). 

The data is in the '/mnt/Genoma/brefar/Project_VARELA_2564_150702B3_Comprimidos_originales/'
directory of the 'dna.lavis.unam.mx' cluster. It has the following structure:

    ├── adapters
    │   ├── NexteraPE-PE.fa
    │   ├── TruSeq2-PE.fa
    │   ├── TruSeq2-SE.fa
    │   ├── TruSeq3-PE-2.fa
    │   ├── TruSeq3-PE.fa
    │   └── TruSeq3-SE.fa
    │
    ├── Sample_mm1L
    │   ├── mm1L_ATCACG_L003_R1_001.fastq
    │   ...
    │   ├── mm1L_ATCACG_L003_R1_039.fastq
    │   ├── mm1L_ATCACG_L003_R2_001.fastq
    │   ...
    │   ├── mm1L_ATCACG_L003_R2_039.fastq
    │   ├── mm1L.fastq
    │   └── SampleSheet.csv
    │   
    ├── Sample_mm1R
    │   ├── mm1R_CGATGT_L003_R1_001.fastq
    │   ...
    │   ├── mm1R_CGATGT_L003_R1_044.fastq
    │   ├── mm1R_CGATGT_L003_R2_001.fastq
    │   ...
    │   ├── mm1R_CGATGT_L003_R2_044.fastq
    │   ├── mm1R.fastq
    │   └── SampleSheet.csv
    │   
    ├── Sample_mm2L
    │   ├── mm2L.fastq
    │   ├── mm2L_TTAGGC_L003_R1_001.fastq
    │   ...
    │   ├── mm2L_TTAGGC_L003_R1_045.fastq
    │   ├── mm2L_TTAGGC_L003_R2_001.fastq
    │   ...
    │   ├── mm2L_TTAGGC_L003_R2_045.fastq
    │   └── SampleSheet.csv
    │ 
    ├── Sample_mm2R
    │   ├── mm2R.fastq
    │   ├── mm2R_TGACCA_L003_R1_001.fastq
    │   ...
    │   ├── mm2R_TGACCA_L003_R1_048.fastq
    │   ├── mm2R_TGACCA_L003_R2_001.fastq
    │   ...
    │   ├── mm2R_TGACCA_L003_R2_048.fastq
    │   └── SampleSheet.csv
    │   
    ├── Sample_mm3L
    │   ├── mm3L_ACAGTG_L003_R1_001.fastq
    │   ...
    │   ├── mm3L_ACAGTG_L003_R1_053.fastq
    │   ├── mm3L_ACAGTG_L003_R2_001.fastq
    │   ...
    │   ├── mm3L_ACAGTG_L003_R2_053.fastq
    │   ├── mm3L.fastq
    │   └── SampleSheet.csv
    │   
    └── Sample_mm3R
        ├── mm3R.fastq
        ├── mm3R_GCCAAT_L003_R1_001.fastq
        ...
        ├── mm3R_GCCAAT_L003_R1_046.fastq
        ├── mm3R_GCCAAT_L003_R2_001.fastq
        ...
        ├── mm3R_GCCAAT_L003_R2_046.fastq
        └── SampleSheet.csv

    7 directories, 568 files
    
The analysis
------------

The current script represents the pre-first part of the analysis pipeline, 
we are fetching all the data from the folders it is contained in and linking
it to a new folder.

As there are many samples and many paired read files, this script automates
the process of searching through the folders and files.


Note for the developer or maintainer
------------------------------------
This script relies heavily on the use of pathlib.Path objects, present in the Python
standard library. Also on generator functions.

"""

from pathlib import Path


def search_files(data_path):
    """Search for the data files for each sample.
    
    Input: The path to the data folder (as pathlib.Path object).
    
    Assumes the data folder has the following structure:
    
        RNAseq_data (<-- data_path points here)
            │
            ├── adapters
            │  
            ├── Sample_mm1L   
            ├── Sample_mm1R
            ├── Sample_mm2L
            ├── Sample_mm2R
            ├── Sample_mm3L
            ├── Sample_mm3R
            ...

    And, in turn, each sample folder has the following structure:
    (X stands for not important stuff and # for the file numbering)

        Sample_mm<SAMPLE NO.>X
            ├── mm<SAMPLE NO.>X.fastq
            ├── mm3R_XXXXXX_XXXX_X1_###.fastq (several files)
            ├── mm3R_XXXXXX_XXXX_X2_###.fastq (several files)
            └── SampleSheet.csv

    We yield (create an iterator) over all fastq files in the folders.
    
    """
    sample_dirs = (dir for dir in data_path.glob('Sample*'))
    
    for sample_dir in sample_dirs:
        print(f'Examining directory {sample_dir}')
        # Get all the fastq files
        yield from sample_dir.glob('*.fastq')
# ---


#### <<<<<< MAIN PROCEDURE >>>>>>> ####


data_path = Path('../RNAseq_data').resolve()
output_path = Path('./data').resolve()

# 1. --- Find the raw data files.
#        The data is in the directory "../RNAseq_data" (a symbolic link to the actual data.)
#        Here we fetch information of the files containing the data.
files = search_files(data_path)


# 2. --- Link them to the new path
for file in files:
    # What the new file will be?
    new = output_path / file.name
    
    # Link to the old one
    print(f"Making link {new} -> {file}.")
    new.symlink_to(file)
