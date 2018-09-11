#! /bin/env python3

"""
Trimming the sequences using Trimmomatic
========================================

Author: Andrés García García @ May 2018

About the project
-----------------
NOTE: This is the second script in the pipeline of the project.

We are trying to detect if there are changes in the expression of
long non-coding RNAs between the left and right hemisphere of a mouse's
brain (telencephalon). For this, 3 samples where taken and sequenced using
RNAseq. For more information about RNAseq, see: 
https://galaxyproject.org/tutorials/rb_rnaseq/


The data
--------
The input data for the current script are the raw FASTQ files from the
RNAseq experiment.

    
The analysis
------------
We are basing our protocol on the instructions provided in:
https://davetang.org/muse/2017/10/25/getting-started-hisat-stringtie-ballgown/
https://www.biostars.org/p/207680/#207685
https://www.biostars.org/p/287500/

Procedure
---------
All the FASTQ files are already in a single folder (raw_data/), and the adapters used 
are there also (raw_data/alladapters.fa)

Why do we need to generate another script? In order to get computing resources, we need to
enqueue the job through the SGE tasks system, this is done by specifying the task in a script.
That is the script that is generated here and submitted to the queue system through 'qsub' at 
the end of this file.

"""

import re
import click
import textwrap
import subprocess
from itertools import chain
from pathlib import Path
from typing import Union, Generator, Iterable, List


def get_output(command: Union[str, List[str]], **kwargs) -> str:
    """Execute a command through the shell, get the output as a string.
    """
    if isinstance(command, str) and not kwargs.get('shell'):
        command = command.split()
    bytes_output = subprocess.check_output(command, **kwargs)
    return bytes_output.decode('UTF-8')
# ---

def run(command: Union[str, List[str]], **kwargs) -> subprocess.CompletedProcess:
    """Execute a command through the shell. Doesn't capture output.
    """
    if isinstance(command, str) and not kwargs.get('shell'):
        command = command.split()
    return subprocess.run(command, **kwargs)
# ---

def find_paired(dir: Union[str, Path]):
    """Get pairs of sequence files.
    
    Search the given directory for pairs of fastq files,
    return a list of pairs of sequence file names. 
    """
    dir = Path(dir)
    
    R1 = dir.glob('*R1*')
    R2 = dir.glob('*R2*')
    
    return zip(sorted(str(f) for f in R1), 
               sorted(str(f) for f in R2))
# ---

def find_unpaired(dir: Union[str, Path], 
                  already_paired: Iterable[str]) -> List[str]:
    """Get unpaired sequence files.
    
    Search the given directory for unpaired FASTQ files.
    """
    already_paired = set(already_paired)
    
    return [str(f) 
                for f in dir.glob('*.fastq') 
                if str(f) not in already_paired]
# ---

def search_files(data_path: Union[str, Path]):
    """Search for the data files for each sample.
    
    Input: The path to the data folder (as pathlib.Path object).
    
    Assumes the data folder has the following structure:
    
        data/ (<-- data_path points here)
            │
            ├── mm<SAMPLE NO.>X.fastq (several files)
            ├── mm3R_XXXXXX_XXXX_X1_###.fastq (several files)
            └── mm3R_XXXXXX_XXXX_X2_###.fastq (several files)
    
    """
    pairs = list(find_paired(data_path))
    loners = find_unpaired(
                    data_path, 
                    already_paired=chain.from_iterable(pairs))
    
    return {'paired': pairs,
            'unpaired': loners}
# ---

def assemble_commands(files,
                      output_path: Union[str, Path],
                      adapters_file: str) -> Generator[str, None, None]:
    """Assemble the mapping commands.
    
    Input:
        samples: A dictionary with the RNAseq files location and pairing information
                 as returned from the 'search_files' function.
        output_path: A valid Path object pointing to the output directory.
    
    Generates the commands that will be executed.
    
    The trimming is done using the following commands
        For paired reads:
            java -jar trimmomatic-0.35.jar PE -phred33 {input1} {input2}\
            {output_forward_paired} {output_forward_unpaired}\
            {output_reverse_paired} {output_reverse_unpaired}\ 
            ILLUMINACLIP:{adapters_file}:2:30:10 LEADING:3 TRAILING:3 \
            SLIDINGWINDOW:4:15 MINLEN:36
        For unpaired reads:
            java -jar trimmomatic-0.35.jar SE -phred33 {input} {output} \
            ILLUMINACLIP:{adapters_file}:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36
    """
    output_path = Path(output_path)
    
    fullpath = lambda filename : (
                    # Append the paths
                    str(output_path/filename) 
                )  
    
    # Unpaired reads
    loners = files['unpaired']

    for unpaired_f in loners:
            
        output = re.sub('fastq$','trimmed.fastq', Path(unpaired_f).name)

        yield (f'trimmomatic SE -threads 1 -phred33 {unpaired_f} {fullpath(output)}'
               f' ILLUMINACLIP:{adapters_file}:2:30:10 LEADING:3 TRAILING:3'
                ' SLIDINGWINDOW:4:15 MINLEN:36')
        
    # Paired reads
    pairs = files['paired']

    for p1, p2 in pairs:
            
        output_forward_paired = re.sub('_R[12]_', '_R1_paired_', Path(p1).name)
        output_forward_unpaired = re.sub('_R[12]_', '_R1_unpaired_', Path(p1).name)
        output_reverse_paired = re.sub('_R[12]_', '_R2_paired_', Path(p1).name)
        output_reverse_unpaired = re.sub('_R[12]_', '_R2_unpaired_', Path(p1).name)

        yield (f'trimmomatic PE -threads 1 -phred33 {fullpath(p1)} {fullpath(p2)}'
               f' {fullpath(output_forward_paired)} {fullpath(output_forward_unpaired)}'
               f' {fullpath(output_reverse_paired)} {fullpath(output_reverse_unpaired)}'
               f' ILLUMINACLIP:{adapters_file}:2:30:10 LEADING:3 TRAILING:3'
                ' SLIDINGWINDOW:4:15 MINLEN:36')
# ---

#### <<<<<< MAIN PROCEDURE >>>>>>> ####

# Command line interface
@click.command()

@click.option('--input_dir', '-i',
              help='The directory where the input files reside.'
                   ' Default: "./raw_data".')

@click.option('--output_dir', '-o',
              help='The directory where to output the results.'
                   ' Default: "./trimmed".')

@click.option('--adapters_file', '-a',
              help='The FASTA file specifying the adapters to trimm.'
                   ' Default: A file "all_adapters.fa" in the input folder.')

@click.option('--ram', '-r', 
              help='RAM amount per job (in Gb). Default 8.')

def main(input_dir, output_dir, adapters_file, ram):
    """Assemble the script with the commands for trimming and submit (qsub) it."""
    
    input_dir = Path(input_dir 
                         if input_dir 
                         else './raw_data').resolve()
    output_dir = Path(output_dir 
                          if output_dir 
                          else './trimmed').resolve()
    
    adapters_file = adapters_file 
                        if adapters_file 
                        else str(input_dir / 'all_adapters.fa')
    
    ram = ram if ram else 8

    print( 'Resolved parameters: \n'
          f'    Input directory: {input_dir}\n'
          f'    Output directory: {output_dir}\n'
          f'    Adapters file: {adapters_file}\n'
          f'    RAM per process: {ram}'))
    

    #1. --- Find the data.
    #        Here we fetch information of the files containing the data, whether they are paired 
    #        and their location in the filesystem.
    files = search_files(input_dir)


    # 2. --- Generate the commands.
    #        From the information of the files, generate the commands
    #        needed.

    commands = list(assemble_commands(files,
                                      output_dir,
                                      adapters_file))


    # 3. --- Assemble the script.
    #        Create the script that will launch the paralell jobs.
    python3_exec_path = get_output('which python3')

    # We want every command to be associated to a job id.
    # (we add one to i because job ids start from 1) 
    commands_str = "\n".join( f"commands[{i+1}]='{s}'" 
                              for i,s in enumerate(commands) )

    # vvvvvv This is the script to be generated
    script_contents = f"""\
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
    #$ -N trimming

    # Pass environment
    #$ -V

    # Specify available RAM per process, per core.
    #$ -l vf={ram}G

    # Use as many jobs as needed
    #$ -t 1-{len(commands)}


    '''

    Paralell trimming jobs
    -----------------------

    The current script was autogenerated with the 
    file `script.trimming.py`, look there for documentation.

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


    # Execute the job
    print(f'Task {{task_id}}. Executing command @ {{maya.now()}} : {{command}}', flush=True)

    subprocess.run(command.split()) # <-- Here it is executed, splitting is 
                                    #     necessary to pass the arguments 
                                    #     appropriately                            
    print(f'Task {{task_id}}. Finished execution @ {{maya.now()}}', flush=True)
    """
    # Remove indentation
    script_contents = textwrap.dedent(script_contents)
    

    # 4. --- Write the script to a file.

    script_name = 'script.autogenerated.trimming_jobs.py'

    with open(script_name, 'w') as outf:
        outf.write(script_contents)


    # 5. --- Execute the script

    run(f"qsub {script_name}")
# ---



if __name__ == '__main__':
    # Command line interface
    main()