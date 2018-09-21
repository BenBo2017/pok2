from import_export import resources
from .models import Messwert, Sonde

class MesswertResource(resources.ModelResource):
    class Meta:
        model = Messwert
        fields = ('Serialnumber', 'Date', 'Temperature','Pressure','geom')
        
class SondeResource(resources.ModelResource):
    class Meta:
        model = Sonde
        fields = ('Serial', 'Date', 'geom')