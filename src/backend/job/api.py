## views 

from .models import Job
from .serializers import JobSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics


## Function based views
@api_view(['GET'])
def job_list_api(request):
    all_jobs = Job.objects.all()
    data = JobSerializer(all_jobs, many=True).data
    return Response({'data':data})


@api_view(['GET'])
def job_detail_api(request,id):
    job_detail = Job.objects.get(id=id)
    data = JobSerializer(job_detail).data
    return Response({'data':data})


## class based views (give more features in less code implementation)
## ex: using the class "ListCreateAPIView", you can list "get" or Create "post" at the same time, feature of class bases views
class JobListApi(generics.ListCreateAPIView):
    queryset = Job.objects.all()        # queryset is a method in the class "generics.ListCreateAPIView" so it is name restrictive
    serializer_class = JobSerializer


class JobDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobSerializer
    queryset = Job.objects.all()
    lookup_field = 'id'