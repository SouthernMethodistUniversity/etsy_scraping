#!/bin/bash
#SBATCH -J htmlStripper
#SBATCH -o htmlStripper.out
#SBATCH -p htc
#SBATCH --mem=32G
#SBATCH --cpus-per-task=1

module purge
module load python
python3 htmlStripper.py
