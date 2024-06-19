sbatch --cpus-per-task=1 --error="./errors/slurm-%A_%a.out" --output="./out/slurm-%A_%a.out" --time=00:30:00 --array=0-5:1  submit_1_job.sh
