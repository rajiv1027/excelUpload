import os
from geopy.geocoders import Nominatim
from django.views.static import serve
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
from tablib import Dataset
import pandas as pd

geolocator = Nominatim(user_agent="excelUpload")

# Create your views here.


def read_excel(fileHandle):

    finalData = {'Address': [], 'longitude': [], 'latitude': []}
    # Read excel sheet
    dataset = Dataset()
    excel_data = dataset.load(fileHandle.read())
    for data in excel_data:
        address = data[0]
        #Get location by address
        location = geolocator.geocode(address)
        longitude = location.longitude
        latitude = location.latitude
        finalData['Address'].append(address)
        finalData['longitude'].append(longitude)
        finalData['latitude'].append(latitude)
    return finalData


def excel(request):

    if "GET" == request.method:
        print('GET ')
        return render(request, 'upload_form.html', {})
    else:
        fileHandle = request.FILES['excel_file']
        if str(fileHandle).split('.')[-1] not in ['xlsx', 'xls']:
            messages.info(request, 'File format is wrong, Please upload an excel sheet.')
            return render(request, 'upload_form.html', {})
        returnData = read_excel(fileHandle)

        filename = 'Address_lo_lat.xlsx'
        filePath = os.path.join(settings.MEDIA_ROOT, filename)
        df = pd.DataFrame(returnData, columns=['Address', 'longitude', 'latitude'])
        df.to_excel(filePath, index=False, header=True)
        # download excel sheet
        return serve(request, os.path.basename(filePath),
                     os.path.dirname(filePath))
