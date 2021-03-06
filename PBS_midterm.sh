#!/bin/bash
#PBS -l nodes=1:ppn=5
#PBS -l walltime=0:30:00
#PBS -q pace-ice
#PBS -N training_job
#PBS -o stdout
#PBS -e stderr
cd $PBS_O_WORKDIR

source /storage/home/hpaceice1/fwang356/sparc_run/sparc_env.sh
python midterm.py
