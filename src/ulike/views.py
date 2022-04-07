from django.db.models import Q
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from apps.job.models import Job
from apps.account.models import Company


def home(request):
    top_job_companies = Company.objects.filter(
        Q(is_active=True) & Q(job__job_type='top_job', job__is_draft=False)).distinct()
    hot_job_companies = Company.objects.filter(
        Q(is_active=True) & Q(job__job_type='hot_job', job__is_draft=False)).distinct()

    return render(request, 'index.html', {
        'top_job_companies': top_job_companies,
        'hot_job_companies': hot_job_companies
    })


def search(request):
    q = request.GET.get('q', '')
    location = request.GET.get('location', None)

    if location and q:
        search_query = Q(title__icontains=q, employment_type__icontains=q) | Q(employment_type__icontains=q) | Q(
            job_location__location__icontains=location)
    elif not location and q:
        search_query = Q(title__icontains=q) | Q(employment_type__icontains=q)
    elif not q and location:
        search_query = Q(job_location__location__icontains=location)

    else:
        search_query = Q(title__icontains=q, employment_type__icontains=q) | Q(employment_type__icontains=q) | Q(
            job_location__location__icontains=location)

    jobs = Job.objects.filter(search_query, is_draft=False, is_approved=True).distinct().order_by('-updated_date')

    return render(request, 'search.html', context={
        'q': q,
        'object_list': jobs,
        'location': location
    })


# Company Urls.
def company_detail(request, name):
    if not name:
        return HttpResponseRedirect('/')

    com_id = name.split('-')[-1]
    name = ' '.join(name.split('-')[0:-1])
    if not com_id:
        return HttpResponseRedirect('/search?q=' + name)
    company = get_object_or_404(Company, pk=com_id)
    return render(request, 'account/company/company_detail.html', {
        'object': company

    })
