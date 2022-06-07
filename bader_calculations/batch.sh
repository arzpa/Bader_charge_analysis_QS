#!/bin/bash
#SBATCH --account=-
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --mem=0
#SBATCH --time=01:00:00
#SBATCH --job-name=Zn-POS
#SBATCH --mail-user=-
#SBATCH --mail-type=ALL
module load StdEnv/2020 intel/2020.1.217  openmpi/4.0.3
module load quantumespresso/6.8
srun pw.x < Cu_scf.in > Cu_scf.out
srun pp.x < Cu.cube.in > Cu.cube.out
