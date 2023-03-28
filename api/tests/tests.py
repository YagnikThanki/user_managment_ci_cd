from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient,APITestCase
from django.urls import reverse
from api.models import CustomUser
from rest_framework.authtoken.models import Token


class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'first_name':'robert',
            'last_name':'segall',
            'email':'shivamdube0718@gmail.com',
            'username':'robert789',
            'password':'robert789'
            }
        self.register_url = reverse('register')
    
    def test_valid_user_registration(self):
        response = self.client.post(self.register_url,self.user_data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_duplicate_user_registration(self):
        CustomUser.objects.create_user(**self.user_data)
        response = self.client.post(self.register_url,self.user_data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_null_data(self):
        response =self.client.post(self.register_url)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username=' ', email='luckyshah0718@gmail.com', password='Dipesh789')
        self.url = reverse('login')

    def test_login(self):
        data = {'email': 'luckyshah0718@gmail.com', 'password': 'Dipesh789'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_user_login(self):
        data = {'email': 'tes1@gmail.com', 'password': 'Dipesh789'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_null_data(self):
        response =self.client.post(self.url)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)


class LogoutTestCase(TestCase): 
    def setUp(self):
        self.user = CustomUser.objects.create_user(username=' ',email='luckyshah0718@gmail.com', password='Dipesh789')
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        self.logout_url = reverse('logout')

    def api_authentication(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_logout(self):
        response = self.client.delete(self.logout_url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)



class ChangePasswordTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username=' ',email='luckyshah0718@gmail.com', password='Dipesh789')
        self.token = Token.objects.create(user=self.user)
        self.change_password_api_authentication()
        self.change_password_url = reverse('change_password')

    def change_password_api_authentication(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)

    # done change password 
    def test_change_password(self):
        data = {'password':'Dipesh789','new_password':'yug99999','conf_password':'yug99999'}
        response = self.client.patch(self.change_password_url, data,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # wrong old password 
    def test_wrong_register_password(self):
        data = {'password':'Dipesh123','new_password':'yug99999','conf_password':'yug99999'}
        response = self.client.patch(self.change_password_url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    # old password and new password those are same
    def test_password_equal_newpassword(self):
        data = {'password':'Dipesh789','new_password':'Dipesh789','conf_password':'yug99999'}
        response = self.client.patch(self.change_password_url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    # new password and conform password 
    def test_newpassword_notequal_confpassword(self):
        data = {'password':'Dipesh789','new_password':'yug88888','conf_password':'yug99999'}
        response = self.client.patch(self.change_password_url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_null_data(self):
        response =self.client.patch(self.change_password_url)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)    

class SendotpTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username=' ',email='luckyshah0718@gmail.com',password='Dipesh789')
        self.token = Token.objects.create(user=self.user)
        self.send_otp_api_authentication()
        self.send_otp_url = reverse('send_otp')

    def send_otp_api_authentication(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)
    
    def test_send_otp(self):
        data = {'email':'luckyshah0718@gmail.com'}
        response = self.client.post(self.send_otp_url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_wrong_email_send_otp(self):
        data = {'email':'example@email.com'}
        response = self.client.post(self.send_otp_url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_null_data(self):
        response =self.client.post(self.send_otp_url)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)


class ConfirmationotpTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username=' ',email='luckyshah0718@gmail.com',password='Dipesh789')
        user = CustomUser.objects.get(email=self.user)
        user.otp = '123456'
        user.save()
        self.token = Token.objects.create(user=self.user)
        self.confirm_otp_api_authentication()
        self.confirm_otp_url = reverse('confirmation_otp')
    
    def confirm_otp_api_authentication(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)
    
    def test_valid_otp_confirmation(self):
        data = {'email':'luckyshah0718@gmail.com','otp':'123456'}
        response = self.client.post(self.confirm_otp_url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_invalid_otp_confirmation(self):
        data = {'email':'luckyshah0718@gmail.com','otp':'789456'}
        response = self.client.post(self.confirm_otp_url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)


    def test_valid_email(self):
        data = {'email':'example@gmail.com','otp':'123456'}
        response = self.client.post(self.confirm_otp_url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_null_data(self):
        response =self.client.post(self.confirm_otp_url)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)


class ForgotpasswordTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username=' ',email='luckyshah0718@gmail.com',password='Dipesh789')
        self.token = Token.objects.create(user=self.user)
        self.forgotpassword_api_authentication()
        self.forgotpassword_url = reverse('forgot_password')

    def forgotpassword_api_authentication(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)

    def test_forgot_password(self):
        data = {'email':'luckyshah0718@gmail.com','new_password':'example789'}
        response = self.client.post(self.forgotpassword_url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_valid_email(self):
        data = {'email':'example@email.com','new_password':'example789'}
        response = self.client.post(self.forgotpassword_url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_null_data(self):
        response = self.client.post(self.forgotpassword_url)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)