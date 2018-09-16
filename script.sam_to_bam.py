#! /bin/env python3

"""
Compressing the SAM files to BAM
================================

Author: Andrés García García @ May 2018

About the project
-----------------
NOTE: This is the third script in the pipeline of the project.

We are trying to detect if there are changes in the expression of
long non-coding RNAs between the left and right hemisphere of a mouse's
brain (telencephalon). For this, 3 samples where taken and sequenced using
RNAseq. For more information about RNAseq, see: 
https://galaxyproject.org/tutorials/rb_rnaseq/


The data
--------
The input data for the current script are the SAM files resulting of the
alignment of the RNAseq expression data to the reference genome.
    
The analysis
------------
We are basing our protocol on the instructions provided in:
https://davetang.org/muse/2017/10/25/getting-started-hisat-stringtie-ballgown/

Procedure
---------
Converting the files in a sequential way would be terribly slow, so we are trying to 
paralelize as much as we can.

The present script first gets the names of the files to convert. Then, the command to 
be executed is assembled for each file and a new script is assembled and executed that 
kickstarts the paralell jobs.

Why do we need an additional script? Well, in SGE, the number of jobs in a job array
must be specified in advance, but it's only at runtime when we know how many jobs we'll use. So
we need to invoke another process to perform the task. The generated script is saved
for debugging and repeatability purposes.

"""

import click
import textwrap
import subprocess
from pathlib import Path
from typing import Union, List, Generator, Iterable


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

def search_files(data_path: Union[str, Path]) -> Generator[Path, None, None]:
    """Search for the SAM files in the directory.
    
    Input: The path to the folder containing the files
    Output: The files.
    
    """
    sam_files = data_path.glob('*.sam')
    
    return sam_files
# ---

def assemble_commands(sam_files: Iterable[Union[str, Path]], 
                      output_path: Union[str, Path], 
                      n_cores: int = 1) -> Generator[str, None, None]:
    """Assemble the commands.
    
    Input:
        sam_files: The SAM files
        output_path: A valid object pointing to the output directory.
        n_cores: The number of threads that each process will be able to use.
    
    """
    output_path = Path(output_path)

    for sam_file in sam_files:
        
        sam_file = Path(sam_file)
        
        # Base the output file name on the input file name
        output_file = output_path / sam_file.with_suffix('.bam').name
        
        yield f'samtools sort -@ {n_cores} -o {output_file} {sam_file}'
# ---

#### <<<<<< MAIN PROCEDURE >>>>>>> ####

# Command line interface
@click.command()

@click.option('--input_dir', '-i',
              help='The directory where the input files reside.'
                   ' Default "./mapped".')

@click.option('--output_dir', '-o',
              help='The directory where to output the results.'
                   ' Default "./mapped".')

@click.option('--cores', '-p',
              help='The number of cores to use per process.'
                   ' Default 1.')

@click.option('--ram', '-r', 
              help='RAM amount per job (in Gb). Default 8.')
    
def main(input_dir, output_dir, cores, ram):
    """Assemble the script with the commands for trimming and submit (qsub) it."""
    
    input_dir = Path(input_dir 
                         if input_dir 
                         else './mapped').resolve()
    output_dir = Path(output_dir 
                          if output_dir 
                          else './mapped').resolve()
    
    cores = cores if cores else 1
    ram = ram if ram else 8
    
    print( 'Resolved parameters: \n'
          f'    Input directory: {input_dir}\n'
          f'    Output directory: {output_dir}\n'
          f'    Cores per task: {cores}\n'
          f'    RAM per process: {ram}')
    
    # 1. --- Find the files to convert.
    #        The data is in the directory "./map" 
    #        Here we fetch the location of the files in the filesystem.
    input_files = search_files(input_dir)



    # 2. --- Generate the conversion commands.
    #        From the information of the files, generate the commands
    #        needed.
    commands = list(assemble_commands(input_files,
                                      output_dir,
                                      cores))



    # 3. --- Assemble the script.
    #        Create the script that will launch the paralell jobs.

    python3_exec_path = get_output('which python3')

    # We want every command to be associated to a job id.
    # (we add one to i because job ids start from 1) 
    commands_str = "\n    ".join( f"commands[{i+1}]='{s}'" 
                                  for i,s in enumerate(commands) )

    script_contents = f"""\
    #! {python3_exec_path}

    #Run through this shell
    #$ -S {python3_exec_path}

    # Use current working directory
    #$ -cwd

    # Join stdout and stderr
    #$ -j y

    # If modules are needed, source modules environment (Do not delete the next line):
    #. /etc/profile.d/modules.sh

    # Name the job array
    #$ -N sam_to_bam

    # Pass environment
    #$ -V

    #$ -pe openmp {cores}
    #export OMP_NUM_THREADS={cores}

    # Work with {ram}G RAM per process
    #$ -l vf={ram}G

    # Use as many jobs as needed
    #$ -t 1-{len(commands)}

    '''
    Convert SAM files to BAM
    ------------------------

    The current script was autogenerated with the 
    file `script.sam_to_bam.py`, look there for documentation.

    '''

    import os
    import maya
    import subprocess
    from pathlib import Path


    # The commands to be executed
    commands = dict()
    {commands_str}

    # Fetch the job id
    task_id = int( os.environ['SGE_TASK_ID'] )

    # Fetch the command corresponding to the current job
    command = commands[task_id]

    # Get the name of the output file
    #   -> The output file is the next string after the '-o' argument
    output_file = command.split()[command.split().index('-o') + 1]

    # Execute the job
    if Path(output_file).exists():
        print(f'Task {{task_id}}. Output file already exists:', output_file, flush=True)
    
    else:
        print(f'Task {{task_id}}. Executing command @', maya.now(), ':', command, flush=True)

        subprocess.run(command.split()) # <-- Here it is executed, splitting is 
                                        #     necessary to pass the arguments 
                                        #     appropriately                            
        print(f'Task {{task_id}}. Finished execution @', maya.now(), flush=True)
    """
    # Remove indentation
    script_contents = textwrap.dedent(script_contents)



    # 4. --- Write the mapping script to a file.

    script_name = 'script.autogenerated.sam_to_bam_jobs.py'

    with open(script_name, 'w') as outf:
        outf.write(script_contents)



    # 5. --- Execute the script

    run(f"qsub {script_name}")
# ---



if __name__ == '__main__':
    # Command line interface
    main()
