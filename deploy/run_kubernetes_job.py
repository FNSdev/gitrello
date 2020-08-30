# TODO it will not work correctly if job can fail and restart""

import argparse
import os
import sys
import time

import requests


class KubernetesJobException(Exception):
    pass


# TODO logging
class KubernetesJob:
    ACTIVE = 'active'
    SUCCEEDED = 'succeeded'
    FAILED = 'failed'

    def __init__(self, name, file_name, k8s_url, k8s_token):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'manifests', 'gitrello', file_name))

        with open(path, 'r') as file:
            self.manifest = file.read()
        self.name = name
        self._url = k8s_url
        self._token = k8s_token

    def clean_up(self):
        headers = {
            'Authorization': f'Bearer {self._token}',
            'Content-Type': 'application/json',
        }
        data = {
            'kind': 'DeleteOptions',
            'apiVersion': 'batch/v1',
            'propagationPolicy': 'Background',
            'gracePeriodSeconds': 0,
        }

        print('Cleaning up')
        response = requests.delete(
            f'{self._url}/apis/batch/v1/namespaces/default/jobs/{self.name}',
            headers=headers,
            json=data,
        )
        if not response.status_code == 200:
            print(response.text)
            raise KubernetesJobException('Clean up failed')

        print('Clean up succeeded')

    def create(self):
        headers = {
            'Authorization': f'Bearer {self._token}',
            'Content-Type': 'application/yaml',
        }

        print('Creating job')
        response = requests.post(
            f'{self._url}/apis/batch/v1/namespaces/default/jobs',
            data=self.manifest,
            headers=headers
        )

        if response.status_code not in (200, 201, 202):
            print(response.text)
            raise KubernetesJobException('Creating job failed')

        print('Job created')

    def get_status(self):
        headers = {'Authorization': f'Bearer {self._token}'}

        print('Getting status')
        response = requests.get(f'{self._url}/apis/batch/v1/namespaces/default/jobs/{self.name}', headers=headers)

        if response.status_code != 200:
            print(response.text)
            raise KubernetesJobException('Check job status failed')

        response = response.json()
        if response['status'].get('active') is not None:
            return self.ACTIVE

        if response['status'].get('failed') is not None:
            return self.FAILED

        return self.SUCCEEDED

    def get_logs(self):
        headers = {'Authorization': f'Bearer {self._token}'}

        print('Getting logs')
        response = requests.get(
            f'{self._url}/api/v1/namespaces/default/pods?labelSelector=job-name%3D{self.name}',
            headers=headers,
        )
        if response.status_code != 200:
            print(response.text)
            raise KubernetesJobException('Get logs failed. Could not get pods list')

        pod = response.json()['items'][0]
        pod_name = pod['metadata']['name']

        response = requests.get(f'{self._url}/api/v1/namespaces/default/pods/{pod_name}/log', headers=headers)

        if response.status_code != 200:
            print(response.text)
            raise KubernetesJobException('Get logs failed. Could not get pod`s logs')

        return response.text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', type=str)
    parser.add_argument('-f', '--file-name', type=str)
    parser.add_argument('-l', '--time-limit', type=int)
    parser.add_argument('-s', '--sleep-time', type=int)
    args = parser.parse_args()

    job = KubernetesJob(
        name=args.name,
        file_name=args.file_name,
        k8s_url=os.getenv('K8S_URL'),
        k8s_token=os.getenv('K8S_TOKEN'),
    )

    try:
        job.create()

        waiting_for = 0
        while True:
            time.sleep(args.sleep_time)
            waiting_for += args.sleep_time

            status = job.get_status()
            if status != job.ACTIVE or waiting_for >= args.time_limit:
                break

        print(job.get_logs())
        print(f'Job status: {status}')
        job.clean_up()

        if status != job.SUCCEEDED:
            sys.exit(-1)

    except KubernetesJobException as e:
        print(e)
        job.clean_up()
        sys.exit(-1)
    except Exception as e:
        print(e)
        sys.exit(-1)


if __name__ == '__main__':
    main()
