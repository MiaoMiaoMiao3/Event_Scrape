# Scraping the Web and Sending Emails With Google Cloud

## Overview
Like most people today, I find it hard to discover things to do outside of the house with the social distancing restrictions in place (there's only so much Netflix I can watch). <br/>
 I decided to write an application to combat the cabin fever by scraping the web for events around my home town and sending me an email every week with events found. The application integrates several Google Cloud Services including Compute Engine, Cloud Storage, and Cloud Functions. <br/>

## Requirements
To execute this program, I used:
- A Google Cloud account
- An email delivery service called Mailjet

<br/>

## Architecture Diagram <br/>
![architecture diagram](https://drive.google.com/uc?export=view&id=1nkhoop7bb8wDr8_b8Q_gng5VKIBkSvkh)
<br/><sup>Diagram of Integrated Services</sup><br/><br/>

The architecture diagram above shows the purpose of each service and how they integrate together. There are two Python scripts that exist - one that lives on the Compute Engine, the VM which scrapes the website (Event_Scrape_VM.py) and one that is stored in Cloud Functions, which sends an email with the scraped data content when new data is uploaded into Cloud Storage (main.py).

## Setting Up Cloud Storage
To store the scraped data, I created a new storage bucket with a standard storage class using gcloud: <br/>

```bash
gsutil mb gs://event_scraper
```
Each time a web scrape is done, it generates a file (event.txt) that I upload into this storage bucket. The uploaded data is currently set to overwrite any existing file of the same name (since I'm not concerned with tracking events over time). <br/>
To access the bucket with Cloud Functions, I created a service account tied to this bucket with the 'Owner' role and downloaded the JSON file for the secret key associated with this account ('event_scraper_key.json', see image in 'Creating An Event Trigger' below).<br/>

<br/>

## Setting Up the Virtual Machine
To create the weekly cron job that executes the web scraper, I created a f1-micro VM with f1-micro machine type and read/write access enabled.
Once the instance has been created, I SSH'ed into the instance to install tmux and pip package manager. I use tmux to detach my terminal from running processes, which allows me to run the python program after the terminal window is closed:

```bash
sudo apt-get install python3-pip
sudo apt-get install tmux
```
I created a directory to store the webscraper code (Event_Scrape_VM.py) along with its dependencies (requirements_VM.txt) using pip package manager:

```bash
pip3 install -r requirements_VM.txt
```
Event_Scrape_VM.py uses a module called 'Beautiful Soup' to scrape a website that contains events collected throughout Seattle; it's set up to filter out just the events (using html tags and class names) and ensures no duplicate events are stored. The scraped events are then written to a file called 'events.txt'. To execute the code using a cron job, I first need to use Linux change mode to convert the Python script into an executable:

```bash
chmod +x Event_Scrape_VM.py
```

## Creating the Cron Job
After completing the steps above, I created the cron job within a tmux session:<br/>
<br/>
![Viewing the cron jobs](https://drive.google.com/uc?export=view&id=1mAXzxUnGBPdcCe_CL-hibv2UlpsaFVcB)
<sup> Command Run On Table (Crontab) with Cron jobs</sup> <br/><br/>
I used crontab to create 2 cron jobs: <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;one, to execute the python code and generate 'event.txt' and, <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;two, to upload the file to Cloud Storage
<br/>
<br/>
Note: <br/>
Times specified in cron jobs are UTC times. My two jobs are set to run at 5:00 A.M. and 5:02 A.M. UTC, respectively, on the fifth day (Friday) of every week. This means that they will run at 9:00 P.M. and 9:02 P.M. <strong>PST</strong> Thursday night. <br/>

After saving the cron jobs, I closed the terminal without exiting the tmux session to keep it running.

## Creating An Event Trigger
Once I set up the web scraper in the VM, I set up the python code in 'Cloud Functions' to trigger when a new file is uploaded to Cloud Storage . I used the runtime environment variables to store all api keys, sender and receiver approved emails, and JSON keys. <br/><br/>

![Environment Variables](https://drive.google.com/uc?export=view&id=1MZPn4Zy-C1G-vZnNLDRSlwfpfDxLug3b)
<br/>
<sup>Environment Variables used in main.py</sup> <br/><br/>
![Cloud Function - Code Setup](https://drive.google.com/uc?export=view&id=1QDQvOX7OblR8Cpbd_0_1RypWalndYIlZ)
<br/>
<sup>Inline Code Editor with associated files </sup>

## Testing Functionality
To test the Cloud Function, I uploaded a dummy text file into Cloud Storage and confirmed that this triggers my Cloud Function and that an email is sent. Voila, email received!
<br/>

![Cloud Function - Code Setup](https://drive.google.com/uc?export=view&id=1iI2y5QDue2p-e4KpcjhCGsyc62ocH3ZD)
