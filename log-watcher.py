import time
from watchdog.observers import Observer #core class -> watches for file system events
from watchdog.events import FileSystemEventHandler #base class -> handles file system events 
import json
import redis

from checkpoint import CheckpointHandler #import the class created in checkpoint.py file



class LogHandler(FileSystemEventHandler): #LogHandler class extends FleSystemEventHandler to handle file modifcations.
    def __init__(self):
        self.checkpoint_handler = CheckpointHandler("log_checkpoint.txt")
        self.redis_client = redis.Redis(host="localhost", port=6379, db=0)
        self.last_processed_position = self.checkpoint_handler.last_position # keeps track of postion where log were last processed

        
    def on_modified(self, event): #code called when the log file is changed
        if event.src_path.endswith("app.log"):
            self.process_new_logs(event.src_path) #calls process new logs method on our path where app.log is stored
            
    def process_new_logs(self, file_path):
        
        with open(file_path, 'r') as file:
            print("Opened file")
            file.seek(self.last_processed_position) #looks at where we last left off based on the number in the chekpoint_text fle
            print(f"Seeking to last processed position: {self.last_processed_position}")
            
          
            new_logs = file.read() #reads from where we last processed
            
            
            if new_logs: #only runs if new logs exist since we last processed
                print(f"Read {len(new_logs)} bytes of new log data")
                
                for log_line in new_logs.splitlines():
                    if log_line: #ensures the code only processes non empty log lines -> avoids empty string errors
                        print("Processing log line")
                        log_entry = json.loads(log_line) #convert to JSON
                        self.publish_log(log_entry) #publish log to REDIS event broker
                 
                 
                        
                current_position = file.tell() #update current position after publishing the log 
              
               #update both checkpoint and last processed position to ensure we dont miss any logs between file modifcations
                self.checkpoint_handler.update_position(current_position)
                self.last_processed_position = current_position
                         
                print(f"Updated checkpoint to position: {current_position}")
                
            
                    
    def publish_log(self, log_entry): 
        channel = f"logs:{log_entry['type']})"
        message = json.dumps(log_entry)
        self.redis_client.publish(channel, message)
        print(f"Published to channel {channel} {message}")
        
        

def main():
        path = "."  # Watch the current directory
        event_handler = LogHandler()
        observer = Observer() #compoent which monitors the file
        observer.schedule(event_handler, path, recursive=False) #tell event handler to use observer to watch the file for changes
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
             
main()