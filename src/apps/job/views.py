from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages

from apps.job.models import Category, Industry
from .models import Job
from apps.account.decorators import jobseeker_required
from django.contrib.auth.decorators import login_required
from apps.job.models import JobAppliedByUser, JobBookMarked
from django.db.transaction import atomic


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


def job_by_category(request, title):
    if not title:
        return HttpResponseRedirect('/')

    cat_id = title.split('-')[-1]
    title = ' '.join(title.split('-')[0:-1])
    if not cat_id:
        return HttpResponseRedirect('/search?q=' + title)
    category = get_object_or_404(Category, pk=cat_id)
    return render(request, 'job/job_by_category.html', {
        'object': category

    })


def job_by_industry(request, title):
    if not title:
        return HttpResponseRedirect('/')

    ind_id = title.split('-')[-1]
    title = ' '.join(title.split('-')[0:-1])
    if not ind_id:
        return HttpResponseRedirect('/search?q=' + title)
    industry = get_object_or_404(Industry, pk=ind_id)
    return render(request, 'job/job_by_industry.html', {
        'object': industry

    })


@login_required
@jobseeker_required
def apply_job(request):
    if request.method == "POST":
        job_id = request.POST.get('job_id', None)
        user = request.user
        current_path = request.POST.get('absolute_path')
        job = get_object_or_404(Job, id=job_id)

        already_applied = JobAppliedByUser.objects.filter(user=user.profile, job=job).count()

        if already_applied:
            messages.add_message(request, message="You have already applied for this job", level=messages.ERROR)
            return HttpResponseRedirect(current_path)

        if job and request.user.is_job_seeker:
            applied_job = JobAppliedByUser.objects.create(user=user.profile, job=job)
            applied_job.save()
            messages.add_message(request, message="Job applied Successfully", level=messages.SUCCESS)
            return HttpResponseRedirect(current_path)

        else:
            messages.add_message(request, message="Error while applying job", level=messages.ERROR)
            return HttpResponseRedirect(current_path)

    else:
        return HttpResponseRedirect('/')




@login_required
@jobseeker_required
def bookmark_job(request):
    if request.method == "POST":
        job_id = request.POST.get('job_id', None)
        user = request.user
        current_path = request.POST.get('absolute_path')
        job = get_object_or_404(Job, id=job_id)

        already_bookmarked = JobBookMarked.objects.filter(user=user.profile, job=job).count()

        if already_bookmarked:
            messages.add_message(request, message="You have already saved this job", level=messages.ERROR)
            return HttpResponseRedirect(current_path)

        if job and request.user.is_job_seeker:
            bookmarked_job = JobBookMarked.objects.create(user=user.profile, job=job)
            bookmarked_job.save()
            messages.add_message(request, message="Job Saved Successfully", level=messages.SUCCESS)
            return HttpResponseRedirect(current_path)

        else:
            messages.add_message(request, message="Error while saving job", level=messages.ERROR)
            return HttpResponseRedirect(current_path)

    else:
        return HttpResponseRedirect('/')

# TODO: APPLIED JOB, APPLIED JOB LIST (EMPLOYEE SIDE), JOB STATUS(JOBSEEKER SIDE)