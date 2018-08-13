Project's Log
==============

About the project
-----------------
We are trying to detect if there are changes in the expression of
long non-coding RNAs between the left and right hemisphere of a mouse's
brain (telencephalon). For this, 3 samples where taken and sequenced using
RNAseq. For more information about RNAseq, see: 
https://galaxyproject.org/tutorials/rb_rnaseq/

For more documentation on the scripts, look at the scripts themselves.

Thanks to Villay for suggesting the creation of this log.

## May

### First half of May

*Step 1: Mapping to the genome.*

- The work has begun on the raw RNAseq data.

- Due to the really big quantity of data files and the amount of 
  repeated work that needs to be done on them, it was decided 
  that the best way to analyze them is via batch scripts that 
  process many (or all) the files at once. This also adds to the
  repeatability of the process.
  
- It was decided that the scripts are to be written in Xonsh (a 
  Bash-Python hybrid language) for convenience and ease of use, 
  besides being easy to install (via "pip install xonsh").
  
- The batch mapping process was run for 2 weeks, from May 9th to 
  May 17th. Later it was found that the script had a bug and the 
  results are not useful.

- Due to how complicated it was to chase the bug, Villay's advise 
  was followed and exhaustive documentation was added to each 
  script used now and will be uadded to future scripts.

- The script was corrected and documented and a new job was run.
  It was observed that if the jobs are done sequentially, as in 
  the current script, the time required to finish will be too 
  large, so the process was killed and the decision was made to 
  use an SGE script to launch multiple paralell processes.

- The script with SGE Job Arrays was made and the processes 
  where submitted.
  Apparently everything goes well.

- Days later, Luis Aguilar noted the jobs where using resources 
  not assignated to them, thus saturating the cluster and rendering 
  other users uncapable to submit their jobs, so he had to kill my 
  processes. Later we found out that my jobs where using 8 cores
  each, but I had not requested that, so the system was not aware of 
  it and the workload distribution wasn't working properly.
  

### May 29th
- Luis advise for the previous problem was to add the next lines to my SGE script:
    ```
	#$ -pe openmp {CORES}
	export OMP_NUM_THREADS={CORES}
    ```
  
-  The script was edited to check if the output file lready exists, 
  in orer to avoid duplication of work.

- The new script with the modified job array was submitted.

- The raw data mapping to the genome was apparently completed, but 
  due to the fact that some processes had ended prematuerly in the 
  previous job array, we estimate that at least 55 of the 281 jobs
  didn't finish correctly and their output files are corrupted. When 
  we tried to check which of the output files where in such a state,
  it was noted that such information was not available from the logs
  and thus they must be improved.

- Due to the previous problems, it was concluded that the best 
  solution is to modify the script, throw away all output files and 
  repeat the whole analysis. (This is practical, given it takes ~2 day 
  to finish, which is not too much)

- Following Villay's advise, this log was created in order to have a 
  register of my work and to avoid future errors.
  
- 13:43. The job array 100543 was submitted which restarts the mapping 
  process from scratch.
  
- The scipt for the next step was created. To convert the SAM files to BAM.


### May 30th

- 15:03 The cluster "DNA" had a physical failure and the job array was killed.

### May 31st

- Due to the failure on May 30th, some output files are incomplete due to processes
  that where writing to them at the time of the failure. It was posible due to the logs
  to detect which ones where in such state and they where deleted. The commands for that
  purpose are in a new script: `script.delete_incomplete_output.xsh`.
  
- 14:45 The job array was submitted again. The job ID is 156.

### June 8

- The job array looks dead. No new output since May 31st, although the resource consumption 
  looks normal and no error has been logged (checked with Luis Aguilar). So, we killed the job.

### June 12

- There was a problem with the cleanup script that is now corrected.

- The mapping script was modified. Now prints the date & time of execution start.
  A new job array was submitted (435)

- It was noticed that it is also convenient to have the date & time when the jobs finish
  execution, so the job array was killed, incomplete output files where cleaned up, and a 
  new job array with the desired functionality was submitted (437). 

- The output looked well at first like in the previous execution but once again froze 
  after a while.
  In order to discard some obscure bug from the Xonsh shell, the script that is submitted is
  now in pure Python.
  For this, we killed the previous job array and submitted the modified one (job array 441).

### July 29

- The work was left until today when there was a failure with the DNA cluster and the job 
  array was killed.
  Only 2 jobs where completed by that time, so there is surely something wrong. The jobs 
  should not last that long! The hypothesis is that the problem lies in the job script being 
  a Python script, I don't know why this would affect but is the best i've got for now. So, 
  the script will be changed to a bash script.

### August 12

- The script "script.rnaseq_map.xsh" was modified in order that it's output, the script
  "script.autogenerated.rnaseq_map_jobs.*" is pure Bash (instead of Python). The latter 
  script is the one that is submitted via qsub. This change allows to test the hypothesis 
  that the jobs are hanging out because of some issue of Python with parallelism.

- The new script was submitted but the cluster complained of a nonexistent parallel 
  environment "openmp" (Which is weird, given that Luis instructed me to use that if I wanted 
  to use multiple cores). 
  To solve this, the script was modified so that each job uses only one core.
  
- A new error was thrown at execution time, this time in the output logs lie the messages:
    ```
    Unable to run job: denied: host "compute-00-00.cm.cluster" is no submit host.
    Exiting.
    /cm/local/apps/sge/var/spool/compute-00-00/job_scripts/302: line 325: task_id: command not found
    /cm/local/apps/sge/var/spool/compute-00-00/job_scripts/302: line 615: syntax error near unexpected token `"Task ",'
    /cm/local/apps/sge/var/spool/compute-00-00/job_scripts/302: line 615: `print("Task ", task_id, end='. ')'
    ```
  I dont know what is happening. Luis whas already been informed of this.
  
- In the meantime, the log parts that where in spanish where translated to english so that 
  it can be read by more people (mainly Villay that doesn't know spanish)
