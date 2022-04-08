from datetime import datetime

import pytz
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from ..abstract_model import AbstractBaseModel


class Category(AbstractBaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Title"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'

    def get_jobs(self):
        return self.job_categories.filter(is_draft=False, is_approved=True)

    def get_absolute_url(self):
        return reverse('job:job-by-category', kwargs={
            'title': slugify(self.title + '-' + str(self.pk))

        })


class Location(AbstractBaseModel):
    location = models.CharField(max_length=255, verbose_name=_("Location"))

    def __str__(self):
        return self.location

    class Meta:
        verbose_name_plural = 'Locations'


class Skill(AbstractBaseModel):
    skill = models.CharField(max_length=255, verbose_name=_("Skill"))
    skill_type = models.CharField(
        max_length=20,
        choices=(
            ('soft', _('Soft Skill')),
            ('technical', _('Technical Skill')),
        ),
        verbose_name=_("Skill")
    )

    def __str__(self):
        return self.skill

    class Meta:
        verbose_name_plural = 'Skills'


class Industry(AbstractBaseModel):
    title = models.CharField(max_length=255, verbose_name="Industry title")

    class Meta:
        verbose_name_plural = 'Industries'

    def __str__(self):
        return self.title

    def get_jobs(self):
        return self.jobs.filter(is_draft=False, is_approved=True)

    def get_absolute_url(self):
        return reverse('job:job-by-industry', kwargs={
            'title': slugify(self.title + '-' + str(self.pk))

        })


class Job(AbstractBaseModel):
    company = models.ForeignKey('account.Company', on_delete=models.SET_NULL, null=True, verbose_name='Company')
    title = models.CharField(max_length=255, verbose_name=_('Job title'), help_text=_("IT manager"))
    description = models.TextField(verbose_name=_('Job description'))
    posted_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Posted Date"))
    specification = models.TextField(verbose_name=_("Job specification"))
    job_category = models.ForeignKey(Category, null=True, related_name="job_categories", on_delete=models.SET_NULL)
    is_approved = models.BooleanField(default=False)
    no_of_vacancies = models.PositiveIntegerField(default=1, help_text='10', verbose_name=_("No of Vacancies"))
    employment_type = models.CharField(
        choices=(
            ('full_time', 'Full time'),
            ('part_time', 'Part time'),
            ('contract', 'Contract'),
            ('remote', 'Remote'),
            ('temporary', 'Temporary'),
            ('freelance', 'Freelance'),
            ('internship', 'Internship'),
            ('traineeship', 'Traineeship'),
            ('volunteer', 'Volunteer'),),
        default="contract",
        max_length=20,
        verbose_name=_("Employment Type")
    )

    job_education = models.CharField(
        choices=(
            ('phd', _('Ph.d')),
            ('master', _('Master')),
            ('bachelor', _('Bachelor')),
            ('intermediate', _('Intermediate (+2)')),
            ('slc', _('Slc (10th)')),
            ('other', _('Other')),),
        default="bachelor",
        verbose_name="Education",
        max_length=50
    )

    experience = models.CharField(max_length=255, help_text="2 year", verbose_name=_("Experience required"))
    skills = models.ManyToManyField(Skill, related_name='jobs')
    job_level = models.CharField(
        choices=(
            ('entry', _("Entry Level")),
            ('mid', _("Mid Level")),
            ('senior', _("Senior Level")),
            ('top', _("Top Level")),
        ),
        default="entry",
        max_length=10,
        verbose_name=_("Job level")
    )

    is_draft = models.BooleanField(default=True)
    job_location = models.ManyToManyField(Location)
    job_type = models.CharField(
        choices=(
            ('hot_job', 'Hot Job'),
            ('top_job', 'Top Job'),
            ('free_job', 'Free Job'),
            ('feature_job', 'Featured job'),
            ('newspaper_job', 'NewsPaper Job')
        ),
        max_length=255,
        default='top_job'
    )
    offered_salary = models.CharField(help_text='45K to 75K or Negotiable', default=_('Negotiable'), max_length=255,
                                      verbose_name=_("Offered Salary"))
    job_industry = models.ForeignKey(Industry, related_name="jobs", on_delete=models.SET_NULL, null=True)
    what_we_offer = models.TextField(max_length=255, verbose_name=_("What we offer"))
    apply_method = models.CharField(help_text="Send your CV to hr@yourcompany.com or apply through ulike",
                                    max_length=255, verbose_name=_("Apply method"))
    deadline = models.DateTimeField(help_text="YYYY-MM-DD")

    def __str__(self):
        return self.title

    @property
    def slug(self):
        return slugify(self.title)

    def get_absolute_url(self):
        return reverse('job:job-detail', kwargs={
            'title': slugify(self.title + '-' + str(self.pk))

        })

    @property
    def is_expired(self):
        return (self.deadline - datetime.utcnow().replace(tzinfo=pytz.UTC)).days < 0

    def get_views(self):
        return (datetime.utcnow().replace(tzinfo=pytz.UTC) - self.posted_date).days + 5

    def is_job_bookmarked(self, user):
        user = JobBookMarked.objects.get(job__id=self.pk, user__id=self.user.profile__id).count()
        if user:
            return True
        return False

    def is_job_applied(self, user):
        user = JobAppliedByUser.objects.get(job__id=self.pk, user__id=self.user.profile__id).count()
        if user:
            return True
        return False

    def status(self):
        if self.is_expired:
            return 'Expired'
        elif self.is_draft:
            return 'Draft'
        elif self.is_approved and not self.is_expired:
            return 'Active'
        elif not self.is_approved and not self.is_draft:
            return 'Pending'

    @property
    def get_related_jobs(self):
        return self._meta.model.objects.filter(
            Q(skills__in=[skill.id for skill in self.skills.all()]) |
            Q(job_category=self.job_category) |
            Q(job_industry=self.job_industry)
        ).distinct()[:7]


class JobAppliedByUser(AbstractBaseModel):
    user = models.ForeignKey('account.UserProfile', related_name='applied_jobs', on_delete=models.SET_NULL, null=True)
    job = models.ForeignKey(Job, related_name='applied_jobs', on_delete=models.SET_NULL, null=True)
    status = models.CharField(
        max_length=255,
        default='pending',
        choices=(
            ('pending', 'Pending'),
            ('rejected', 'Rejected'),
            ('accepted', 'Accepted'),
        )
    )

    class Meta:
        unique_together = ('user', 'job',)

    def __str__(self):
        return str(self.job.title) + 'applied by ' + str(self.user.full_name)


class JobBookMarked(AbstractBaseModel):
    user = models.ForeignKey('account.UserProfile', related_name='bookmarked_jobs', on_delete=models.SET_NULL,
                             null=True)
    job = models.ForeignKey(Job, related_name='bookmarked_jobs', on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('user', 'job',)

    def __str__(self):
        return str(self.job.title) + 'applied by' + str(self.user.full_name)
