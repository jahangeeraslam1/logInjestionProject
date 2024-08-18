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
        self.last_processed_position = self.checkpoint_handler.last_position

        
    def on_modified(self, event): #code called when the log file is changed
        if event.src_path.endswith("app.log"):
            self.process_new_logs(event.src_path) #calls process new logs method on our path where app.log is stored
            
    def process_new_logs(self, file_path):
        with open(file_path, 'r') as file:
            print("opened file")
            file.seek(self.checkpoint_handler.last_position) #looks at where we last left off based on the number in the chekpoint_text fle
            print("got checkpoint from file")
            # new_logs = file.read() #reads all new logs from last checkpoint
            # current_position = file.tell() #records new position once it has all been read
            
        
            # for log_line in new_logs.strip().split('\n'):  #strip to remove new lines, split to divide the string into a list of sub-strings

            #     if log_line: #ensures the code only processes non empty log lines -> avoids empty string errors
            #         log_entry = json.loads(log_line) #converts to JSON format
            #         self.publish_log(log_entry) #publishes single log to REDIS event broker
            #         self.checkpoint_handler.update_position(current_position) #updates checkpoint.txt file with current read position
           
            print("about to read logs")
            while True: 
                print("reading logs")
                log_line = file.readline() #progress through new logs one at a time
                if not log_line: # if no new logs then break - HERE IS THE ISSUE
                    print("breaking ou the loop")
                    break
                
                log_line = log_line.strip() #strip => removes new lines 
                if log_line: #ensures the code only processes non empty log lines -> avoids empty string errors
                    print ("checked log not empty")
                    log_entry = json.loads(log_line) #convert to JSO
                    self.publish_log(log_entry) #publish log to REDIS event broker
                    
                current_position = file.tell() #update current position after publishing the log 
                self.checkpoint_handler.update_position(current_position)
                
            
                    
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