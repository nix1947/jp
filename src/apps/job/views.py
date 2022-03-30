from django.shortcuts import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import DetailView, TemplateView

from .models import Job


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



