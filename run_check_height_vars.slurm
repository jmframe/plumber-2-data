#!/bin/bash -x
#SBATCH --job-name="gaps"
#SBATCH --account=s2027
#SBATCH --time=12:00:00
#SBATCH --constraint=hasw
#SBATCH --output="missing_heights.out"
#SBATCH --error="missing_heights.err"

# memory
ulimit -s unlimited
python print_no_height.py
