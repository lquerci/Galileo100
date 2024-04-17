#!/bin/bash
#SBATCH --job-name=run_python
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=1
#SBATCH --time=00:05:00
#SBATCH --mem=31200
#SBATCH --error=%x.%j.err
#SBATCH --output=%x.%j.out
#SBATCH --partition=g100_usr_dbg
#SBATCH --account=IscrC_UFD-SHF
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=lapo.querci1@unifi.it

python3 LatinHypercube_analysis.py