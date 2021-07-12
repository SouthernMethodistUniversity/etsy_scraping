#!/bin/bash
#SBATCH -J pageScrapper
#SBATCH -o /scratch/group/kbnk_group/projects/etsy_scraping/runs/out/pageScrapper_%A-%a.out
#SBATCH -p standard-mem-l
#SBATCH --mem=250G
#SBATCH --cpus-per-task=36
#SBATCH --array=1-279

module purge
module use /scratch/group/kbnk_group/projects/etsy_scraping/src
module load environment
python3 pageScrapper.py $SLURM_ARRAY_TASK_ID
