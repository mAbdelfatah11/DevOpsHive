## in models test, we assume that there is no available db, so each test case generates its required object data

from django.test import TestCase
from django.template.defaultfilters import slugify
from job.models import Job, Category
from django.contrib.auth.models import User

class ModelsTestCase(TestCase):
    def setUp(self):
        # Create a user for the job owner
        # User: predefined builtin module imported through django.contrib.auth.models
        # user: property used at Job model as a forign key so need to be created before creating job instance
        self.user = User.objects.create(username="testuser", password="password123")
        
        # Create a category
        # Category: model, need to be created as it is used as a forign key in job model
        self.category = Category.objects.create(name="Development")
        
        # Create a job instance
        self.job = Job.objects.create(
            owner=self.user,            # above created user
            title="Django Developer",
            job_type="Full Time",
            description="Looking for an experienced Django Developer.",
            Vacancy=2,
            salary=5000,
            experience=3,
            category=self.category,  # Provide the created category
        )

    def test_jobs_list_loads_properly(self):
        response = self.client.get(f'/jobs/{self.job.slug}')  # Use the correct slug in the URL
        self.assertEqual(response.status_code, 200)  # Check if the page loads correctly

    def test_job_has_slug(self):
        """Jobs are given slugs correctly when saving"""
        job = Job.objects.create(
            owner=self.user,
            title="My First Job",
            job_type="Part Time",
            description="Looking for a part-time developer.",
            Vacancy=1,
            salary=2000,
            experience=1,
            category=self.category,
        )
        job.save()          # when you hit save button at the admin page in the ui, it should save the title to the slug property after being slugified "like-this"
        self.assertEqual(job.slug, slugify(job.title))  # Validate slug is generated correctly
        # title = "My First Job
        # slugify(job.title) = my-first-job
        # job.slug = my-first-job
