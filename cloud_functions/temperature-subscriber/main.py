import base64
import json

from googleapiclient import discovery
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials

project_id = "isep-asi"
cloud_region = "europe-west1"
registry_id = "main-registry"

credentials = ServiceAccountCredentials.from_json_keyfile_name("isep-asi-5f38abd0c314.json", ['https://www.googleapis.com/auth/cloud-platform'])

service = discovery.build(
            'cloudiot',
            'v1',
            discoveryServiceUrl='https://cloudiot.googleapis.com/$discovery/rest',
            credentials=credentials,
            cache_discovery=False)

def telemetry_subscriber(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    device_id = event['attributes']['deviceId']
    data = json.loads(base64.b64decode(event['data']).decode('utf-8'))

    config_data = None
    print('The device ({}) has a temperature of: {}'.format(device_id, data['temperature']))
    if data['temperature'] < 0:
        # Turn off the fan.
        config_data = {'fan_on': False}
        print('Setting fan state for device', device_id, 'to off.')
    elif data['temperature'] > 10:
        # Turn on the fan
        config_data = {'fan_on': True}
        print('Setting fan state for device', device_id, 'to on.')
    else:
        # Temperature is OK, don't need to push a new config.
        return

    config_data_json = json.dumps(config_data)
    body = {
        # The device configuration specifies a version to update, which
        # can be used to avoid having configuration updates race. In this
        # case, you use the special value of 0, which tells Cloud IoT to
        # always update the config.
        'version_to_update': 0,
        # The data is passed as raw bytes, so you encode it as base64.
        # Note that the device will receive the decoded string, so you
        # do not need to base64 decode the string on the device.
        'binary_data': base64.b64encode(
                config_data_json.encode('utf-8')).decode('ascii')
    }

    device_name = ('projects/{}/locations/{}/registries/{}/'
                    'devices/{}'.format(
                        project_id,
                        cloud_region,
                        registry_id,
                        device_id))

    request = service.projects().locations().registries().devices(
    ).modifyCloudToDeviceConfig(name=device_name, body=body)

    request.execute()
