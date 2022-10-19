from django.test import TestCase ,RequestFactory
from django.urls import reverse

# Create your tests here.


class CustomerProfileTest(TestCase):

    @classmethod
    def setUpTestData(self):
        pass

    def setUp(self):
        pass

    def test_response(self):
        response = self.client.get(reverse('homepage'))
        print(response)
        self.assertEqual(response.status_code, 200)
