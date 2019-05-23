import io

from googleapiclient import discovery
from google.oauth2 import service_account


def get_client():
    """
    Returns an authorized API client by discovering the IoT API and creating
    a service object using the service account credentials JSON.
    """
    api_scopes = ['https://www.googleapis.com/auth/cloud-platform']
    api_version = 'v1'
    discovery_api = 'https://cloudiot.googleapis.com/$discovery/rest'
    service_name = 'cloudiotcore'

    credentials = service_account.Credentials.from_service_account_file("isep-asi-8ba6252066fb.json")
    scoped_credentials = credentials.with_scopes(api_scopes)

    discovery_url = '{}?version={}'.format(
            discovery_api, api_version)

    return discovery.build(
            service_name,
            api_version,
            discoveryServiceUrl=discovery_url,
            credentials=scoped_credentials)


def create_rs256_device(
        project_id, cloud_region, registry_id, device_id,
        certificate):
    """
    Create a new device with the given id, using RS256 for
    authentication.
    """
    registry_name = 'projects/{}/locations/{}/registries/{}'.format(
            project_id, cloud_region, registry_id)

    client = get_client()

    # Note: You can have multiple credentials associated with a device.
    device_template = {
        'id': device_id,
        'credentials': [{
            'publicKey': {
                'format': 'RSA_X509_PEM',
                'key': certificate
            }
        }]
    }

    devices = client.projects().locations().registries().devices()
    return devices.create(parent=registry_name, body=device_template).execute()



if __name__ == '__main__':
    for i in range(1, 6):
        f = open("rsa_cert"+str(i)+".pem", "r")
        cert = f.read()
        create_rs256_device("isep-asi", "europe-west1", "main-registry", "device"+str(i), cert)