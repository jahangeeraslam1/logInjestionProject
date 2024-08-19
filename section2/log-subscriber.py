import redis
import json 
from datetime import datetime 
import random

def parse_log(log_entry):
    
    #CAN ADD LOG PARSERS HERE 
    
    print(f"(Section 2) Parsed Log {log_entry}")
    
    

def main():
    
    redis_client = redis.Redis(host="localhost", port=6379, db=0)
    pubsub = redis_client.pubsub()
    pubsub.psubscribe("logs:*") #suscribes to all channels which begin with "logs:"
    
    #NOTE:subsrcibe to listen to an exact channel
    #NOTE psubscribe to listen to multiple channels matching a pattern
    print("Log Subscriber started. Waiting for messages...")
    

    for msg in pubsub.listen():
        if msg['type'] == "pmessage":
            
            log_entry = json.loads(msg['data'].decode('utf-8')) # Decodes the message and parse the JSON
            parse_log(log_entry)
if __name__ == "__main__":
    main()