from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import HttpResponse, redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView

from .forms import JobForm
from .models import Job
from ..account.decorators import employer_required


def job_detail(request, title):
    job_id = title.split('-')[-1]
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'job/job_detail.html', context={
        'object': job
    })


class JobSearchView(TemplateView):
    template_name = 'job/job_search.html'

    def get(self, request, *args, **kwargs):
        return HttpResponse("search page")




