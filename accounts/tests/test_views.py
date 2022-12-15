from django.test import TestCase, RequestFactory, Client
from django.urls import reverse

from accounts.models import CustomUser, Customer
from .mixins import TestDataMixin
from django.contrib import auth
from django.contrib.messages import get_messages

# Create your tests here.
# user = auth.get_user(self.c)


class RegisterFormTest(TestDataMixin, TestCase):

    def setUp(self):
        self.c = Client()
        pass

    def test_get(self):
        response = self.c.get(reverse('register'))
        form = response.context['form']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(dict(form.data),{})

    def test_user_authenticated_redirect(self):
        self.c.login(username='testuser1', password='testpassword1')
        response = self.c.get(reverse('register'))

        self.assertRedirects(response, '/', status_code=302, target_status_code=302)

    def test_form_valid_post(self):
        valid_data = {'username': 'john',
                    'password1': 'smithsmith',
                    'password2':'smithsmith',
                    'email':'test@email.com'}
        response = self.c.post(reverse('register'), valid_data)
        
        self.assertIn(self.customers_group, response.wsgi_request.user.groups.all())
        self.assertEqual(response.wsgi_request.user.username, 'john')
        self.assertEqual(response.status_code, 302)
        
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
    

class AdminRegisterTest(TestDataMixin, TestCase):

    def setUp(self):
        self.c = Client()
        self.c.login(username= self.super_user.username, password='testsuperuser2')

    # def test_get(self):
    #     response = self.c.get(reverse('register'))
    #     # self.c.login(username='testuser1', password='testpassword1')
    #     self.assertEqual(response.status_code, 200)
    #     # print(response.content)

    def test_register_admin_redirect(self):
        # self.c.login(username='testuser1', password='testpassword1')
        # self.c.login(username= self.super_user.username, password='testsuperuser2')
        session = self.c.session
        session['new_admin_user'] = self.user_admin.id
        session.save()
        response = self.c.get(reverse('admin_register'), follow=True)
        messages = list(response.context['messages'])
        
        self.assertRedirects(response, '/accounts/administrator/admin_profile/', status_code=302,
                                        target_status_code=200 , fetch_redirect_response=True)
        self.assertEqual(str(messages[0]), f'Create a profile for User "{self.user_admin}" !')

    def test_register_admin_redirect_normal(self):
        # self.c.login(username='testuser1', password='testpassword1')
        # self.c.login(username= self.super_user.username, password='testsuperuser2')
       
        response = self.c.get(reverse('admin_register'), follow=True)
        form = response.context['form']
        self.assertEqual(dict(form.data), {})
        self.assertEqual(response.wsgi_request.path, reverse('admin_register'))

    def test_form_valid_post(self):
        valid_data = {'username': 'john',
                    'password1': 'smithsmith',
                    'password2':'smithsmith',
                    'email':'test@email.com'}
        response = self.c.post(reverse('admin_register'), valid_data)
        admin_user_id = self.c.session.get('new_admin_user')
        admin_user = CustomUser.objects.get(id=admin_user_id)
        group_names = admin_user.groups.values_list('name',flat = True)

        self.assertIn('administrators', group_names)
        self.assertEqual(admin_user.username, 'john')
        self.assertRedirects(response, reverse('admin_profile'), status_code=302,
                                        target_status_code=200 )
        
    def test_form_invalid_post(self):
        invalid_data = {'username': 'john',
                    'password1': 'smithsmith',
                    'password2':'smithjhon',
                    'email':'test@email.com'}
        response = self.c.post(reverse('admin_register'), invalid_data)
       
        form = response.context['form']
        self.assertEqual(response.wsgi_request.path, reverse('admin_register'))
        self.assertEqual(form.data['username'], 'john')
    

class AdminProfileTest(TestDataMixin, TestCase):

    def setUp(self):
        self.c = Client()
        self.c.login(username= self.super_user.username, password='testsuperuser2')

    # def test_get(self):
    #     response = self.c.get(reverse('register'))
    #     # self.c.login(username='testuser1', password='testpassword1')
    #     self.assertEqual(response.status_code, 200)
    #     # print(response.content)

    def test_unregister_admin_redirect(self):
        response = self.c.get(reverse('admin_profile'))
        self.assertRedirects(response, reverse('admin_register'), status_code=302,
                                        target_status_code=200 , fetch_redirect_response=True)

    def test_form_valid_post(self):
        session = self.c.session
        session['new_admin_user'] = self.user_admin.id
        session.save()
        valid_data = {'first_name': 'john',
                    'last_name': 'smithsmith'}
        response = self.c.post(reverse('admin_profile'), valid_data)
        empty = response.wsgi_request.session.get('new_admin_user')
        admin_user = CustomUser.objects.get(id=self.user_admin.id)
        
        self.assertFalse(empty)
        self.assertEqual(admin_user.administrator.first_name, 'john')
        self.assertRedirects(response, reverse('homepage'), status_code=302,
                                        target_status_code=200 )
        
    def test_form_invalid_post(self):
        session = self.c.session
        session['new_admin_user'] = self.user_admin.id
        session.save()
        invalid_data = {'first_name': 'john321',
                    'last_name': 'smithsmith'}
        response = self.c.post(reverse('admin_profile'), invalid_data)
       
        form = response.context['form']
        self.assertEqual(response.wsgi_request.path, reverse('admin_profile'))
        self.assertEqual(form.data['first_name'], 'john321')