from rest_framework.test import APITestCase
from school.models import School
from school.factories import SchoolFactory


class AccountTests(APITestCase):

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        SchoolFactory()
        print(School.objects.all())
        print('test_create_account')
        url = '/fairy/client/school/school/'
        response = self.client.get(url, format='json')
        print(response.data)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), 1)
