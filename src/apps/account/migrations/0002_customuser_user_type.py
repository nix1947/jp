# Generated by Django 3.2.8 on 2021-10-25 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('employer', 'Employer'), ('js', 'Job Seeker')], default='js', max_length=10),
            preserve_default=False,
        ),
    ]
