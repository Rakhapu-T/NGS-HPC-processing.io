#!/bin/sh

############################### Trimmer Script ######################################

# The line below indicates which accounting group to log your job against
#SBATCH --account=pathology

# The line below selects the group of nodes you require
#SBATCH --partition=ada

# The line below reserves 1 worker node and 4 cores
#SBATCH --nodes=1 --ntasks=8

# The line below requests 8 hours to run the script
#SBATCH --time=08:00:00

# A sensible name for the job:
#SBATCH --job-name="Download_files_wget"


# >>>>>>>>>> Enter your email address here to get job status emails <<<<<<<<<<<<
# ==============================================================================
#SBATCH --mail-user="example.uct.ac.za"
# ==============================================================================


# Configure email notification, can be NONE, BEGIN, END, FAIL, ALL
#SBATCH --mail-type=BEGIN,END,FAIL


#########################################################################################

