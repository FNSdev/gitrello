import os
import sys
import time

import requests

TIME_LIMIT = 180
SLEEP_TIME = 10


def clean_up(k8s_url, k8s_token):
    headers = {
        'Authorization': f'Bearer {k8s_token}',
        'Content-Type': 'application/json',
    }
    data = {
        'kid': 'DeleteOptions',
        'apiVersion': 'batch/v1',
        'propagationPolicy': 'Background',
        'gracePeriodSeconds': 0,
    }

    response = requests.delete(
        f'{k8s_url}/apis/batch/v1/namespaces/test/jobs/run-tests-job',
        headers=headers,
        json=data,
    )
    if not response.status_code == 200:
        print('Clean up failed')
        print(response.text)
        sys.exit(-1)

    print('Clean up succeeded')


# TODO use logging
def main():
    k8s_token = os.getenv('K8S_TOKEN')
    k8s_url = os.getenv('K8S_URL')

    assert k8s_token, 'K8S_TOKEN env variable must be set'
    assert k8s_url, 'K8S_URL env variable must be set'

    with open('deploy/manifests/jobs/run-tests-job.yaml', 'r') as file:
        job_config = file.read()

    headers = {
        'Authorization': f'Bearer {k8s_token}',
        'Content-Type': 'application/yaml',
    }

    print('Creating job')
    response = requests.post(f'{k8s_url}/apis/batch/v1/namespaces/test/jobs', data=job_config, headers=headers)

    if response.status_code not in (200, 201, 202):
        print('Failed to create job')
        print(response.text)
        clean_up(k8s_url, k8s_token)
        sys.exit(1)

    print('Job created')
    waiting_for = 0
    while True:
        time.sleep(SLEEP_TIME)
        waiting_for += SLEEP_TIME

        print('Checking job status')

        headers = {'Authorization': f'Bearer {k8s_token}'}
        response = requests.get(f'{k8s_url}/apis/batch/v1/namespaces/test/jobs/run-tests-job', headers=headers)

        if response.status_code != 200:
            print('Failed to check job status')
            print(response.text)
            clean_up(k8s_url, k8s_token)
            sys.exit(2)

        response = response.json()
        if not response['status'].get('active'):
            break

        if waiting_for >= TIME_LIMIT:
            print('Reached time limit, exiting')
            clean_up(k8s_url, k8s_token)
            sys.exit(3)

    if response['status'].get('succeeded', 0) == 1:
        status = 'Success'
    elif response['status'].get('failed', 0) == 1:
        status = 'Fail'
    else:
        status = 'Unknown'

    response = requests.get(
        f'{k8s_url}/api/v1/namespaces/test/pods?labelSelector=job-name%3Drun-tests-job',
        headers=headers,
    )
    if response.status_code != 200:
        print('Failed to get pods list')
        print(response.text)
        clean_up(k8s_url, k8s_token)
        sys.exit(4)

    pod = response.json()['items'][0]
    pod_name = pod['metadata']['name']

    response = requests.get(f'{k8s_url}/api/v1/namespaces/test/pods/{pod_name}/log', headers=headers)

    clean_up(k8s_url, k8s_token)

    if response.status_code != 200:
        print('Failed to get pod`s logs')
        print(response.text)
        sys.exit(5)

    print(response.text)
    print(status)
    if status == 'Fail':
        sys.exit(6)


if __name__ == '__main__':
    main()
