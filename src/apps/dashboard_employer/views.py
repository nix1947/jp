from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import (PermissionRequiredMixin)
from django.shortcuts import (HttpResponse, redirect,
                              render)
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, TemplateView

from apps.account.decorators import employer_required
from apps.job.forms import JobForm
from apps.job.models import Job


@login_required
def dashboard(request):
    # posted_jobs = Job.objects.filter(company=request.user.company).count()
    total_applicants = 256
    jobs_view = 16
    applied_rate = 18.6
    return render(request, 'dashboard_employer/dashboard-main.html', {
        # 'posted_jobs': posted_jobs, 
        'total_applicants': total_applicants,
        'jobs_view': jobs_view,
        'applied_rate': applied_rate
    })


class JobCreateView(CreateView):
    model = Job
    form_class = JobForm
    template_name = "dashboard_employer/job/add.html"

    @method_decorator(login_required)
    @method_decorator(employer_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        record = form.save(commit=False)
        record.company = self.request.user.company
        record.save()
        messages.add_message(self.request, messages.SUCCESS,
                             "Job submitted successfully and will be posted after review")
        return redirect("dashboard_employer:dashboard")

    def form_invalid(self, form):
        return render(self.request, self.template_name, context={
            'form': form
        })


class JobUpdateView(UpdateView):
    template_name = 'dashboard_employer/job/update.html'
    form_class = JobForm
    model = Job

    @method_decorator(login_required)
    @method_decorator(employer_required)
    @method_decorator(permission_required('job.change_job'))
    def dispatch(self, request, *args, **kwargs):
        job = self.get_object()
        if job.company != self.request.user.company or None:
            return HttpResponse('Unauthorized Access', status=401)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("dashboard_employer:dashboard")

    def form_valid(self, form):
        record = form.save(commit=False)
        record.save()
        messages.add_message(self.request, level=messages.SUCCESS, message="Record updated successfully")
        return super().form_valid(form)


class JobListView(PermissionRequiredMixin, ListView):
    model = Job
    template_name = 'dashboard_employer/job/list.html'
    permission_required = ('job.view_job',)

    @method_decorator(login_required)
    @method_decorator(employer_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Job.objects.filter(company=self.request.user.company).order_by('-updated_date')


class JobDeleteView(DeleteView):
    model = Job
    template_name = 'dashboard_employer/job/add.html'

    @method_decorator(login_required)
    @method_decorator(employer_required)
    @method_decorator(permission_required('job.delete_job'))
    def dispatch(self, request, *args, **kwargs):
        job = self.get_object()
        if job.company != self.request.user.company:
            return HttpResponse('Unauthorized', status=401)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, self.object.title + " " + "Deleted successfully")
        return reverse("dashboard_employer:dashboard")


class JobActiveList(TemplateView):
    template_name = 'dashboard_employer/job/active_list.html'

    @method_decorator(login_required, employer_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class JobPendingList(TemplateView):
    template_name = 'dashboard_employer/job/active_list.html'

    @method_decorator(login_required, employer_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class JobDraftList(TemplateView):
    template_name = 'dashboard_employer/job/active_list.html'

    @method_decorator(login_required, employer_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class JobExpiredList(TemplateView):
    template_name = 'dashboard_employer/job/active_list.html'

    @method_decorator(login_required, employer_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class JobTemplateView(TemplateView):
    @method_decorator(login_required, employer_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
