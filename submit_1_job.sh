#!/bin/sh

#export PATH="$PATH:/home/julius_te/ispiero/miniconda3/condabin/"
#source /home/julius_te/ispiero/miniconda3/etc/profile.d/conda.sh
#conda activate SR_environment  

SCRIPT="code/simulate_adapted_datasets.py" #HPC: "/home/julius_te/ispiero/systematicreviews/code/ASReview_main_ss_new_sep2024.py"
BS=$SLURM_ARRAY_TASK_ID
export TORCH_HOME=/hpc/local/Rocky8/julius_te/ispiero/

python $SCRIPT -sim_id $BS
