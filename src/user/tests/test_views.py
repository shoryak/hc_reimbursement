
from django.test import TestCase, Client
from django.urls import reverse
from grpc import StatusCode 
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
        self.form_url = reverse('form')
        self.form_submit_url = reverse('formsubmit')
        self.patient_dashboard_display_url = reverse('patient_dashboard_display')
        self.hcadmin_dashboard_display_url = reverse('hcadmin_dashboard_display')
        self.doctor_dashboard_display_url = reverse('doctor_dashboard_display')
        self.accounts_dashboard_display_url = reverse('accounts_dashboard_display')
        self.acceptForDoctorApproval_url = reverse('acceptForDoctorApproval')
        self.acceptFormByHC_url = reverse('acceptFormByHC')
        self.rejectFormByHC_url = reverse('rejectFormByHC')
        self.acceptByDoctor_url = reverse('acceptByDoctor')
        self.rejectByDoctor_url = reverse('rejectByDoctor')
        self.acceptByAccounts_url = reverse('acceptByAccounts')
        self.rejectByAccounts_url = reverse('rejectByAccounts')
        self.adminsignup_url = reverse('adminsignup')
        self.register_any_user_url = reverse('register_any_user')
        self.patient_profile_url = reverse('patient_profile')
        self.update_patient_profile_url = reverse('update_patient_profile')
        self.doctor_profile_url = reverse('doctor_profile')
        self.update_doctor_profile_url = reverse('update_doctor_profile')
        self.hcadmin_profile_url = reverse('hcadmin_profile')
        self.update_hcadmin_profile_url = reverse('update_hcadmin_profile')
        self.accounts_profile_url = reverse('accounts_profile')
        self.update_accounts_profile_url = reverse('update_accounts_profile')
        self.med_and_test_url = reverse('med_and_test')
        self.add_medicine_url = reverse('add_medicine')
        self.add_test_url = reverse('add_test')



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
    
    def test_logout_del(self):

        response = self.client.get(self.logout_url)
        request = response.wsgi_request
        self.client.delete(self.logout_url)

    def test_form(self):

        response = self.client.get(self.form_url)
        request = response.wsgi_request
        user = IsLoggedIn(request)
        if user is None:
            self.assertEquals(response.status_code, 302)
        elif user.roles != "patient":
            self.assertEquals(response.status_code, 302)
        else:
            self.assertEquals(response.status_code, 200)

    def test_submitForm_get(self):

        response = self.client.get(self.form_submit_url)
        request = response.wsgi_request
        user = IsLoggedIn(request)
        if user is None:
            self.assertEquals(response.status_code, 302)
        elif user.roles != "patient":
            self.assertEquals(response.status_code, 302)
        else:
            self.assertEquals(response.status_code, 200) 

    def test_submitForm_POST(self):

        response = self.client.post(self.form_submit_url, {

            'patient' : 'XYZ',
            'patient_name' : 'yzx',
            'relationship' : 'nice',
            'consultation_date' : '123455',
            'designation' : 'student',
            'department' : 'FF',
            'password' : MAKE_PASSWORD('pass')

        })
        self.assertEquals(response.status_code, 302)

    def test_doctor_dashboard_display(self):

        response = self.client.get(self.doctor_dashboard_display_url)
        request = response.wsgi_request
        user = IsLoggedIn(request)
        if user is None:
            self.assertEquals(response.status_code, 302)
        elif user.roles != "doctor":
            self.assertEquals(response.status_code, 302)
        else:
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed("doctor_dashboard.html")

    def test_patient_dashboard_display(self):

        response = self.client.get(self.patient_dashboard_display_url)
        request = response.wsgi_request
        user = IsLoggedIn(request)
        if user is None:
            self.assertEquals(response.status_code, 302)
        elif user.roles != "patient":
            self.assertEquals(response.status_code, 302)
        else:
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed("patient_dashboard.html")

    def test_hcadmin_dashboard_display(self):

        response = self.client.get(self.hcadmin_dashboard_display_url)
        request = response.wsgi_request
        user = IsLoggedIn(request)
        if user is None:
            self.assertEquals(response.status_code, 302)
        elif user.roles != "hcadmin":
            self.assertEquals(response.status_code, 302)
        else:
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed("hcadmin_dashboard.html")

    def test_accounts_dashboard_display(self):

        response = self.client.get(self.accounts_dashboard_display_url)
        request = response.wsgi_request
        user = IsLoggedIn(request)
        if user is None:
            self.assertEquals(response.status_code, 302)
        elif user.roles != "accounts":
            self.assertEquals(response.status_code, 302)
        else:
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed("accounts_dashboard.html")


    def test_acceptForDoctorApproval_Get(self):

        response = self.client.get(self.acceptForDoctorApproval_url)
        request = response.wsgi_request
        user = IsLoggedIn(request)
        self.assertEquals(response.status_code, 302)

    def test_acceptForDoctorApproval_Post(self):

        response = self.client.post(self.acceptForDoctorApproval_url, {

            'status' : 'XYZ',
            'feedback' : 'yzx',

        })
        self.assertEquals(response.status_code, 302)


    def test_acceptFormByHC_Get(self):

        response = self.client.get(self.acceptFormByHC_url)
        request = response.wsgi_request
        user = IsLoggedIn(request)
        self.assertEquals(response.status_code, 302)

    def test_acceptFormByHC_Post(self):

        response = self.client.post(self.acceptFormByHC_url, {

            'status' : 'XYZ',
            'feedback' : 'yzx',

        })
        self.assertEquals(response.status_code, 302)

    def test_rejectFormByHC_Get(self):

        response = self.client.get(self.rejectFormByHC_url)
        request = response.wsgi_request
        user = IsLoggedIn(request)
        self.assertEquals(response.status_code, 302)

    def test_rejectFormByHC_Post(self):

        response = self.client.post(self.rejectFormByHC_url, {

            'status' : 'XYZ',
            'feedback' : 'yzx',

        })
        self.assertEquals(response.status_code, 302)

    def test_acceptByDoctor_Get(self):

        response = self.client.get(self.acceptByDoctor_url)
        request = response.wsgi_request
        user = IsLoggedIn(request)
        self.assertEquals(response.status_code, 302)

    def test_acceptByDoctor_Post(self):

        response = self.client.post(self.acceptByDoctor_url, {

            'status' : 'XYZ',
            'feedback' : 'yzx',

        })
        self.assertEquals(response.status_code, 302)

    def test_acceptByAccounts_Get(self):

        response = self.client.get(self.acceptByAccounts_url)
        request = response.wsgi_request
        user = IsLoggedIn(request)
        self.assertEquals(response.status_code, 302)

    def test_acceptByAccounts_Post(self):

        response = self.client.post(self.acceptByAccounts_url, {

            'status' : 'XYZ',
            'feedback' : 'yzx',

        })
        self.assertEquals(response.status_code, 302)

    def test_adminsignup(self):

        response = self.client.get(self.adminsignup_url)
        request = response.wsgi_request
        user = IsLoggedIn(request)

        if user is None:
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'signup.html')

        elif user.roles == "hcadmin":
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'signup_admin.html')
        
        else:
            self.assertEquals(response.status_code, 302)

    def test_register_any_user_Get(self):

        response = self.client.get(self.register_any_user_url)
        self.assertEquals(response.status_code, 302)

    def test_register_any_user_Post(self):

        response = self.client.post(self.register_any_user_url, {

            'name' : 'XYZ',
            'username' : 'yzx',
            'roll' : '222222',
            'email' : 'lorem@ipsum.com',
            'designation' : 'student',
            'department': 'cse',
            'password1' : 'lorem',
            'password2' : 'ipsum'

        })

        self.assertEquals(response.status_code, 302)

    def test_patient_profile(self):
        
        response = self.client.get(self.patient_profile_url)
        request = response.wsgi_request
        user = IsLoggedIn(request)

        if user is None:
            self.assertEquals(response.status_code, 302)
        
        elif user.roles == "patient":
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, "patient_profile.html")
        else:
            self.assertEquals(response.status_code, 302)

    def test_update_patient_profile_Get(self):

        response = self.client.get(self.update_patient_profile_url)
        self.assertEquals(response.status_code, 302)

    def test_update_patient_profile_Post(self):

        response = self.client.post(self.update_patient_profile_url, {
            
            'username' : 'yzx',
            'contact' : '222222',
            'address' : 'lorem@ipsum.com',
            'bank_name' : 'student',
            'bank_IFSC': 'cse',
            'bank_AC' : 'lorem',
            
        })
        self.assertEquals(response.status_code, 302)
        

    def test_doctor_profile(self):

        response = self.client.get(self.doctor_profile_url)
        request = response.wsgi_request
        user = IsLoggedIn(request)

        if user is None:
            self.assertEquals(response.status_code, 302)
            

        elif user.roles == "doctor":
            self.assertEquals(response.status_code, 302)
            
        else:
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'doctor_profile.html')

    
    def test_update_doctor_profile_Get(self):

        response = self.client.get(self.update_doctor_profile_url)
        self.assertEquals(response.status_code, 302)

    def test_update_doctor_profile_Post(self):

        response = self.client.post(self.update_doctor_profile_url, {
            
            'username' : 'yzx',
            'contact' : '222222',
            'address' : 'lorem@ipsum.com',
            'specialization' : 'heart',
            
        })
        self.assertEquals(response.status_code, 302)

    def test_hcadmin_profile(self):
        response = self.client.get(self.hcadmin_profile_url)
        request = response.wsgi_request
        user = IsLoggedIn(request)

        if user is None:
            self.assertEquals(response.status_code, 302)
            

        elif user.roles == "hcadmin":
            self.assertEquals(response.status_code, 302)
            
        else:
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'hcadmin_profile.html')
    
    def test_update_hcadmin_profile_Get(self):

        response = self.client.get(self.update_hcadmin_profile_url)
        self.assertEquals(response.status_code, 302)

    def test_update_hdadmin_profile_Post(self):

        response = self.client.post(self.update_hcadmin_profile_url, {
            
            'contact' : '222222',
            'address' : 'lorem@ipsum.com',
            
        })
        self.assertEquals(response.status_code, 302)


    def test_accounts_profile(self):
        response = self.client.get(self.accounts_profile_url)
        request = response.wsgi_request
        user = IsLoggedIn(request)

        if user is None:
            self.assertEquals(response.status_code, 302)
            

        elif user.roles != "accounts":
            self.assertEquals(response.status_code, 302)
            
        else:
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'accounts_profile.html')
    
    def test_update_accounts_profile_Get(self):

        response = self.client.get(self.update_accounts_profile_url)
        self.assertEquals(response.status_code, 302)

    def test_update_accounts_profile_Post(self):

        response = self.client.post(self.update_accounts_profile_url, {
            
            'username' : 'lorem',
            'contact' : '222222',
            'address' : 'lorem@ipsum.com',
            
        })
        self.assertEquals(response.status_code, 302)

    
    def test_med_and_test(self):

        response = self.client.get(self.med_and_test_url)
        request = response.wsgi_request
        user = IsLoggedIn(request)

        if user is None:
            self.assertEquals(response.status_code, 302)
            

        elif user.roles != "hcadmin":
            self.assertEquals(response.status_code, 302)
            
        else:
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'med_and_test.html')

    def test_add_medicine_Get(self):

        response = self.client.get(self.add_medicine_url)
        self.assertEquals(response.status_code, 302)

    def test_add_medicine_Post(self):

        response = self.client.post(self.add_medicine_url, {
            
            'medicine_name' : 'lorem',
            'brand' : '222222',
            'price' : 'lorem@ipsum.com',
            
        })
        self.assertEquals(response.status_code, 302)


    def test_add_test_Get(self):

        response = self.client.get(self.add_test_url)
        self.assertEquals(response.status_code, 302)

    def test_add_test_Post(self):

        response = self.client.post(self.add_test_url, {
            
            'test_name' : 'lorem',
              
        })
        self.assertEquals(response.status_code, 302)

        



    
            









    
    








    


    




    
        

            




    

    



            
        







    
            

    
        
        

    
    

        






    
    

    
        
        






            



