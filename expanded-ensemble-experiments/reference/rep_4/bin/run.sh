#!/bin/sh
#SBATCH --job-name HG_FW7
#SBATCH --ntasks 1
#SBATCH --output CB7.out
#SBATCH --qos long
#SBATCH --nodes 1
#SBATCH --time 120:00:00
#SBATCH --partition shas
#SBATCH --ntasks-per-node 24
ml gromacs/5.1.2
gmx grompp -f CB7_expanded.mdp -po CB7_mdout.mdp -c CB7_Guest3.gro -p CB7_Guest3.top -o CB7_Guest3.tpr -n CB7_Guest3.ndx -maxwarn 4
gmx mdrun -deffnm CB7_Guest3 -dhdl CB7_Guest3_dhdl.xvg -g CB7_Guest3_log.log -nt 24
