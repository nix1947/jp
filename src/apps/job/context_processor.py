from .models import Category, Industry, Job


def sidebar_jobs(request):
    return {'industries': Industry.objects.all()[:10],
            'categories': Category.objects.all()[:10],
            'employment_types': Job.employment_type.field.choices}
