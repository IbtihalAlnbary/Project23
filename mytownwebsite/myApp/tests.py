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