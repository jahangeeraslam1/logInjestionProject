import json 
from datetime import datetime 
import random

from google.cloud import storage
from google.cloud import pubsub_v1


def setup_gcs_client():
    return storage.Client()

def upload_to_gcs(client, bucket_name, log_entry):
    bucket = client.bucket(bucket_name) 
    
    blob_name = f"logs/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-{random.randint(1, 100)}.json" 
    
    blob = bucket.blob(blob_name)
    
    blob.upload_from_string(json.dumps(log_entry), content_type='application/json') #converts python object back to JSON

    print(f"Uploaded log to gs://{bucket_name}/{blob_name}") #DEBUGGING
    
    
def process_message(message, gcs_client, bucket_name):
    log_entry = json.loads(message.data.decode('utf-8')) #decodes object from bytes, and transofrms it to python object e.g dictonary
    parsed_log = parse_log(log_entry)
    
    upload_to_gcs(gcs_client, bucket_name, parsed_log)
    #sends acknowledgement back to google pub/sub topic
    message.ack()


def parse_log(log_entry):
    
    #CAN ADD log parsers here to parse log into correct format 
    
    #added a simple transfomation below to demonstrate functionality 
    #this makes all the keys inside the JSON log uppercase.
    uppercaseLog = {key.upper(): value for key, value in log_entry.items()}
    

    print(f"Parsed log: {uppercaseLog}") #DEBUGGING
    
    return log_entry
    

def main():
    
    subscriber = pubsub_v1.SubscriberClient() #pub/sub subscriber client setup 
    subscription_path = subscriber.subscription_path("chronicle-project-432815", "section4-chronicle-injestion_sub") #define subscipriton path
    
    print(f"Google Pub Sub Subscriber started. Currently subscribed to {subscription_path}")
    
    gcs_client = setup_gcs_client() 
    bucket_name = "section4-gcs_bucket" 
    
    
    #this starts a background thread that listens for messages on the subscription_path.
    #callback basically runs the process_messsage function on each message recieved
    
    future = subscriber.subscribe(subscription_path, callback=lambda message: process_message(message, gcs_client, bucket_name))

    try:
        future.result()
    except KeyboardInterrupt:
        future.cancel()
        
if __name__ == "__main__":
    main()
            
    
    
    
    
