#!/bin/bash
#SBATCH --job-name=run_copy_files_00_mdm50
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=1
#SBATCH --time=00:50:00
#SBATCH --mem=31200
#SBATCH --error=jobs_out/%x.%j.err
#SBATCH --output=jobs_out/%x.%j.out
#SBATCH --partition=g100_usr_dbg
#SBATCH --account=IscrC_UFD-SHF


FILE_NAME="run_00.tar.gz"
DIRECTORY="00"

cd $SCRATCH/LatinHypercubeSampling/mdm_50

echo moved to
pwd

tar -cpvzf $FILE_NAME $DIRECTORY/*

echo coping
cp $FILE_NAME $WORK/lquerci0/LatinHypercubeSampling/mdm_50


cd $WORK/lquerci0/LatinHypercubeSampling/mdm_100

echo 
echo
echo move to
pwd

echo unzipp
tar -xvzf $FILE_NAME
 
echo end