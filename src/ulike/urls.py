"""ulike URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .views import home, search, company_detail


urlpatterns = [
    path('admin_/', admin.site.urls),
    path('', home, name="homepage"),
    path('job/', include('apps.job.urls'), name="job"),
    path('search/', search, name="job"),


    # Company Url
    path('company/<str:name>', company_detail, name="company"),

    path('account/', include('apps.account.urls')),
    path('dashboard/js/', include('apps.dashboard_jobseeker.urls')),
    path('dashboard/employer/', include('apps.dashboard_employer.urls')),
   


]


if settings.DEBUG:
    # Serve media in development mode
    urlpatterns +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
