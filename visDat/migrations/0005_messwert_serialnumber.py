# Generated by Django 2.0.6 on 2018-07-18 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visDat', '0004_auto_20180718_0838'),
    ]

    operations = [
        migrations.AddField(
            model_name='messwert',
            name='Serialnumber',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]
