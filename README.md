# 🚀 SIEM Log Ingestion

## 🌟 Project Overview

Let's be hoenst, injesting logs from multiple data sources into a SIEM can be a challenging task within SIEM migrations...

You need to identify all the data soruces within the organisation, collate a list of every single log type, figure out how you are going to handle migration of threat detection rules, its a sticky one. 

I've created this github repo to outline some of the methods which can be leveraged for log injestion into your new SIEM. 

> *Disclaimer: The code, logic, and explanations provided here are based on my personal opinion and understanding. While I believe the information to be accurate, I make no guarantees regarding its correctness or completeness. I am not liable for any issues that may arise from using this knowledge*

## 🌟 GoogleSecOps

Working with GoogleSecOps(formerly Chronicle SIEM) for this project,
typically (in my opinion) there are 4 ways to get your logs into Chronicle SIEM. 

**Injestion Methods**
### A. Direct Injestion from GCP
- test5
### B. Chronicle Forwarders/Collectors
- test4
### C. GCP Injestion API
- test3
### D. Cloud Bucket Sync
- test

In this repo, we're gonna foucs on **C. GCP Injestion API** and **D. Cloud Bucket Sync**. 

**Direct Injestion from GCP** and **Chronicle Forwarders/Collectorsc** will be covered in another repo soon. 

## Repo Guide

Have a look at this repo in the following order to grasp how to undertake Log Injestion into Chornicle SIEM. 

 #### section1 - Event Driven Architecture  
 
 - explains event driven arechitecutre concepts and why it is useful for SIEM log injestion

 #### section2 - REDIS Log Gathering System 
 
 section2a: log injestion setup
 - creates sample logs to work with
 - sets up a watcher to watch the log file and record changes
 - Publishes changes to the REDIS 
 - Creates subscriber to rertieve logs from REDIS

 section2b: adding fault tolerance
 - accounts for what happens when log watcher goes offline
 - determines and how it handles logs missed
 - ensures duplicate logs are not processed 


 #### section3 - REDIS Log Gathering System with GCS 

 - set up GCS bucket via Terraform to hold our logs
 - create workflow to auto send logs to this gcp bucket 


### section4 - Google Pub/Sub Log Gathering System with GCS 
 
 - switches from using REDIS to Google Pub/Sub 
 - sets up Google Pub/Sub pipelines via Terraform
 - sends logs from subscriber to GCS in batches

### section5 - Google Pub/Sub Log Gathering System with Injestion API 
 
 - switches from using REDIS to Google Pub/Sub 
 - sets up Google Pub/Sub pipelines via Terraform
 - sends logs from subscriber to Injestion API
 - covers API set up + authentication



## 🚀 Getting Started

1. Clone the repo
2. Set up your Google Cloud credentials in your CLI
3. Create virtual envrioement (reccomended but optional)
4. Install dependencies: `pip install -r requirements.txt`
5. Start the log generator: `python log_generator.py`
6. Launch the log watcher: `python log_watcher.py`
7. Run the log subscriber: `python log_subscriber.py`

> *Don't forget to launch the redis-server when working with section1,section2 and section3 and update auth/port details if needed*


## 

Built with ❤️ by [Jag Aslam]