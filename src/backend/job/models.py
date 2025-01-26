from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


# Any class created like "Job", it inherites from the "models" library to get the following features:
'''
 django model give your class : 
    - html widget: it applies htlm widget at the default admin page for any field created like text boxes, choices field, or others
    - validation: you request specific field regulations like max_lenght, model checks for that
    - db size: apply the required field size in db
'''

# passed to the choices parameter at one of the table columns
JOB_TYPE = (
    ('Full Time','Full Time'),
    ('Part Time','Part Time'),
)

def image_upload(instance,filename):
    imagename , extension = filename.split(".")
    return "jobs/%s.%s"%(instance.id,extension)



class Job(models.Model):  # table == Model
    owner = models.ForeignKey(User, related_name='job_owner', on_delete=models.CASCADE) # column == field record
    title = models.CharField(max_length=100)  # column
    # location 
    job_type = models.CharField(max_length=15 , choices=JOB_TYPE)
    description = models.TextField(max_length=1000)
    published_at = models.DateTimeField(auto_now=True)
    Vacancy = models.IntegerField(default=1)
    salary = models.IntegerField(default=0)
    experience = models.IntegerField(default=1) 
    category = models.ForeignKey('Category',on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload)
    # slug field would be identical to the title, it is used in url instead of id
    slug = models.SlugField(blank=True, null=True)

    # slug
    '''
        - Once you finishd creating Job in the admin page, you hit save
        - before you hit save, i need to reformat the "job title" to be like a slug "one shot"
        - ex: Python developer needed ---->>  python-developer-needed
        - Outcomes:
            - use this slug to fetch db to get the job details instead of using id number: 
            - ex --> site:8000/jobs/1   ====>>   site:8000/jobs/python-developer-needed
            
    '''

    # save
    '''
        - when you hit save, the following save function will apply the "slug" field format automatically 
        - class "Job" that inherites from "models" already has a builtin method clalled "save" to manage the save process
        - in the following save method, you actually override the current method, you call the base save from the class
        - before that, make the "slugifying process" which reformats the "title" and add it to the "slug" field
    '''
    def save(self,*args, **kwargs):
        self.slug = slugify(self.title) # add slug field equal to the job titile before saving the job details
        super(Job,self).save(*args, **kwargs)      # call base "save" method 

    # in the admin page, when i create job mnually, it displayes the created job with name called "job object <number>"
    # i need to return the actual job title when i create object from the class "job" so that job appears with thier name
    def __str__(self):
        return self.title



class Category(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name




class Apply(models.Model):
    job = models.ForeignKey(Job, related_name='apply_job', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    webiste = models.URLField()
    cv = models.FileField(upload_to='apply/')
    cover_letter = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name