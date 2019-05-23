import time
from temperature_device import TemperatureDevice
from position_device import PositionDevice

from constants import project_id, cloud_region, registry_id, algorithm

def main():

    rooms = ["bedroom", "living_room", "bathroom", "kitchen"]
    devices = []

    for i in range(1, 5):
        devices.append(PositionDevice("device{}".format(i), "keys/rsa_private{}.pem".format(i), rooms[i-1]))
        
    devices.append(TemperatureDevice("device5", "keys/rsa_private5.pem"))

    # Update and publish temperature readings at a rate of one per second.
    for _ in range(100):
        # In an actual device, this would read the device's sensors. Here,
        # you update the temperature based on whether the fan is on.
        for device in devices:
            device.update_sensor_data()
            device.send_message()
            
        time.sleep(1)


    for device in devices:
        device.client.disconnect()
        device.client.loop_stop()

    print('Done!')


if __name__ == '__main__':
    main()