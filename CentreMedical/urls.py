from django.urls import path
from .views import *
app_name = 'centremedical'

urlpatterns = [
    path('création/produit', produit, name='createproduit'),
    path('création/patient', CreationPatient, name='createpatient'),
    path('création/consultation', Consult, name='consultation'),
    path('création/ordonance', Ordonance, name='ordonance'),
    path('getpatient/consult', GetConsultPatient, name='getconsultpatient'),
    path('insert/data', InsertDate, name='insertdata'),
    path('pharmatie', Pharmacie, name="pharmatie"),
    path('getpatient', getPatient, name="getPatient"),
    path('getfacture', getfacture, name="getfacture")
]
