from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.shortcuts import redirect, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from apps.account.models import Company, UserProfile, CustomUser
from . import usertype
from .forms import EmployerLoginForm, EmployerRegistrationForm, JobSeekerLoginForm, \
    JobSeekerRegistrationForm

from django.contrib.auth.views import PasswordChangeView as DjangoAdminPasswordChangeView


def jobseeker_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard_jobseeker:dashboard')
    login_form = JobSeekerLoginForm()

    if request.method == 'GET':
        login_from = login_form

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
    if request.user.is_authenticated:
        return redirect('dashboard_jobseeker:dashboard')
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
                user.set_password(user.password)
                user.save()

                # User profile
                user_profile = UserProfile(
                    user=user,
                    full_name=form.cleaned_data["full_name"],
                    phone=form.cleaned_data["mobile"]
                )

                user_profile.save()
                # TODO: pass the email sent by the user.
            return redirect("account:registered-email-verification", email=user.email)

        else:
            return render(request, 'account/jobseeker_registration.html', {
                'form': form
            })
    return render(request, 'account/jobseeker_registration.html', {
        'form': form
    })


def employer_login(request):
    if request.user.is_authenticated and request.user.user_type == usertype.EMPLOYER:
        return redirect('dashboard_employer:dashboard')

    elif request.user.is_authenticated and request.user.user_type == usertype.JOBSEEKER:
        return redirect('dashboard_jobseeker:dashboard')

    form = EmployerLoginForm()
    if request.method == "POST":
        form = EmployerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None and user.user_type == usertype.EMPLOYER:
                login(request, user)
                messages.add_message(request, level=messages.SUCCESS, message="Successfully logged in")
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
    if request.user.is_authenticated and request.user.user_type == usertype.EMPLOYER:
        return redirect('dashboard_employer:dashboard')
    elif request.user.is_authenticated and request.user.user_type == usertype.JOBSEEKER:
        return redirect('dashboard_employer:dashboard')

    form = EmployerRegistrationForm()
    if request.method == "POST":
        form = EmployerRegistrationForm(request.POST)

        if form.is_valid():
            organization_name = form.cleaned_data['organization_name']
            with transaction.atomic():
                # User attribute
                user = form.save(commit=False)
                user.user_type = usertype.EMPLOYER
                # TODO: make True to enable email verification.
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


def email_verification(request, email):
    return render(request, 'account/email_verification.html', context={
        'email': email
    })


def logout(request):
    request.session.destroy()
    return HttpResponseRedirect('/')


class PasswordChangeView(DjangoAdminPasswordChangeView):
    success_url = reverse_lazy('account:password_change_done')
    template_name = 'account/password_change_form.html'
    title = 'Password Change'
