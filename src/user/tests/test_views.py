
from django.test import TestCase, Client
from django.urls import reverse 
from user.models import *
from user.utils import *
import json


class TestViews(TestCase):


    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.signup_url = reverse('signup')
        self.registerpatient_url = reverse('registerPatient')
        self.loginUser_url = reverse('loginUser')
        self.logout_url = reverse('logout')

    def test_login(self):

        
        response = self.client.get(self.login_url)
        request = response.wsgi_request
        user = IsLoggedIn(request)
        if user:
            self.assertEquals(response.status_code, 302)
        else:
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'signin.html')


    
    def test_patientsignup(self):
        
        response = self.client.get(self.signup_url)
        request = response.wsgi_request
        user = IsLoggedIn(request)
        if user:
            self.assertEquals(response.status_code, 302)
        else:
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'signup.html')


    def test_registerPatient_GET(self):

        response = self.client.get(self.registerpatient_url)
        self.assertEquals(response.status_code, 302)
        
    def test_registerPatient_POST(self):

        

        response = self.client.post(self.registerpatient_url, {
            'name' : 'XYZ',
            'username' : 'yzx',
            'roll' : '111111',
            'email' : 'lorem@ipsum.com',
            'designation' : 'student',
            'department' : 'FF',
            'password' : MAKE_PASSWORD('pass')
        })
        

        self.assertEquals(response.status_code, 302)

    def test_loginUser_GET(self):

        response = self.client.get(self.loginUser_url)
        self.assertEquals(response.status_code, 302)

    def test_loginUser_POST(self):

        response = self.client.post(self.loginUser_url, {
            'username' : 'XYZ',
            'password' : 'pass'
        })

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.signup_url)

    def test_logout(self):

        response = self.client.get(self.logout_url)
        self.assertEquals(response.status_code, 302)

    
    

        






    
    

    
        
        






            



