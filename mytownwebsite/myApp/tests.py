from django.test import TestCase
from .models import AddReport,AssignedReport,citezinreports,Workerlogin
from datetime import date
from .models import *

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib import messages
from django.shortcuts import redirect



class AddReportModelTest(TestCase):
    def setUp(self):
        AddReport.objects.create(
            title='Test Report',
            # email='test@example.com',
            neighborhood='BEER',
            description='Test description',
            location='Test location'
        )

    def test_report_str_method(self):
        report = AddReport.objects.get(title='Test Report')
        self.assertEqual(str(report), 'Test Report')

    def test_report_save_and_retrieve(self):
       
        AddReport.objects.create(
            title='New Report',
            # email='new@example.com',
            neighborhood='ASD',
            description='New description',
            location='New location'
        )
        
        saved_report = AddReport.objects.get(title='New Report')

        self.assertEqual(saved_report.title, 'New Report')
        # self.assertEqual(saved_report.email, 'new@example.com')
        self.assertEqual(saved_report.neighborhood, 'ASD')
        self.assertEqual(saved_report.description, 'New description')
        self.assertEqual(saved_report.location, 'New location')
 


class AddReportTestCase(TestCase):
    def setUp(self):
        self.report = AddReport.objects.create(
            title="Test Report",
             neighborhood="Beer Sheva",
            description="Test description",
            location="Test location",
        )

    def test_add_report_creation(self):
        self.assertEqual(self.report.title, "Test Report")
        self.assertEqual(self.report.neighborhood, "Beer Sheva")
        self.assertEqual(self.report.description, "Test description")
        self.assertEqual(self.report.location, "Test location")

class ReportsListTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.report = AddReport.objects.create(
            title="Test Report",
        neighborhood="Beer Sheva",
            description="Test description",
            location="Test location",
        )
        self.reportslist = AssignedReport.objects.create(
            # date=date.today(),
             reportnumber=1,
            choose=False,
            reports=self.report,
        )

    def test_reports_list_creation(self):
        # self.assertEqual(self.reportslist.date, date.today())
        self.assertEqual(self.reportslist. reportnumber, 1)
        self.assertFalse(self.reportslist.choose)
        self.assertEqual(self.reportslist.reports, self.report)

class WorkerLoginTestCase(TestCase):
    def setUp(self):
        self.worker = Workerlogin.objects.create(username="testworker", password="testpassword")

    def test_worker_login_creation(self):
        self.assertEqual(self.worker.username, "testworker")
        self.assertEqual(self.worker.password, "testpassword")

# from django.test import TestCase, RequestFactory
# from django.contrib.auth.models import User
# from django.contrib.messages.storage.fallback import FallbackStorage
# from django.contrib import messages
# from django.shortcuts import redirect

# from mytownwebsite.views import signup








from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import logout

from django.contrib.auth import authenticate, login


class SignUpTest(TestCase):
    
    def test_signup(self):
        # Prepare data for the test
        data = {
            'username': 'testuser',
            'fname': 'Test',
            'lname': 'User',
            'email': 'test@example.com',
            'pass1': 'testpassword',
            'pass2': 'testpassword',
        }

        # Send POST request to signup endpoint with test data
        response = self.client.post(reverse('signup'), data)

        # Check if the user was created successfully
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertRedirects(response, reverse('signin'))  # Check redirection to signin page

        # Check if the user exists in the database
        created_user = User.objects.get(username='testuser')
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.first_name, 'Test')
        self.assertEqual(created_user.last_name, 'User')
        self.assertEqual(created_user.email, 'test@example.com')

        # Clean up after the test
        created_user.delete()




  

class LogoutRequestTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.password = 'testpassword'
        
        # Create a test user
        self.user = User.objects.create_user(username=self.username, password=self.password)
    
    def test_logout_request(self):
        # Log in the test user
        self.client.login(username=self.username, password=self.password)
        
        # Make a request to the logout endpoint
        response = self.client.get(reverse('logout'))
        
        # Check if the user is logged out
        self.assertNotIn('_auth_user_id', self.client.session)
        
        # Check if the response redirects to the home page
        self.assertRedirects(response, reverse('home'))
        
        # Check if the "Logged out successfully!" message is displayed
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Logged out successfully!")





class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.signin_url = reverse('signin')
        self.manager_home_url = reverse('managerHomePage')
        self.home_client_url = reverse('HomeClient')
        self.manager_signin_url = reverse('managerSignIn')
        self.worker_home_url = reverse('workerHomePage')
        self.index_url = reverse('index')

    
    def test_signin_view(self):
        response = self.client.get(self.signin_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mytown/signin.html')

    def test_manager_home_view(self):
        response = self.client.get(self.manager_home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mytown/managerHomePage.html')

    def test_home_client_view(self):
        response = self.client.get(self.home_client_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mytown/HomeClient.html')

    def test_manager_signin_view(self):
        response = self.client.get(self.manager_signin_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mytown/managerSignIn.html')

    def test_worker_home_view(self):
        response = self.client.get(self.worker_home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mytown/workerHomePage.html')

    def test_index_view(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mytown/index.html')
