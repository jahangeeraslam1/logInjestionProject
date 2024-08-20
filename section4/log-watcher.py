import time
from watchdog.observers import Observer 
from watchdog.events import FileSystemEventHandler
import json

from google.cloud import pubsub_v1 #import Google Cloud Pub/Sub client library.

from checkpoint import CheckpointHandler 

class LogHandler(FileSystemEventHandler): 
    
    def __init__(self):
        self.checkpoint_handler = CheckpointHandler("log-watcher-checkpoint.txt")
        self.last_processed_position = self.checkpoint_handler.last_position 
        
        #sets up the connection to Pub/Sub
        self.publisher = pubsub_v1.PublisherClient() #create a pubsub client
        self.topic_path = self.publisher.topic_path("chronicle-project-432815", "section4-chronicle-injestion-topic")  #specifiy the topic we'll be publishing our messages to (REPLACES REDIS CHANNELS)

       
    def on_modified(self, event): 
        if event.src_path.endswith("app.log"):
            self.process_new_logs(event.src_path) 
    
          
    def process_new_logs(self, file_path):
        with open(file_path, 'r') as file:
            
            file.seek(self.last_processed_position) 
            
            print(f"Seeking to last processed position: {self.last_processed_position}") #DEBUGGING STATEMENT
            
          
            new_logs = file.read() 
            
            
            if new_logs:
                
                print(f"Read {len(new_logs)} bytes of new log data") #DEBUGGING STATEMENT
        
                for log_line in new_logs.splitlines():
                    if log_line: 
                        print("Processing new log") #DEBUGGING STATEMENT
                        log_entry = json.loads(log_line)
                        self.publish_log(log_entry)
                 
                
                current_position = file.tell() 
              
                self.checkpoint_handler.update_position(current_position) 
                self.last_processed_position = current_position 
                         
                print(f"Updated checkpoint to position: {current_position}") #DEBUGGING STATEMENT
                
            
                    
    def publish_log(self, log_entry): 
        data = json.dumps(log_entry).encode('utf-8') #convert to JSON then bytes since pub/sub requires bytes input
        send = self.publisher.publish(self.topic_path, data)
        send.result()  # Wait for the publish to complete
        print(f"Published message to {self.topic_path} :  {log_entry}")
        
        
        

def main():
    
    
        path = "."  
        event_handler = LogHandler()
        observer = Observer() 
        observer.schedule(event_handler, path, recursive=False) 
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
             
main()