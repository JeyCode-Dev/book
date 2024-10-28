
from django.contrib import admin
from django.urls import path,include
from .views import *
app_name='pointvente'
urlpatterns = [
    path('', home,name='home'),
    path('check', check, name="check"),
    path('uncheck', uncheck, name="uncheck"),

    path('raprecette', raprecette,name='raprecette'),
    path('getrecettes', getrecettes,name='getrecettes'),
    # path('getboncommande', getboncommande,name='getboncommande'),
    path('deletearticle', deletearticle,name='deletearticle'),
    path('annulercommande', annulercommande,name='annulercommande'),
    path('getfacture', getfacture,name='getfacture'),

    path('getrecette', getrecette, name="getrecette"),
    path('gettiers', gettiers, name="gettiers"),


    path('valcmd', valcmd, name="valcmd"),
    path('getclienttake', getclienttake, name="getclienttake"),
    path('getclienttakeone', getclienttakeone, name="getclienttakeone"),
    path('getclienttakedetele', getclienttakedetele, name="getclienttakedetele"),



    path('getrecettecatsnack', getrecettecatsnack, name="getrecettecatsnack"),
    path('getrecettesnack', getrecettesnack, name="getrecettesnack"),
    path('gettabledispo', gettabledispo, name="gettabledispo"),
    path('client', client,name='client'),
    path('pointvente', pointvente,name='pointvente'),
    path('pointvente1', pointvente1,name='pointvente1'),
    path('pointvente2', pointvente2,name='pointvente2'),
    path('pointvente3', pointvente3,name='pointvente3'),
    path('pointvente4', pointvente4,name='pointvente4'),
    path('pointvente5', pointvente5,name='pointvente5'),
    path('sessionuser', sessionuser,name='sessionuser'),



    path('addrectempoaff', addrectempoaff, name="addrectempoaff"),
    path('addrectempo', addrectempo, name="addrectempo"),
    path('addrectempodel', addrectempodel, name="addrectempodel"),
    path('numerorectempodel', numerorectempodel, name="numerorectempodel"),
    path('validerrec', validerrec, name="validerrec"),
    # path('addition', addition, name="addition"),

    path('commande', commande, name="commande"),
    path('cuisine', impression, name="cuisine"),
    path('bar', bar, name="bar"),
    path('cuisinetempo', cuisinetempo, name="cuisinetempo"),
    path('prosnack', prosnack, name="prosnack"),
    path('catprosnack', catprosnack, name="catprosnack"),
    path('reimprimer', reimprimer,name='reimprimer'),
    path('validation', validation,name='validation'),
    path('annulation', annulation,name='annulation'),
    path('transferttable', transferttable,name='transferttable'),
    path('transfertserveur', transfertserveur,name='transfertserveur'),
    path('transfertcompte', transfertcompte,name='transfertcompte'),
    path('transfertproduit', transfertproduit,name='transfertproduit'),
    path('synthesepointvente', synthesepointvente,name='synthesepointvente'),
    path('profit', profit,name='profit'),
    path('pointventeliste', pointventeliste,name='pointventeliste'),
    path('liste', liste,name='liste'),
    ]
