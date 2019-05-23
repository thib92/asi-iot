# IoT Platform on Google Cloud Platform

## Abstract

In this project, we aimed at creating the bases of a cloud platform capable of handling data from sensors places at elderly people's homes in order to monitor their activity and therefore detect any anomalies that could be a sign of diseases like urinary tract infections or dementia. 

## Requirements

You only need to run the script `main_devices.py` locally in order to test the pipeline. For this, you need Python 3 (preferably Python 3.7), and the following modules:
* `pyjwt`
* `paho-mqtt`

You can install these dependencies using the Python PIP package manager.

## Running the project

Just use the following command:

`python3 main_devices.py`

The script will take care of instanciating five devices (4 position sensors and one temperature device).
Once all of them have an open connection to the MQTT Bridge, the script will ask each device to update its value and to send their value to the bridge, once per second.

Once in a while, the temperature device will receive a command from our Google Cloud Function, instructing it to turn on the fan because the temperature is too high.

To stop the script, just press `Ctrl+C`

## GitHub

https://github.com/thib92/asi-iot