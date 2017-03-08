from datetime import timedelta
import json
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from match.models import Programme
from match.serializers import ProgrammeSerializer
from oauth2_provider.compat import urlencode
from oauth2_provider.models import AccessToken, Application
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.tests.test_utils import TestCaseUtils
from rest_framework import status
from rest_framework.test import APITestCase

class ProgrammeAPITests(TestCaseUtils, APITestCase):

    def setUp(self):
        self.test_user = User.objects.create_user("test@example.com", "test@example.com", "hunter23")
        self.staff_user = User.objects.create_user("staff@example.com", "staff@example.com", "hunter23", is_staff=True)

        self.application = Application(
            name = "Django Test",
            user= self.test_user,
            client_type = Application.CLIENT_PUBLIC,
            authorization_grant_type = Application.GRANT_PASSWORD,
        )
        self.application.save()

    def test_create_programme_if_staff(self):
        url = reverse('programme-list')
        data = {
            'name': 'Test Programme',
            'description': 'This is a test programme.',
            'defaultCohortSize': 100,
            'createdBy': self.staff_user.pk
        }
        token = self._create_token(self.staff_user, 'write staff')
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=self._get_auth_header(token=token.token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cant_create_programme_if_not_staff(self):
        url = reverse('programme-list')
        data = {
            'name': 'Test Programme',
            'description': 'This is a test programme.',
            'defaultCohortSize': 100,
            'createdBy': self.test_user.pk
        }
        token = self._create_token(self.staff_user, 'write staff')
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=self._get_auth_header(token=token.token))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    ## HELPER FUNCTIONS

    def _get_auth_header(self, token=None):
        return "Bearer {0}".format(token or self.access_token.token)

    def _create_token(self,user,scope):
        return AccessToken.objects.create(
            user=user,
            token='123456789',
            application=self.application,
            expires=timezone.now() + timedelta(days=1),
            scope=scope
        )
