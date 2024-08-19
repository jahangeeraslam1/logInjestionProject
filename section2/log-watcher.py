import time
from watchdog.observers import Observer #core class needed -> Observer watches a file for events
from watchdog.events import FileSystemEventHandler #base class needed -> handles file system events 
import json
import redis

from checkpoint import CheckpointHandler #imports the class created in checkpoint.py file

class LogHandler(FileSystemEventHandler): 
    
    def __init__(self):
        self.checkpoint_handler = CheckpointHandler("log-watcher-checkpoint.txt")
        self.redis_client = redis.Redis(host="localhost", port=6379, db=0)
        self.last_processed_position = self.checkpoint_handler.last_position # keeps track of postion where log was last processed

       
    def on_modified(self, event): #method called each time the log file changes
        if event.src_path.endswith("app.log"):
            self.process_new_logs(event.src_path) #calls process_new_logs method on the path of app.log.
    
          
    def process_new_logs(self, file_path):
        with open(file_path, 'r') as file:
            
            file.seek(self.last_processed_position) #identifies where the last processed log is, based on the value inside log-watcher-checkpoint.txt
            
            print(f"Seeking to last processed position: {self.last_processed_position}") #DEBUGGING STATEMENT
            
          
            new_logs = file.read() #starts reading from where the log-watcher last processed
            
            
            if new_logs: #only runs if new logs exist since last processed
                
                print(f"Read {len(new_logs)} bytes of new log data") #DEBUGGING STATEMENT
        
                for log_line in new_logs.splitlines():
                    if log_line: #ensures the code only processes non empty log lines (avoiding empty string errors)
                        print("Processing new log") #DEBUGGING STATEMENT
                        log_entry = json.loads(log_line) #convert log from str to JSON (was read as str)
                        self.publish_log(log_entry) #publish log to event broker
                 
                #update variables publishing to event broker 
                current_position = file.tell() # amend current prosition in file 
               #update both checkpoint and last processed position to ensure we dont miss any logs between file modifcations
                self.checkpoint_handler.update_position(current_position) #updated checkpoint_handler allowing it to either hold the checkpoint in memory or write to disk
                self.last_processed_position = current_position #set last processed position to now
                         
                print(f"Updated checkpoint to position: {current_position}")  #DEBUGGING STATEMENT
                
            
                    
    def publish_log(self, log_entry): 
        channel = f"logs:{log_entry['type']})" #create new REDIS channel for each log type
        message = json.dumps(log_entry) 
        self.redis_client.publish(channel, message)
        print(f"Published to channel {channel} {message}")
        
        

def main():
        path = "."  # watch the current directory, replace with location of .log file in prod env
        event_handler = LogHandler()
        observer = Observer() 
        observer.schedule(event_handler, path, recursive=False) #tells event_handler to use observer to watch the .log file  for changes
        observer.start()
        try:
            while True:
                time.sleep(1) # watches for new logs every second -> added to avoid CPU drain
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
             
if __name__ == "__main__":
    main()