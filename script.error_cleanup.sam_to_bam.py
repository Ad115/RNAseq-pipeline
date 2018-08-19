#! /bin/env python3

"""
Error cleanup for step 2
=========================

Author: Andrés García García @ Aug 2018

If the conversion of a SAM file from the mapping step failed,
the SAM file was probably corrupted, so delete it. The name of
the corrupted file is in the logs of the conversion.

About the project
-----------------
We are trying to detect if there are changes in the expression of
long non-coding RNAs between the left and right hemisphere of a mouse's
brain (telencephalon). For this, 3 samples where taken and sequenced using
RNAseq. For more information about RNAseq, see: 
https://galaxyproject.org/tutorials/rb_rnaseq/

"""

import os
import pathlib
import subprocess


#NOTE: The script may need to be 
#      customized to adapt to the 
#      specific files you want to target.

def run(command, **kwargs):
    """Execute a command through the shell. Doesn't capture output."""
    command = command.split()
    subprocess.run(command, **kwargs)
# ---

def get_files(command): 
    """Extract the input/output files from the command

    Return as a tuple of pathlib.Path objects
    """
    parts = command.strip().split()
    # The output file name is specified after the -o flag
    output_str = parts[parts.index('-o') + 1]
    output = pathlib.Path(output_str)
    # The input is the same but with changed extension
    input = output.with_suffix('.sam')
    # Return the name without the extension
    return input, output
# ---


#### <<<<<< MAIN PROCEDURE >>>>>>> ####


# Get the log files from the conversion step
log_files = pathlib.Path().glob('sam_to_bam.*')

for log in log_files:
    log_text = log.read_text()
    
    if log_text:
        log_lines = log_text.split('\n')
        # Parse the executed command for the input and output files
        input, output = get_files(log_lines[0])
        
        # Search for a truncated file error
        if any("truncated file. Aborting" in line for line in log_lines):
            # Remove both the SAM and the BAM files
            for file in input,output:
                if file.exists():
                    run(f'rm --verbose {file.resolve()}')
                else:
                    print(f'File does not exists: {file.resolve()}')
                        
                
