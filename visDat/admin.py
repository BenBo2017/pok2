from django.contrib import admin
from django.db import models
from django.contrib.auth.models import Group
from leaflet.admin import LeafletGeoAdmin

from .models import Sonde, KundenAdmin,Nutzer, Messwert

class MesswertAdmin(admin.ModelAdmin):
    exclude = ('geom','Serialnumber')

admin.site.register(KundenAdmin)
admin.site.register(Nutzer)
admin.site.register(Messwert,MesswertAdmin)
admin.site.register(Sonde, LeafletGeoAdmin)

admin.site.unregister(Group)


