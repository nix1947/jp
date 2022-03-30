from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic.edit import FormView

from apps.account.models import Company, UserProfile, CustomUser
from . import usertype

from .forms import EmployerLoginForm, EmployerLoginForm, EmployerRegistrationForm, JobSeekerLoginForm, \
    JobSeekerRegistrationForm


class LoginView(FormView):
    form_class = JobSeekerLoginForm
    template_name = 'account/jobseeker_login.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        user = authenticate(self.request, email=email, password=password)
        print(dir(user))
        return HttpResponse(dir(user))

        if user is not None:
            # Add to session 
            login(self.request, user)

            if user.user_type == 'employer':
                return redirect('dashboard_employer:dashboard')
            elif user.user_type == 'js':
                return redirect('dashboard_jobseeker:dashboard')

        else:
            messages.add_message(self.request, messages.ERROR, 'Invalid username or password',
                                 extra_tags="alert-danger")
            return 'account:login'


def jobseeker_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard_jobseeker:dashboard')
    login_form = JobSeekerLoginForm()

    if request.method == 'GET':
        login_from = JobSeekerLoginForm()

    elif request.method == 'POST':
        login_form = JobSeekerLoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']

            # Query user.
            user = authenticate(request, email=email, password=password)

            if user is not None and user.user_type == usertype.JOBSEEKER:
                # authenticate the user and redirect to dashboard
                data = login(request, user)
                return redirect('dashboard_jobseeker:dashboard')
            else:
                messages.add_message(request, messages.ERROR, message="You are not authorized to login ")
                return redirect('account:jobseeker-login')

    return render(request, 'account/jobseeker_login.html', {
        'login_form': login_from
    })


def jobseeker_registration(request):
    # if request.user.is_authenticated:
    #     return redirect('dashboard_jobseeker:dashboard')
    form = JobSeekerRegistrationForm()

    if request.method == "POST":
        form = JobSeekerRegistrationForm(request.POST)
        if form.is_valid():

            with transaction.atomic():
                # User fields 
                user = form.save(commit=False)
                user.user_type = usertype.JOBSEEKER
                # TODO: change is_active to False for enabling email verification
                user.is_active = True
                user = CustomUser.objects.create_user(email=user.email, password=user.password,
                                                      user_type=user.user_type,
                                                      is_active=user.is_active)
                # user.set_password(user.password)
                # user.save()

                # User profile 
                user_profile = UserProfile(
                    user=user,
                    full_name=form.cleaned_data["full_name"],
                    phone=form.cleaned_data["mobile"]
                )

                user_profile.save()
                request.email = 'maiilifno'

            return redirect("account:registered-email-verification", email=user.email)

        else:
            return render(request, 'account/jobseeker_registration.html', {
                'form': form
            })

    return render(request, 'account/jobseeker_registration.html', {
        'form': form
    })


def email_verification(request, email):
    return render(request, 'account/email_verification.html', context={
        'email': email
    })


def employer_login(request):
    if request.user.is_authenticated and request.user.user_type == 'employer':
        return redirect('dashboard_employer:dashboard')

    elif request.user.is_authenticated and request.user.user_type == 'js':
        return redirect('dashboard_jobseeker:dashboard')

    form = EmployerLoginForm()
    if request.method == "POST":
        form = EmployerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None and user.user_type == 'employer':
                login(request, user)
                return redirect('dashboard_employer:dashboard')
            else:
                messages.add_message(request, level=messages.ERROR, message="Invalid email or password")
                # return redirect('account:employer-login')
                return render(request, 'account/employer_login.html', {
                    'form': form
                })

        return render(request, 'account/employer_login.html', {
            'form': form
        })

    return render(request, 'account/employer_login.html', {
        'form': form
    })


def employer_registration(request):
    # if request.user.is_authenticated and request.user.user_type == 'employer':
    #     return redirect('dashboard_employer:dashboard')
    # elif request.user.is_authenticated and request.user.user_type == 'js':
    #     return redirect('dashboard_employer:dashboard')

    form = EmployerRegistrationForm()
    if request.method == "POST":
        form = EmployerRegistrationForm(request.POST)

        if form.is_valid():
            organization_name = form.cleaned_data['organization_name']
            with transaction.atomic():
                # User attribute
                user = form.save(commit=False)
                user.user_type = 'employer'
                user.is_active = False
                user.save()

                # Company Profile 
                company = Company(user=user, organization_name=organization_name)
                company.save()

            return redirect('dashboard_employer:dashboard')

        return render(request, 'account/employer_registration.html', {
            'form': form
        })

    return render(request, 'account/employer_registration.html', {
        'form': form
    })
