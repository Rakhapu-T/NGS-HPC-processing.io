---
layout: post
title:  "Cutadapt cheetsheet"
date:   2025-12-10 12:53:04 +0200
categories: NGS proc
---

### 1. Determine number of cores:
   ```
   # Detailed CPU info:
   lscpu
   
   # Number of threads:
   nproc
   ```

### 2. Understanding Read 1 (R1) and Read 2 (R2) in Paired-End Sequencing

#### What are R1 and R2?
Illumina paired-end sequencing reads each DNA fragment **from both ends**, producing two FASTQ files:

- **Read 1 (R1)** — forward read  
  - The sequencer reads the fragment from one end.
  - File typically ends with `_R1_001.fastq.gz`.

- **Read 2 (R2)** — reverse read  
  - The sequencer reads the same fragment from the opposite end.
  - File typically ends with `_R2_001.fastq.gz`.

### ✅ Why two files?
Each DNA fragment generates **two reads**:
- R1 reads left → right  
- R2 reads right → left  
Together, they form a matched pair representing the same original fragment.
    
### ⭐ Key Points
- R1 and R2 always stay in the **same order**.
- Each line position in R1 corresponds to the **same fragment** as the same line position in R2.
- Tools like **cutadapt**, **fastp**, and **alignment software** require both files together.


### 3. Trim the 5' region of the read1 and read2 sequences:

### Single Reads Command:
```
cutadapt -j <NUM_CORES> \
		 -a <ADAPTER_SEQUENCE> \
         -q <QUALITY_THRESHOLD> \
         -m <MIN_LENGTH> \
         -o <OUTPUT_R1_FILE> \
         <INPUT_R1_FILE>
```

#### Paired Reads Command:
```
cutadapt -j <NUM_CORES> \
  -g <ADAPTER_SEQ_READ1_5P> \
  -G <ADAPTER_SEQ_READ2_5P> \
  -o <OUTPUT_TRIMMED_READ1.fastq> \
  -p <OUTPUT_TRIMMED_READ2.fastq> \
  <INPUT_READ1.fastq.gz> \
  <INPUT_READ2.fastq.gz> \
  --discard-untrimmed
```
### Argument Descriptions
| Placeholder                    | Meaning                                                  |
| ------------------------------ | -------------------------------------------------------- |
| `<NUM_CORES>`                  | Number of CPU cores to use for parallel processing.      |
| `<ADAPTER_SEQ_READ1_5P>`       | 5′ adapter sequence expected at the start of **Read 1**. |
| `<ADAPTER_SEQ_READ2_5P>`       | 5′ adapter sequence expected at the start of **Read 2**. |
| `<OUTPUT_TRIMMED_READ1.fastq>` | Output FASTQ file for trimmed Read 1.                    |
| `<OUTPUT_TRIMMED_READ2.fastq>` | Output FASTQ file for trimmed Read 2.                    |
| `<INPUT_READ1.fastq.gz>`       | Raw Read 1 input FASTQ file.                             |
| `<INPUT_READ2.fastq.gz>`       | Raw Read 2 input FASTQ file.                             |

### Trim the 3' ends off the read1 and read2 sequences:

#### Command:
```
cutadapt -j <NUM_CORES> \
  -a <ADAPTER_SEQ_READ1_3P> \
  -A <ADAPTER_SEQ_READ2_3P> \
  -o <OUTPUT_READ1.fastq> \
  -p <OUTPUT_READ2.fastq> \
  <INPUT_READ1.fastq> \
  <INPUT_READ2.fastq> \
  --maximum-length <MAX_READ_LENGTH>
```

#### Arguments Descriptions:
| Placeholder              | Meaning                                                                        |
| ------------------------ | ------------------------------------------------------------------------------ |
| `<NUM_CORES>`            | Number of CPU cores to use for parallel processing.                            |
| `<ADAPTER_SEQ_READ1_3P>` | 3′ adapter sequence expected at the end of **Read 1**.                         |
| `<ADAPTER_SEQ_READ2_3P>` | 3′ adapter sequence expected at the end of **Read 2**.                         |
| `<OUTPUT_READ1.fastq>`   | Output FASTQ file for trimmed Read 1.                                          |
| `<OUTPUT_READ2.fastq>`   | Output FASTQ file for trimmed Read 2.                                          |
| `<INPUT_READ1.fastq>`    | Input Read 1 FASTQ file (may be previously trimmed).                           |
| `<INPUT_READ2.fastq>`    | Input Read 2 FASTQ file (paired with R1).                                      |
| `<MAX_READ_LENGTH>`      | After trimming, any read longer than this will be clipped down to this length. |

#### Notes:
- Trim the 5' end and then take the output and trim the 3' region of this output.
  **untrimmed** -> **5'_trimmed** -> **5' + 3' trimmed** = **fully trimmed**
- At 5' stage, make sure that the names of the output files reflect the sample name of the files that you are analysing.
- At 3' stage, make sure that the output file names match the sample number of the trimmed reads.
- This process is executed on one sample.

### 4. Outputs
To understand what the program is doing to your sequences you can manually import them into geneious and check at how the program has edited your sequences in each step.

Look at the summary reporting outputs for each file and put a trimming summary together for each file processed.

If you would like to have a summary report for each read you could add one more argument to the script. The report type can be changed to a one-line summary with the option `--report=minimal`. The output will be a tab-separated table (tsv) with one header row and one row of content.

### 5. Link to documentation:
See [Cutadapt Documentation](https://cutadapt.readthedocs.io/en/stable/guide.html) for more details.