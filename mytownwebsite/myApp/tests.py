from django.test import TestCase
from .models import AddReport,AssignedReport,citezinreports,Workerlogin
from datetime import date
from .models import *

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib import messages
from django.shortcuts import redirect

from mytownwebsite.views import signup

class SignupTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_successful_signup(self):
        # Create a POST request with valid data
        request = self.factory.post('/signup/', {
            'username': 'testuser',
            'fname': 'Test',
            'lname': 'User',
            'email': 'test@example.com',
            'pass1': 'password123',
            'pass2': 'password123',
        })

        # Set up message storage
        setattr(request, '_messages', FallbackStorage(request))

        # Call the signup view function
        response = signup(request)

        # Verify that the user is redirected to the signin page
        self.assertEqual(response.url, '/signin/')

        # Verify that the user is created
        self.assertTrue(User.objects.filter(username='testuser').exists())

        # Verify success message is set
        messages.success.assert_called_once_with(request, "Your account has been successfully created!")

    def test_unsuccessful_signup_password_mismatch(self):
        # Create a POST request with mismatched passwords
        request = self.factory.post('/signup/', {
            'username': 'testuser',
            'fname': 'Test',
            'lname': 'User',
            'email': 'test@example.com',
            'pass1': 'password123',
            'pass2': 'password456',  # Mismatched password
        })

        # Set up message storage
        setattr(request, '_messages', FallbackStorage(request))

        # Call the signup view function
        response = signup(request)

        # Verify that the user is redirected back to the signup page
        self.assertEqual(response.url, '/signup/')

        # Verify that the user is not created
        self.assertFalse(User.objects.filter(username='testuser').exists())

        # Verify error message is set
        messages.error.assert_called_once_with(request, "Passwords do not match.")
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

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib import messages
from django.shortcuts import redirect

from mytownwebsite.views import signup

class SignupTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_successful_signup(self):
        # Create a POST request with valid data
        request = self.factory.post('/signup/', {
            'username': 'testuser',
            'fname': 'Test',
            'lname': 'User',
            'email': 'test@example.com',
            'pass1': 'password123',
            'pass2': 'password123',
        })

        # Set up message storage
        setattr(request, '_messages', FallbackStorage(request))

        # Call the signup view function
        response = signup(request)

        # Verify that the user is redirected to the signin page
        self.assertEqual(response.url, '/signin/')

        # Verify that the user is created
        self.assertTrue(User.objects.filter(username='testuser').exists())

        # Verify success message is set
        messages.success.assert_called_once_with(request, "Your account has been successfully created!")

    def test_unsuccessful_signup_password_mismatch(self):
        # Create a POST request with mismatched passwords
        request = self.factory.post('/signup/', {
            'username': 'testuser',
            'fname': 'Test',
            'lname': 'User',
            'email': 'test@example.com',
            'pass1': 'password123',
            'pass2': 'password456',  # Mismatched password
        })

        # Set up message storage
        setattr(request, '_messages', FallbackStorage(request))

        # Call the signup view function
        response = signup(request)

        # Verify that the user is redirected back to the signup page
        self.assertEqual(response.url, '/signup/')

        # Verify that the user is not created
        self.assertFalse(User.objects.filter(username='testuser').exists())

        # Verify error message is set
        messages.error.assert_called_once_with(request, "Passwords do not match.")













