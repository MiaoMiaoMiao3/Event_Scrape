# Scraping the Web and Sending Emails With Google Cloud

## Overview
Like most people today, I find it hard to discover things to do outside of the house with the social distancing restrictions in place (a girl can only watch so much Netflix). <br/> I decided to write an application to combat the cabin fever by scraping the web for events around my home town and sending <br/>
me an email every week with events found. The application integrates several Google Cloud Services including Compute Engine, Cloud Storage, and Cloud Functions. <br/>
As with most things Cloud, there are several ways to implement the same solution (one could, for example, use App Engine and the built in Cron Jobs feature <br/>
instead of a VM for web scraping); ultimately, this solution is meant to demonstrate how a solution is developed by integrating several Cloud services.

## Requirements
To execute this program you will need:
- A Google Cloud account
- An email delivery service account (I used Mailjet)  
- Familiarity with Python and Linux (TMUX, Cron jobs)

<br/>

## Architecture Diagram <br/>
![architecture diagram](https://drive.google.com/uc?export=view&id=1nkhoop7bb8wDr8_b8Q_gng5VKIBkSvkh)
<br/><br/>

## Setting Up Cloud Storage
To store the scraped data, we create a new storage bucket with standard storage. This can be done using the following command in gcloud: <br/>

```bash
gsutil mb gs://some-bucket
```
Each time a web scrape is done, it generates a file (event.txt) we'll specify the bucket that we created as the location we want to upload this file. <br/>
Note: The uploaded data is currently set to overwrite any existing file of the same name, since I'm not concerned about logging or tracking events over time. <br/><br/>

## Setting Up the Virtual Machine
To create the weekly cron job that executes the web scraper, we first have to create a virtual machine. Since this job only runs once per week and doesn't require <br/>
massive amounts of processing power, using an f1-micro machine type is fine. Make sure the boot disk image specified is Debian GNU/Linux 10. For the Service Account, <br/> permission must be given to read and write to Cloud Storage:  <br/><br/><br/>
![Creating the VM in Cloud Console](https://drive.google.com/uc?export=view&id=1VEvL5zzT_Yp6aorTQCIQ50VTgrQ324Ut)

## Installing Dependencies
Once the instance has been created, SSH into the instance and install tmux and pip package manager. tmux is a multiplexer that allows us to run the web scraper <br/>
in a detached state (runs even when the terminal window is closed):

```bash
sudo apt-get install python3-pip
sudo apt-get install tmux
```
By default, Python3 should be installed on the VM, you can check if this is true by running the following command:

```bash
python3 -V
```
Use the same procedure as stated above to install Python3 if it does not exist. Create a directory where you want to store the webscraper code (Event_Scrape_VM.py) along with <br/>
dependencies (requirements_VM.txt). You can either do this using the Cloud SDK and 'gsutil cp' or using your favorite text editor (vim, nano), creating new files and copying <br/>
and pasting the code in 'Event_Scrape_VM.py' and 'requirements_VM.txt' in: <br/> <br/>
![Copying Event_Scrape_VM.py over](https://drive.google.com/uc?export=view&id=18-wc4LBperOFjg70KK2YwjiA7lR7-Sou)

To ensure all of the modules required to run the python program are installed, we can run the pip package manager to install the modules listed in 'requirements_VM.txt':

```bash
pip3 install -r requirements_VM.txt
```
Event_Scrape_VM.py uses a module called 'Beautiful Soup' to scrape a website that contains events collected throughout Seattle, it's set up to filter out just the events <br/> (using html tags and class names as a filter) and makes use of the set data structure to ensure no duplicate events are stored. The scraped events are then stored in a file <br/> called 'events.txt'. Note on LINE 7 you need to change the directory to the new directory you created:

```python
TXT_FILE = '/home/utp56479user/Event_Scraper/event.txt' #REPLACE WITH THE DIRECTORY YOU CREATED
```

Change the python code into an executable using Linux change mode:

```bash
chmod +x Event_Scrape_VM.py
```

## Creating the Cron Job
After completing the steps in 'Installing Dependencies', we can create the cron job within a tmux session. To start a new tmux session, type 'tmux' in the command prompt <br/> 
and hit enter. Start the cron job by typing 'crontab -e':<br/>
<br/>
![Viewing the cron jobs](https://drive.google.com/uc?export=view&id=1mAXzxUnGBPdcCe_CL-hibv2UlpsaFVcB)

You'll need to create 2 cron jobs: <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;one, to execute the python code and generate 'event.txt' and, <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;two, to upload the file to Cloud Storage
<br/>
<br/>
A few things to note: <br/>
Times specified in cron jobs are UTC times. My two jobs are set to run at 5:00 A.M. and 5:02 A.M. UTC, respectively, on the fifth day (Friday) of every week. <br/>
This means that they will run at 9:00 P.M. and 9:02 P.M. <strong>PST</strong> Thursday night. <br/>
Replace 'NEW_DIRECTORY' and 'BUCKET_NAME' with the directory you created earlier in 'Installing Dependencies' and the bucket you created in 'Setting Up Cloud Storage' <br/>

Save the file and close the terminal without stopping the tmux session.

## Creating An Event Trigger
Navigate to 'Cloud Functions' in the Cloud Console and create a function with 'Trigger Type' set to 'Cloud Storage', 'Event Type' set to 'Finalize/Create' and the bucket <br/>
name set to the bucket created in 'Setting Up Cloud Storage':




