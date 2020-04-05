import os
import sys

import requests


def main():
    k8s_url = os.getenv('K8S_URL')
    k8s_token = os.getenv('K8S_TOKEN')
    data = {
        'spec': {
            'template': {
                'spec': {
                    'containers': [
                        {
                            'name': 'gitrello',
                            'image': f'fnsdev/gitrello:{os.getenv("RELEASE_VERSION")}'
                        }
                    ]
                }
            }
        }
    }
    headers = {
        'Content-Type': 'application/strategic-merge-patch+json',
        'Authorization': f'Bearer {k8s_token}',
    }

    print('Patch deployment')
    response = requests.patch(
        f'{k8s_url}/apis/apps/v1/namespaces/default/deployments/gitrello',
        headers=headers,
        json=data,
    )

    if response.status_code not in (200, 201):
        print(response.text)
        print('Patching deployment failed')
        sys.exit(-1)

    # TODO check deployment status
    print('Patch deployment succeeded')


if __name__ == '__main__':
    main()
