# Generated by Django 3.2.12 on 2022-03-30 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20220324_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='language',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='education',
            unique_together={('user', 'degree')},
        ),
    ]
