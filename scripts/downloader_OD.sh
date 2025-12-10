#!/bin/sh

############################### ONEDRIVE DOWNLOADER ######################################

# The line below indicates which accounting group to log your job against
#SBATCH --account=pathology

# The line below selects the group of nodes you require
#SBATCH --partition=ada

# The line below reserves 1 worker node and 4 cores
#SBATCH --nodes=1 --ntasks=4

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


# >>>>>>>>>>>>>>>>>>>>>>>>> Enter the Download Link <<<<<<<<<<<<<<<<<<<<<<<<<<<<
# ==============================================================================
LINK="https://example.com/download_link"
# ==============================================================================


# >>>>>>>>>>>>>>>>>>>>>>>>> Enter the FileName <<<<<<<<<<<<<<<<<<<<<<<<<<<<
# ==============================================================================
LINK="https://example.com/download_link"
# ==============================================================================

# >>>>>>>>>>>>>>>>>>>>>>>>> Enter the file name <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# ==============================================================================
FILE="file_name"
# ==============================================================================


cd $SLURM_SUBMIT_DIR

LINK --output "$FILE"

if file "$FILE" | grep -q "Zip archive"; then
    unzip "$FILE" && rm "$FILE"
    echo "Download Complete."
else
    echo "Download Complete."
fi