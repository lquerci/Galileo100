#!/bin/bash
#SBATCH --job-name=run_python
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=1
#SBATCH --time=00:05:00
#SBATCH --mem=31200
#SBATCH --error=jobs_out/python/%x.%j.err
#SBATCH --output=jobs_out/python/%x.%j.out
#SBATCH --partition=g100_usr_dbg
#SBATCH --account=IscrC_UFD-SHF

python3 LatinHypercube_analysis.py