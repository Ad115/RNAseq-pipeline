#! /cm/shared/apps/python36/3.6.3/bin/python3


#Run through this shell
#$ -S /cm/shared/apps/python36/3.6.3/bin/python3


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

#$ -pe openmp 1
#export OMP_NUM_THREADS=1

# Work with 4G RAM per process
#$ -l vf=4G

# Use as many jobs as needed
#$ -t 1-281

'''
Convert SAM files to BAM
------------------------

The current script was autogenerated with the 
file `script.sam_to_bam.py`, look there for documentation.

'''

import os
import subprocess
from pathlib import Path


# The commands to be executed
commands = dict()
commands[1]='samtools sort -@ 1 -o map/mm1L_001_paired.bam map/mm1L_001_paired.sam'
commands[2]='samtools sort -@ 1 -o map/mm1L_002_paired.bam map/mm1L_002_paired.sam'
commands[3]='samtools sort -@ 1 -o map/mm3L_005_paired.bam map/mm3L_005_paired.sam'
commands[4]='samtools sort -@ 1 -o map/mm1L_006_paired.bam map/mm1L_006_paired.sam'
commands[5]='samtools sort -@ 1 -o map/mm3L_028_paired.bam map/mm3L_028_paired.sam'
commands[6]='samtools sort -@ 1 -o map/mm1L_004_paired.bam map/mm1L_004_paired.sam'
commands[7]='samtools sort -@ 1 -o map/mm1L_007_paired.bam map/mm1L_007_paired.sam'
commands[8]='samtools sort -@ 1 -o map/mm1L_008_paired.bam map/mm1L_008_paired.sam'
commands[9]='samtools sort -@ 1 -o map/mm1L_009_paired.bam map/mm1L_009_paired.sam'
commands[10]='samtools sort -@ 1 -o map/mm3L_004_paired.bam map/mm3L_004_paired.sam'
commands[11]='samtools sort -@ 1 -o map/mm3L_030_paired.bam map/mm3L_030_paired.sam'
commands[12]='samtools sort -@ 1 -o map/mm1L_011_paired.bam map/mm1L_011_paired.sam'
commands[13]='samtools sort -@ 1 -o map/mm1L_013_paired.bam map/mm1L_013_paired.sam'
commands[14]='samtools sort -@ 1 -o map/mm1L_014_paired.bam map/mm1L_014_paired.sam'
commands[15]='samtools sort -@ 1 -o map/mm1L_015_paired.bam map/mm1L_015_paired.sam'
commands[16]='samtools sort -@ 1 -o map/mm1L_017_paired.bam map/mm1L_017_paired.sam'
commands[17]='samtools sort -@ 1 -o map/mm1L_016_paired.bam map/mm1L_016_paired.sam'
commands[18]='samtools sort -@ 1 -o map/mm3L_034_paired.bam map/mm3L_034_paired.sam'
commands[19]='samtools sort -@ 1 -o map/mm1L_019_paired.bam map/mm1L_019_paired.sam'
commands[20]='samtools sort -@ 1 -o map/mm1L_020_paired.bam map/mm1L_020_paired.sam'
commands[21]='samtools sort -@ 1 -o map/mm1L_021_paired.bam map/mm1L_021_paired.sam'
commands[22]='samtools sort -@ 1 -o map/mm1L_022_paired.bam map/mm1L_022_paired.sam'
commands[23]='samtools sort -@ 1 -o map/mm1L_023_paired.bam map/mm1L_023_paired.sam'
commands[24]='samtools sort -@ 1 -o map/mm3L_033_paired.bam map/mm3L_033_paired.sam'
commands[25]='samtools sort -@ 1 -o map/mm1L_025_paired.bam map/mm1L_025_paired.sam'
commands[26]='samtools sort -@ 1 -o map/mm1L_026_paired.bam map/mm1L_026_paired.sam'
commands[27]='samtools sort -@ 1 -o map/mm1L_027_paired.bam map/mm1L_027_paired.sam'
commands[28]='samtools sort -@ 1 -o map/mm1L_028_paired.bam map/mm1L_028_paired.sam'
commands[29]='samtools sort -@ 1 -o map/mm1L_029_paired.bam map/mm1L_029_paired.sam'
commands[30]='samtools sort -@ 1 -o map/mm1L_030_paired.bam map/mm1L_030_paired.sam'
commands[31]='samtools sort -@ 1 -o map/mm1L_031_paired.bam map/mm1L_031_paired.sam'
commands[32]='samtools sort -@ 1 -o map/mm1L_032_paired.bam map/mm1L_032_paired.sam'
commands[33]='samtools sort -@ 1 -o map/mm1L_033_paired.bam map/mm1L_033_paired.sam'
commands[34]='samtools sort -@ 1 -o map/mm1L_034_paired.bam map/mm1L_034_paired.sam'
commands[35]='samtools sort -@ 1 -o map/mm1L_035_paired.bam map/mm1L_035_paired.sam'
commands[36]='samtools sort -@ 1 -o map/mm1L_036_paired.bam map/mm1L_036_paired.sam'
commands[37]='samtools sort -@ 1 -o map/mm1L_037_paired.bam map/mm1L_037_paired.sam'
commands[38]='samtools sort -@ 1 -o map/mm3L_035_paired.bam map/mm3L_035_paired.sam'
commands[39]='samtools sort -@ 1 -o map/mm1L_039_paired.bam map/mm1L_039_paired.sam'
commands[40]='samtools sort -@ 1 -o map/mm3L_037_paired.bam map/mm3L_037_paired.sam'
commands[41]='samtools sort -@ 1 -o map/mm2R_001_paired.bam map/mm2R_001_paired.sam'
commands[42]='samtools sort -@ 1 -o map/mm3L_036_paired.bam map/mm3L_036_paired.sam'
commands[43]='samtools sort -@ 1 -o map/mm2R_003_paired.bam map/mm2R_003_paired.sam'
commands[44]='samtools sort -@ 1 -o map/mm2R_004_paired.bam map/mm2R_004_paired.sam'
commands[45]='samtools sort -@ 1 -o map/mm2R_005_paired.bam map/mm2R_005_paired.sam'
commands[46]='samtools sort -@ 1 -o map/mm2R_006_paired.bam map/mm2R_006_paired.sam'
commands[47]='samtools sort -@ 1 -o map/mm2R_007_paired.bam map/mm2R_007_paired.sam'
commands[48]='samtools sort -@ 1 -o map/mm2R_008_paired.bam map/mm2R_008_paired.sam'
commands[49]='samtools sort -@ 1 -o map/mm2R_009_paired.bam map/mm2R_009_paired.sam'
commands[50]='samtools sort -@ 1 -o map/mm1L_024_paired.bam map/mm1L_024_paired.sam'
commands[51]='samtools sort -@ 1 -o map/mm2R_018_paired.bam map/mm2R_018_paired.sam'
commands[52]='samtools sort -@ 1 -o map/mm2R_024_paired.bam map/mm2R_024_paired.sam'
commands[53]='samtools sort -@ 1 -o map/mm1L_012_paired.bam map/mm1L_012_paired.sam'
commands[54]='samtools sort -@ 1 -o map/mm1L_010_paired.bam map/mm1L_010_paired.sam'
commands[55]='samtools sort -@ 1 -o map/mm1L_005_paired.bam map/mm1L_005_paired.sam'
commands[56]='samtools sort -@ 1 -o map/mm1L_unpaired.bam map/mm1L_unpaired.sam'
commands[57]='samtools sort -@ 1 -o map/mm2R_002_paired.bam map/mm2R_002_paired.sam'
commands[58]='samtools sort -@ 1 -o map/mm2R_025_paired.bam map/mm2R_025_paired.sam'
commands[59]='samtools sort -@ 1 -o map/mm2R_010_paired.bam map/mm2R_010_paired.sam'
commands[60]='samtools sort -@ 1 -o map/mm2R_013_paired.bam map/mm2R_013_paired.sam'
commands[61]='samtools sort -@ 1 -o map/mm2R_014_paired.bam map/mm2R_014_paired.sam'
commands[62]='samtools sort -@ 1 -o map/mm2R_011_paired.bam map/mm2R_011_paired.sam'
commands[63]='samtools sort -@ 1 -o map/mm2R_012_paired.bam map/mm2R_012_paired.sam'
commands[64]='samtools sort -@ 1 -o map/mm2R_026_paired.bam map/mm2R_026_paired.sam'
commands[65]='samtools sort -@ 1 -o map/mm2R_019_paired.bam map/mm2R_019_paired.sam'
commands[66]='samtools sort -@ 1 -o map/mm2R_022_paired.bam map/mm2R_022_paired.sam'
commands[67]='samtools sort -@ 1 -o map/mm2R_041_paired.bam map/mm2R_041_paired.sam'
commands[68]='samtools sort -@ 1 -o map/mm2R_021_paired.bam map/mm2R_021_paired.sam'
commands[69]='samtools sort -@ 1 -o map/mm2R_020_paired.bam map/mm2R_020_paired.sam'
commands[70]='samtools sort -@ 1 -o map/mm2R_017_paired.bam map/mm2R_017_paired.sam'
commands[71]='samtools sort -@ 1 -o map/mm2R_023_paired.bam map/mm2R_023_paired.sam'
commands[72]='samtools sort -@ 1 -o map/mm2R_unpaired.bam map/mm2R_unpaired.sam'
commands[73]='samtools sort -@ 1 -o map/mm2R_046_paired.bam map/mm2R_046_paired.sam'
commands[74]='samtools sort -@ 1 -o map/mm2R_015_paired.bam map/mm2R_015_paired.sam'
commands[75]='samtools sort -@ 1 -o map/mm2R_016_paired.bam map/mm2R_016_paired.sam'
commands[76]='samtools sort -@ 1 -o map/mm2R_028_paired.bam map/mm2R_028_paired.sam'
commands[77]='samtools sort -@ 1 -o map/mm2R_029_paired.bam map/mm2R_029_paired.sam'
commands[78]='samtools sort -@ 1 -o map/mm2R_027_paired.bam map/mm2R_027_paired.sam'
commands[79]='samtools sort -@ 1 -o map/mm2R_031_paired.bam map/mm2R_031_paired.sam'
commands[80]='samtools sort -@ 1 -o map/mm2R_036_paired.bam map/mm2R_036_paired.sam'
commands[81]='samtools sort -@ 1 -o map/mm2R_032_paired.bam map/mm2R_032_paired.sam'
commands[82]='samtools sort -@ 1 -o map/mm2R_033_paired.bam map/mm2R_033_paired.sam'
commands[83]='samtools sort -@ 1 -o map/mm2R_034_paired.bam map/mm2R_034_paired.sam'
commands[84]='samtools sort -@ 1 -o map/mm2R_035_paired.bam map/mm2R_035_paired.sam'
commands[85]='samtools sort -@ 1 -o map/mm2R_030_paired.bam map/mm2R_030_paired.sam'
commands[86]='samtools sort -@ 1 -o map/mm2R_038_paired.bam map/mm2R_038_paired.sam'
commands[87]='samtools sort -@ 1 -o map/mm2R_037_paired.bam map/mm2R_037_paired.sam'
commands[88]='samtools sort -@ 1 -o map/mm3L_010_paired.bam map/mm3L_010_paired.sam'
commands[89]='samtools sort -@ 1 -o map/mm2R_044_paired.bam map/mm2R_044_paired.sam'
commands[90]='samtools sort -@ 1 -o map/mm2R_042_paired.bam map/mm2R_042_paired.sam'
commands[91]='samtools sort -@ 1 -o map/mm2R_043_paired.bam map/mm2R_043_paired.sam'
commands[92]='samtools sort -@ 1 -o map/mm2R_039_paired.bam map/mm2R_039_paired.sam'
commands[93]='samtools sort -@ 1 -o map/mm2R_040_paired.bam map/mm2R_040_paired.sam'
commands[94]='samtools sort -@ 1 -o map/mm3L_008_paired.bam map/mm3L_008_paired.sam'
commands[95]='samtools sort -@ 1 -o map/mm2R_045_paired.bam map/mm2R_045_paired.sam'
commands[96]='samtools sort -@ 1 -o map/mm2R_047_paired.bam map/mm2R_047_paired.sam'
commands[97]='samtools sort -@ 1 -o map/mm3L_003_paired.bam map/mm3L_003_paired.sam'
commands[98]='samtools sort -@ 1 -o map/mm2R_048_paired.bam map/mm2R_048_paired.sam'
commands[99]='samtools sort -@ 1 -o map/mm3L_011_paired.bam map/mm3L_011_paired.sam'
commands[100]='samtools sort -@ 1 -o map/mm3L_002_paired.bam map/mm3L_002_paired.sam'
commands[101]='samtools sort -@ 1 -o map/mm3L_001_paired.bam map/mm3L_001_paired.sam'
commands[102]='samtools sort -@ 1 -o map/mm3L_006_paired.bam map/mm3L_006_paired.sam'
commands[103]='samtools sort -@ 1 -o map/mm3L_007_paired.bam map/mm3L_007_paired.sam'
commands[104]='samtools sort -@ 1 -o map/mm3L_009_paired.bam map/mm3L_009_paired.sam'
commands[105]='samtools sort -@ 1 -o map/mm1L_003_paired.bam map/mm1L_003_paired.sam'
commands[106]='samtools sort -@ 1 -o map/mm1L_018_paired.bam map/mm1L_018_paired.sam'
commands[107]='samtools sort -@ 1 -o map/mm1L_038_paired.bam map/mm1L_038_paired.sam'
commands[108]='samtools sort -@ 1 -o map/mm3L_012_paired.bam map/mm3L_012_paired.sam'
commands[109]='samtools sort -@ 1 -o map/mm3L_016_paired.bam map/mm3L_016_paired.sam'
commands[110]='samtools sort -@ 1 -o map/mm3L_013_paired.bam map/mm3L_013_paired.sam'
commands[111]='samtools sort -@ 1 -o map/mm3L_014_paired.bam map/mm3L_014_paired.sam'
commands[112]='samtools sort -@ 1 -o map/mm3L_015_paired.bam map/mm3L_015_paired.sam'
commands[113]='samtools sort -@ 1 -o map/mm3L_019_paired.bam map/mm3L_019_paired.sam'
commands[114]='samtools sort -@ 1 -o map/mm3L_020_paired.bam map/mm3L_020_paired.sam'
commands[115]='samtools sort -@ 1 -o map/mm3L_021_paired.bam map/mm3L_021_paired.sam'
commands[116]='samtools sort -@ 1 -o map/mm3L_017_paired.bam map/mm3L_017_paired.sam'
commands[117]='samtools sort -@ 1 -o map/mm3L_022_paired.bam map/mm3L_022_paired.sam'
commands[118]='samtools sort -@ 1 -o map/mm3L_018_paired.bam map/mm3L_018_paired.sam'
commands[119]='samtools sort -@ 1 -o map/mm3L_023_paired.bam map/mm3L_023_paired.sam'
commands[120]='samtools sort -@ 1 -o map/mm3L_027_paired.bam map/mm3L_027_paired.sam'
commands[121]='samtools sort -@ 1 -o map/mm3L_024_paired.bam map/mm3L_024_paired.sam'
commands[122]='samtools sort -@ 1 -o map/mm3L_025_paired.bam map/mm3L_025_paired.sam'
commands[123]='samtools sort -@ 1 -o map/mm3L_026_paired.bam map/mm3L_026_paired.sam'
commands[124]='samtools sort -@ 1 -o map/mm3L_029_paired.bam map/mm3L_029_paired.sam'
commands[125]='samtools sort -@ 1 -o map/mm3L_031_paired.bam map/mm3L_031_paired.sam'
commands[126]='samtools sort -@ 1 -o map/mm3L_032_paired.bam map/mm3L_032_paired.sam'
commands[127]='samtools sort -@ 1 -o map/mm3L_038_paired.bam map/mm3L_038_paired.sam'
commands[128]='samtools sort -@ 1 -o map/mm2L_007_paired.bam map/mm2L_007_paired.sam'
commands[129]='samtools sort -@ 1 -o map/mm3L_040_paired.bam map/mm3L_040_paired.sam'
commands[130]='samtools sort -@ 1 -o map/mm3R_046_paired.bam map/mm3R_046_paired.sam'
commands[131]='samtools sort -@ 1 -o map/mm3L_041_paired.bam map/mm3L_041_paired.sam'
commands[132]='samtools sort -@ 1 -o map/mm3L_046_paired.bam map/mm3L_046_paired.sam'
commands[133]='samtools sort -@ 1 -o map/mm3L_043_paired.bam map/mm3L_043_paired.sam'
commands[134]='samtools sort -@ 1 -o map/mm3L_044_paired.bam map/mm3L_044_paired.sam'
commands[135]='samtools sort -@ 1 -o map/mm3L_045_paired.bam map/mm3L_045_paired.sam'
commands[136]='samtools sort -@ 1 -o map/mm3L_048_paired.bam map/mm3L_048_paired.sam'
commands[137]='samtools sort -@ 1 -o map/mm3L_047_paired.bam map/mm3L_047_paired.sam'
commands[138]='samtools sort -@ 1 -o map/mm3L_049_paired.bam map/mm3L_049_paired.sam'
commands[139]='samtools sort -@ 1 -o map/mm3L_051_paired.bam map/mm3L_051_paired.sam'
commands[140]='samtools sort -@ 1 -o map/mm3L_052_paired.bam map/mm3L_052_paired.sam'
commands[141]='samtools sort -@ 1 -o map/mm3L_053_paired.bam map/mm3L_053_paired.sam'
commands[142]='samtools sort -@ 1 -o map/mm3L_050_paired.bam map/mm3L_050_paired.sam'
commands[143]='samtools sort -@ 1 -o map/mm1R_001_paired.bam map/mm1R_001_paired.sam'
commands[144]='samtools sort -@ 1 -o map/mm3R_035_paired.bam map/mm3R_035_paired.sam'
commands[145]='samtools sort -@ 1 -o map/mm1R_002_paired.bam map/mm1R_002_paired.sam'
commands[146]='samtools sort -@ 1 -o map/mm1R_003_paired.bam map/mm1R_003_paired.sam'
commands[147]='samtools sort -@ 1 -o map/mm1R_005_paired.bam map/mm1R_005_paired.sam'
commands[148]='samtools sort -@ 1 -o map/mm1R_004_paired.bam map/mm1R_004_paired.sam'
commands[149]='samtools sort -@ 1 -o map/mm2L_008_paired.bam map/mm2L_008_paired.sam'
commands[150]='samtools sort -@ 1 -o map/mm1R_006_paired.bam map/mm1R_006_paired.sam'
commands[151]='samtools sort -@ 1 -o map/mm2L_002_paired.bam map/mm2L_002_paired.sam'
commands[152]='samtools sort -@ 1 -o map/mm1R_009_paired.bam map/mm1R_009_paired.sam'
commands[153]='samtools sort -@ 1 -o map/mm2L_010_paired.bam map/mm2L_010_paired.sam'
commands[154]='samtools sort -@ 1 -o map/mm1R_011_paired.bam map/mm1R_011_paired.sam'
commands[155]='samtools sort -@ 1 -o map/mm1R_012_paired.bam map/mm1R_012_paired.sam'
commands[156]='samtools sort -@ 1 -o map/mm2L_001_paired.bam map/mm2L_001_paired.sam'
commands[157]='samtools sort -@ 1 -o map/mm2L_011_paired.bam map/mm2L_011_paired.sam'
commands[158]='samtools sort -@ 1 -o map/mm1R_015_paired.bam map/mm1R_015_paired.sam'
commands[159]='samtools sort -@ 1 -o map/mm1R_016_paired.bam map/mm1R_016_paired.sam'
commands[160]='samtools sort -@ 1 -o map/mm1R_017_paired.bam map/mm1R_017_paired.sam'
commands[161]='samtools sort -@ 1 -o map/mm1R_018_paired.bam map/mm1R_018_paired.sam'
commands[162]='samtools sort -@ 1 -o map/mm1R_019_paired.bam map/mm1R_019_paired.sam'
commands[163]='samtools sort -@ 1 -o map/mm1R_020_paired.bam map/mm1R_020_paired.sam'
commands[164]='samtools sort -@ 1 -o map/mm1R_021_paired.bam map/mm1R_021_paired.sam'
commands[165]='samtools sort -@ 1 -o map/mm1R_022_paired.bam map/mm1R_022_paired.sam'
commands[166]='samtools sort -@ 1 -o map/mm1R_023_paired.bam map/mm1R_023_paired.sam'
commands[167]='samtools sort -@ 1 -o map/mm1R_024_paired.bam map/mm1R_024_paired.sam'
commands[168]='samtools sort -@ 1 -o map/mm1R_025_paired.bam map/mm1R_025_paired.sam'
commands[169]='samtools sort -@ 1 -o map/mm3L_042_paired.bam map/mm3L_042_paired.sam'
commands[170]='samtools sort -@ 1 -o map/mm3R_041_paired.bam map/mm3R_041_paired.sam'
commands[171]='samtools sort -@ 1 -o map/mm3R_043_paired.bam map/mm3R_043_paired.sam'
commands[172]='samtools sort -@ 1 -o map/mm3R_045_paired.bam map/mm3R_045_paired.sam'
commands[173]='samtools sort -@ 1 -o map/mm3R_unpaired.bam map/mm3R_unpaired.sam'
commands[174]='samtools sort -@ 1 -o map/mm2L_004_paired.bam map/mm2L_004_paired.sam'
commands[175]='samtools sort -@ 1 -o map/mm2L_006_paired.bam map/mm2L_006_paired.sam'
commands[176]='samtools sort -@ 1 -o map/mm2L_012_paired.bam map/mm2L_012_paired.sam'
commands[177]='samtools sort -@ 1 -o map/mm1R_026_paired.bam map/mm1R_026_paired.sam'
commands[178]='samtools sort -@ 1 -o map/mm2L_014_paired.bam map/mm2L_014_paired.sam'
commands[179]='samtools sort -@ 1 -o map/mm1R_031_paired.bam map/mm1R_031_paired.sam'
commands[180]='samtools sort -@ 1 -o map/mm1R_030_paired.bam map/mm1R_030_paired.sam'
commands[181]='samtools sort -@ 1 -o map/mm1R_029_paired.bam map/mm1R_029_paired.sam'
commands[182]='samtools sort -@ 1 -o map/mm1R_027_paired.bam map/mm1R_027_paired.sam'
commands[183]='samtools sort -@ 1 -o map/mm1R_028_paired.bam map/mm1R_028_paired.sam'
commands[184]='samtools sort -@ 1 -o map/mm2L_005_paired.bam map/mm2L_005_paired.sam'
commands[185]='samtools sort -@ 1 -o map/mm2L_017_paired.bam map/mm2L_017_paired.sam'
commands[186]='samtools sort -@ 1 -o map/mm1R_038_paired.bam map/mm1R_038_paired.sam'
commands[187]='samtools sort -@ 1 -o map/mm1R_036_paired.bam map/mm1R_036_paired.sam'
commands[188]='samtools sort -@ 1 -o map/mm1R_035_paired.bam map/mm1R_035_paired.sam'
commands[189]='samtools sort -@ 1 -o map/mm1R_037_paired.bam map/mm1R_037_paired.sam'
commands[190]='samtools sort -@ 1 -o map/mm1R_040_paired.bam map/mm1R_040_paired.sam'
commands[191]='samtools sort -@ 1 -o map/mm1R_039_paired.bam map/mm1R_039_paired.sam'
commands[192]='samtools sort -@ 1 -o map/mm1R_041_paired.bam map/mm1R_041_paired.sam'
commands[193]='samtools sort -@ 1 -o map/mm1R_042_paired.bam map/mm1R_042_paired.sam'
commands[194]='samtools sort -@ 1 -o map/mm2L_013_paired.bam map/mm2L_013_paired.sam'
commands[195]='samtools sort -@ 1 -o map/mm3R_001_paired.bam map/mm3R_001_paired.sam'
commands[196]='samtools sort -@ 1 -o map/mm2L_016_paired.bam map/mm2L_016_paired.sam'
commands[197]='samtools sort -@ 1 -o map/mm1R_044_paired.bam map/mm1R_044_paired.sam'
commands[198]='samtools sort -@ 1 -o map/mm3R_003_paired.bam map/mm3R_003_paired.sam'
commands[199]='samtools sort -@ 1 -o map/mm3R_002_paired.bam map/mm3R_002_paired.sam'
commands[200]='samtools sort -@ 1 -o map/mm2L_019_paired.bam map/mm2L_019_paired.sam'
commands[201]='samtools sort -@ 1 -o map/mm3R_005_paired.bam map/mm3R_005_paired.sam'
commands[202]='samtools sort -@ 1 -o map/mm3R_006_paired.bam map/mm3R_006_paired.sam'
commands[203]='samtools sort -@ 1 -o map/mm3R_007_paired.bam map/mm3R_007_paired.sam'
commands[204]='samtools sort -@ 1 -o map/mm3R_008_paired.bam map/mm3R_008_paired.sam'
commands[205]='samtools sort -@ 1 -o map/mm3R_009_paired.bam map/mm3R_009_paired.sam'
commands[206]='samtools sort -@ 1 -o map/mm3R_010_paired.bam map/mm3R_010_paired.sam'
commands[207]='samtools sort -@ 1 -o map/mm3R_011_paired.bam map/mm3R_011_paired.sam'
commands[208]='samtools sort -@ 1 -o map/mm3R_012_paired.bam map/mm3R_012_paired.sam'
commands[209]='samtools sort -@ 1 -o map/mm3R_013_paired.bam map/mm3R_013_paired.sam'
commands[210]='samtools sort -@ 1 -o map/mm3R_040_paired.bam map/mm3R_040_paired.sam'
commands[211]='samtools sort -@ 1 -o map/mm2L_003_paired.bam map/mm2L_003_paired.sam'
commands[212]='samtools sort -@ 1 -o map/mm2L_015_paired.bam map/mm2L_015_paired.sam'
commands[213]='samtools sort -@ 1 -o map/mm1R_008_paired.bam map/mm1R_008_paired.sam'
commands[214]='samtools sort -@ 1 -o map/mm3L_039_paired.bam map/mm3L_039_paired.sam'
commands[215]='samtools sort -@ 1 -o map/mm3L_unpaired.bam map/mm3L_unpaired.sam'
commands[216]='samtools sort -@ 1 -o map/mm1R_007_paired.bam map/mm1R_007_paired.sam'
commands[217]='samtools sort -@ 1 -o map/mm1R_013_paired.bam map/mm1R_013_paired.sam'
commands[218]='samtools sort -@ 1 -o map/mm1R_014_paired.bam map/mm1R_014_paired.sam'
commands[219]='samtools sort -@ 1 -o map/mm1R_010_paired.bam map/mm1R_010_paired.sam'
commands[220]='samtools sort -@ 1 -o map/mm3R_033_paired.bam map/mm3R_033_paired.sam'
commands[221]='samtools sort -@ 1 -o map/mm3R_004_paired.bam map/mm3R_004_paired.sam'
commands[222]='samtools sort -@ 1 -o map/mm1R_034_paired.bam map/mm1R_034_paired.sam'
commands[223]='samtools sort -@ 1 -o map/mm1R_033_paired.bam map/mm1R_033_paired.sam'
commands[224]='samtools sort -@ 1 -o map/mm1R_032_paired.bam map/mm1R_032_paired.sam'
commands[225]='samtools sort -@ 1 -o map/mm1R_043_paired.bam map/mm1R_043_paired.sam'
commands[226]='samtools sort -@ 1 -o map/mm3R_014_paired.bam map/mm3R_014_paired.sam'
commands[227]='samtools sort -@ 1 -o map/mm1R_unpaired.bam map/mm1R_unpaired.sam'
commands[228]='samtools sort -@ 1 -o map/mm3R_016_paired.bam map/mm3R_016_paired.sam'
commands[229]='samtools sort -@ 1 -o map/mm3R_015_paired.bam map/mm3R_015_paired.sam'
commands[230]='samtools sort -@ 1 -o map/mm3R_019_paired.bam map/mm3R_019_paired.sam'
commands[231]='samtools sort -@ 1 -o map/mm3R_018_paired.bam map/mm3R_018_paired.sam'
commands[232]='samtools sort -@ 1 -o map/mm3R_025_paired.bam map/mm3R_025_paired.sam'
commands[233]='samtools sort -@ 1 -o map/mm3R_021_paired.bam map/mm3R_021_paired.sam'
commands[234]='samtools sort -@ 1 -o map/mm3R_030_paired.bam map/mm3R_030_paired.sam'
commands[235]='samtools sort -@ 1 -o map/mm3R_027_paired.bam map/mm3R_027_paired.sam'
commands[236]='samtools sort -@ 1 -o map/mm3R_024_paired.bam map/mm3R_024_paired.sam'
commands[237]='samtools sort -@ 1 -o map/mm3R_029_paired.bam map/mm3R_029_paired.sam'
commands[238]='samtools sort -@ 1 -o map/mm3R_023_paired.bam map/mm3R_023_paired.sam'
commands[239]='samtools sort -@ 1 -o map/mm3R_026_paired.bam map/mm3R_026_paired.sam'
commands[240]='samtools sort -@ 1 -o map/mm3R_028_paired.bam map/mm3R_028_paired.sam'
commands[241]='samtools sort -@ 1 -o map/mm3R_031_paired.bam map/mm3R_031_paired.sam'
commands[242]='samtools sort -@ 1 -o map/mm3R_032_paired.bam map/mm3R_032_paired.sam'
commands[243]='samtools sort -@ 1 -o map/mm3R_022_paired.bam map/mm3R_022_paired.sam'
commands[244]='samtools sort -@ 1 -o map/mm3R_020_paired.bam map/mm3R_020_paired.sam'
commands[245]='samtools sort -@ 1 -o map/mm3R_017_paired.bam map/mm3R_017_paired.sam'
commands[246]='samtools sort -@ 1 -o map/mm3R_036_paired.bam map/mm3R_036_paired.sam'
commands[247]='samtools sort -@ 1 -o map/mm3R_034_paired.bam map/mm3R_034_paired.sam'
commands[248]='samtools sort -@ 1 -o map/mm3R_038_paired.bam map/mm3R_038_paired.sam'
commands[249]='samtools sort -@ 1 -o map/mm3R_042_paired.bam map/mm3R_042_paired.sam'
commands[250]='samtools sort -@ 1 -o map/mm3R_037_paired.bam map/mm3R_037_paired.sam'
commands[251]='samtools sort -@ 1 -o map/mm3R_039_paired.bam map/mm3R_039_paired.sam'
commands[252]='samtools sort -@ 1 -o map/mm3R_044_paired.bam map/mm3R_044_paired.sam'
commands[253]='samtools sort -@ 1 -o map/mm2L_009_paired.bam map/mm2L_009_paired.sam'
commands[254]='samtools sort -@ 1 -o map/mm2L_018_paired.bam map/mm2L_018_paired.sam'
commands[255]='samtools sort -@ 1 -o map/mm2L_020_paired.bam map/mm2L_020_paired.sam'
commands[256]='samtools sort -@ 1 -o map/mm2L_021_paired.bam map/mm2L_021_paired.sam'
commands[257]='samtools sort -@ 1 -o map/mm2L_023_paired.bam map/mm2L_023_paired.sam'
commands[258]='samtools sort -@ 1 -o map/mm2L_022_paired.bam map/mm2L_022_paired.sam'
commands[259]='samtools sort -@ 1 -o map/mm2L_024_paired.bam map/mm2L_024_paired.sam'
commands[260]='samtools sort -@ 1 -o map/mm2L_025_paired.bam map/mm2L_025_paired.sam'
commands[261]='samtools sort -@ 1 -o map/mm2L_026_paired.bam map/mm2L_026_paired.sam'
commands[262]='samtools sort -@ 1 -o map/mm2L_028_paired.bam map/mm2L_028_paired.sam'
commands[263]='samtools sort -@ 1 -o map/mm2L_033_paired.bam map/mm2L_033_paired.sam'
commands[264]='samtools sort -@ 1 -o map/mm2L_032_paired.bam map/mm2L_032_paired.sam'
commands[265]='samtools sort -@ 1 -o map/mm2L_031_paired.bam map/mm2L_031_paired.sam'
commands[266]='samtools sort -@ 1 -o map/mm2L_027_paired.bam map/mm2L_027_paired.sam'
commands[267]='samtools sort -@ 1 -o map/mm2L_029_paired.bam map/mm2L_029_paired.sam'
commands[268]='samtools sort -@ 1 -o map/mm2L_030_paired.bam map/mm2L_030_paired.sam'
commands[269]='samtools sort -@ 1 -o map/mm2L_034_paired.bam map/mm2L_034_paired.sam'
commands[270]='samtools sort -@ 1 -o map/mm2L_038_paired.bam map/mm2L_038_paired.sam'
commands[271]='samtools sort -@ 1 -o map/mm2L_042_paired.bam map/mm2L_042_paired.sam'
commands[272]='samtools sort -@ 1 -o map/mm2L_036_paired.bam map/mm2L_036_paired.sam'
commands[273]='samtools sort -@ 1 -o map/mm2L_044_paired.bam map/mm2L_044_paired.sam'
commands[274]='samtools sort -@ 1 -o map/mm2L_043_paired.bam map/mm2L_043_paired.sam'
commands[275]='samtools sort -@ 1 -o map/mm2L_041_paired.bam map/mm2L_041_paired.sam'
commands[276]='samtools sort -@ 1 -o map/mm2L_035_paired.bam map/mm2L_035_paired.sam'
commands[277]='samtools sort -@ 1 -o map/mm2L_040_paired.bam map/mm2L_040_paired.sam'
commands[278]='samtools sort -@ 1 -o map/mm2L_037_paired.bam map/mm2L_037_paired.sam'
commands[279]='samtools sort -@ 1 -o map/mm2L_045_paired.bam map/mm2L_045_paired.sam'
commands[280]='samtools sort -@ 1 -o map/mm2L_unpaired.bam map/mm2L_unpaired.sam'
commands[281]='samtools sort -@ 1 -o map/mm2L_039_paired.bam map/mm2L_039_paired.sam'

# Fetch the job id
job_id = int( os.environ['SGE_TASK_ID'] )

# Fetch the command corresponding to the current job
command = commands[job_id]

# Get the name of the output file
#   -> The output file is the next string after the '-o' argument
output_file = command.split()[command.split().index('-o') + 1]

# Execute the job
if Path(output_file).exists():
    print('Output file already exists:', output_file)
    
else:
    print("Executing command:", command)

    subprocess.run(command.split()) # <-- Here it is executed, splitting is 
                                    #     necessary to pass the arguments 
                                    #     appropriately
                       
    print("Finished execution.")
