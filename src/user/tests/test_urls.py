import imp
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from user.views import * #login,patientsignup,registerPatient
class TestUrls(SimpleTestCase):


    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, login)
    
    def test_signup_url_is_resolved(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func, patientsignup)
    
    def test_registerPatient_is_resolved(self):
        url = reverse('registerPatient')
        self.assertEquals(resolve(url).func,registerPatient )
    
    def test_loginUser_is_resolved(self):
        url = reverse('loginUser')
        self.assertEquals(resolve(url).func,loginUser)
    
    def test_logout_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logout)
    
    def test_patient_dashboard_display_is_resolved(self):
        url = reverse('patient_dashboard_display')
        self.assertEquals(resolve(url).func,patient_dashboard_display)

    def test_doctor_dashboard_display_is_resolved(self):
        url = reverse('doctor_dashboard_display')
        self.assertEquals(resolve(url).func,doctor_dashboard_display)

    def test_hcadmin_dashboard_display_is_resolved(self):
        url = reverse('hcadmin_dashboard_display')
        self.assertEquals(resolve(url).func,hcadmin_dashboard_display)
    
    def test_accounts_dashboard_display_is_resolved(self):
        url = reverse('accounts_dashboard_display')
        self.assertEquals(resolve(url).func,accounts_dashboard_display)
    
    def test_form_is_resolved(self):
        url = reverse('form')
        self.assertEquals(resolve(url).func,form)
    
    def test_formsubmit_is_resolved(self):
        url = reverse('formsubmit')
        self.assertEquals(resolve(url).func,submitForm)

    def test_acceptForDoctorApproval_is_resolved(self):
        url = reverse('acceptForDoctorApproval')
        self.assertEquals(resolve(url).func,acceptForDoctorApproval)

    def test_acceptFormByHC_is_resolved(self):
        url = reverse('acceptFormByHC')
        print(resolve(url))
        self.assertEquals(resolve(url).func,acceptFormByHC)
    
    def test_rejectFormByHC_is_resolved(self):
        url = reverse('rejectFormByHC')
        self.assertEquals(resolve(url).func,rejectFormByHC)
    
    def test_acceptByDoctor_is_resolved(self):
        url = reverse('acceptByDoctor')
        self.assertEquals(resolve(url).func,acceptByDoctor)

    def test_rejectByDoctor_is_resolved(self):
        url = reverse('rejectByDoctor')
        self.assertEquals(resolve(url).func,rejectByDoctor)

    def test_acceptByAccounts_is_resolved(self):
        url = reverse('acceptByAccounts')
        self.assertEquals(resolve(url).func,acceptByAccounts)
    
    def test_adminsignup_is_resolved(self):
        url = reverse('adminsignup')
        self.assertEquals(resolve(url).func,adminsignup)

    def test_register_any_user_is_resolved(self):
        url = reverse('register_any_user')
        self.assertEquals(resolve(url).func,register_any_user)

    
    def test_patient_profile_is_resolved(self):
        url = reverse('patient_profile')
        self.assertEquals(resolve(url).func,patient_profile)
    

    def test_update_patient_profile_is_resolved(self):
        url = reverse('update_patient_profile')
        self.assertEquals(resolve(url).func,update_patient_profile)
    

    def test_doctor_profile_is_resolved(self):
        url = reverse('doctor_profile')
        self.assertEquals(resolve(url).func,doctor_profile)
    
    def test_update_doctor_profile_is_resolved(self):
        url = reverse('update_doctor_profile')
        self.assertEquals(resolve(url).func,update_doctor_profile)

    
    def test_accounts_profile_is_resolved(self):
        url = reverse('accounts_profile')
        self.assertEquals(resolve(url).func,accounts_profile)

    
    def test_update_accounts_profile_is_resolved(self):
        url = reverse('update_accounts_profile')
        self.assertEquals(resolve(url).func,update_accounts_profile)

    
    def test_hcadmin_profile_is_resolved(self):
        url = reverse('hcadmin_profile')
        self.assertEquals(resolve(url).func,hcadmin_profile)

    
    def test_update_hcadmin_profile_is_resolved(self):
        url = reverse('update_hcadmin_profile')
        self.assertEquals(resolve(url).func,update_hcadmin_profile)
    



