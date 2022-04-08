from django import template
from apps.job.models import JobAppliedByUser, JobBookMarked

register = template.Library()


@register.filter(name="is_job_bookmarked")
def is_job_bookmarked(job, user):
    """ Add placeholder attribute, esp. for form inputs and textareas """
    user = JobBookMarked.objects.get(job__id=self.pk, user__id=self.user.profile__id).count()
    if user:
        return True
    return False


@register.filter(name="is_job_applied")
def is_job_applied(job, user):
    """ Add placeholder attribute, esp. for form inputs and textareas """
    user = JobAppliedByUser.objects.get(job__id=self.pk, user__id=self.user.profile__id).count()
    if user:
        return True
    return False
