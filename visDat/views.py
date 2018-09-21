from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.core import serializers

from django.contrib.auth.decorators import login_required

from .models import Sonde, Messwert
from .forms import date_choice
from .resources import SondeResource, MesswertResource

import json as js
import pandas as pd

@login_required
def index(request):
    latest_Measurement = Messwert.objects.filter(Serial__owned_by__Kundennummer = request.user.nutzer.KundenAdmin.Kundennummer).order_by('-Date')[:3]
    
    form = date_choice(currentUserID = request.user.nutzer.KundenAdmin.Kundennummer)
    subsetData = Sonde.objects.filter(owned_by__Kundennummer = request.user.nutzer.KundenAdmin.Kundennummer)
    
    request.session['modTyp'] = str(subsetData.model)
    
    gotData = False

    
    if request.method == 'POST':
        form = date_choice(request.POST,currentUserID = request.user.nutzer.KundenAdmin.Kundennummer)
        startDate = request.POST.get("start")
        endDate = request.POST.get("end")
        
        subsetData = Messwert.objects.filter(Serial__Serial=request.POST.get("avSonden")).filter(Date__range=(startDate,endDate)).order_by('Date')
        request.session['modTyp'] = str(subsetData.model)
        
        
        request.session['subsetData'] = serializers.serialize('json',subsetData)
        request.session['startDate'] = startDate
        request.session['endDate'] = endDate
        request.session['Serial'] = request.POST.get("avSonden")

        if subsetData.exists():
            gotData = True
            

            
    else:
        form = date_choice(currentUserID = request.user.nutzer.KundenAdmin.Kundennummer)
        
    if gotData == True:
        context = {
                'latest_Measurement': latest_Measurement,
                'form': form,
                'qs_results':subsetData,
                'gotData': gotData,
                }
    else:
        context = {
            'latest_Measurement': latest_Measurement,
            'qs_results':subsetData,
            'form': form,
            'gotData': gotData,
         } 

    return render(request,'visDat/index.html',context)


def exportData(request):
    endDate = request.session.get('endDate')
    startDate = request.session.get('startDate')
    avSerial = request.session.get('Serial') 
    
    modTyp = request.session['modTyp']
    
    print(modTyp)
    if modTyp == "<class 'visDat.models.Sonde'>":
        queryset = Sonde.objects.filter(owned_by__Kundennummer = request.user.nutzer.KundenAdmin.Kundennummer).filter(Serial=avSerial).filter(Date__range=(startDate,endDate)).order_by('Date')
        data = SondeResource().export(queryset)
    else:
        queryset = Messwert.objects.filter(Serial__Serial=avSerial).filter(Date__range=(startDate,endDate)).order_by('Date')
        data = MesswertResource().export(queryset)
        
    response = HttpResponse(data.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Messwerte.csv"'
    return response
    

def renderData(request):

    endDate = request.session.get('endDate')
    startDate = request.session.get('startDate')
    avSerial = request.session.get('Serial') 
    
    dat = Messwert.objects.filter(Serial__Serial=avSerial).filter(Date__range=(startDate,endDate)).order_by('Date').values_list('Date','Temperature','Pressure')
    dates = []
    values = []
    meas = []
    
    for item  in dat:
        values.append(item[1])
        meas.append("Temperature")
        values.append(item[2])
        meas.append("Pressure")
        
        for i in range(2):
            dates.append(item[0])
            
    df = pd.DataFrame({'Date':dates,'Meas':meas,'Value':values})
    jsonDf = df.to_json(index=False, orient='table')
   
    
    subsetData = request.session.get('subsetData')   
    d = js.loads(jsonDf)
  
    return JsonResponse(d,safe=False)


