# Section 3 - REDIS Log Gathering System with GCS

In this section, I'll cover how to:

- Set up a Google Cloud Storage Bucket via Terraform
- Create a workflow allowing our subscriber to send logs to GCS

## Architecture

![Image Alt text](images/section2-diagram.png)

## Repo Overview

There are 2 main components inside this section. Let's discuss them one by one.

### 1. GCS Set-Up

We set up our Terraform configurations as standard in our provider.tf file. 

We also leverage a variables.tf which specifies the GCP_PROJECTID, GCP_REGION, and GCP_ZONE.

We leverage the following resource from Terraform Registry to create our bucket:

```hcl
resource "google_storage_bucket" "logging_bucket" {
  # ... configuration ...
}
```

Authentication was done via the GCP CLI, but for better security, it is generally recommended to use service accounts.

### 2. Feeding logs from Subscriber to GCS
The Google Cloud Storage client is set up in the main method below:

```
gcs_client = setup_gcs_client() # sets up gcs client to send logs to gcs bucket 
bucket_name = "section3-gcs-bucket" # specifies bucket name to send logs to
 ```

The following two methods were added to our log-subscrber.py script:

```
def setup_gcs_client():
    return storage.Client()

def upload_to_gcs(client, bucket_name, log_entry):
    bucket = client.bucket(bucket_name) # tells client which bucket we are working with 
    
    blob_name = f"logs7/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-{random.randint(1, 1000)}.json" #name of file
    
    blob = bucket.blob(blob_name) #creates new blob object with the name we made -> blob = a file in GCS.
    
    blob.upload_from_string(json.dumps(log_entry), content_type='application/json') 
    # uses json.dumps(log_entry) to convert log_entry object to a JSON string
    # content_type -  sets the MIME type of the file to JSON
    
    print(f"Uploaded log to gs://{bucket_name}/{blob_name}") #shows where it was uploaded
    
```

### 3. Parsing Example

We also added some form of parsing here to our log before sending it to the GCS bucket.

When working with GoogleSecOps, normalization of logs can take place here (converting raw logs into UDM formatting) or manipulating the log data into a format you want.

```
def parse_log(gcs_client,bucket_name,log_entry):
    
    
    uppercaseLog = {key.upper(): value for key, value in log_entry.items()}
    

    print(f"Parsed log: {uppercaseLog}") #DEBUGGING
    
    #call function to upload log to GCS 
    upload_to_gcs(gcs_client, bucket_name, uppercaseLog)
```

## Run the code

First run terrafrom apply to create the GCS bucket.

Once all three files (log-generator, log_watcher and log_subscriber) are running, logs which are created by the generator should appear instantaneously within the subscriber window.

Check the GCS bucket, and you should see a new log file being added for each log new log made by the generator. 


## Congratulations

You have now just taken logs from an on-premsis program and created a workflow to allow them to be send to your cloud envriomeent. 

The project is almost production ready, its just time to switch out REDIS for a similar event processing tool. 

Check out section4 :) 
