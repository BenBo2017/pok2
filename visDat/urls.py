from django.urls import path
from django.conf.urls import url
from django.conf import settings
from djgeojson.views import GeoJSONLayerView
from django.conf.urls.static import static

from . import views
from .models import Sonde

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^api/renderData',views.renderData, name='renderData'),
    url(r'^api/exportCSV',views.exportData, name='exportCSV'),
    url(r'^data.geojson$', GeoJSONLayerView.as_view(model=Sonde), name='data'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)