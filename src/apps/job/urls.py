from django.urls import path 

from .views import job_detail, JobSearchView


app_name = 'job'
urlpatterns = [
    path('<slug:title>/', job_detail, name="job-detail"),
    path('search/', JobSearchView.as_view(), name="search"),
]