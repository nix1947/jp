from django.db.models import Q
from django.shortcuts import render, HttpResponse

from apps.job.models import Job, Location
from apps.account.models import Company


def home(request):
    top_job_companies = Company.objects.filter(Q(is_active=True) & Q(job__job_type='top_job')).distinct()
    hot_job_companies = Company.objects.filter(Q(is_active=True) & Q(job__job_type='hot_job')).distinct()

    return render(request, 'index.html', {
        'top_job_companies': top_job_companies,
        'hot_job_companies': hot_job_companies
    })


def search(request):
    q = request.GET.get('q', '')
    location = request.GET.get('location', '')

    #  &
    jobs = Job.objects.filter(
        Q(title__icontains=q) &
        Q(job_location__location__icontains=location)
    ).distinct().order_by('-updated_date')

    return render(request, 'search.html', context={
        'q': q,
        'object_list': jobs,
        'location': location
    })
