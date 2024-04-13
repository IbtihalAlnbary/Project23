from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import RequestFactory
from myApp.models import AddReport, AssignedReport, Workerlogin, managermessagecitizen, managermessageworker
from django.test import TestCase, Client
from django.urls import reverse
from .models import AddReport
from django.contrib.auth.models import User

class TestHomeView(TestCase):

    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        response = self.client.get(reverse('home'))  # Updated reverse name
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mytown/home.html')


class TestWorkerLogin(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_worker_login(self):
        response = self.client.post(reverse('workerlogin'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)  # Redirects after successful login

class TestAddReportsView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_add_reports_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('addreports'), {'title': 'Test Title', 'neighborhood': 'Test Neighborhood', 'facility': 'Test Facility', 'description': 'Test Description', 'location': 'Test Location'})
        self.assertEqual(response.status_code, 302)  # Redirects after successful form submission
        self.assertTrue(AddReport.objects.exists())  # Checks if the report was created

class TestReportsListView(TestCase):

    def setUp(self):
        self.client = Client()

    def test_reports_list_view(self):
        response = self.client.get(reverse('reports_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mytown/reportslist.html')

class TestCitizenReportsView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_citizen_reports_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('citezinreports'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mytown/citizenreports.html')

class TestManagerReportsView(TestCase):

    def setUp(self):
        self.client = Client()

    def test_manager_reports_view(self):
        response = self.client.get(reverse('managerreports'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mytown/managerlist.html')



class TestDeleteReportView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.report = AddReport.objects.create(
            title='Test Title',
            neighborhood='Test Neighborhood',
            facility='Test Facility',
            description='Test Description',
            location='Test Location',
            user=self.user
        )

    def test_delete_report(self):
        initial_count = AddReport.objects.count()
        response = self.client.post(reverse('delete', kwargs={'id': self.report.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(AddReport.objects.count(), initial_count - 1)
        with self.assertRaises(AddReport.DoesNotExist):
            AddReport.objects.get(pk=self.report.pk)


class TestUpdateReportView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.report = AddReport.objects.create(
            title='Original Title',
            neighborhood='Original Neighborhood',
            facility='Original Facility',
            description='Original Description',
            location='Original Location',
            user=self.user
        )

    def test_update_report(self):
        new_title = 'Updated Title'
        new_neighborhood = 'Updated Neighborhood'
        new_facility = 'Updated Facility'
        new_description = 'Updated Description'
        new_location = 'Updated Location'

        # Send a POST request to update the report
        response = self.client.post(reverse('updatereport', kwargs={'id': self.report.pk}), {
            'title': new_title,
            'neighborhood': new_neighborhood,
            'facility': new_facility,
            'description': new_description,
            'location': new_location
        })

        # Check if the response status code is a redirect
        self.assertEqual(response.status_code, 200)

        # Refresh the report from the database
        updated_report = AddReport.objects.get(pk=self.report.pk)

        # Check if the report fields have been updated
        self.assertEqual(updated_report.title, new_title)
        self.assertEqual(updated_report.neighborhood, new_neighborhood)
        self.assertEqual(updated_report.facility, new_facility)
        self.assertEqual(updated_report.description, new_description)
        self.assertEqual(updated_report.location, new_location)

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
