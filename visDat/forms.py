from django import forms
from .models import Sonde

import datetime

class date_choice(forms.Form):
    
    avSonden = forms.ModelChoiceField(queryset = Sonde.objects.none(),label=u'Sonden')
    
    def __init__(self, *args, **kwargs):

        currentUserID = kwargs.pop('currentUserID', None)
        qs = kwargs.pop('qs',Sonde.objects.filter(owned_by__Kundennummer = -999999))
         
        super(date_choice, self).__init__(*args, **kwargs)
       
        if currentUserID:
            qs = Sonde.objects.filter(owned_by__Kundennummer = currentUserID).values_list("Serial",flat=True).distinct()
        
        self.fields['avSonden'].queryset = qs

        
    
    start = forms.DateField(input_formats=['%Y-%m-%d'])
    end = forms.DateField(input_formats=['%Y-%m-%d'],initial = datetime.date.today())
   
    def clean(self):
        #call status clean method
        self.cleaned_data["avSonden"]=self.clean_Sonden()
        return self.cleaned_data
    
    def clean_Sonden(self):
        #valid if a value has been selected
        if self["avSonden"].value()!="":
            del self._errors["avSonden"]
        return self["avSonden"].value()
  
    def clean_start(self):
        start = self.cleaned_data['start']

        
        if start > datetime.date.today():
            raise forms.ValidationError(u'Start liegt in der Zukunft!')
        
        return start
    
    def clean_end(self):
        end = self.cleaned_data['end']
        
        if end > datetime.date.today():
            raise forms.ValidationError(u'Ende liegt in der Zukunft!')
        

        return end
    
