from django.urls import path

from .views import (
    dashboard, editprofile, profile_detail,
    ReferenceEditView,
    ReferenceDetailView,
    ReferenceCreateView,
    profile_reference,
    ReferenceDeleteView,

    # Language
    LanguageCreateView,
    LanguageUpdateView,
    LanguageDeleteView,
    LanguageListView,

    # Education
    EducationCreateView,
    EducationUpdateView,
    EducationDeleteView,

    # Working Experience
    WorkingExperienceCreateView,
    WorkingExperienceUpdateView,
    WorkingExperienceListView,
    WorkingExperienceDeleteView,

    # Training
    TrainingCreateView,
    TrainingUpdateView,
    TrainingListView,
    TrainingDeleteView,
)

app_name = "dashboard_jobseeker"

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('profile/detail/<int:pk>', profile_detail, name='profile'),
    path('profile/edit/<int:pk>', editprofile, name='edit-profile'),

    # Reference form.

    path('profile/reference', profile_reference, name='profile-reference'),
    path('profile/reference/add/', ReferenceCreateView.as_view(), name='add-reference'),
    path('profile/reference/edit/<int:pk>', ReferenceEditView.as_view(), name='edit-reference'),
    path('profile/reference/delete/<int:pk>', ReferenceDeleteView.as_view(), name='delete-reference'),
    path('profile/reference/detail/<int:pk>', ReferenceDetailView.as_view(), name='detail-reference'),

    # Language url. 
    path('profile/language/list/', LanguageListView.as_view(), name='list-language'),
    path('profile/language/create/', LanguageCreateView.as_view(), name='create-language'),
    path('profile/language/edit/<int:pk>', LanguageUpdateView.as_view(), name='edit-language'),
    path('profile/language/delete/<int:pk>', LanguageDeleteView.as_view(), name='delete-language'),

    # Education url.
    path('profile/education/list/', LanguageListView.as_view(), name='list-education'),
    path('profile/education/create/', EducationCreateView.as_view(), name='create-education'),
    path('profile/education/edit/<int:pk>', EducationUpdateView.as_view(), name='edit-education'),
    path('profile/education/delete/<int:pk>', EducationDeleteView.as_view(), name='delete-education'),

    # Working Experience Urls.
    path('profile/experience/list/', WorkingExperienceListView.as_view(), name='list-experience'),
    path('profile/experience/create/', WorkingExperienceCreateView.as_view(), name='create-experience'),
    path('profile/experience/edit/<int:pk>', WorkingExperienceUpdateView.as_view(), name='edit-experience'),
    path('profile/experience/delete/<int:pk>', WorkingExperienceDeleteView.as_view(), name='delete-experience'),

    # Training urls.

    path('profile/training/list/', TrainingListView.as_view(), name='list-training'),
    path('profile/training/create/', TrainingCreateView.as_view(), name='create-training'),
    path('profile/training/edit/<int:pk>', TrainingUpdateView.as_view(), name='edit-training'),
    path('profile/training/delete/<int:pk>', TrainingDeleteView.as_view(), name='delete-training')

]
