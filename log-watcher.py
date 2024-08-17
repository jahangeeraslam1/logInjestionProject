import time
from watchdog.observers import Observer #core class -> watches for file system events
from watchdog.events import FileSystemEventHandler #base class -> handles file system events 
import json
import redis

class LogHandler(FileSystemEventHandler): #LogHandler class extends FleSystemEventHandler to handle file modifcations.
    def __init__(self):
        self.last_position = 0 #keeps track of where it previously read so we start it at 0
        self.redis_client = redis.Redis(host="localhost", port=6379, db=0)
        
    def on_modified(self, event): #code called when the log file is changed
        if event.src_path.endswith("app.log"):
            self.process_new_logs(event.src_path) #calls process new logs method on our 
            
    def process_new_logs(self, file_path):
        with open(file_path, 'r') as file:
            file.seek(self.last_position) #looks at where we last left off 
            new_logs = file.read() #reads all new content
            self.last_position = file.tell() #updates last read till position to be used next time on_modified is called
        
            for log_line in new_logs.strip().split('\n'):  #strip to remove new lines, split to divide the string into a list of sub-strings

                if log_line: #ensures the code only processes non empty log lines -> avoids JSON loads to occur on an empty string
                    log_entry = json.loads(log_line) #converts sub-strings to JSON format
                    self.publish_log(log_entry)
                    
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