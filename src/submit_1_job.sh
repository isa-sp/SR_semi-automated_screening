#!/bin/sh

#export PATH="$PATH:/home/julius_te/ispiero/miniconda3/condabin/"
#source /home/julius_te/ispiero/miniconda3/etc/profile.d/conda.sh
#conda activate SR_environment  #env create -f TM_environment.yml -p /home/julius_te/ispiero/env/TM_environment

SCRIPT="/path/to/scripts/ASReview_main_ss.py"
BS=$SLURM_ARRAY_TASK_ID
export TORCH_HOME=/hpc/local/Rocky8/julius_te/ispiero/

python $SCRIPT -sim_id $BS
