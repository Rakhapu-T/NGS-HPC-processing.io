---
layout: post
title:  "Uploading Files to the HPC "
date:   2025-12-10 12:53:04 +0200
categories: NGS proc
---

There are many different ways to upload files to the UCT HPC. Four methods are discussed below:
1. [[#1. Transfer from device (your pc) to HPC|Transfer from device (your pc) to HPC]]
2. [[#2. Transfer from personal OneDrive/Dropbox to HPC|Transfer from personal OneDrive/Dropbox to HPC]]
3. [[#3. Transfer using download link|Interactive transfer using download link (e.g. shared Dropbox link)]]
4. [[#4. Transfer using Download link [Non-Interactive]|Non-Interactive Transfer using download link]] -> Recommended for very Large files (> 50gB)

## 1. Transfer from device (your pc) to HPC

If you will be using the HPC to transfer files frequently, I suggest setting up a GUI application for files transfer. Once setup this is much faster and easier to use. below are suggested programs for doing so:
1. Windows: [WinSCP](https://winscp.net/eng/download.php)
2. MAC: [Cyberduck](https://cyberduck.io) - Use the website

If setting up the GUI is problematic, or you will not be transferring too many files SCP is the alternative. `The following commands should be executed on your local machine (your pc).`

### A) Copying a Single File

#### **Upload (Local PC $\rightarrow$ HPC)**

Copy a single file (`myfile.txt`) from your local machine to your `/home` directory on the HPC.
```
scp myfile.txt username@hpc.uct.ac.za:/home/username
```

#### **Download (HPC $\rightarrow$ Local PC)**

Copy a file (`myfile.txt`) from your `/home` directory on the HPC to your current local directory. The local directory is denoted by ("`.`").
```
scp username@hpc.uct.ac.za:/home/username/myfile.txt .
```


### B) Copying an Entire Directory (Recursive)

To copy a directory and all its contents (including subdirectories), you must use the **`-r` (recursive)** option.

#### **Upload Directory**

Copy the entire local directory (`local_data/`) to a remote directory on the HPC (e.g., in your `/scratch` space).
```
scp -r local_data/ username@hpc.uct.ac.za:/scratch/username/
```

#### **Download Directory**

Download the remote directory (`analysis_output/`) and everything inside it to your current local directory. Don't forget the ("`.`").
```
scp -r username@hpc.uct.ac.za:/scratch/username/analysis_output/ .
```

### C) Important Considerations for HPC

1. **Always use your UCT Username:** `username@hpc.uct.ac.za`

2. **File System Paths:** Ensure you are copying files to the correct HPC storage location:
    - `/home/username/` (Small quota, for scripts/configs only) - 10GB by default - permanent storage  
    - `/scratch/username/` (Large quota, for all research data and large outputs) - 50GB by default - temporary storage (files are deleted when not used for a while)

3. **Authentication:** You will be prompted for your HPC password (or a two-factor authentication code if enforced) after running the command.


### 2. Transfer from personal OneDrive/Dropbox to HPC

```
TBD - rClone
```


### 3. Transfer using download link

#### 3.1. DropBox (Interactive)
- Start an interactive job using the command below:
  ```
  sintx
  ```
  
  Your terminal should then look like this with the highlighted "srvrochpcXXX":![[Pasted image 20251209112954.png]]

- Go to the directory where you want to download the file:
  ```
  cd destination_path
  ```

Replace `destination_path` with an actual path. See example below:
![[Pasted image 20251209113217.png]]

- Go to the dropbox link containing the file you want to download and copy the download link. This is illustrated in the screenshot below:
  
  **For entire folder:** click the share button
![[Pasted image 20251209113519.png]]


---
**Note:** If the interface with the share button is not available you can just copy the URL as follows:
![[Pasted image 20251209114259.png]]

The copied URL should then look something like this:
```
https://www.dropbox.com/scl/fo/p5abmlu1q7y730k5kjl76/AHfkHel61a2l62Xa2TCPGlA/DN19309?dl=0&preview=MAS651A11_S11_L002_R1_001.fastq.gz&rlkey=x4hcnf6ofmmodtatr6q8cphbi&subfolder_nav_tracking=1
```

To proceed you must then truncate the url, such that it ends at dl=0. The above link would then become:
```
https://www.dropbox.com/scl/fo/p5abmlu1q7y730k5kjl76/AHfkHel61a2l62Xa2TCPGlA/DN19309?dl=0
```

---

The copied link should look something like this:
```
https://www.dropbox.com/scl/fo/afx5hadlri6zkzu77xpnb/AAuzQ1l5ko7SnZRsI-0JmaY?rlkey=ld3w7uq033rsnet0936ey3gre&st=rsd8wn0w&dl=0
```

The URL should end with dl=0, change this to dl=1 such that the above link becomes the following
```
https://www.dropbox.com/scl/fo/afx5hadlri6zkzu77xpnb/AAuzQ1l5ko7SnZRsI-0JmaY?rlkey=ld3w7uq033rsnet0936ey3gre&st=rsd8wn0w&dl=1
```

Now go back to the terminal, and run the following command
```
wget -O output_fileName file_Link
```

An example:
```
wget -O myfile https://www.dropbox.com/scl/fo/afx5hadlri6zkzu77xpnb/AAuzQ1l5ko7SnZRsI-0JmaY?rlkey=ld3w7uq033rsnet0936ey3gre&st=rsd8wn0w&dl=1
```

Running the above command should give an output of the form:
![[Pasted image 20251209150240.png]]

To check if download is complete run the following command
```
tail wget-log
```

This should give an output as follows:
![[Pasted image 20251209150515.png]]
the line `2025-12-09 15:00:36 (18.7 MB/s) - ‘myfile’ saved [592714337/592714337]` indicated that the download is complete.

To verify this run `ls -lh` and check for the file:
![[Pasted image 20251209150646.png]]

You should see your file on the list of files. Check the size of the file to ensure that you downloaded the correct file. In the screenshot above, the size of myfile is 566M -> 566MB.

When downloading an entire directory, It tends to be packaged in a `.zip` file. The final step is to verify if the file is a `.zip` file.
```
# check the file type
file file_name
```
- replace file_name with the actual name of your downloaded file.

	if it is a zip file
	![[Pasted image 20251209151143.png]]
	- In the screenshot above myfile is the file_name
	- the output `file_name: Zip archive data, at least v2.0 to extract` indicates that the file is indeed a zip file.
	- To extract the zip file, run the following command:
	  ```
	  unzip file_name
	  ```

	if it is not a zip file
	![[Pasted image 20251209151550.png]]
	- In the example above the file is an ASCII text file (not a zip file).
	- In this case no further processing is needed.


#### 3.2 OneDrive (Interactive)
- Start an interactive job using the command below:
  ```
  sintx
  ```
  
  Your terminal should then look like this with the highlighted "srvrochpcXXX":![[Pasted image 20251209112954.png]]

- Go to the directory where you want to download the file:
  ```
  cd destination_path
  ```

Replace `destination_path` with an actual path. See example below:
![[Pasted image 20251209113217.png]]

#### Obtaining the OneDrive Download link:
##### A. Navigate to the file you want to download in the browser
![[Pasted image 20251209154004.png]]
#### B. Open Dev Tools (Press F12 or `Ctrl+Shift+I` / `Cmd+Option+I`)
![[Pasted image 20251209154449.png]]


##### C. Go to the network tab
![[Pasted image 20251209154643.png]]

#### D. Clear and Start Record
Ensure the **record** button (a small circle/dot) is red and the log is clear (use the clear button, typically a circle with a slash). 
![[Pasted image 20251209155223.png]]
- Click the button highlighted with the arrow.

#### E. Click the download button
In the main browser window, click the **"Download"** button. (For folders, it will first aggregate the files and then download the zip).
![[Pasted image 20251209155505.png]]
- Make sure to immediately cancel the download once it begins. unless you actually want to download the file onto your personal device.
#### F. Find the Request
Watch the Network log. Look for a request URL that starts with: `zip?`:
![[Pasted image 20251209155937.png]]

#### G. Copy as cURL (bash)
right click on the request url and copy as cURL (bash):
![[Pasted image 20251209160133.png]]

#### H. Save the Output
 Go to the terminal into your `destination_path`, and paste the command you just copied from the browser. Example:
 ```
 curl 'https://southafricawest1-mediap.svc.ms/transform/zip?cs=fFNQTw' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'accept-language: en-US,en;q=0.9,en-ZA;q=0.8' \
  -H 'cache-control: max-age=0' \
  -H 'content-type: application/x-www-form-urlencoded' \
  -H 'origin: https://uctcloud-my.sharepoint.com' \
  -H 'priority: u=0, i' \
  -H 'sec-ch-ua: "Chromium";v="142", "Microsoft Edge";v="142", "Not_A Brand";v="99"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'sec-fetch-dest: iframe' \
  -H 'sec-fetch-mode: navigate' \
  -H 'sec-fetch-site: cross-site' \
  -H 'sec-fetch-storage-access: active' \
  -H 'upgrade-insecure-requests: 1' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0' \
  --data-raw 'zipFileName=UntrimmedData-Msm-NRG-GM.zip&guid=d467bc37-9572-4e78-be2d-078c2f5edc0b&provider=spo&files=%7B%22items%22%3A%5B%7B%22name%22%3A%22UntrimmedData-Msm-NRG-GM%22%2C%22size%22%3A0%2C%22docId%22%3A%22https%3A%2F%2Fuctcloud-my.sharepoint.com%3A443%2F_api%2Fv2.0%2Fdrives%2Fb%218D_aH0kqGEOC6uoZmkGQ7px02gtZMf5Asw58DIQMTxDoSDoxlB42S4ZyZ4bnB9WL%2Fitems%2F01XEMHTP6WUQOBEXWGQ5ALEQNRYY24KURJ%3Fversion%3DPublished%26access_token%3Dv1.eyJzaXRlaWQiOiIxZmRhM2ZmMC0yYTQ5LTQzMTgtODJlYS1lYTE5OWE0MTkwZWUiLCJhdWQiOiIwMDAwMDAwMy0wMDAwLTBmZjEtY2UwMC0wMDAwMDAwMDAwMDAvdWN0Y2xvdWQtbXkuc2hhcmVwb2ludC5jb21AOTI0NTQzMzUtNTY0ZS00Y2NmLWIwYjAtMjQ0NDViOGMwM2Y3IiwiZXhwIjoiMTc2NTMwMzIwMCJ9.CggKA3N0cBIBdAoKCgRzbmlkEgIzMxIGCOjtOxABGg8xOTcuMjM5LjE4NS4xNTciFG1pY3Jvc29mdC5zaGFyZXBvaW50Kix6VWZ2b3ZvMXV0RFB3WTlWYlc3K0hIZWlTZ0RvQ2hxVWpiVm9hdWRUQm9vPTB2OAFKEGhhc2hlZHByb29mdG9rZW5SCFsia21zaSJdYgR0cnVlaiQwMGFhMDM4OS0zOWQ2LWVjMTktOTg5OC02Y2E5MWUyYjg5NGVyKTBoLmZ8bWVtYmVyc2hpcHwxMDAzMjAwMTkzMWU3MzJkQGxpdmUuY29tegEwwgElMCMuZnxtZW1iZXJzaGlwfHJraHRvaDAwMUBteXVjdC5hYy56YdIBJGVhMjkyN2Q5LTYzZTktNDU2Yi1iZjlmLWQzNDY1NGRiYWM2MNoBEglc1eF3GcsoQhG0R67zo0mYxOIBFmVFS1ZoRTE2ZlUtR0F3M0piM0k3QUHqAQdbIkNQMSJd8gEBMQ.5Ka5Ij0aMVfVt4npiwRiSxA05ra-_byImVZbD1Z0A1Y%22%2C%22isFolder%22%3Atrue%7D%5D%7D&oAuthToken=eyJ0eXAiOiJKV1QiLCJub25jZSI6IjdlbE9WMXQ1eW50dmxGMjNzN25PTkZKTVk3MC1INnFmTjhWNExqbnk0bm8iLCJhbGciOiJSUzI1NiIsIng1dCI6InJ0c0ZULWItN0x1WTdEVlllU05LY0lKN1ZuYyIsImtpZCI6InJ0c0ZULWItN0x1WTdEVlllU05LY0lKN1ZuYyJ9.eyJhdWQiOiJodHRwczovL3NvdXRoYWZyaWNhd2VzdDEtbWVkaWFwLnN2Yy5tcyIsImlzcyI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzkyNDU0MzM1LTU2NGUtNGNjZi1iMGIwLTI0NDQ1YjhjMDNmNy8iLCJpYXQiOjE3NjUyODgyNDUsIm5iZiI6MTc2NTI4ODI0NSwiZXhwIjoxNzY1MjkyNTEyLCJhY3IiOiIxIiwiYWNycyI6WyJwMSJdLCJhaW8iOiJBWFFBaS84YUFBQUFxS3h3MnpFUE9MbFRETERPZVM1QTgvcjdRQnpIZDFEUkg4MmtKY1FTQStRTHA3RHVEUi9OTTNXNEptRCtieWMzSXMwWkM5SFlUWGQ2dHVWTi94VFR6enJ5dkovc3JadDN6WHdaZUVTakFXTTlzeVZyQURSeFZwOGxOeFZZZDRuL2I3cmt0ZkR0TDRrRFRCRDl4VHFjM3c9PSIsImFtciI6WyJwd2QiLCJyc2EiLCJtZmEiXSwiYXBwX2Rpc3BsYXluYW1lIjoiU2hhcmVQb2ludCBPbmxpbmUgV2ViIENsaWVudCBFeHRlbnNpYmlsaXR5IiwiYXBwaWQiOiIwOGUxODg3Ni02MTc3LTQ4N2UtYjhiNS1jZjk1MGMxZTU5OGMiLCJhcHBpZGFjciI6IjAiLCJkZXZpY2VpZCI6ImUyYzBmNGMzLTA4MTgtNGMwMS05YzIzLTJhNGVjNGIwNjkzNyIsImZhbWlseV9uYW1lIjoiUmFraGFwdSIsImdpdmVuX25hbWUiOiJUb2hsYW5nIiwiaWR0eXAiOiJ1c2VyIiwiaXBhZGRyIjoiMTk3LjIzOS4xODUuMTU3IiwibmFtZSI6IlRvaGxhbmcgUmFraGFwdSIsIm9pZCI6ImVhMjkyN2Q5LTYzZTktNDU2Yi1iZjlmLWQzNDY1NGRiYWM2MCIsIm9ucHJlbV9zaWQiOiJTLTEtNS0yMS0xODc0NDQzODE5LTE4NTQ1NzA4NDMtMjIxMDAyNTQyOS04Njk4NTgiLCJwdWlkIjoiMTAwMzIwMDE5MzFFNzMyRCIsInJoIjoiMS5BU0VBTlVORmtrNVd6MHl3c0NSRVc0d0Q5OUVMVDVSN0VSeExyeWFBVHRsZWRuNGhBQVFoQUEuIiwic2NwIjoicmVhZHdyaXRlIiwic2lkIjoiMDBhYTAzODktMzlkNi1lYzE5LTk4OTgtNmNhOTFlMmI4OTRlIiwic2lnbmluX3N0YXRlIjpbImttc2kiXSwic3ViIjoidW9PZXdCSGZDa3A3WnhqYzBLSHVjNXNQTGY5cUpHcE90eUxhSm1udnNnWSIsInRpZCI6IjkyNDU0MzM1LTU2NGUtNGNjZi1iMGIwLTI0NDQ1YjhjMDNmNyIsInVuaXF1ZV9uYW1lIjoiUktIVE9IMDAxQG15dWN0LmFjLnphIiwidXBuIjoiUktIVE9IMDAxQG15dWN0LmFjLnphIiwidXRpIjoidWhvZGp0akxuRXFraXdxQkdmOFNBQSIsInZlciI6IjEuMCIsInhtc19hY2QiOjE1MjgwOTI4MzgsInhtc19hY3RfZmN0IjoiMyA1IiwieG1zX2Z0ZCI6IjRYYjdUMHBZSmtBQ09mazlKZ0NNRUFPd3FKWjRVS1JZNF83SXpKZGtQVGdCWm5KaGJtTmxZeTFrYzIxeiIsInhtc19pZHJlbCI6IjMwIDEiLCJ4bXNfc3ViX2ZjdCI6IjMgMTIiLCJ4bXNfdG50X2ZjdCI6IjggMyJ9.CmIdG-83RHPpj1ZMAjpamAoHpKXP_ouvlTWFUhoCyQ7Ow3gIJBnxDAlj8jrOgtzFL2fu7ubAZsjWDQ9tFQ1JFSTj4Ex7hEivdf9nHsDZqbwAg8K4KwCCYW6HRG1vjiWD3iXQhPEaw12hrqqncT6VOqbtBGOtlBVDf1_eBDz6Acr-ZQDAq2mysVmI3Jkm7t9lWbfFRLEg4YdGKTbo7MHablv1nn380l2y0blyuUD4GahHndcqS7OV0kmwp3s9hP56MGOYEiNMc4tP9mfE917bvB-4P-yPtCt_LppVWxoHzw4h6xvgVd__BT4s6xgcfMIKwVRtQ6roKX8wxKmzXGY9Xw'
 ```
 - As Illustrated above the command is very long.
 - add the --output flag to the end of the command as follows:
 ```
 ...83RHPpj1ZMAjpamAoHpKXP_ouvlTWFUhoCyQ7Ow3gIJBnxDAlj8jrOgtzFL2fu7ubAZsjWDQ9tFQ1JFSTj4Ex7hEivdf9nHsDZqbwAg8K4KwCCYW6HRG1vjiWD3iXQhPEaw12hrqqncT6VOqbtBGOtlBVDf1_eBDz6Acr-ZQDAq2mysVmI3Jkm7t9lWbfFRLEg4YdGKTbo7MHablv1nn380l2y0blyuUD4GahHndcqS7OV0kmwp3s9hP56MGOYEiNMc4tP9mfE917bvB-4P-yPtCt_LppVWxoHzw4h6xvgVd__BT4s6xgcfMIKwVRtQ6roKX8wxKmzXGY9Xw' --output file_name
 ```

The output should be as follows:
![[Pasted image 20251209161410.png]]

Once the download is complete run `ls -lh` and check for the file:
![[Pasted image 20251209161632.png]]

You should see your file on the list of files. Check the size of the file to ensure that you downloaded the correct file. In the screenshot above, the size of myfile is 566M -> 566MB.

When downloading an entire directory, It tends to be packaged in a `.zip` file. The final step is to verify if the file is a `.zip` file.
```
# check the file type
file file_name
```
- replace file_name with the actual name of your downloaded file.

	if it is a zip file
	![[Pasted image 20251209151143.png]]
	- In the screenshot above myfile is the file_name
	- the output `file_name: Zip archive data, at least v2.0 to extract` indicates that the file is indeed a zip file.
	- To extract the zip file, run the following command:
	  ```
	  unzip file_name && rm file_name
	  ```

	if it is not a zip file
	![[Pasted image 20251209151550.png]]
	- In the example above the file is an ASCII text file (not a zip file).
	- In this case no further processing is needed.

## 4. Transfer using Download link \[Non-Interactive]

### Step1: Download the slurm script
```
# move to the scratch directory - where very large files are stored.
# Replace username with your actual username e.g. XYZABC001
cd /sractch/username/

# create directory to store the files
mkdir -p downloads && cd downloads
```

#### For DropBox:
copy and paste into the terminal
```
# Download the download script
wget -O download.sh "https://raw.githubusercontent.com/Rakhapu-T/NGS-HPC-processing.io/refs/heads/main/scripts/downloader_DB.sh"
```

#### For OneDrive:
copy and paste into the terminal
```
# Download the yml file for configuring the environment
wget -O download.sh "https://raw.githubusercontent.com/Rakhapu-T/NGS-HPC-processing.io/refs/heads/main/scripts/downloader_OD.sh"
```

### Step2: Configure the script parameters

##### Open the Slurm script for editing:
```
nano downloader.sh
```

##### Using the keyboard arrows, scroll to the bottom of the and find the following:
```
# >>>>>>>>>> Enter your email address here to get job status emails <<<<<<<<<<<<
# ==============================================================================
#SBATCH --mail-user="example.uct.ac.za"
# ==============================================================================
```
- Change `example.uct.ac.za` to your email.

##### Scroll further down and enter the download link:
```
# >>>>>>>>>>>>>>>>>>>>>>>>> Enter the Download Link <<<<<<<<<<<<<<<<<<<<<<<<<<<<
# ==============================================================================
LINK="https://example.com/download_link"
# ==============================================================================
```
- Replace https://example.com/download_link with your download link
- Follow the instruction in [[Download Link]] in order to retrieve the file's download link.

##### Enter the file name (Optional):
```
# >>>>>>>>>>>>>>>>>>>>>>>>> Enter the file name <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# ==============================================================================
FILE="file_name"
# ==============================================================================
```
##### Save the changes and close the file
1. press: `ctrl + s` (This saves the file)
2. press: `ctrl + x` (This closes the file)

### Step3: run the script
Copy and paste in the terminal
```
# change file permissions:
chmod +x downloader.sh

# run the script:
sbatch downloader.sh
```

### Step4: Verify the download
You should receive email notifications, updating you on the progress of the script. Once the script is done, the download by running `ls -lh`:
![[Pasted image 20251209150646.png]]
