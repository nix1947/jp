from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.shortcuts import reverse, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, TemplateView
from django.forms.models import model_to_dict
from apps.account.decorators import jobseeker_required
from apps.account.forms import EducationForm
from apps.account.forms import (
    ReferenceForm,
    LanguageForm,
    WorkExperienceForm,
    TrainingForm,
    UserProfileForm
)
from apps.account.models import CustomUser
from apps.account.models import Language
from apps.account.models import Reference, UserProfile, Education, WorkExperience, Training


@login_required
def dashboard(request):
    return render(request, 'dashboard_jobseeker/dashboard-main.html', {

    })


@login_required
@jobseeker_required
def profile_reference(request):
    references = Reference.objects.filter(user=request.user.id)
    return render(request, 'dashboard_jobseeker/reference/reference.html', {
        'references': references
    })


# # Userprofile related forms
# User profile related views.. 
# Reference,
# Language,
# WorkExperience,
# Training,
# Education,
# UserProfile,

class UpdateProfileView(UpdateView):
    form_class = UserProfileForm
    model = UserProfile
    template_name = 'dashboard_jobseeker/edit-profile.html'

    @method_decorator(login_required, jobseeker_required)
    def dispatch(self, request, *args, **kwargs):
        super(UpdateProfileView, self).dispatch()

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.save()

        return redirect('dashboard_jobseeker:edit-profile', pk=profile.id)


@login_required
@jobseeker_required
# TODO: User has permission to edit the profile.

@login_required
@jobseeker_required
def editprofile(request, pk):
    if request.user.profile.id != pk:
        raise PermissionDenied("You are not authorized to access this page")

    if request.method == 'GET':
        user_profile = get_object_or_404(UserProfile, id=pk)
        form = UserProfileForm(initial=model_to_dict(user_profile))

    elif request.method == 'POST':
        form = UserProfileForm(request.POST)
        form.save()

    return render(request, 'dashboard_jobseeker/edit-profile.html', {
        'form': form

    })


@login_required()
@jobseeker_required
def profile_detail(request, pk):
    user = get_object_or_404(CustomUser, id=pk)
    if user.id != pk:
        raise PermissionDenied("Not authorized to access this page")
    return render(request, 'dashboard_jobseeker/profile_detail.html', context={
        'user': user
    })


# Reference CUDDL: CREATE, UPDATED, DETAIL, DELETE, LIST
class ReferenceDetailView(UpdateView):
    form_class = ReferenceForm
    model = Reference
    template_name = 'dashboard_jobseeker/reference/detail.html'

    @method_decorator(login_required, jobseeker_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self):
        record = self.object
        if record.user != self.request.user.profile:
            raise PermissionDenied("You are not authorized to access this object")

        return super().get(self)


class ReferenceUpdateView(UpdateView):
    form_class = ReferenceForm
    model = Reference
    template_name = 'dashboard_jobseeker/reference/update.html'

    @method_decorator(login_required, jobseeker_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.user.profile.id != self.get_object().id:
            raise PermissionDenied("You are not authorized to update this object")

        record = form.save(commit=False)
        record.user = self.request.user.profile
        record.save()
        messages.add_message(self.request, messages.INFO, f'{record.reference_name}  updated successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, 'dashboard_jobseeker/edit-reference.html', {
            'form': form
        })

    def get_success_url(self):
        messages.add_message(request=self.request, level=messages.SUCCESS,
                             message=self.get_object() + " Updated Successfully")
        return reverse("dashboard_jobseeker:profile-reference")


class ReferenceCreateView(CreateView):
    form_class = ReferenceForm
    model = Reference
    template_name = 'dashboard_jobseeker/reference/add.html'

    @method_decorator(login_required, jobseeker_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        reference = form.save(commit=False)
        reference.user = self.request.user.profile
        reference.save()
        messages.add_message(self.request, level=messages.SUCCESS, message="Reference added successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        return render(self, self.request, 'dashboard_jobseeker/reference/add.html', {
            'form': form
        })

    def get_success_url(self) -> str:
        messages.add_message(request=self.request, level=messages.SUCCESS,
                             message="Reference record added Successfully")
        return reverse("dashboard_jobseeker:profile", kwargs={
            'pk': self.request.user.profile.id
        })


class ReferenceDeleteView(DeleteView):
    model = Reference
    template_name = 'dashboard_jobseeker/reference/delete.html'

    @method_decorator(login_required, jobseeker_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user.id != self.request.user.profile.id:
            raise PermissionDenied("You are not authorized to delete this object ")

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        messages.add_message(request=self.request, level=messages.SUCCESS,
                             message="Reference Deleted Successfully")
        return reverse('dashboard_jobseeker:profile', kwargs={
            'pk': self.request.user.profile.id
        })


# Language db views.

class LanguageListView(ListView):
    model = Language
    template_name = 'jobseeker_dashboard/language/list.html'

    @method_decorator(login_required, jobseeker_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_object_name(self, object_list):
        # Only return language list belong to this owner.
        object_list = Language.objects.filter(user=self.request.user.profile.id)
        return object_list


class LanguageUpdateView(UpdateView):
    form_class = LanguageForm
    model = Language
    template_name = 'dashboard_jobseeker/language/update.html'

    @method_decorator(login_required, jobseeker_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        record = form.save(commit=False)
        if record.user.id != self.request.user.profile.id:
            raise PermissionDenied("Not authorized to update this record")

        record.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, 'dashboard_jobseeker/language/update.html', {
            'form': form
        })

    def get_success_url(self):
        messages.add_message(request=self.request, level=messages.SUCCESS,
                             message="Record updated Successfully")
        return reverse('dashboard_jobseeker:profile', kwargs={
            'pk': self.request.user.profile.id
        })


class LanguageCreateView(CreateView):
    form_class = LanguageForm
    model = Language
    template_name = 'dashboard_jobseeker/language/add.html'

    @method_decorator(login_required, jobseeker_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            record = form.save(commit=False)
            record.user = self.request.user.profile
            record.save()
            return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, 'dashboard_jobseeker/language/add.html', {
            'form': form
        })

    def get_success_url(self, **kwargs):
        messages.add_message(request=self.request, level=messages.SUCCESS,
                             message="Record added successfully")
        return reverse('dashboard_jobseeker:profile', kwargs={
            'pk': self.request.user.pk
        })


class LanguageDeleteView(DeleteView):
    model = Language
    template_name = 'dashboard_jobseeker/language/delete.html'

    @method_decorator(login_required, jobseeker_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user.id != self.request.user.profile.id:
            raise PermissionDenied("You are not authorized to delete this object ")

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        messages.add_message(request=self.request, level=messages.SUCCESS,
                             message="Record deleted successfully")
        return reverse('dashboard_jobseeker:profile', kwargs={
            'pk': self.request.user.profile.id
        })


# Education Model views.
class EducationCreateView(CreateView):
    template_name = 'dashboard_jobseeker/education/add.html'
    form_class = EducationForm
    model = Education

    @method_decorator(login_required, jobseeker_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            record = form.save(commit=False)
            record.user = self.request.user.profile
            record.save()
            return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, 'dashboard_jobseeker/education/add.html', {
            'form': form
        })

    def get_success_url(self, **kwargs):
        messages.add_message(request=self.request, level=messages.SUCCESS,
                             message="Record added Successfully")
        return reverse('dashboard_jobseeker:profile', kwargs={
            'pk': self.request.user.pk
        })


class EducationListView(ListView):
    template_name = 'dashboard_jobseeker/education/list.html'
    model = Education

    @method_decorator(login_required, jobseeker_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Education.objects.filter(user=self.request.user.profile.id)

    def get_success_url(self):
        return reverse('dashboard_jobseeker:profile', kwargs={
            'pk': self.request.user.id
        })


class EducationUpdateView(UpdateView):
    form_class = EducationForm
    model = Education
    template_name = 'dashboard_jobseeker/education/update.html'

    @method_decorator(login_required, jobseeker_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        record: object = form.save(commit=False)
        if record.user.id != self.request.user.profile.id:
            raise PermissionDenied("Not authorized to update this record")

        record.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, 'dashboard_jobseeker/education/update.html', {
            'form': form
        })

    def get_success_url(self):
        messages.add_message(request=self.request, level=messages.SUCCESS,
                             message="Successfully updated ")
        return reverse('dashboard_jobseeker:profile', kwargs={
            'pk': self.request.user.id
        })


class EducationDeleteView(DeleteView):
    model = Education
    template_name = 'dashboard_jobseeker/education/delete.html'

    @method_decorator(login_required, jobseeker_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user.id != self.request.user.profile.id:
            raise PermissionDenied("You are not authorized to delete this object ")

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        messages.add_message(request=self.request, level=messages.SUCCESS,
                             message="Successfully Deleted ")
        return reverse('dashboard_jobseeker:profile', kwargs={
            'pk': self.request.user.profile.id
        })


# WorkingExperience
class WorkingExperienceCreateView(CreateView):
    template_name = 'dashboard_jobseeker/experience/add.html'
    form_class = WorkExperienceForm
    model = WorkExperience

    @method_decorator(login_required, jobseeker_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            record = form.save(commit=False)
            record.user = self.request.user.profile
            record.save()
            return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, 'dashboard_jobseeker/experience/add.html', {
            'form': form
        })

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, level=messages.SUCCESS, message="Working Experience added successfully")
        return reverse('dashboard_jobseeker:profile', kwargs={
            'pk': self.request.user.pk
        })


class WorkingExperienceListView(ListView):
    template_name = 'dashboard_jobseeker/education/list.html'
    model = WorkExperience

    @method_decorator(login_required, jobseeker_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return WorkExperience.objects.filter(user=self.request.user.profile.id)

    def get_success_url(self):
        return reverse('dashboard_jobseeker:profile', kwargs={
            'pk': self.request.user.id
        })


class WorkingExperienceUpdateView(UpdateView):
    form_class = WorkExperienceForm
    model = WorkExperience
    template_name = 'dashboard_jobseeker/experience/update.html'

    @method_decorator(login_required, jobseeker_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        record: object = form.save(commit=False)
        if record.user.id != self.request.user.profile.id:
            raise PermissionDenied("Not authorized to update this record")

        record.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, 'dashboard_jobseeker/experience/update.html', {
            'form': form
        })

    def get_success_url(self):
        messages.add_message(request=self.request, level=messages.SUCCESS,
                             message="Successfully updated ")
        return reverse('dashboard_jobseeker:profile', kwargs={
            'pk': self.request.user.id
        })


class WorkingExperienceDeleteView(DeleteView):
    model = WorkExperience
    template_name = 'dashboard_jobseeker/experience/delete.html'

    @method_decorator(login_required, jobseeker_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user.id != self.request.user.profile.id:
            raise PermissionDenied("You are not authorized to delete this object ")

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        messages.add_message(request=self.request, level=messages.SUCCESS,
                             message="Successfully Deleted ")
        return reverse('dashboard_jobseeker:profile', kwargs={
            'pk': self.request.user.profile.id
        })


# Training

class TrainingCreateView(CreateView):
    template_name = 'dashboard_jobseeker/training/add.html'
    form_class = TrainingForm
    model = Training

    @method_decorator(login_required, jobseeker_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            record = form.save(commit=False)
            record.user = self.request.user.profile
            record.save()
            return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, 'dashboard_jobseeker/training/add.html', {
            'form': form
        })

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, level=messages.SUCCESS, message="Training added successfully")
        return reverse('dashboard_jobseeker:profile', kwargs={
            'pk': self.request.user.pk
        })


class TrainingListView(ListView):
    template_name = 'dashboard_jobseeker/training/list.html'
    model = Training

    @method_decorator(login_required, jobseeker_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Training.objects.filter(user=self.request.user.profile.id)

    def get_success_url(self):
        return reverse('dashboard_jobseeker:profile', kwargs={
            'pk': self.request.user.id
        })


class TrainingUpdateView(UpdateView):
    form_class = TrainingForm
    model = Training
    template_name = 'dashboard_jobseeker/training/update.html'

    @method_decorator(login_required, jobseeker_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        record: object = form.save(commit=False)
        if record.user.id != self.request.user.profile.id:
            raise PermissionDenied("Not authorized to update this record")

        record.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, 'dashboard_jobseeker/training/update.html', {
            'form': form
        })

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user.id != self.request.user.profile.id:
            raise PermissionDenied("Not authorized")

        return super().get(self, request, *args, **kwargs)

    def get_success_url(self):
        messages.add_message(request=self.request, level=messages.SUCCESS,
                             message="Successfully updated ")
        return reverse('dashboard_jobseeker:profile', kwargs={
            'pk': self.request.user.id
        })


class TrainingDeleteView(DeleteView):
    model = Training
    template_name = 'dashboard_jobseeker/training/delete.html'

    @method_decorator(login_required, jobseeker_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user.id != self.request.user.profile.id:
            raise PermissionDenied("You are not authorized to delete this object ")

        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user.id != self.request.user.profile.id:
            raise PermissionDenied("Not authorized")

        return super().get(self, request, *args, **kwargs)

    def get_success_url(self):
        messages.add_message(request=self.request, level=messages.SUCCESS,
                             message="Successfully Deleted ")
        return reverse('dashboard_jobseeker:profile', kwargs={
            'pk': self.request.user.profile.id
        })


class ProfileEditView(UpdateView):
    model = UserProfile
    template_name = 'dashboard_jobseeker/edit-profile.html'
    form_class = UserProfileForm

    @method_decorator(login_required, jobseeker_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        record = form.save(commit=False)
        if record.user.id != self.request.user.id:
            raise PermissionDenied("Not Authorized")

        return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, 'dashboard_jobseeker/edit-profile.html', {
            'form': form
        })

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user.id != self.request.user.id:
            raise PermissionDenied("Not authorized")

        return super().get(self, request, *args, **kwargs)

    def get_success_url(self):
        messages.add_message(request=self.request, level=messages.SUCCESS,
                             message="Profile Updated Successfully ")
        return reverse('dashboard_jobseeker:profile', kwargs={
            'pk': self.request.user.profile.id
        })


class CvDetailView(TemplateView):
    template_name = 'dashboard_jobseeker/cv/cv.html'
    model = UserProfile

    @method_decorator(login_required, jobseeker_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.get_object().id != self.request.user.profile.id:
            raise PermissionDenied()

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        raise PermissionDenied()


class AppliedJobView(TemplateView):
    template_name = 'dashboard_jobseeker/job/applied_job.html'

    @method_decorator(login_required, jobseeker_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class BookMarkedJobView(TemplateView):
    template_name = 'dashboard_jobseeker/job/saved_job.html'

    @method_decorator(login_required, jobseeker_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ScheduledInterviewView(TemplateView):
    template_name = 'dashboard_jobseeker/job/scheduled_interview_job.html'

    @method_decorator(login_required, jobseeker_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class RecommendedJobView(TemplateView):
    template_name = 'dashboard_jobseeker/job/recommended_job.html'

    @method_decorator(login_required, jobseeker_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

