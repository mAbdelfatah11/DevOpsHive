from django.urls import include, path

from . import views
from . import api 


app_name='job'

urlpatterns = [
    path('',views.job_list , name='job_list'),  # nothing after the base "jobs/" will return the job_list function ,,,,
    path('add',views.add_job , name='add_job'), #  name: it is a refernce to the url path to be used in the current app locations like html templates, instead of using / , u use /job_details inside code 
    path('<str:slug>',views.job_detail , name='job_detail'),   # use slug field name to refer to each job instaed of the id (more to know at models.py)

    ## apis
    path('api/jobs',api.job_list_api , name='job_list_api'),
    path('api/jobs/<int:id>',api.job_detail_api , name='job_detail_api'),


    ## class based views
    path('api/v2/jobs',api.JobListApi.as_view() , name='job_list_api'),
    path('api/v2/jobs/<int:id>',api.JobDetail.as_view() , name='job_detail_api'),
]