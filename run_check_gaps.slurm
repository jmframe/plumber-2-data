#!/bin/bash -x
#SBATCH --job-name="gaps"
#SBATCH --account=s2027
#SBATCH --time=12:00:00
#SBATCH --constraint=hasw
#SBATCH --output="slurm.out"
#SBATCH --error="slurm.err"

# memory
ulimit -s unlimited
python check_data_for_gaps.py
