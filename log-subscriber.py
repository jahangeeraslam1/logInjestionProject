import redis
import json 
from google.cloud import storage
from datetime import datetime 
import random


def setup_gcs_client():
    return storage.Client()


def upload_to_gcs(client, bucket_name, log_entry):
    bucket = client.bucket(bucket_name) # tells client which bucket we are working with 
    
    blob_name = f"logs2/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-{random.randint(1, 1000)}.json" #name of file
    
    blob = bucket.blob(blob_name) #creates new blob object with the name we made -> blob = a file in GCS.
    
    blob.upload_from_string(json.dumps(log_entry), content_type='application/json') 
    # uses json.dumps(log_entry) to convert log_entry object to a JSON string
    # content_type -  sets the MIME type of the file to JSON
    
    print(f"Uploaded log to gs://{bucket_name}/{blob_name}") #shows where it was uploaded
    
    

def parse_log(gcs_client,bucket_name,log_entry):
    
    
    #can add log parsers here to parse log into correct format 
    #
    #
    print(f"Parsed log: {log_entry}")
    
    #call function to upload log to GCS 
    upload_to_gcs(gcs_client, bucket_name, log_entry)
    

def main():
    
    redis_client = redis.Redis(host="localhost", port=6379, db=0)
    pubsub = redis_client.pubsub() #allows you to subscribe to channels and listen for messages that get published to them.
    pubsub.psubscribe("logs:*") #suscribes to all channels which begin with "logs:"
    #use subsrcibe when you know the exact channel name you wanna listen to.
    #use psubscribe when you know you wanna to listen to multiple channels which are matching a pattern.
    print("Log Subscriber started. Waiting for messages...")
    
    
    gcs_client = setup_gcs_client() #sets up gcs client for to send logs to gcs bucket 
    bucket_name = "logging_bucket-448" #specifies bucket name to send logs to 
    
     
    for msg in pubsub.listen():
        if msg['type'] == "pmessage":
            # Decodes the message and parse the JSON
            log_entry = json.loads(msg['data'].decode('utf-8'))
            parse_log(gcs_client,bucket_name,log_entry)
            

if __name__ == "__main__":
    main()
            
    
    
    
    
