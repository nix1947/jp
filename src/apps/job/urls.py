from django.urls import path

from .views import job_detail, JobSearchView, job_by_category, job_by_industry, apply_job, bookmark_job


app_name = 'job'
urlpatterns = [
    path('<slug:title>/', job_detail, name="job-detail"),
    path('search/', JobSearchView.as_view(), name="search"),
    path('category/<str:title>', job_by_category, name="job-by-category"),
    path('industry/<str:title>/', job_by_industry, name="job-by-industry"),

    # Job apply
    path('apply/now', apply_job, name="job-apply"),
    path('save/job', bookmark_job, name="job-bookmark"),


]
