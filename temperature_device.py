from device import Device
import random
import json

class TemperatureDevice(Device):
    def __init__(self, device_id, private_key_file):
        Device.__init__(self, device_id, private_key_file, "temperature")
        self.temperature = 20
        self.fan_on = False


    def update_sensor_data(self):
        """Pretend to read the device's sensor data.
        If the fan is on, assume the temperature decreased one degree,
        otherwise assume that it increased one degree.
        """
        if self.fan_on:
            if random.random() < 0.5:
                self.temperature -= 1
        else:
            self.temperature += 1

    def send_message(self):
        json_payload = json.dumps({'temperature': self.temperature})
        super().do_send_message(json_payload)
