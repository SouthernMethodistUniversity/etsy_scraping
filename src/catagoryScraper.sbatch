#!/bin/bash
#SBATCH -J catagoryScraper
#SBATCH -o catagoryScraper.out
#SBATCH -p htc
#SBATCH --mem=32G
#SBATCH --cpus-per-task=1

module purge
module use /scratch/group/kbnk_group/projects/etsy_scraping/src
module load environment
python3 catagoryScraper.py
