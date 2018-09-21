#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 16:42:37 2018

@author: henning
"""

from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.auth.admin import User
from django.conf import settings

from django.utils import timezone


def create_superuser(apps, schema_editor):
    superuser = User()
    superuser.is_active = True
    superuser.is_superuser = True
    superuser.is_staff = True
    superuser.username = 'admin'
    superuser.email = 'admin@admin.net'
    superuser.set_password('1234test')
    superuser.last_login = timezone.now()
    superuser.save()

class Migration(migrations.Migration):

    dependencies = [
            migrations.swappable_dependency(settings.AUTH_USER_MODEL),
            ('visDat', '0001_initial')
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]