#! /bin/env python3

"""
Mapping the RNAseq data with HISAT2.
=====================================

Author: Andrés García García @ May 2018

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

The current script represents the first part of the analysis pipeline, the
mapping of the reads to the genome (Mus musculus). 

As there are many samples and many paired read files, this script automates
the process of doing the mapping for all the files and the data.

The mapping is done using HISAT2, the successor of TOPHAT2. For this, we
downloaded the pre-built HGFM index for reference plus SNPs and transcripts
from the link on the official HISAT2 page 
(ftp://ftp.ccb.jhu.edu/pub/infphilo/hisat2/data/grcm38_snp_tran.tar.gz).

We are basing our protocol on the instructions provided in:
https://davetang.org/muse/2017/10/25/getting-started-hisat-stringtie-ballgown/
So we are executing:
    hisat2 -p 8 --dta -x <index folder with prefix> -1 <sample1> -2 <sample2> -S <outputfile.sam>

Procedure
---------
To map the files pair by pair would be terribly slow, so we are trying to 
paralelize as much as we can.

The present script first gets the names of the files to map, finding paired and
unpaired files. Then, the command to be executed is assembled for each mapping process
and a new script is assembled and executed that kickstarts the paralell jobs.

Why do we need an additional script? Well, in SGE, the number of jobs in a job array
must be specified in advance, but it's only at runtime when we know how many jobs we'll use. So
we need to invoke another process to perform the task. The generated script is saved
for debugging and repeatability purposes.


Note for the developer or maintainer
------------------------------------
This script relies heavily on the use of pathlib.Path objects, present in the Python
standard library. Also on generator functions and on the use of the subprocess 'run' and 
'check_output' functions. Nothing that doesn't come with Python's batteries included 
standard library. If something doesn't sound familiar, please use Google.

"""

import subprocess
from pathlib import Path


def get_output(command):
    """Execute a command through the shell, get the output as a string.
    """
    command = command.split()
    bytes_output = subprocess.check_output(command)
    return bytes_output.decode('UTF-8')
# ---

def run(command, **kwargs):
    """Execute a command through the shell. Doesn't capture output."""
    command = command.split()
    subprocess.run(command, **kwargs)
# ---

def get_unpaired(dir, sample_name=None):
    """Get unpaired sequence file.
    
    Search the given directory for an unpaired fastq 
    file associated with the given sample. If the sample 
    is not given, inferr it from the folder's name.
    """
    if sample_name is None:
        sample_name = dir.name.split('_')[-1]
    
    return str(next(dir.glob(sample_name + '.fastq')))
# ---

def get_paired(dir):
    """Get pairs of sequence files.
    
    Search the given directory for pairs of fastq files,
    return a list of pairs of sequence file names. 
    """
    R1 = dir.glob('*R1*')
    R2 = dir.glob('*R2*')
    
    return list(zip(sorted(str(f) for f in R1), 
                    sorted(str(f) for f in R2)))
# ---

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

    In this section, we parse the directory to assemble the 'samples'
    information:
           
        samples = {'mm1L': {'unpaired': '../RNAseq_data/Sample_mm1L/mm1L.fastq',
                            'paired': [('../RNAseq_data/Sample_mm1L/mm1L_ATCACG_L003_R1_001.fastq',
                                        '../RNAseq_data/Sample_mm1L/mm1L_ATCACG_L003_R2_001.fastq'),
                                       (..., ...),
                                       ...
                                      ]
                            },
                   'mm1R': {...},
                   ...
                  }
    """
    sample_dirs = [dir for dir in data_path.glob('Sample*')]

    sample_names = [s_dir.name.split('_')[-1] for s_dir in sample_dirs]

    # Asociate the sample name to the data files.
    samples = {sname: {'unpaired': get_unpaired(sdir, sname),
                       'paired': get_paired(sdir)}
                   for sname, sdir in zip(sample_names, sample_dirs) }
    
    return samples
# ---

def assemble_commands(samples, idx_prefix, output_path):
    """Assemble the mapping commands.
    
    Input:
        samples: A dictionary with the RNAseq files location and pairing information
                 as returned from the 'search_files' function.
        idx_prefix: A string with the path and file prefix for the genome index.
        output_path: A valid pathlib.Path object pointing to the output directory.
    
    Generates the commands that would be executed to make the map.
    
    The mapping is done using the following commands
        For paired reads:
            hisat2 --dta -x <index folder with prefix> -1 <pair1> -2 <pair2> -S <outputfile.sam>
        For unpaired reads:
            hisat2 --dta -x <index folder with prefix> -U <unpaired> -S <outputfile.sam>
    """
    
    for s_name,sample in samples.items():

        # Paired reads
        pairs = sample['paired']

        for p1, p2 in pairs:
            pair_no = p1.split('_')[-1].split('.')[0]

            S = str(output_path / f'{s_name}_{pair_no}_paired.sam') # The / is for appending to the path object.

            yield f'hisat2 --dta -x {idx_prefix} -1 {p1} -2 {p2} -S {S}'

        # Unpaired reads
        unpaired_f = sample['unpaired']

        U = unpaired_f
        S = str(output_path / f'{s_name}_unpaired.sam')

        yield f'hisat2 --dta -x {idx_prefix} -U {U} -S {S}'
# ---

#### <<<<<< MAIN PROCEDURE >>>>>>> ####

# 1. --- Find the data to map.
#        The data is in the directory "../RNAseq_data" (a symbolic link to the actual data.)
#        Here we fetch information of the files containing the data, whether they are paired 
#        and their location in the filesystem.
samples = search_files(data_path=Path('../RNAseq_data'))


# 2. --- Generate the mapping commands.
#        From the information of the files, generate the commands
#        needed.
RAM_Gb = 8

index_dir = Path('./index/grcm38_snp_tran/').resolve()
idx = str(index_dir / 'genome_snp_tran') # The / is for appending to the path object.

output = Path('./map').resolve()

commands = list(assemble_commands(samples,
                                  idx_prefix=idx,
                                  output_path=output))


# 2. --- Assemble the mapping script.
#        Create the script that will launch the paralell jobs.
python3_exec_path = get_output('which python3')

# We want every command to be associated to a job id.
# (we add one to i because job ids start from 1) 
commands_str = "\n".join( f"commands[{i+1}]='{s}'" 
                          for i,s in enumerate(commands) )

# vvvvvv This is the script to be generated
script_contents = f"""
#! {python3_exec_path}

# Run through this shell
#$ -S {python3_exec_path}

# Use current working directory
#$ -cwd

# Join stdout and stderr
#$ -j y

# If modules are needed, source modules environment (Do not delete the next line):
#. /etc/profile.d/modules.sh

# Name the job array
#$ -N rnaseq_map

# Pass environment
#$ -V

# Specify available RAM per process, per core.
#$ -l vf={RAM_Gb}G

# Use as many jobs as needed
#$ -t 1-{len(commands)}


'''

Paralell mapping jobs
---------------------

The current script was autogenerated with the 
file `script.rnaseq_map.py`, look there for documentation.

'''
import os
import subprocess
import maya
from pathlib import Path


# The commands to be executed
commands = dict()
{commands_str}

# Fetch the job id
task_id = int( os.environ['SGE_TASK_ID'] )

# Fetch the command corresponding to the current job
command = commands[task_id]

# Get the name of the output file for the current job
output_file = command.split()[command.split().index("-S") + 1]

# Execute the job
if Path(output_file).exists():
    print(f'Task {{task_id}}. Output file already exists:', output_file)
    
else:
    print(f'Task {{task_id}}. Executing command @', maya.now(), ':', command)
    
    subprocess.run(command.split()) # <-- Here it is executed, splitting is 
                                    #     necessary to pass the arguments 
                                    #     appropriately                            
    print(f'Task {{task_id}}. Finished execution @', maya.now())
"""


# 3. --- Write the mapping script to a file.

script_name = 'script.autogenerated.rnaseq_map_jobs.py'

with open(script_name, 'w') as outf:
    outf.write(script_contents)


# 4. --- Execute the script

run(f"qsub {script_name}")
