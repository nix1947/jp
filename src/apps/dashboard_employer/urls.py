from django.urls import path

from .views import dashboard, JobCreateView, JobListView, JobUpdateView, JobDeleteView, JobTemplateView


app_name = "dashboard_employer"
urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('job/create/', JobCreateView.as_view(), name="job-create"),
    path('job/posted/', JobListView.as_view(), name="job-list"),
    path('job/edit/<int:pk>/', JobUpdateView.as_view(), name="job-edit"),
    path('job/delete/<int:pk>/', JobDeleteView.as_view(), name="job-delete"),

    # Jobs.
    path('job/active/',  JobTemplateView.as_view(template_name='dashboard_employer/job/active_list.html'),
         name="job-active"),
    path('job/pending/',  JobTemplateView.as_view(template_name='dashboard_employer/job/pending_list.html'),
         name="job-pending"),
    path('job/draft/',  JobTemplateView.as_view(template_name='dashboard_employer/job/draft_list.html'),
         name="job-draft"),
    path('job/expired/',  JobTemplateView.as_view(template_name='dashboard_employer/job/expired_list.html'),
         name="job-expired"),
    path('job/all/', JobTemplateView.as_view(template_name='dashboard_employer/job/all_list.html'),
         name="job-all"),

]
