from device import Device
import random
import json
from queue import Queue

class PositionDevice(Device): 
    def __init__(self, device_id, private_key_file, name):
        Device.__init__(self, device_id, private_key_file, "position")
        
        self.name = name
        self.triggered = False
        self.i = 30*60
        
        self.queue = Queue()
        self.file = open("location.txt", "r")
        
        for line in self.file:
            if line == self.name:
                self.queue.put(True)
            else :
                self.queue.put(False)

    
    def update_sensor_data(self):
        if self.i % (30*60) == 0:
            self.triggered = self.queue.get()

        self.i += 1


    def send_message(self):
        json_payload = json.dumps({'triggered': self.triggered})
        super().do_send_message(json_payload)