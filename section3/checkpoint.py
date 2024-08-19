#adds a checkpoint system to the log-watcher file
#captures upto which point in the file logs have already been published to the event broker
#avoids duplicate logs being sent to the messages broker -> hence avoids duplicates beign sent to GCS. 
#without this functionality, each time the log-watcher is restarted it would sent all logs from the beginning of the file to the event broker
# designed to ensure if the low watcher goes offline (even for a couple of secs), once back online it only publishes what it missed to the event broker, and not evertything.

import time


class CheckpointHandler:
    def __init__(self, checkpoint_file, max_logs_before_write=50, max_time_before_write=2):
        #instance variables of class
  
        self.checkpoint_file = checkpoint_file
        self.max_logs_before_write = max_logs_before_write
        self.max_time_before_write = max_time_before_write
        
        #keeps track of last known position  and the current position in the log file.
        self.last_position = self.read_checkpoint()
        self.current_position = self.last_position
        
        #creates variables to messaure how many logs have been processed before last write and the last write time
        self.logs_processed_since_write = 0
        self.last_write_time = time.time()

    #method reads the number from the checkpoint.txt file when initalised
    #if file doesnt exist it outputs 0 
    def read_checkpoint(self):
        try:
            with open(self.checkpoint_file, 'r') as f:
                return int(f.read().strip() or 0)
        except FileNotFoundError:
            return 0
    
    #method writes the current position to the checkpoint.txt file
    def write_checkpoint(self):
        with open(self.checkpoint_file, 'w') as f:
            f.write(str(self.current_position))

        # sets the last position to the current position since it has just written out 
        self.last_position = self.current_position
        
        #updates the checkpoint variables in the code to reset counters based on this write
        self.logs_processed_since_write = 0
        self.last_write_time = time.time()


    #called after processing logs to update the current position and decide whether to write a new checkpoint.
    def update_position(self, new_position):
        self.current_position = new_position
        self.logs_processed_since_write += 1
        #check if we should write a new checkpoint based time elapsed since last write / no of logs read since last write
        if (self.logs_processed_since_write >= self.max_logs_before_write or
            time.time() - self.last_write_time >= self.max_time_before_write):
            self.write_checkpoint()