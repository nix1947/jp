# Generated by Django 3.2.12 on 2022-04-07 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_auto_20220405_1713'),
        ('job', '0010_jobappliedbyuser_jobbookmarked'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='jobappliedbyuser',
            unique_together={('user', 'job')},
        ),
        migrations.AlterUniqueTogether(
            name='jobbookmarked',
            unique_together={('user', 'job')},
        ),
    ]