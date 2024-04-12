from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import RequestFactory

from myApp.models import AddReport, AssignedReport, Workerlogin, managermessagecitizen, managermessageworker


class AddReportModelTest(TestCase):
    def setUp(self):
        AddReport.objects.create(
            title='Test Report',
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
            neighborhood='ASD',
            description='New description',
            location='New location'
        )
        saved_report = AddReport.objects.get(title='New Report')

        self.assertEqual(saved_report.title, 'New Report')
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
            reportnumber=1,
            choose=False,
            reports=self.report,
        )

    def test_reports_list_creation(self):
        self.assertEqual(self.reportslist.reportnumber, 1)
        self.assertFalse(self.reportslist.choose)
        self.assertEqual(self.reportslist.reports, self.report)


class WorkerLoginTestCase(TestCase):
    def setUp(self):
        self.worker = Workerlogin.objects.create(username="tom", password="123maisa")

    def test_worker_login_creation(self):
        self.assertEqual(self.worker.username, "tom")
        self.assertEqual(self.worker.password, "123maisa")


class SignUpTest(TestCase):
    def test_signup(self):
        data = {
            'username': 'testuser',
            'fname': 'Test',
            'lname': 'User',
            'email': 'test@example.com',
            'pass1': 'testpassword',
            'pass2': 'testpassword',
        }
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertRedirects(response, reverse('signin'))

        created_user = User.objects.get(username='testuser')
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.first_name, 'Test')
        self.assertEqual(created_user.last_name, 'User')
        self.assertEqual(created_user.email, 'test@example.com')
        created_user.delete()


class LogoutRequestTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_logout_request(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('logout'))
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertRedirects(response, reverse('home'))
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


class TestContactUsView(TestCase):
    def test_post_request(self):
        client = Client()
        response = client.post('/contactus/', {'name': 'John Doe', 'email': 'john@example.com', 'description': 'Test message'})
        self.assertEqual(response.status_code, 200)  # Assuming the view returns a success response

    def test_get_request(self):
        client = Client()
        response = client.get('/contactus/')
        self.assertEqual(response.status_code, 200)  # Assuming the view returns a success response


class ManagerMessageWorkerViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_request(self):
        request = self.factory.get(reverse('managermessageworker'))
        request.user = User.objects.create(username='testuser')
        response = managermessageworker(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mytown/managermessageworker.html')
        self.assertIn('form', response.context)

    def test_post_request(self):
        request = self.factory.post(reverse('managermessageworker'), data={'message_text': 'Test message'})
        request.user = User.objects.create(username='testuser')
        response = managermessageworker(request)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('managerHomePage'))  # Corrected redirect URL
        self.assertTrue(managermessageworker.objects.filter(message_text='Test message').exists())

class ManagerMessageCitizenModelTest(TestCase):
    def setUp(self):
        self.message = managermessagecitizen.objects.create(
            name='John Doe',
            worker_email='worker@example.com',
            message='Test message'
        )

    def test_string_representation(self):
        expected_string = f"Message to {self.message.name} - {self.message.worker_email}"
        self.assertEqual(str(self.message), expected_string)
