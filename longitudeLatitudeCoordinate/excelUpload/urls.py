from django.urls import path, include
from . import views

app_name='excelUpload'

urlpatterns = [
    path('', views.excel, name='excel')
]
