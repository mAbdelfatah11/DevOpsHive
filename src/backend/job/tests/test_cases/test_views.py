
from django.test import TestCase
from django.urls import reverse
from job.models import Job, Category
from django.contrib.auth.models import User

class ApiViewTestCase(TestCase):  # Inherits from TestCase

    def setUp(self):
        '''
            # Set up necessary test data
            # Runs before each test case
            # Creates a test user, category, and job instance. These objects are used in all test cases.
            # This avoids duplicating setup code in individual test cases.
        '''
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.category = Category.objects.create(name="Development")
        self.job = Job.objects.create(
            owner=self.user,
            title="Django Developer",
            job_type="Full Time",
            description="Looking for an experienced Django Developer.",
            Vacancy=2,
            salary=5000,
            experience=3,
            category=self.category,
        )

    # url:8000/jobs view
    def test_job_list_view(self):
        """Test view for listing jobs"""
        response = self.client.get('/jobs/')                   
        self.assertEqual(response.status_code, 200)
        self.assertIn('Django Developer', response.content.decode())

    def test_job_list_api(self):
        """Test API rest for listing jobs"""
        response = self.client.get('/jobs/api/jobs')                # rest api: url:8000/jobs/api/jobs
        self.assertEqual(response.status_code, 200)
        self.assertIn('Django Developer', response.content.decode())

    def test_job_detail_api(self):
        """Test API endpoint for job detail with valid ID"""
        response = self.client.get(reverse('job:job_detail_api', kwargs={'id': self.job.id}))  # /jobs/api/jobs/<id> , it expects a value for 'id'
        self.assertEqual(response.status_code, 200)
        self.assertIn('Django Developer', response.content.decode())

    def test_job_detail_api_invalid_id(self):
        """Test API endpoint for job detail with invalid ID"""
        response = self.client.get(reverse('job:job_detail_api', kwargs={'id': 999}))           # /jobs/api/jobs/<id>
        self.assertEqual(response.status_code, 404)     # Expecting 404 for non-existing job


    def test_job_detail_api_v2(self):                                       # class based views
        """Test API v2 endpoint for job detail with valid ID"""
        response = self.client.get(reverse('job:job_detail_api', kwargs={'id': self.job.id}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Django Developer', response.content.decode())


