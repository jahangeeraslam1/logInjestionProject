import json 
from datetime import datetime 
import time

from google.cloud import pubsub_v1
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

# Constants
SCOPES = ['https://www.googleapis.com/auth/malachite-ingestion']
ING_SERVICE_ACCOUNT_FILE = '/path/to/your/service-account-key.json'
CHRONICLE_INGESTION_URL = 'https://malachiteingestion-pa.googleapis.com/v2/projects/YOUR_PROJECT_ID/locations/YOUR_LOCATION/lake:batchCreateLogs'

def create_authorized_session():
    credentials = service_account.Credentials.from_service_account_file(
        ING_SERVICE_ACCOUNT_FILE, 
        scopes=SCOPES
    )
    return AuthorizedSession(credentials)

def send_to_chronicle(session, log_entry):
    body = {
        "customer_id": "YOUR_CUSTOMER_ID",
        "log_type": "YOUR_LOG_TYPE",
        "entries": [log_entry]
    }
    
    try:
        response = session.post(CHRONICLE_INGESTION_URL, json=body)
        response.raise_for_status()
        print(f"Successfully sent log to Chronicle: {log_entry}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send log to Chronicle. Error: {e}")

def process_message(message, chronicle_session):
    try:
        log_entry = json.loads(message.data.decode('utf-8'))
        parsed_log = parse_log(log_entry)
        send_to_chronicle(chronicle_session, parsed_log)
        message.ack()
    except json.JSONDecodeError as e:
        print(f"Error decoding message: {e}")
        message.nack()
    except Exception as e:
        print(f"Error processing message: {e}")
        message.nack()

def parse_log(log_entry):
    # You can add any necessary log parsing logic here
    return log_entry

def main():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path("chronicle-project-432815", "chronicle-injestion_sub")
    
    print(f"Google Pub/Sub Subscriber started. Currently subscribed to {subscription_path}")
    
    chronicle_session = create_authorized_session()
    
    def callback(message):
        process_message(message, chronicle_session)

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}")

    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
        print("Subscriber is shutting down.")
    finally:
        subscriber.close()
        chronicle_session.close()

if __name__ == "__main__":
    main()