---
layout: post
title:  "Count Spacers MTBP3"
date:   2025-12-10 12:53:04 +0200
categories: NGS proc
---

# sgRNA Library Analysis Tool

A Python script for analyzing sequencing data to assess sgRNA library distribution and quality metrics.

## Dependencies

### Required Python Packages

```bash
# Using conda (recommended)
conda install -y biopython numpy

# Or using pip
pip install biopython numpy
```

**Package Details:**
- **biopython** - For parsing FASTQ files and handling biological sequences
- **numpy** - For statistical calculations (percentiles, means, etc.)

### Built-in Python Modules
The following modules are part of Python's standard library (no installation needed):
- `csv` - Reading/writing CSV files
- `collections` (OrderedDict, defaultdict) - Data structures
- `argparse` - Command-line argument parsing
- `os`, `glob` - File system operations
- `sys` - System-specific parameters
- `gzip` - Reading compressed FASTQ files
- `multiprocessing` - Parallel processing

## Installation

### 1. Create Conda Environment (Recommended)

```bash
# Create a new conda environment
conda create -n pythonCount python=3.14

# Activate the environment
conda activate pythonCount

# Install dependencies
conda install -y biopython numpy
```

### 2. Verify Installation

```bash
python -c "import Bio; import numpy; print('All dependencies installed successfully!')"
```

## Usage

### Basic Usage

#### Process All FASTQ Files in Current Directory

```bash
python count_spacers_mtbP3_nokey_nomatch.py --input RLC0001_RC_all.csv
```

This will:
- Find all `.fastq` and `.fastq.gz` files in the current directory
- Process them in parallel using all available CPU cores
- Create a new `results/` directory with output files

#### Process a Single FASTQ File

```bash
python count_spacers_mtbP3_nokey_nomatch.py \
    --input RLC0001_RC_all.csv \
    --fastq Trim3and5ends_MAS651A11_S11_L002_R1_001.fastq.gz
```

### Command-Line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--input` | `-i` | Path to reference library CSV file | `library_sequences.csv` |
| `--fastq` | `-f` | Specific FASTQ file to process | (processes all if not specified) |
| `--output` | `-o` | Output filename (currently unused) | `library_count.csv` |
| `--processes` | `-p` | Number of parallel processes | All CPU cores |
| `--no-g` | | Flag if NO guanine before spacer | False (guanine present) |

### Examples

#### Use 4 CPU Cores

```bash
python count_spacers_mtbP3_nokey_nomatch.py \
    --input RLC0001_RC_all.csv \
    --processes 4
```

#### Process with Custom Library File

```bash
python count_spacers_mtbP3_nokey_nomatch.py \
    --input my_custom_library.csv \
    --fastq my_sample.fastq.gz
```

#### No Guanine Flag

```bash
python count_spacers_mtbP3_nokey_nomatch.py \
    --input RLC0001_RC_all.csv \
    --no-g
```

## Input File Format

### Reference Library CSV (`--input`)
- Plain text CSV file
- One guide sequence per row
- First column contains the guide sequence
- No header required

**Example:**
```csv
ATCGATCGATCGATCGATCG
GCTAGCTAGCTAGCTAGCTA
TTAATTAATTAATTAATTAA
```

### FASTQ Files
- Standard FASTQ format (`.fastq` or `.fastq.gz`)
- Gzip-compressed files are automatically detected and handled

## Output Files

All output files are created in a `results/` directory (or `results_2/`, `results_3/`, etc. if previous results exist).

### 1. `guide_counts.csv`
Contains counts for all guides that matched the reference library.

**Format:**
```csv
filename,guide_sequence,count
Trim3and5ends_MAS651A11_S11_L002_R1_001.fastq.gz,ATCGATCGATCGATCGATCG,1523
Trim3and5ends_MAS651A11_S11_L002_R1_001.fastq.gz,GCTAGCTAGCTAGCTAGCTA,1487
```

### 2. `noMatch_counts.csv`
Contains sequences that did NOT match any guide in the reference library.

**Format:**
```csv
filename, sequence, count
Trim3and5ends_MAS651A11_S11_L002_R1_001.fastq.gz, NNNATCGATCGATCGATCG, 45
```

### 3. `statistics.txt`
Comprehensive statistics for all processed files.

**Structure:**
- **Overall aggregate statistics** (at the top)
- Individual file statistics (below)

**Example:**
```
=================================================================
OVERALL STATISTICS (Aggregate from 11 files)
=================================================================
Total perfect guide matches: 12450678
Total nonperfect guide matches: 567890
Total reads processed: 13018568
Percentage of guides that matched perfectly: 95.6
Percentage of undetected guides: 4.2
Average skew ratio of top 10% to bottom 10%: 2.34
=================================================================

-----------------------------------------------------------------
Results for file: Trim3and5ends_MAS651A11_S11_L002_R1_001.fastq.gz
Number of perfect guide matches: 1131880
Number of nonperfect guide matches: 51626
Number of reads processed: 1183506
Percentage of guides that matched perfectly: 95.6
Percentage of undetected guides: 4.1
Skew ratio of top 10% to bottom 10%: 2.45
-----------------------------------------------------------------
```

## Performance

### Parallel Processing
- The script automatically uses all available CPU cores by default
- For a typical dataset with 11 FASTQ files, processing time can be reduced significantly
- Use `--processes` to limit CPU usage if needed

### Progress Tracking
During processing, you'll see real-time progress:
```
Processing 11 files using 8 processes...
Processed Trim3and5ends_MAS651A11_S11_L002_R1_001.fastq.gz. [1/11]
Processed Trim3and5ends_MAS651A12_S12_L002_R1_001.fastq.gz. [2/11]
...
Processed Trim3and5ends_MAS651A16_S16_L002_R1_001.fastq.gz. [11/11]

Completed! Successfully processed 11/11 files.
```

## Statistics Explained

### Perfect vs Non-Perfect Matches
- **Perfect matches**: Sequences that exactly match a guide in the reference library
- **Non-perfect matches**: Sequences that don't match any reference guide

### Coverage Metrics
- **Guides with reads**: Number of library guides detected in the sample
- **Percentage of undetected guides**: Guides from the library with zero reads

### Skew Ratio
- Ratio of 90th percentile to 10th percentile of guide counts
- Indicates library distribution uniformity
- Lower values = more uniform distribution
- Higher values = more skewed distribution

## Troubleshooting

### Common Issues

#### "No module named 'Bio'"
```bash
# Install biopython
conda install -y biopython
```

#### "No FASTQ files found to process"
- Ensure `.fastq` or `.fastq.gz` files are in the current directory
- Or specify a file with `--fastq`

#### "could not open library_sequences.csv"
- Specify the correct library file with `--input`
- Ensure the file exists in the current directory

#### Permission Errors
- Ensure you have write permissions in the current directory
- The script creates a `results/` folder

## File Organization

```
project_directory/
├── count_spacers_mtbP3_nokey_nomatch.py  # Main script
├── RLC0001_RC_all.csv                     # Reference library
├── Trim3and5ends_*.fastq.gz               # FASTQ files
└── results/                                # Output directory (auto-created)
    ├── guide_counts.csv
    ├── noMatch_counts.csv
    └── statistics.txt
```

## Notes

- **Results Directory**: Each run creates a new results directory (`results/`, `results_2/`, etc.) to avoid overwriting previous analyses
- **Memory Usage**: For very large FASTQ files, ensure sufficient RAM is available
- **Gzip Support**: Both compressed (`.gz`) and uncompressed FASTQ files are supported automatically
- **CSV Format**: Output CSVs use standard comma delimiters

## Author & Version

**Script**: `count_spacers_mtbP3_nokey_nomatch.py`
**Python Version**: 3.14+ (tested)
**Last Updated**: December 2025
