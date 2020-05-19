from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from authentication.tests.factories import UserFactory
from gitrello.exceptions import APIRequestValidationException
from organizations.exceptions import OrganizationAlreadyExistsException
from organizations.services import OrganizationService
from organizations.tests.factories import OrganizationFactory


class TestOrganizationsView(TestCase):
    def test_create_organization(self):
        payload = {
            'name': 'GITrello',
        }

        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)
        organization = OrganizationFactory()

        with patch.object(
                OrganizationService, 'create_organization', return_value=organization) as mocked_create_organization:
            response = api_client.post('/api/v1/organizations', data=payload, format='json')

        self.assertEqual(response.status_code, 201)
        mocked_create_organization.assert_called_with(
            owner_id=user.id,
            name=payload['name'],
        )
        self.assertDictEqual(response.data, {'id': str(organization.id), 'name': organization.name})

    def test_create_organization_not_authenticated(self):
        payload = {
            'name': 'GITrello',
        }

        api_client = APIClient()
        response = api_client.post('/api/v1/organizations', data=payload, format='json')

        self.assertEqual(response.status_code, 403)

    def test_create_organization_request_not_valid(self):
        payload = {
            'extra_argument': 42,
        }

        api_client = APIClient()
        api_client.force_authenticate(user=UserFactory())
        response = api_client.post('/api/v1/organizations', data=payload, format='json')

        self.assertEqual(response.status_code, 400)

        expected_response = {
            'error_code': APIRequestValidationException.code,
            'error_message': APIRequestValidationException.message,
            'error_details': {
                "name": [
                    "This field is required."
                ],
            }
        }
        self.assertDictEqual(response.data, expected_response)

    def test_create_organization_already_exists(self):
        organization = OrganizationFactory(name='GITRello')
        payload = {
            'name': organization.name,
        }

        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)

        with patch.object(
                OrganizationService,
                'create_organization',
                side_effect=OrganizationAlreadyExistsException) as mocked_create_organization:
            response = api_client.post('/api/v1/organizations', data=payload, format='json')

        self.assertEqual(response.status_code, 400)
        mocked_create_organization.assert_called_with(
            owner_id=user.id,
            name=payload['name'],
        )
        expected_response = {
            'error_code': OrganizationAlreadyExistsException.code,
            'error_message': OrganizationAlreadyExistsException.message,
        }
        self.assertDictEqual(response.data, expected_response)
