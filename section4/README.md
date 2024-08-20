# 🚀 SECTION 4 - Google Pub/Sub Log Gathering System with GCS 

In this section, I'll cover how to:

 - Switch from using Redis to Google Pub/Sub 
 - Set up Google Pub/Sub pipelines via Terraform 
 - Work with Google Pub/Sub topics, subscriptions, and subscribers

## Repo Overview

### 1. Google Pub/Sub Setup

We need to create both an ingestion topic and an ingestion subscription in GCP for our program to leverage Google Pub/Sub for log processing. 

```hcl
resource "google_pubsub_topic" "section4-chronicle-ingestion-topic" {
  name = "section4-chronicle-ingestion-topic" #name of topic in GCP

  labels = {
    environment = "development"
    purpose     = "security_logs_ingestion"
  }

  #CAN ADD CMEK here for sensitive logs.

   
   message_storage_policy { 
    allowed_persistence_regions = [ #only allow messages to be stored in Europe for compliance purposes 
      "europe-west1",
      "europe-west2",
      "europe-west3"
    ] 
    }
}
```

```hcl
resource "google_pubsub_subscription" "section4-chronicle-injestion_sub" {
  name  = "section4-chronicle-injestion_sub" #name of subscibrption in GCP
  topic = google_pubsub_topic.chronicle-injestion-topic.name

  ack_deadline_seconds = 60 #max time for subscriber to acknowledge message
  
  enable_message_ordering = true #messages delivered in the order they were pushed(optional)

  labels = {
    environment = "development"
    purpose     = "security_logs_subscription"
  }
```

### 2. Changes to log-watcher.py

We import the Google Pub/Sub package in Python

```python
from google.cloud import pubsub_v1 #import Google Cloud Pub/Sub client library.
```
Inside the log-watcher.py we remove the Redis client and add a Pub/Sub client to be part of the LogHandler class.
Replace the project ID and the ingestion topics with your own values.

```python
        #sets up the connection to Pub/Sub
        self.publisher = pubsub_v1.PublisherClient() #create a pubsub client
        self.topic_path = self.publisher.topic_path("chronicle-project-432815", "chronicle-injestion-topic")  #specifiy the topic we'll be publishing our messages to (REPLACES REDIS CHANNELS)
```
We also replace the Redis code within our publish_log method and add the following lines of code to publish the message to our Google Pub/Sub topic.

```python
   send = self.publisher.publish(self.topic_path, data) 
        send.result()  # Wait for the publish to complete

```

### 3. Changes to log-subscriber.py

Within our log-subscriber.py file under the main() method we undertake the following:
Add our subscriber client and define the subscription path for it to watch.

```python
 subscriber = pubsub_v1.SubscriberClient() #pub/sub subscriber client setup 
    subscription_path = subscriber.subscription_path("chronicle-project-432815", "chronicle-injestion_sub") #define subscipriton path
```
Upon a new message appearing in our subscription, we call the process_message method on the message received, which in this case would be our log.

```python
    future = subscriber.subscribe(subscription_path, callback=lambda message: process_message(message, gcs_client, bucket_name))
  ```  
The process_message includes the following line which then lets the subscription know we have successfully processed the message.

```python
    message.ack()
```