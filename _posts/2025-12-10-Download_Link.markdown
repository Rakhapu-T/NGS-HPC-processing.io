---
layout: post
title:  "Obtaining Download Links for HPC files upload"
date:   2025-12-10 12:53:04 +0200
categories: NGS proc
---


This file Documents 2 methods for acquiring the download link:
1. [Dropbox](#1-dropbox) download link
2. [OneDrive](#2-onedrive) download link


## 1. Dropbox

 Go to the dropbox link containing the file you want to download and copy the download link. This is illustrated in the screenshots below:

 **For entire folder or single file:** click the share button
![Dropbox Share Button]({{ site.baseurl }}/assets/images/Pasted image 20251209113519.png)

If the Share button is available, skip to [Converting to Download-Link](#converting-to-download-link)


---
**Note:** If the interface with the share button is not available you can just copy the URL as follows:
![Copy Dropbox URL]({{ site.baseurl }}/assets/images/Pasted image 20251209114259.png)

The copied URL should then look something like this:
```
https://www.dropbox.com/scl/fo/p5abmlu1q7y730k5kjl76/AHfkHel61a2l62Xa2TCPGlA/DN19309?dl=0&preview=MAS651A11_S11_L002_R1_001.fastq.gz&rlkey=x4hcnf6ofmmodtatr6q8cphbi&subfolder_nav_tracking=1
```

To proceed you must then truncate the url, such that it ends at dl=0. The above link would then become:
```
https://www.dropbox.com/scl/fo/p5abmlu1q7y730k5kjl76/AHfkHel61a2l62Xa2TCPGlA/DN19309?dl=0
```

---
#### Converting to Download-Link:
The copied link should look something like this:
```
https://www.dropbox.com/scl/fo/afx5hadlri6zkzu77xpnb/AAuzQ1l5ko7SnZRsI-0JmaY?rlkey=ld3w7uq033rsnet0936ey3gre&st=rsd8wn0w&dl=0
```

The URL should end with dl=0, change this to dl=1 such that the above link becomes the following:
```
https://www.dropbox.com/scl/fo/afx5hadlri6zkzu77xpnb/AAuzQ1l5ko7SnZRsI-0JmaY?rlkey=ld3w7uq033rsnet0936ey3gre&st=rsd8wn0w&dl=1
```
- This is the final download link that will be used for file downloads.




---
## 2. OneDrive

#### A. Navigate to the file you want to download in the browser
![OneDrive File Navigation]({{ site.baseurl }}/assets/images/Pasted image 20251209154004.png)
#### B. Open Dev Tools (Press F12 or `Ctrl+Shift+I` / `Cmd+Option+I`)
![Open Developer Tools]({{ site.baseurl }}/assets/images/Pasted image 20251209154449.png)


##### C. Go to the network tab
![Network Tab]({{ site.baseurl }}/assets/images/Pasted image 20251209154643.png)

#### D. Clear and Start Record
Ensure the **record** button (a small circle/dot) is red and the log is clear (use the clear button, typically a circle with a slash). 
![Clear and Record]({{ site.baseurl }}/assets/images/Pasted image 20251209155223.png)
- Click the button highlighted with the arrow.

#### E. Click the download button
In the main browser window, click the **"Download"** button. (For folders, it will first aggregate the files and then download the zip).
![Click Download Button]({{ site.baseurl }}/assets/images/Pasted image 20251209155505.png)
- Make sure to immediately cancel the download once it begins. unless you actually want to download the file onto your personal device.

#### F. Find the Request
Watch the Network log. Look for a request URL that starts with: "`zip?`":
![Find Zip Request]({{ site.baseurl }}/assets/images/Pasted image 20251209155937.png)

#### G. Copy as cURL (bash)
right click on the request url and copy as cURL (bash):
![Copy as cURL]({{ site.baseurl }}/assets/images/Pasted image 20251209160133.png)

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
- This is the final download link that will be used for file downloads.

---
