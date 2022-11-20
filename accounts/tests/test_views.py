from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from .mixins import TestDataMixin
from django.contrib import auth

# Create your tests here.
# user = auth.get_user(self.c)


class RegisterFormTest(TestDataMixin, TestCase):

    def setUp(self):
        self.c = Client()
        pass

    def test_get(self):
        response = self.c.get(reverse('register'))
        # self.c.login(username='testuser1', password='testpassword1')
        self.assertEqual(response.status_code, 200)
        # print(response.content)

    def test_user_authenticated_redirect(self):
        self.c.login(username='testuser1', password='testpassword1')
        response = self.c.get(reverse('register'))
        self.assertEqual(response.status_code, 302)

    def test_form_valid_post(self):
        valid_data = {'username': 'john',
                    'password1': 'smithsmith',
                    'password2':'smithsmith',
                    'email':'test@email.com'}
        response = self.c.post(reverse('register'), valid_data)
        
        self.assertIn(self.customers_group, response.wsgi_request.user.groups.all())
        self.assertEqual(response.wsgi_request.user.username, 'john')
        self.assertEqual(response.status_code, 302)
        # self.assertContains(response, 'testuser1 You are already logged in')
        
    def test_form_invalid_post(self):
        invalid_data = {'username': 'john',
                    'password1': 'smithsmith',
                    'password2':'smithjhon',
                    'email':'test@email.com'}
        response = self.c.post(reverse('register'), invalid_data)
        messages =list(response.context['messages'])
        form = response.context['form']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(messages[0]), 'User Registration failed Make sure the data you entered is valid !')
        self.assertEqual(form.data['username'], 'john')
    
    