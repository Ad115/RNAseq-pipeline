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
  
- Also, a migration from Xonsh scripts to pure Python has been started, 
  mainly thinking about peers that may want to use the scripts and due to
  debugging difficulties while using them. Oh, and due to the sintax highlighting
  (not a really big problem but also contributed).
  
## August 13

- Luis has already answered, by parts, as Jack said xD:
    1. The paralell environment wasn't up, and he hadn't noticed. Now it is fixed.
    2. The issue with the compute host has to do with submitting a job from a compute node.
       (which is actually weird since at no point did I typed qlogin). This was solved via 
       qsub by hand instead of letting the script do it.
    3. The problem with syntax error was pretty obvious and on my face but didn't see it XP.
       It has to do wit having Python code in a Bash script!! Jaja. After that I had another 
       typo on the if-else, but it is now fixed.
       
- The new job array (317) has been generated and submitted and everything looks fine.

- It had to be stopped and resubmitted (job id 318) due to a typo that made each job ask for
  8 cores but only use 1.
  
- 14hrs It looks like the issue with the hanging jobs was solved, in ~15 minutes there has been a 
  steady stream of 27 completed jobs and none seems to be hanging out in a loop. It looks like
  Python was the problem: it is not good for submitting job arrays.
  
- 15:26 28 jobs have already finished but I'm a little worried that the last job finished about 
  an hour ago. Looks like the processes are hanging again. I checked at that time the size of
  an incomplete job's output file and checked again now and the sizes are the same. Looks like
  no new results are being generated. I'm gonna let the processes continue and if by 9 o' clock 
  there have been no new results, I'm killing the job array. The hypothesis now is that somehow 
  the parallel environment is messing up the jobs and so i'll try to resubmit the job array but 
  now removing the use of multiple cores per job.
  
- 23:44 No new job has finished and the file hasn't grown. I'm killing the job array now. I wrote
  earlier that I was suspicious of the parallel environment, but while that is still true, now I
  want to test first if the problem has to do with insufficient RAM memory. So I'm resubmitting
  the job array with 16G RAM (4x the current memory). Hope it works.
  

## August 16

- 16hrs Even though the jobs where submitted with very high resources (8 cores & 16G RAM), 
  the no job finished as of today. So, I made an experiment: Killed the ongoing job array 
  and logged in into a computing node (with qlogin) and started a job of the ones that tend 
  to hang out (job id 128). When I launched the job with 8 cores, the output file grew up to 
  ~300Mb and stayed there for a long time. But when I launched the job with only one core, the
  job finished succesfully in no time, with the output file steadily growing up to 855Mb.
  
- In view of this, it seems the number of cores HISAT2 uses is the problem. So, I'll be relaunching 
  the job array so that HISAT2 uses only 1 core. Also, I'm changing the generated script back to Python 
  as it seems the programming language has nothing to do.
  
- 16:20 Ressubmitted the job array using one core per job. Didn't change the generated submit script to 
  Python as it is not necessary. Maybe I'll do that later.
  
- 16:25. 52 Jobs have finished already! Looks like the problem is solved.

- 16:36. 87 Jobs have finished. Only the unpaired files remain and seem to be moving well.
  In retrospective this huge delay (been trying to do the mapping since May) could have been 
  avoided had I not tried to prematurely optimize by using multiple cores.
  
  
- 23:00 All jobs have finished. Now we proceed to the second step, converting the SAM files to BAM.
  The script 'script.sam_to_bam.xsh' was executed for this purpose, which generated the submit script
  and submitted the job array.


## August 17

- 11:17 The job array has finished, but inspecting the logs, looks like 12 files where truncated and
  where not converted. 

- The next step will be to remove those files and redo the mapping job for them.

## August 18 

- The scripts have been translated to pure Python, for the sake of consistency, 
  computing power and readability. A new script "script.error_cleanup.sam_to_bam.py" has been
  created to remove the truncated SAM files and was executed successfully.
  
- 19:00 The mapping process has been submitted to redo those files that where left truncated (and only those). 

## August 19

- 3:41hrs The process has finished. All files now ae mapped to the 
  genome and the mappings are compressed and sorted in  BAM files. 
  The next step is now to identify the mapped sites
  
- Investigating the next step, I found another protocol (https://www.biostars.org/p/207680/#207685)
  which is tailored speciffically for long non-coding RNAs, which is more complete than the 
  previous one (https://davetang.org/muse/2017/10/25/getting-started-hisat-stringtie-ballgown/).
  
- This made me realize I didn't do quality check on the FASTQ files, so this is what's next.

## August 27

- The script for quality check using FastQC was completed and submitted. The reports are being 
  saved in the 'quality' folder. The fact that all BAM files are now in the same folder 
  simplified greatly this process. 
  
- I discovered that (given that there are 281 SAM files) there exists a tool called MultiQC that
  handles the job of merging the results of the analysis of each sample, so that there's no need
  to analyze separatedly all ~300 sample reports. This is the next step.
  
- The FastQC checks have finished and the MultiQC report has been generated (The MultiQC step is 
  probably worth a script for it's own). Resulting in a large number of low quality reads and to 
  the realization that a necessary trimming step has been ommited, given that lots of reads contain 
  the adaptor. Also, it is necessary to ask Luis for the installation of "featureCount" to quantify 
  long non-coding RNAs. 