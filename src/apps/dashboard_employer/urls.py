from django.urls import path 

from .views import dashboard, JobCreateView, JobListView, JobUpdateView, JobDeleteView


app_name ="dashboard_employer"
urlpatterns = [
    path('', dashboard, name="dashboard" ),
    path('job/create/', JobCreateView.as_view(), name="job-create"),
    path('job/posted/', JobListView.as_view(), name="job-list"),
    path('job/edit/<int:pk>/', JobUpdateView.as_view(), name="job-update"),
    path('job/delete/<int:pk>/', JobDeleteView.as_view(), name="job-delete")

]