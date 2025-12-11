---
layout: post
title:  "Software Installation (HPC)"
date:   2025-12-10 12:53:04 +0200
categories: NGS proc
---

## 1. Logging into the HPC
To login to the HPC, use your operating system's default terminal and run the following command:
```
ssh username@hpc.uct.ac.za
```
- Replace `username` with your assigned UCT HPC username.
- If this does not work, follow the instructions from the [hpc-wiki](https://ucthpc.uct.ac.za/index.php/how-do-i-login/) for your operating system.

**Note:** First-Time Login Warning The first time you connect, your terminal may prompt you about the host's authenticity. This is normal. You should see a message similar to:

`The authenticity of host 'hpc.uct.ac.za' can't be established.`

Type `yes` and press Enter to accept the server's public key (fingerprint) and continue. This information will be saved, and you won't be prompted again unless the key changes.

The login process should look something like this:
![[Pasted image 20251208141047.png]]

---
## ⚠️ Installation Note:

**Core Principle: Use Compute Nodes, Not the Head Node**
The head node is a small, virtual machine used _only_ for login, file management, and job scheduling. Running any CPU-intensive process, including **installing software, compiling code, or setting up environments**, on the head node will negatively impact all users and can lead to immediate account suspension or resource limits being imposed

All installations must be performed within an **Interactive Job**. This allocates dedicated resources (CPU/RAM) on a worker (compute) node for your task.

---
### ⛔ **DO NOT INSTALL SOFTWARE ON THE HEAD NODE**

Not following this rule will result in a heavy load on the head node and **may lead to the immediate revocation of your HPC access**.

---
## 2. Start an Interactive job
To safely install **libraries** or create a **conda environment**, you must first start an interactive job. This should move you from the head node to an interactive worker node, where it is safe to install:

```
# Start an interactive shell
sintx --ntasks=4
```

Running the command above should change the background of the hostname to white. This indicates that you are in a **worker node** which is illustrated below:
![[Pasted image 20251208141500.png]]

---

## 3. Import python module

In order to use python on the cluster run the following comand. This should allow you to use both python and miniconda:

```
# import the miniconda module
module load python/miniconda3-py3.9

# verify the import
conda --version
```

If the above runs successfully, you should get an output similar to the one below:
![[Pasted image 20251208152925.png]]

**Note**: You could use py3.12, this just changes the base python version, which doesn't really matter since we will specify the python version for every environment we create.

---

## 4. Installing Mageck

Copy and paste the commands below into your terminal. These should create a new environment called mageck (You could change the name to your liking) and install the mageck program within this environment. To avoid dependency conflicts, each software shall be run within its own environment.

```
# Create a python environment (select python version from 3.9 to 3.12)
conda create -n mageck python=3.9 -y

# Activate the environment
source activate mageck

# Install mageck
conda install -c bioconda -c conda-forge mageck -y
```

To verify if the installation is successful, run the following command:
```
mageck --version
```

If the install was successful, the version of mageck should be displayed. This is illustrated below:
![[Pasted image 20251208160201.png]]

---

## 5. Installing FastQC and MultQC

Installing multqc using the standard procedure does not work on the HPC. The following instructions is a workaround that was verified using `python/miniconda3-py3.12`.

1. **Step1:**
```
# Deactivate active environment
conda deactivate

# remove loaded modules (ensure miniconda3-py3.9 is not loaded)
module purge

# load the python 3.12 miniconda
module load python/miniconda3-py3.12

# Download the yml file for configuring the environment
wget -O ngs_env.yml https://raw.githubusercontent.com/Rakhapu-T/hpc_processing/refs/heads/main/ngs_env.yml

# Create the ngs_QC environment
conda env create -f ngs_env.yml

# remove the yml configuration file:
rm ngs_env.yml
```

2. **Step2: Verify the software installation**
```
# Activate the environment
source activate ngs_QC

# Verify fastqc installation
fastqc --version

# Verify multiqc installation
multiqc --version
```

If installation is successful the fastqc and multiqc versions should be output to the terminal as follows:
![[Pasted image 20251208230044.png]] 

---
## 6. Installing Cutadapt

Cutadapt can be installed by following the instructions from the [official cutadapt website]([Installation — Cutadapt 5.2 documentation](https://cutadapt.readthedocs.io/en/stable/installation.html)). The installation process is summarized in the snippet below:
```
# deactivate the current conda environment
conda deactivate

# Configure the Biconda channel
conda config --add channels bioconda
conda config --add channels conda-forge
conda config --set channel_priority strict

# Install Cutadapt into a new Conda environment:
conda create -n cutadapt cutadapt -y
```

Verifying the installation:
```
# activate the environment
conda activate cutadapt

# verify the install
cutadapt --version
```

If the installation is successful, the output should be as follows:
![[Pasted image 20251208231918.png]]

---

## Summary:

Three environments were created:
1. [[mageck]]: Used exclusively for **MAGeCK** analysis
2. [[ngs_QC]]: Used for quality checking using fastQC and multiQC
3. [[cutadapt]]: Used for trimming low-quality bases and removing adapter sequences.
