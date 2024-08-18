# 🚀SIEM Log Ingestion

## Simulating the Pulse of Modern SIEM Architecture

## 🌟 Overview

Let's be hoenst, injesting logs from multiple data sources into a SIEM can be a challenging task within SIEM migrations...

You need to identify all the data soruces within the organisation, collate a list of every single log type, figure out how you are going to handle migration of threat detection rules, its a sticky one. 

I've created this github repo to outline some of the methods which can be leveraged for log injestion into your new SIEM. 

> *Disclaimer: The code, logic, and explanations provided here are based on my personal opinion and understanding. While I believe the information to be accurate, I make no guarantees regarding its correctness or completeness. I am not liable for any issues that may arise from using this knowledge*

## 🌟 GoogleSecOps

Working with GoogleSecOps(formerly Chronicle SIEM) for this project,
typically (in my opinion) there are 4 ways to get your logs into Chronicle SIEM. 

**Injestion Methods**
- Direct Injestion from GCP
- Chronicle Forwarders/Collectors
- GCP Injestion API
- Cloud Bucket Sync

In this repo, we're gonna foucs on **GCP Injestion API** and **Cloud Bucket Sync**.

Before that happens, we first need to get farmiliar with **event driven arechitecture** which is popularly used for sending logs to most SIEMS. 


Have a look at this repo in the following order to understand Log Injestion into Chornicle SIEM. 

 phase1-event-driven-archiecture

 - explains event driven arechitecutre concepts and why it is useful for SIEM log injestion

 phase2-log-injestion-setup

 - creates sample logs to work with
 - sets up a watcher to watch the log file and record changes
 - Publishes changes to the REDIS 
 - Creates subscriber to rertieve logs from REDIS

 phase3-gcs-and-terraform
 - set up GCS bucket via Terraform to hold our logs
 - create workflow to auto send logs to this gcp bucket 

 **LOGS READY FOR CHRONICLE VIA "Direct Injestion from GCP"**

 phase4-adding-fault-tolerance
 - accounts for what happens when log watcher goes offline
 - determines and how it handles logs missed
 - ensures duplicate logs are not processed 

 phase5-leveraging-gcp-pub-sub
 - switches from using REDIS to Google Pub/Sub 
 - sets up Google Pub/Sub pipelines via Terraform
 - sends logs from subscriber to GCS in batches

  phase5-using-injestion-API 
 - leverages Google Pub/Sub to send logs to chornicle using Injestion API
 - covers API set up + authentication


## 🚀 Getting Started

1. Clone the repository
2. Set up your Google Cloud credentials in your CLI
4. Install dependencies: `pip install -r requirements.txt`
5. Start the log generator: `python log_generator.py`
6. Launch the log watcher: `python log_watcher.py`
7. Run the log subscriber: `python log_subscriber.py`

## 

Built with ❤️ by [Jag Aslam]