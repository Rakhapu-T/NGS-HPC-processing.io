#!/usr/bin/env bash

############################### run_mageck ######################################

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

set -euo pipefail

#>>>>>>>>>>>> Inputs <<<<<<<<<<<#

# Fastq files (ordered)
FASTQ_FILES=(

)

# Sample Labels (same order as FASTQ_FILES)
SAMPLE_LABELS=(

)

# Path to sgRNA library in CSV format (Relative Path)
LIBR=""

# Output prefix for count files (Relative Path)
OUTPUT_PREFIX=""

# Mageck mle design matrix (Relative Path)
DESIGN_MATRIX=""

# Mageck mle ouput prefix
MLE_OUTPUT_PREFIX=""


#>>>>>>>>>>>> Sanity checks <<<<<<<<<<<#

# ensure arrays have the same length
if [ "${#FASTQ_FILES[@]}" -ne "${#SAMPLE_LABELS[@]}" ]; then
  echo "ERROR: number of FASTQ files (${#FASTQ_FILES[@]}) != number of SAMPLE_LABELS (${#SAMPLE_LABELS[@]})." >&2
  exit 2
fi

# check sgRNA library exists
if [ ! -f "$LIBR" ]; then
  echo "ERROR: sgRNA library not found at: $LIBR" >&2
  exit 3
fi

# check each FASTQ exists (accept .fastq or .fastq.gz)
for f in "${FASTQ_FILES[@]}"; do
  if [ ! -f "$f" ]; then
    echo "ERROR: FASTQ file not found: $f" >&2
    exit 4
  fi
done

# build comma-separated labels string
SAMPLE_LABEL_STR=$(IFS=,; echo "${SAMPLE_LABELS[*]}")

#>>>>>>>>>>>> Run MAGeCK count <<<<<<<<<<<#
echo "Running mageck count with ${#FASTQ_FILES[@]} samples..."
mageck count \
  -l "$LIBR" \
  -n "$OUTPUT_PREFIX" \
  --fastq "${FASTQ_FILES[@]}" \
  --sample-label "$SAMPLE_LABEL_STR" \
  --count-n >> log_mageck_mle.txt 2>&1

echo "Count complete. Results prefixed with: $OUTPUT_PREFIX"


#>>>>>>>>>>>> Mageck Test <<<<<<<<<<<#
#mageck test \
#    -k counts.txt \
#    -t treat_rep1,treat_rep2 \
#    -c ctrl_rep1,ctrl_rep2 \
#    --n pref


#>>>>>>>>>>>> Mageck MLE <<<<<<<<<<<#

COUNT_TABLE="${OUTPUT_PREFIX}.count.txt"

# sanity checks
if [ ! -f "$DESIGN_MATRIX" ]; then
    echo "ERROR: Design matrix not found at: $DESIGN_MATRIX" >&2
    exit 5
fi

if [ ! -f "$COUNT_TABLE" ]; then
    echo "ERROR: Count table not found at: $COUNT_TABLE" >&2
    exit 6
fi


echo "Running mageck mle..."
mageck mle \
  -k "$COUNT_TABLE" \
  -d "$DESIGN_MATRIX" \
  -n "$MLE_OUTPUT_PREFIX" >> log_mageck_mle.txt 2>&1

echo "MLE complete. Results prefixed with: $MLE_OUTPUT_PREFIX"