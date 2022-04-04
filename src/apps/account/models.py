from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.job.models import Job
from apps.job.models import Location
from apps.job.models import Skill, Category, Industry
from . import usertype
from .managers import CustomUserManager
from ..abstract_model import AbstractBaseModel
from django.urls import reverse
from django.db.models import F


class CustomUser(AbstractBaseUser, PermissionsMixin, AbstractBaseModel):
    email = models.EmailField(_('email address'), unique=True,
                              error_messages={'unique': 'This email has already been registered'})
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    user_type = models.CharField(
        choices=(
            (usertype.EMPLOYER, 'Employer'),
            (usertype.JOBSEEKER, 'Job Seeker')
        ),
        max_length=10
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def dashboard(self):
        if self.user_type == usertype.EMPLOYER:
            return reverse('dashboard_employer:dashboard')
        elif self.user_type == usertype.JOBSEEKER:
            return reverse('dashboard_jobseeker:dashboard')

    def logout(self):
        return reverse('account:logout')

    def change_password(self):
        # TODO:
        if self.user_type == usertype.EMPLOYER:
            return ''
        elif self.user_type == usertype.JOBSEEKER:
            return ''

    def profile(self):
        # TODO:
        if self.user_type == usertype.EMPLOYER:
            return ''
        elif self.user_type == usertype.JOBSEEKER:
            return reverse('dashboard_jobseeker:profile', kwargs={
                'pk': self.pk
            })


class Company(AbstractBaseModel):
    user = models.OneToOneField(CustomUser, related_name='company', on_delete=models.CASCADE, null=True)
    logo = models.ImageField(upload_to='uploads/company/profile', null=True)
    organization_name = models.CharField(max_length=255, default="", verbose_name=_("Organization name"),
                                         null=True)
    description = models.TextField(verbose_name=_("About company"), default="", null=True)
    company_size = models.CharField(max_length=255, default="", verbose_name=_("Company Size"), null=True)
    industry = models.ForeignKey(Industry, null=True, blank=True, on_delete=models.SET_NULL,
                                 verbose_name=_("Industry"))
    established = models.CharField(verbose_name=_("Established date"), max_length=4, null=True)
    website = models.URLField(default='', null=True, blank=True)
    headquarter = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL,
                                    verbose_name=_("Location"))
    linkedin = models.URLField(default="#", null=True)
    facebook = models.URLField(default="#", null=True)
    twitter = models.URLField(default="#", null=True)

    class Meta:
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.organization_name

    @property
    def get_user(self):
        """Proxy for profile"""
        return self.profile

    def get_absolute_url(self):
        return '/company'

    def posted_jobs(self):
        self.job_set.objects.filter(is_draft=False)

    def drafted_jobs(self):
        return self.job_set.filter(is_draft=True)


    def expired_jobs(self):
        return [job for job in self.job_set.filter() if
                job.is_expired == True]

    def all_jobs(self):
        return self.job_set.all()

    def pending_jobs(self):
        return self.job_set.filter(is_approved=False, is_draft=False)

    def active_jobs(self):

        return [job for job in self.job_set.filter(is_active=True, is_draft=False) if
                    job.is_expired == False]




class UserProfile(AbstractBaseModel):
    # Basic info

    user = models.OneToOneField(CustomUser, related_name='profile', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, null=True)
    photo = models.ImageField(verbose_name=_("Profile Picture"),
                              upload_to="uploads/user/profile",
                              blank=True, null=True)

    dob = models.DateField()

    current_address = models.CharField(max_length=255, null=True)
    permanent_address = models.CharField(max_length=255, null=True)
    nationality = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=255, choices=(
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others')
    ), null=True)
    martial_status = models.CharField(max_length=255,
                                      choices=(
                                          ('married', 'married'),
                                          ('unmarried', 'unmarried')
                                      ), null=True)

    religion = models.CharField(max_length=255,
                                choices=(
                                    ('Buddhism', 'Buddhism'),
                                    ('Sikhism', 'Sikhism'),
                                    ('Bahai', 'Bahai'),
                                    ('Christianity', 'Christianity'),
                                    ('Hinduism', 'Hinduism'),
                                    ('Islam', 'Islam'),
                                    ('Jainism', 'Jainism'),
                                    ('Nonreligious', 'Nonreligious')
                                ), null=True)

    contact_number = models.CharField(max_length=255, null=True)

    is_disabled = models.BooleanField(default=False, help_text='Tick this for any kind of physical disability.',
                                      null=True)

    website = models.URLField(default='', blank=True, null=True)

    bio = models.TextField(default='', blank=True, null=True)

    phone = models.CharField(max_length=10, blank=True, default='', null=True)

    city = models.CharField(max_length=100, default='', blank=True, null=True)

    country = models.CharField(max_length=100, default='', blank=True, null=True)

    # Job preferences.
    career_objective = models.CharField(max_length=255, null=True)
    job_level = models.CharField(
        choices=(
            ('entry', _("Entry Level")),
            ('mid', _("Mid Level")),
            ('senior', _("Senior Level")),
            ('top', _("Top Level")),
        ),
        default="entry",
        null=True,
        max_length=10,
        verbose_name=_("Job level")
    )

    available_for = models.CharField(
        null=True,
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

    specializations = models.CharField(max_length=255, null=True, help_text="Devops Enginnering")

    skills = models.ManyToManyField(Skill, related_name='skills', null=True)
    job_preference_location = models.CharField(max_length=255, null=True)
    job_preferences = models.ManyToManyField(Category, related_name="categories", null=True)

    def __str__(self):
        return self.user.email

    @property
    def preferred_jobs(self):
        """ return list of preferred jobs"""
        return self.job_preferences.all()

    @property
    def get_age(self):
        return "TODO:"

    @property
    def get_recommended_jobs(self):
        # TODO:
        return Job.objects.all()

    @property
    def get_jobs_applied(self):
        # TODO:
        return ''

    @property
    def get_saved_jobs(self):
        # TODO:
        return ''


class Education(AbstractBaseModel):
    degree = models.CharField(max_length=255, choices=(
        ('phd', 'Phd'),
        ('master', 'Master'),
        ('bachelor', 'Bachelor'),
        ('intermediate', 'Intermediate'),
        ('slc', 'SLC (10th)'),
        ('other', 'Other')
    ))

    education_program = models.CharField(max_length=255, help_text="BSC Computer engineering")

    education_board = models.CharField(max_length=255, help_text="Pokhara University")

    name_of_institue = models.CharField(max_length=255, help_text="Cosmos college")

    started_year = models.DateField()

    current_studying_here = models.BooleanField(default=False)

    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name="educations")

    class Meta:
        unique_together = ('user', 'degree',)

    def __str__(self):
        return self.education_program


class Training(AbstractBaseModel):
    name_of_training = models.CharField(max_length=255, help_text="Excel training")

    institution_name = models.CharField(max_length=255, help_text="Viat Academy nepal")

    duration = models.PositiveIntegerField()
    duration_type = models.CharField(max_length=255,
                                     choices=(
                                         ('day', 'Day'),
                                         ('week', 'Week'),
                                         ('month', 'Month'),
                                         ('year', 'Year'),

                                     ))

    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name="trainings")

    def __str__(self):
        return self.name_of_training


class WorkExperience(AbstractBaseModel):
    organization_name = models.CharField(max_length=255, help_text="Perl Infotech")
    nature_of_organization = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True,
                                               related_name='experiences')
    job_location = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
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
    currently_working_here = models.BooleanField(default=False)
    start_date = models.DateField()
    duties_and_responsibilities = models.TextField()
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name="work_experiences")

    def __str__(self) -> str:
        return self.job_title


class Language(AbstractBaseModel):
    language = models.CharField(max_length=255)
    reading = models.PositiveIntegerField(
        default=1, validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])
    writing = models.PositiveIntegerField(
        default=1, validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])
    speaking = models.PositiveIntegerField(default=1, validators=[
        MaxValueValidator(5),
        MinValueValidator(1)
    ])
    listening = models.PositiveIntegerField(default=1, validators=[
        MaxValueValidator(5),
        MinValueValidator(1)
    ])

    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name="languages")

    def __str__(self):
        return self.language


class Reference(AbstractBaseModel):
    reference_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    organization_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=10)

    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name="references")

    def __str__(self):
        return self.reference_name
