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



import unittest
from django.test import Client

class TestContactUsView(unittest.TestCase):
    
    def test_post_request(self):
        client = Client()
        response = client.post('/contactus/', {'name': 'John Doe', 'email': 'john@example.com', 'description': 'Test message'})
        self.assertEqual(response.status_code, 200)  # Assuming the view returns a success response

        # Add more assertions if necessary

    def test_get_request(self):
        client = Client()
        response = client.get('/contactus/')
        self.assertEqual(response.status_code, 200)  # Assuming the view returns a success response

        # Add more assertions if necessary

if __name__ == '__main__':
    unittest.main()


import unittest
from django.test import Client
from myapp.models import ManagerMessageCitizen  # אני מניח שיש לך מודל בשם ManagerMessageCitizen

class TestManagerMessageCitizenView(unittest.TestCase):
    
    def test_post_request(self):
        client = Client()
        response = client.post('/managermessagecitizen/', {'name': 'John Doe', 'message': 'Test message'})
        self.assertEqual(response.status_code, 200)  # Assuming the view returns a success response

        # Check if message is saved in the database
        self.assertTrue(ManagerMessageCitizen.objects.filter(name='John Doe', message='Test message').exists())

    def test_get_request(self):
        client = Client()
        response = client.get('/managermessagecitizen/')
        self.assertEqual(response.status_code, 200)  # Assuming the view returns a success response

        # Add more assertions if necessary

if __name__ == '__main__':
    unittest.main()


import unittest
from django.test import Client
from mytownwebsite.models import WorkerMessageManager  # אני מניח שיש לך מודל בשם WorkerMessageManager

class TestWorkerMessageManagerView(unittest.TestCase):
    
    def test_post_request(self):
        client = Client()
        response = client.post('/workermessagemanager/', {'name': 'John Doe', 'message': 'Test message'})
        self.assertEqual(response.status_code, 200)  # Assuming the view returns a success response

        # Check if message is saved in the database
        self.assertTrue(WorkerMessageManager.objects.filter(name='John Doe', message='Test message').exists())

    def test_get_request(self):
        client = Client()
        response = client.get('/workermessagemanager/')
        self.assertEqual(response.status_code, 200)  # Assuming the view returns a success response

        # Add more assertions if necessary

if __name__ == '__main__':
    unittest.main()



import unittest
from django.test import Client
from mytownwebsite.models import WorkerMessageCitizen  # אני מניח שיש לך מודל בשם WorkerMessageCitizen

class TestWorkerMessageCitizenView(unittest.TestCase):
    
    def test_post_request(self):
        client = Client()
        response = client.post('/workermessagecitizen/', {'name': 'John Doe', 'message': 'Test message'})
        self.assertEqual(response.status_code, 200)  # Assuming the view returns a success response

        # Check if message is saved in the database
        self.assertTrue(WorkerMessageCitizen.objects.filter(name='John Doe', message='Test message').exists())

    def test_get_request(self):
        client = Client()
        response = client.get('/workermessagecitizen/')
        self.assertEqual(response.status_code, 200)  # Assuming the view returns a success response

        # Add more assertions if necessary

if __name__ == '__main__':
    unittest.main()

import unittest
from django.test import Client
from django.urls import reverse
from mytownwebsite.models import Worker  # אני מניח שיש לך מודל בשם Worker

class TestDeleteWorkerView(unittest.TestCase):

    def test_post_request(self):
        # Create a test worker
        test_worker = Worker.objects.create(name='Test Worker', id=12345)

        # Create a client
        client = Client()

        # Prepare data for POST request
        data = {
            'workerName': 'Test Worker',
            'workerID': 12345,
            'reason': 'Test reason for deletion'
        }

        # Send POST request to delete worker
        response = client.post(reverse('delete_worker'), data)

        # Check if worker is deleted from the database
        self.assertFalse(Worker.objects.filter(name='Test Worker', id=12345).exists())

        # Check if response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if response contains success message
        self.assertIn(b'Worker Deleted Successfully', response.content)

    def test_get_request(self):
        # Create a client
        client = Client()

        # Send GET request to delete worker page
        response = client.get(reverse('delete_worker'))

        # Check if response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Add more assertions if necessary

if __name__ == '__main__':
    unittest.main()
from django.test import TestCase, Client
from django.urls import reverse

class FinishJobTestCase(TestCase):
    def test_post_request(self):
        client = Client()
        # Prepare data for POST request
        data = {
            'workPlace': 'Office',
            'workDuration': '8 hours',
            'additionalNotes': 'Completed tasks A, B, and C.'
        }
        # Send POST request
        response = client.post(reverse('finish_job'), data)
        # Check if the response is successful (status code 200)
        self.assertEqual(response.status_code, 200)
        # Check if the response contains the success message
        self.assertIn(b'Job Finished Successfully', response.content)

    def test_get_request(self):
        client = Client()
        # Send GET request
        response = client.get(reverse('finish_job'))
        # Check if the response is successful (status code 200)
        self.assertEqual(response.status_code, 200)
        # Add more assertions if necessary
