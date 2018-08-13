#! /bin/env python3

"""
Deleting incomplete output files.
=================================

Author: Andrés García García @ May 2018

In this script we delete output files produced by tasks that where killed.

About the project
-----------------
We are trying to detect if there are changes in the expression of
long non-coding RNAs between the left and right hemisphere of a mouse's
brain (telencephalon). For this, 3 samples where taken and sequenced using
RNAseq. For more information about RNAseq, see: 
https://galaxyproject.org/tutorials/rb_rnaseq/

"""
import subprocess


#NOTE: The script may need to be 
#      customized to adapt to the 
#      specific files you want to target.

def get_output_filename(s): 
    """Extract the output file from the command.

    The output file name is specified just after the -S flag.
    """
    parts = s.split()
    return parts[parts.index('-S') + 1]
# ---

# Search for the lines that specify a command execution.
is_interesting = lambda s: 'Executing command' in s


for line in !(tail -n1 rnaseq_map*):
    if is_interesting(line):
        # If the last line in the log is the execution of a command
        # then the command did not finish execution and thus it's 
        # output is incomplete and must be removed.
        filename = get_output_filename(line)
        rm_command = f"rm --verbose {filename}"
        subprocess.run(rm_command.split())
