#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 16:42:37 2018

@author: henning
"""

from __future__ import unicode_literals
from django.db import migrations
from django.conf import settings



def create_admin(apps, schema_editor):
    
    KA = apps.get_model('visDat', 'Kundenadmin')
    
    U = apps.get_model('auth', 'User') 
    u = U.objects.get(username = 'admin')
    
    k = KA(Kundennummer = 1, LizenzExpire = '2020-01-01', user = u)
    k.save()


def create_nutzer(apps, schema_editor):
    
    N = apps.get_model('visDat', 'Nutzer')
    
    U = apps.get_model('auth', 'User') 
    u = U.objects.get(username = 'admin')
    A = apps.get_model('visDat', 'Kundenadmin')
    a = A.objects.get(Kundennummer = 1)
    
    n = N(KundenAdmin = a, user = u, Name = 'John Doe')
    n.save()


class Migration(migrations.Migration):

    dependencies = [
            migrations.swappable_dependency(settings.AUTH_USER_MODEL),
            ('visDat', '0002_createSuper')
    ]

    operations = [
        migrations.RunPython(create_admin),
        migrations.RunPython(create_nutzer)
    ]
