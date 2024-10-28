import math

import json
from django.conf import settings
from django.contrib import messages
import shortuuid as shortuuid
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,permission_required
from django.db.models import Sum, F, Value, Count, Q,CharField

from django.db.models.functions import Concat
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.db import IntegrityError, transaction
from datetime import datetime, timedelta
import os
import random
import string

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_POST
from reportlab.graphics.barcode import code39
from barcode import EAN13
from barcode.writer import ImageWriter
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Image as img, Spacer, Paragraph, Table, TableStyle

from django.template.defaulttags import register
from .models import *
from parametrage.models import CategorieArticle

from pyreportjasper import JasperPy

@login_required
@register.filter
def to_and(value):
    try:
        return value.replace(" ","")
    except:
        return ""

@login_required
@register.filter
def to_and_prix(value):
    try:
        return str(value).replace(",",".")
    except:
        return ""

@login_required
@register.filter
def to_and_icon(value):
    list_icon=[
        "ADA",
        "ADC",
        "AEON",
        "AMP",
        "ANC",
        "ARCH",
        "ARDR",
        "ARK",
        "AUR",
        "BANX",
        "BAT",
        "BAY",
        "BC",
        "BCN",
        "BFT",
        "BRK",
        "BRX",
        "BSD",
        "BTA",
        "BTC",
        "BCH",
        "BTCD",
        "BTM",
        "BTS",
        "CLAM",
        "CLOAK",
        "DAO",
        "DASH",
        "DCR",
        "DCT",
        "DGB",
        "DGD",
        "DGX",
        "DMD",
        "DOGE",
        "EMC",
        "EOS",
        "ERC",
        "ETC",
        "ETH",
        "FC2",
        "FCT",
        "FLO",
        "FRK",
        "FTC",
        "GAME",
        "GBYTE",
        "GDC",
        "GEMZ",
        "GLD",
        "GNO",
        "GNT",
        "GOLOS",
        "GRC",
        "GRS",
        "HEAT",
        "ICN",
        "IFC",
        "INCNT",
        "IOC",
        "IOTA",
        "JBS",
        "KMD",
        "KOBO",
        "KORE",
        "LBC",
        "LDOGE",
        "LISK",
        "LTC",
        "MAID",
        "MCO",
        "MINT",
        "MONA",
        "MRC",
        "MSC",
        "MTR",
        "MUE",
        "NBT",
        "NEO",
        "NEOS",
        "NEU",
        "NLG",
        "NMC",
        "NOTE",
        "NVC",
        "NXT",
        "OK",
        "OMG",
        "OMNI",
        "OPAL",
        "PART",
        "PIGGY",
        "PINK",
        "PIVX",
        "POT",
        "PPC",
        "QRK",
        "QTUM",
        "RADS",
        "RBIES",
        "RBT",
        "RBY",
        "RDD",
        "REP",
        "RISE",
        "SALT",
        "SAR",
        "SCOT",
        "SDC" ,
        "SIA" ,
        "SJCX" ,
        "SLG" ,
        "SLS" ,
        "SNRG" ,
        "START" ,
        "STEEM" ,
        "STR" ,
        "STRAT" ,
        "SWIFT" ,
        "SYNC" ,
        "SYS" ,
        "TRIG" ,
        "TX" ,
        "UBQ" ,
        "UNITY" ,
        "USDT" ,
        "VIOR" ,
        "VNL" ,
        "VPN" ,
        "VRC" ,
        "VTC" ,
        "WAVES" ,
        "XCP" ,
        "XAI" ,
        "XBS" ,
        "XEM" ,
        "XMR" ,
        "XPM" ,
        "XRP" ,
        "XTZ" ,
        "XVG" ,
        "XZC" ,
        "YBC" ,
        "ZEC" ,
        "EIT" ,
    ]
    return random.choice(list_icon)
def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))
#####################################################################

def miseprixtempo(request):
    from django.conf import settings
    import pandas

    path=settings.BASE_DIR + '\\' + 'lushi.xlsx'
    #path=settings.BASE_DIR + '\\' + 'kin.xlsx'
    excel_data_df=pandas.read_excel(path,sheet_name='Feuil4')
    # col=excel_data_df.columns.ravel()
    #annee = Annee.objects.filter(etat=True).first()
    cmpteur=0
    s=None
    #location='1FIH'
    location='2FBM'
    for index, ex in excel_data_df.iterrows():
        inv=Finventaire.objects.filter(article__designation__iexact=ex['article'],location_id=location,periode='2020-12')
        if inv:
            inv.update(prix_vente_u=str(ex['prix']).replace(",","."))
            #print(index)


    return HttpResponse("1")
def ImportExcel(request):
    from django.conf import settings
    import pandas

    path=settings.BASE_DIR + '\\' + 'lushi.xlsx'
    #path=settings.BASE_DIR + '\\' + 'kin.xlsx'
    excel_data_df=pandas.read_excel(path,sheet_name='Feuil3')
    # col=excel_data_df.columns.ravel()
    #annee = Annee.objects.filter(etat=True).first()
    cmpteur=0
    s=None
    #location='1FIH'
    location='2FBM'
    idservice=2
    periode='2021-02'
    cmpp=Farticle.objects.filter(LOCATION_id=location).count()
    for index, ex in excel_data_df.iterrows():

    #     if Farticle.objects.filter(designation__iexact=ex['article']):
    #         cmp+=1
    #         print(ex['article'])
    #     else:
    #         print("--------------------------------------------------"+ex['article'])
    # print(cmp)



        # clss=Fclasse.objects.get(designation=ex['Classe'])
        # fam=Ffamilles.objects.get(designation=ex['Famille'])
        #
        #

        # if cmp:
        #     cmp=cmp.first().article
        # else:

        # print(cmp)


        art=Farticle.objects.filter(designation__iexact=ex['article'],LOCATION_id=location)
        if art:
            pass
        elif str(ex['article'])=="nan":
            pass
        else:
            cmpp+=1
            cmp=location+str(cmpp)#location,famille,classe,compteur
            physique=0

            if str(ex['physique']).replace(",",".")!="nan":
                physique=str(ex['physique']).replace(",",".")

            Farticle.objects.create(
                article=cmp,
                famille_id=idservice,
                classe_id=0,
                designation=str(ex['article']).replace("'","\'"),
                prix_achat=str(ex['prix']).replace(",","."),
                pa=str(ex['prix']).replace(",","."),
                prix_vente=str(ex['prix']).replace(",","."),
                emballagee_id='UNIT',
                emballageu_id='UNIT',
                quantitee=1,
                quantiteu=1,
                categorie=1,
                qte_stock_minimal=1,
                TYPEARTICLE='LOCAL',
                LOCATION_id=location
            )
            #_________prix
            # TempoPrix.objects.create(
            #     article_id=cmp,
            #     dateop=datetime.today().date(),
            #     emb1_id='UNIT',
            #     emb2_id='UNIT',
            #     prix1=str(ex['prix']).replace(",","."),
            #     prix2=str(ex['prix']).replace(",","."),
            #     devise='USD',
            #     etat=True,
            #     user_id=request.user.id,)
            #_________inventaire
            Finventaire.objects.create(
                periode=periode,
                location_id=location,
                article_id=cmp,
                emballage_e='UNIT',
                emballage_u='UNIT',
                quantitee=physique,
                quantiteu=physique,
                qte_u_phys=physique,
                qte_u_log=0,
                prix_vente_u=str(ex['prix']).replace(",","."),
                qte_u_ecart=float(physique)-float(0),
                dateinventaire=datetime.today().date(),
                ndateinvent=str(datetime.today().date()).replace("-","").replace("/",""),
            )
            #----------------------mouvement
            Fmvts.objects.create(
                location_id=location,
                periode=periode,
                datemvt=datetime.today().date(),
                ndatemvt=str(datetime.today().date()).replace("-", "").replace("/", ""),
                # requisition=i.serielivraison.serielivraison,
                document="INV" + str(cmp),
                ajustement_id="INV",
                # tiers_id=i.serielivraison.commande.tiers.tiers,
                article_id=cmp,
                emballage_id='UNIT',
                qte_entree=physique,
                qteunit_entree=physique,
                prix_achat=0,
                prix_vente=0,
                # devise="",
                # txchange="",
                codeuser_id=request.user.id,
            )




            

    return HttpResponse("T")
#


####################################################################


def miseajourprix(article,emb,prix,floc,devise=None,tx=None):
    pa=0
    art = Farticle.objects.filter(article=article, emballagee_id=emb)
    art2 = Farticle.objects.filter(article=article, emballageu_id=emb)
    art3 = Farticle.objects.filter(article=article, emballagea=emb)

    if art:

        if devise is not None and devise == 'CDF':
            pa = float(prix) / float(str(tx).replace(",", "."))
        else:
            pa = float(prix)

        art = art.first()
        if art.prix_achat!=pa:
            art.libemballagee=str(datetime.today().date())
        art.prix_achat = pa
        art.prix_vente = pa + ((float(pa) * float(floc.cptetaxe)) / 100)

        art.save()
    elif art2:
        if devise is not None and devise == 'CDF':
            pa = float(prix) / float(str(tx).replace(",", "."))
        else:
            pa = float(prix)
        art2 = art2.first()
        if art2.pa != pa:
            art2.libemballagee = str(datetime.today().date())
        art2.pa = pa

        art2.prix_vente_cdf = pa + ((float(pa) * float(floc.cptetaxev)) / 100)
        art2.save()
    elif art3:
        if devise is not None and devise == 'CDF':
            pa = float(prix) / float(str(tx).replace(",", "."))
        else:
            pa = float(prix)
        art3 = art3.first()
        if art3.old_prix_achat != pa:
            art3.libemballagee = str(datetime.today().date())
        art3.old_prix_achat = pa
        art3.old_prix_vente = pa + ((float(pa) * float(floc.cptechf)) / 100)
        art3.save()
    return pa

def getstock(request):
    t=getstockproduit(request.session.get('idlocationuser'), request.GET.get('article'), request.GET.get('emb'))
    return JsonResponse({'qte':t},safe=False)

def getstockproduit(location,produit,emballage,veri=0):
    # ----------------------------------
    
    pro=Farticle.objects.get(article=produit)



    b1 = 0
    b2 = 0
    b3 = 0

    c1 = 0
    c2 = 0
    c3 = 0
    b1 = Fmvts.objects.filter(location_id=location, article_id=produit, emballage_id=pro.emballagee_id,
                             ajustement_id__in=("ACH", "PAT", "TRFR", "INV")).aggregate(Sum("qte_entree")).get(
        "qte_entree__sum")
    if b1 is None:  # entrer
        b1 = 0


    c1 = Fmvts.objects.filter(location_id=location, article_id=produit, emballage_id=pro.emballagee_id,
                             ajustement_id__in=("VTE", "TRTO", "FACT", "DECL", "INV")).aggregate(
        Sum("qte_sortie")).get("qte_sortie__sum")
    if c1 is None:  # sortie
        c1 = 0


    b2 = Fmvts.objects.filter(location_id=location, article_id=produit, emballage_id=pro.emballageu_id,
                             ajustement_id__in=("ACH", "PAT", "TRFR", "INV")).aggregate(Sum("qte_entree")).get(
        "qte_entree__sum")
    if b2 is None:  # entrer
        b2 = 0


    c2 = Fmvts.objects.filter(location_id=location, article_id=produit, emballage_id=pro.emballageu_id,
                             ajustement_id__in=("VTE", "TRTO", "FACT", "DECL", "INV")).aggregate(
        Sum("qte_sortie")).get("qte_sortie__sum")
    if c2 is None:  # sortie
        c2 = 0



    b3 = Fmvts.objects.filter(location_id=location, article_id=produit, emballage_id=pro.emballagea,
                             ajustement_id__in=("ACH", "PAT", "TRFR", "INV")).aggregate(Sum("qte_entree")).get(
        "qte_entree__sum")
    if b3 is None:  # entrer
        b3 = 0


    c3 = Fmvts.objects.filter(location_id=location, article_id=produit, emballage_id=pro.emballagea,
                             ajustement_id__in=("VTE", "TRTO", "FACT", "DECL", "INV")).aggregate(
        Sum("qte_sortie")).get("qte_sortie__sum")
    if c3 is None:  # sortie
        c3 = 0




    if veri == 0:

        art = Farticle.objects.filter(article=produit, emballagee_id=emballage)
        art2 = Farticle.objects.filter(article=produit, emballageu_id=emballage)
        art3 = Farticle.objects.filter(article=produit, emballagea=emballage)
        if art:

            if pro.quantitee != 0:
                b=b1+((pro.quantiteu/pro.quantitee)*b2)+((pro.quantitea/pro.quantitee)*b3)
                c=c1+((pro.quantiteu/pro.quantitee)*c2)+((pro.quantitea/pro.quantitee)*c3)
            else:
                b = b1
                c = c1 
            tot=b-c
            # tot1+=((pro.quantiteu*tot2)*(pro.quantitea/pro.quantitee))+(tot3*(pro.quantitea/pro.quantitee))
            return int(tot)
        elif art2:
            if pro.quantiteu != 0:
                b = b2 + ((pro.quantitea/pro.quantiteu) * b3) + ((pro.quantitee/pro.quantiteu) * b1)
                c = c2 + ((pro.quantitea/pro.quantiteu) * c3) + ((pro.quantitee/pro.quantiteu) * c1)
            else:
                b = b2
                c = c2

            tot = b - c
            return int(tot)
        elif art3:

            b = b3 + ((pro.quantiteu) * b2) + ((pro.quantitee) * b1)
            c = c3 + ((pro.quantiteu) * c2) + ((pro.quantitee) * c1)
            tot = b - c
            return tot
        else:
            return 0
    else:
        b = b1 + ((pro.quantiteu / pro.quantitee) * b2) + ((pro.quantitea / pro.quantitee) * b3)
        c = c1 + ((pro.quantiteu / pro.quantitee) * c2) + ((pro.quantitea / pro.quantitee) * c3)
        tot = b - c # 1 emballage
        reste0=int(tot) # 1 emballage

        if pro.quantiteu!=0:
            tot1 = (tot - int(tot))*(pro.quantitee/pro.quantiteu)  # 2 emballage
        else:
            tot1 = (tot - int(tot))  # 2 emballage
        reste1=int(tot1)  # 2 emballage

        if pro.quantitea != 0:
            tot2=(tot1 - int(tot1))*(pro.quantiteu/pro.quantitea)  # 3 emballage
        else:
            tot2=(tot1 - int(tot1))  # 3 emballage
        reste2 = int(tot2)  # 3 emballage
        return [reste0,reste1,reste2]


    # cmpr=0
    #
    # b = Fmvts.objects.filter(location_id=location, article_id=produit, emballage_id=emballage,
    #                          ajustement_id__in=("ACH", "PAT", "TRFR", "INV")).aggregate(Sum("qte_entree")).get("qte_entree__sum")
    # if b is None:  # entrer
    #     b = 0
    # else:
    #     cmpr=1
    #
    # c = Fmvts.objects.filter(location_id=location, article_id=produit,emballage_id=emballage,
    #                          ajustement_id__in=("VTE", "TRTO", "FACT", "DECL", "INV")).aggregate(Sum("qte_sortie")).get("qte_sortie__sum")
    # if c is None:  # sortie
    #     c = 0
    # else:
    #     cmpr=1
    #
    # tot = b- c
    #
    # if veri==1:
    #     if cmpr==1:
    #         return tot
    #     else:
    #         return -1
    # else:
    #     return tot


def colr(x,y,z):
    return (x/255,y/255,z/255)


@login_required
def listappro(request):
    a = Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser'))
    d = []
    for i in a:
        s = getstockproduit(request.session.get('idlocationuser'), i.article, i.emballagee_id)
        if s <= i.qte_stock_minimal:
            d.append({"article":i.designation,"qte":str(s)})
    context={
        "matieres":d
    }
    return render(request, 'gestionstock/listappro.html',context)
def home(request):

    # x1=Fmvts.objects.filter(location_id=request.session.get('idlocationuser'),ajustement_id='FACT',article__isnull=True,ndatemvt=str(
    #                     str(datetime.today().date()).replace("-", "").replace("/", ""))).aggregate(
    #     t=Sum(F("qte_sortie") * F("prix_achat"))).get('t')
    # if x1 is None:
    #     x1=0

    x2tot=0
    numerore=""
    x2=Fmvts.objects.filter(location_id=request.session.get('idlocationuser'),ajustement_id='FACT',article__isnull=True,ndatemvt=str(
                        str(datetime.today().date()).replace("-", "").replace("/", "")))
    for ic in x2:
        if ic.requisition==numerore:
            pass
        else:
            ic.requisition = numerore
            x2tot+=ic.prix_total

    # a=Farticle.objects.filter(fmvts__article__isnull=False,LOCATION_id=request.session.get('idlocationuser')).order_by('article').annotate(Count('article'))
    # d=0
    # dd=0
    # for i in a:
    #     s=getstockproduit(request.session.get('idlocationuser'),i.article,i.emballagee_id,1)
    #     if s==-1:
    #         pass
    #     elif s<=i.qte_stock_minimal:
    #         d+=1

    t = Fmvts.objects.filter(location=request.session.get('idlocationuser'), ajustement='FACT',
                             ndatemvt=str(str(datetime.today().date()).replace("-", "").replace("/",""))).values('destination').annotate(
        t=Sum((F("qte_sortie") * F("prix_vente"))-(((F("qte_sortie") * F("prix_vente"))*F("remise"))/100))).order_by('destination')


    context={
        # "totartapro":d,
        # "totapro":dd,
        "totproduit":Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser')).count(),
        # "totclientnon":Ftiers.objects.filter(typetiers="1").count(),
        # "totarticl":Recettes.objects.all().count(),
        # "totcmd":(x2tot),
        "totfac": t,
        # "totprix":Ftiers.objects.filter(typetiers="0").count(),
        # "totproalerte":Farticle.objects.filter(etat=0).count(),
    }

    #print(request.user.LocationUser_set.user)

    if not request.user.is_authenticated: 
        context['location']=Flocation.objects.all().order_by("designation")

    return render(request, 'main.html',context)


def check(request):

    username = request.POST['username']
    password = request.POST['pass']
    user = authenticate(username=username, password=password)
    if user is not None:
        veri = user.affectation.filter(location=request.POST.get('location'))
        print(veri)
        if veri:
            request.session['locationuser']=veri.first().designation
            request.session['idlocationuser']=veri.first().location
            login(request, user)


    return redirect(reverse('gestionstock:home'))



    

def uncheck(request):
    del request.session['locationuser']
    del request.session['idlocationuser']
    logout(request)
    return redirect(reverse('gestionstock:home'))

#
# def situation(request):
#     context = {"location": Flocation.objects.all().order_by('designation'),
#                }
#
#     if request.method=="POST":
#         from .cnx import connexion
#
#         cnxQ = connexion()  # creer instance connexion
#         cnxQ2 = connexion()  # creer instance connexion
#         cnxQ3 = connexion()  # creer instance connexion
#         cnxQ4 = connexion()  # creer instance connexion
#         cnxQ5 = connexion()  # creer instance connexion
#
#         dbx = str(request.POST.get('dtd')).replace('-', '')
#         dbfinx = str(request.POST.get('dtf')).replace('-', '')
#
#         Titretyle = ParagraphStyle(
#             name='titre',
#             fontName='Helvetica-Bold',
#             fontSize=14,
#             textColor='DarkGray',
#             borderPadding=(2, 2, 7, 2),
#             borderWidth=0,
#             borderColor='Gray',
#             alignment=TA_CENTER
#         )
#
#         Paragraphstyle = ParagraphStyle(
#             name='MyDoctorHeader',
#             fontName='Helvetica',
#             fontSize=12,
#             textColor='Teal',
#             leading=10,
#             alignment=TA_LEFT
#         )
#         Headerstyle = ParagraphStyle(
#             name='headesr',
#             fontName='Helvetica-Bold',
#             fontSize=15,
#             textColor='Gray',
#             # borderPadding=(2, 2, 7, 2),
#             # borderWidth=0,
#             # borderColor='Gray',
#             alignment=TA_LEFT
#         )
#
#         styles = getSampleStyleSheet()
#         styleN = styles["BodyText"]
#         styleN.alignment = TA_LEFT
#
#         styleB = styles["Normal"]
#         styleB.alignment = TA_RIGHT
#
#         elements = []
#
#         header = Paragraph("""
#                                                                    <b>%s</b><br/>
#                                                                    %s<br/>
#                                                                    <i>%s</i><br/>
#                                                                    """ % (
#             "République Democratique du Congo", "Miltex SARLU", "Kinshasa/Gombe"),
#                            style=Headerstyle)
#         #
#         tab = Table([[header]], style=[('VALIGN', (0, 0), (-1, -1), 'TOP')],
#                     colWidths=[25 * cm, 3 * cm])
#
#         elements.append(tab)
#
#         elements.append(Spacer(1, 20))
#
#         rc = cnxQ.Selection([
#             """
# select * from(select  FMVTS.DESIGNATION,ARTICLE
# from FMVTS
# where FMVTS.LOCATION ='{}' and convert(Float,NDATEMVT)>=convert(Float,'{}')  and convert(Float,NDATEMVT)<=convert(Float,'{}') group by FMVTS.DESIGNATION,ARTICLE) as FMVTS order by DESIGNATION
#                """.format(request.POST.get('location'),
#                           dbx, dbfinx)])
#         txt = 'STATISTIQUE COUT MOYEN PONDERE LOCATION {}<br/><br/><u>DU {} AU {}</u>'.format(request.POST.get('location'), request.POST.get('dtd'), request.POST.get('dtf'))
#         data = [[Paragraph(txt,
#                            style=Titretyle)]]
#         titre = Table(data)
#
#         elements.append(titre)
#         elements.append(Spacer(1, 20))
#
#         temp = ['#', 'Désignation', 'PUR', 'QTR', 'OP', 'PUE', 'QTE', 'VE', 'QTS', 'VS', 'QI', 'PUI', 'VI']
#         diver_table = [temp]
#
#         if rc:
#
#             libpro = ''
#             libstringDate = ''
#             libstringPro = ''
#             MVT = ''
#
#             libstringDatex = ''
#             libstringProx = ''
#
#             libdate = 0
#             compteur = 1
#             sommepue = 0.0
#             sommeqte = 0.0
#             sommeqts = 0.0
#
#             onepue = 0.0
#             oneqte = 0.0
#             oneqts = 0.0
#
#             tempo = []
#
#
#             for i in rc:
#
#                 tempo = []
#
#
#                 qteARTICLE = 0
#                 prixARTICLE = 0
#                 EmballageART1 = ''
#                 EmballageART2 = ''
#
#                 ####################################################qteinuit
#
#                 rqtART = cnxQ5.Selection([
#                     """
#                     SELECT QUANTITEE,EMBALLAGEE,EMBALLAGEU,PRIXREVIENTGRO FROM dbo.FARTICLE where ARTICLE='{}'
#                     """.format(str(i[1]))
#
#                 ])
#
#                 if rqtART:
#                     for b in rqtART:
#                         qteARTICLE = b[0]
#                         EmballageART1 = b[1]
#                         EmballageART2 = b[2]
#                         prixARTICLE = b[3]
#
#                 ####################################################
#                 # # # historik
#                 if qteARTICLE != 0:
#
#                     rctempoE = cnxQ2.Selection(["""select sum(totpu) as totpu,sum(valori) as valori,sum(qte) as qte,sum(cmp) as cmp,NDATEMVT,sum(qteS) as qteS from(
#         select totpu,0 as valori,qte,cmp,NDATEMVT,'' as qteS from(
#         select qte,pu/cmp as totpu,cmp,NDATEMVT from(
#
#         select sum(qte) as qte,sum(pu) as pu,COUNT(*) as cmp,NDATEMVT
#
#         from(
#         select FMVTS.QTEUNIT_ENTREE/{} as qte,FMVTS.PRIX_ACHAT as pu,convert(Float,LEFT(Ltrim(rtrim(str(NDATEMVT))),6)) as NDATEMVT,DATEMVT,FMVTS.MVT,'' as qteS
#         from FMVTS
#         where convert(Float,NDATEMVT)<convert(Float,'{}')
#         and  ARTICLE='{}' and LOCATION ={}
#         and FMVTS.AJUSTEMENT='ACH'
#
#         union
#
#         select FMVTS.QTEUNIT_ENTREE/{} as qte,{} as pu,convert(Float,LEFT(Ltrim(rtrim(str(NDATEMVT))),6)) as NDATEMVT,DATEMVT,FMVTS.MVT,FMVTS.QTEUNIT_SORTIE/{} as qteS
#         from FMVTS
#         where convert(Float,NDATEMVT)<convert(Float,'{}')
#         and ARTICLE='{}' and LOCATION ={}
#         and FMVTS.AJUSTEMENT='INV' and FMVTS.QTEUNIT_ENTREE is NOT NULL and FMVTS.QTEUNIT_SORTIE is NOT NULL
#
#
#         )as FMVTS group by NDATEMVT
#
#         )as FMVTS
#         )as FMVTS
#
#         union
#
#         select 0 as totpu ,0 as valori,0 as qte,0 as cmp,NDATEMVTE as NDATEMVT,sum(qteS) as qteS
#
#         from(
#         select FMVTS.QTEUNIT_SORTIE/{} as qteS,convert(Float,LEFT(Ltrim(rtrim(str(NDATEMVT))),6)) as NDATEMVTE
#         from FMVTS
#         where convert(Float,NDATEMVT)<convert(Float,'{}')
#         and ARTICLE='{}' and LOCATION ={}
#         and AJUSTEMENT ='TRTO'
#
#         )as FMVTS group by NDATEMVTE
#
#
#         )as FMVTS group by NDATEMVT
#                                 """.format(qteARTICLE,
#                                            dbx, str(i[1]), request.POST.get('location'), qteARTICLE, prixARTICLE, qteARTICLE, dbx,
#                                            str(i[1]), request.POST.get('location'), qteARTICLE, dbx, str(i[1]), request.POST.get('location'))])
#
#                     valorso = 0
#                     valoren = 0
#                     pue = 0
#                     qts = 0
#                     qte = 0
#                     qti = 0
#                     valorii = 0
#                     Rpue = 0
#                     Rqti = 0
#
#                     for tempg in rctempoE:
#
#                         if not tempg[0] is None:
#
#                             if pue == 0:
#                                 pue = (pue + tempg[0])  # 0
#
#                                 qte = tempg[2] + qte  # 0
#
#                                 valoren = pue * qte  # 0000000
#                                 qts = tempg[5]  #
#                                 valorso = pue * qts  # 000000
#                                 qti = qte - qts
#                                 valorii = qti * pue  # 000000
#                             else:
#                                 pue = (pue + tempg[0]) / 2
#
#                                 qte = tempg[2] + qti
#
#                                 valoren = pue * qte
#                                 qts = tempg[5]
#                                 valorso = pue * qts
#                                 qti = qte - qts
#                                 valorii = qti * pue
#
#                             Rpue = pue
#                             Rqti = qti
#
#                     # for tempg in rctempoS:
#                     #     if not tempg[0] is None:
#                     #         qts = tempg[0]
#
#                     # if pue==0:
#                     #     compteur=0
#                     #     diver_table.append(
#                     #         [len(diver_table), 'Rep.', i[0], compteur, "%.2f" % pue, "%.2f" % qti,
#                     #          "%.2f" % valorii, 0, 0,
#                     #          0, 0, 0])
#                     # else:
#                     #     diver_table.append(
#                     #     [len(diver_table), 'Rep.', i[0], compteur, "%.2f" % pue, "%.2f" % qti, "%.2f" % valorii, 0, 0,
#                     #      0, 0, 0])
#
#                     # # # historik
#                     if pue == 0:
#                         compteur = 0
#                         tempo.append(len(diver_table))
#                         tempo.append(i[0])
#                         tempo.append("%.2f" % pue)
#                         tempo.append("%.2f" % qti)
#
#                     else:
#                         tempo.append(len(diver_table))
#                         tempo.append(i[0])
#                         tempo.append("%.2f" % pue)
#                         tempo.append("%.2f" % qti)
#
#                     # # # historik
#
#                     # # # Fin Periode
#
#                     rqt = cnxQ4.Selection([
#                         """
# select sum(totpu) as totpu,sum(valori) as valori,sum(qte) as qte,sum(cmp) as cmp,NDATEMVT,sum(qteS) as qteS from(
# select totpu,0 as valori,qte,cmp,NDATEMVT,'' as qteS from(
# select qte,pu/cmp as totpu,cmp,NDATEMVT from(
#
# select sum(qte) as qte,sum(pu) as pu,COUNT(*) as cmp,NDATEMVT
#
# from(
# select FMVTS.QTEUNIT_ENTREE/{} as qte,FMVTS.PRIX_ACHAT as pu,convert(Float,LEFT(Ltrim(rtrim(str(NDATEMVT))),6)) as NDATEMVT,DATEMVT,FMVTS.MVT,'' as qteS
# from FMVTS
# where convert(Float,NDATEMVT)>=convert(Float,'{}')  and convert(Float,NDATEMVT)<=convert(Float,'{}')
# and  ARTICLE='{}' and LOCATION ={}
# and FMVTS.AJUSTEMENT='ACH'
#
# union
#
# select FMVTS.QTEUNIT_ENTREE/{} as qte,{} as pu,convert(Float,LEFT(Ltrim(rtrim(str(NDATEMVT))),6)) as NDATEMVT,DATEMVT,FMVTS.MVT,FMVTS.QTEUNIT_SORTIE/{} as qteS
# from FMVTS
# where convert(Float,NDATEMVT)>=convert(Float,'{}')  and convert(Float,NDATEMVT)<=convert(Float,'{}')
# and ARTICLE='{}' and LOCATION ={}
# and FMVTS.AJUSTEMENT='INV' and FMVTS.QTEUNIT_ENTREE is NOT NULL and FMVTS.QTEUNIT_SORTIE is NOT NULL
#
#
# )as FMVTS group by NDATEMVT
#
# )as FMVTS
# )as FMVTS
#
# union
#
# select 0 as totpu ,0 as valori,0 as qte,0 as cmp,NDATEMVTE as NDATEMVT,sum(qteS) as qteS
#
# from(
# select FMVTS.QTEUNIT_SORTIE/{} as qteS,convert(Float,LEFT(Ltrim(rtrim(str(NDATEMVT))),6)) as NDATEMVTE
# from FMVTS
# where convert(Float,NDATEMVT)>=convert(Float,'{}')  and convert(Float,NDATEMVT)<=convert(Float,'{}')
# and ARTICLE='{}' and LOCATION ={}
# and AJUSTEMENT ='TRTO'
#
# )as FMVTS group by NDATEMVTE
#
#
# )as FMVTS group by NDATEMVT
#                     """.format(qteARTICLE,
#                                dbx, dbfinx, str(i[1]), request.POST.get('location'), qteARTICLE, prixARTICLE, qteARTICLE, dbx, dbfinx,
#                                str(i[1]), request.POST.get('location'), qteARTICLE, dbx, dbfinx, str(i[1]), request.POST.get('location'))])
#
#                     if rqt:
#
#                         valorsow = 0
#                         valorenw = 0
#                         puew = 0
#                         qtsw = 0
#                         qtew = 0
#                         qtiw = 0
#                         valoriiw = 0
#                         cmpx = 0
#
#                         for tempg in rqt:
#                             if not tempg[0] is None:
#
#                                 if Rpue == 0:
#                                     puew = (Rpue + tempg[0])
#                                 else:
#                                     puew = (Rpue + tempg[0]) / 2
#
#                                 qtew = tempg[2] + Rqti
#                                 cmpx += tempg[3]
#                                 valorenw = puew * qtew
#                                 qtsw = tempg[5]
#                                 valorsow = puew * qtsw
#                                 qtiw = qtew - qtsw
#                                 Rqti = qtiw
#                                 Rpue = puew
#                                 valoriiw = qtiw * puew
#
#                         tempo.append(cmpx)
#                         tempo.append("%.2f" % puew)
#                         tempo.append("%.2f" % qtew)
#                         tempo.append("%.2f" % valorenw)
#                         tempo.append("%.2f" % qtsw)
#                         tempo.append("%.2f" % valorsow)
#                         tempo.append("%.2f" % qtiw)
#                         tempo.append("%.2f" % puew)
#                         tempo.append("%.2f" % valoriiw)
#                         diver_table.append(tempo)
#
#             medstable = Table(diver_table, repeatRows=1,
#                               colWidths=[1 * cm, 4 * cm, 2 * cm])
#             medstable.setStyle(TableStyle([
#
#                 ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
#                 ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
#                 ('FONTSIZE', (0, 0), (-1, -1), 7),
#                 ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
#                 ('BACKGROUND', (0, 0), (-1, 0), colr(119, 136, 153)),
#                 ('GRID', (0, 0), (-1, 0), 0.5, '#CFEAD4'),
#                 ('INNERGRID', (0, 0), (-1, 0), 0.5, '#CFEAD4'),
#
#                 ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
#                 ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#
#                 ('GRID', (0, 0), (-1, -1), 0.5, '#CFEAD4'),
#                 ('INNERGRID', (0, 0), (-1, -1), 0.5, '#CFEAD4'),
#             ]))
#             elements.append(medstable)
#
#
#         doc = SimpleDocTemplate("situation.pdf", pagesize=landscape(letter), rightMargin=20, leftMargin=20,
#                                 topMargin=20, bottomMargin=20, allowSplitting=1,
#                                 )
#
#         # doc.build(elements,onFirstPage=drawPageFrame)
#         doc.multiBuild(elements)
#
#
#         with open("situation.pdf") as pdf:
#             response = HttpResponse(pdf, content_type='application/pdf')
#             response['Content-Disposition'] = 'inline;filename=rapportnew.pdf'
#             return response
#
#         return response
#         # os.open('output.pdf')
#
#         return HttpResponse(str(request.POST.get('dtd')).replace('-', ''))
#
#
#     return render(request, 'gestionstock/situation.html', context)
#
# def rapportentreecmp(request):
#
#     if request.method=="POST":
#
#
#         fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#         input_file = fn+"\{}".format("rapportentreestock.jrxml")
#
#         # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")
#
#         output =fn+"\media"
#
#         con = {
#             'driver': 'generic',
#             'jdbc_driver':'net.sourceforge.jtds.jdbc.Driver',
#             'jdbc_url':'jdbc:sqlserver://localhost:1433;databaseName='+ str(settings.DATABASES['default']['NAME']),
#             'jdbc_dir':fn,
#             'username': settings.DATABASES['default']['USER'],
#             'password': settings.DATABASES['default']['PASSWORD']
#             # 'host': 'localhost',
#             # 'database': 'STOCKPRO',
#             # 'port': '1433'
#         }
#
#         jasper = JasperPy()
#         # jasper.compile("D:/test1.jrxml")
#         # jasper.path_executable = "D:/JasperStarter/bin/"
#
#
#
#         jasper.process(
#             input_file,
#             output,
#             format_list=["pdf"],
#             db_connection=con,
#             parameters={'taux':request.POST.get('taux'),'liblocation':request.POST.get('liblocation'),'location':request.POST.get('location'),'dd': '{}'.format(request.POST.get('dtd')),'df': '{}'.format(request.POST.get('dtf')),'ddl': '{}'.format(str(request.POST['dtd']).replace("-","")),'dfl':'{}'.format(str(request.POST['dtf']).replace("-",""))},
#             locale='en_US'
#         )
#
#
#         return HttpResponse("true")
#     context = {"location": Flocation.objects.all().order_by('designation'),}
#
#     return render(request, 'gestionstock/rapportentreecmp.html', context)
#
#
# def rapportsortiecmp(request):
#
#     if request.method=="POST":
#
#
#         fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#         input_file = fn+"\{}".format("rapportsortiestock.jrxml")
#
#         # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")
#
#         output =fn+"\media"
#
#         con = {
#             'driver': 'generic',
#             'jdbc_driver':'net.sourceforge.jtds.jdbc.Driver',
#             'jdbc_url':'jdbc:sqlserver://localhost:1433;databaseName='+ str(settings.DATABASES['default']['NAME']),
#             'jdbc_dir':fn,
#             'username': settings.DATABASES['default']['USER'],
#             'password': settings.DATABASES['default']['PASSWORD']
#             # 'host': 'localhost',
#             # 'database': 'STOCKPRO',
#             # 'port': '1433'
#         }
#
#         jasper = JasperPy()
#         # jasper.compile("D:/test1.jrxml")
#         # jasper.path_executable = "D:/JasperStarter/bin/"
#
#
#
#         jasper.process(
#             input_file,
#             output,
#             format_list=["pdf"],
#             db_connection=con,
#             parameters={'taux':request.POST.get('taux'),'liblocation':request.POST.get('liblocation'),'location':request.POST.get('location'),'dd': '{}'.format(request.POST.get('dtd')),'df': '{}'.format(request.POST.get('dtf')),'ddl': '{}'.format(str(request.POST['dtd']).replace("-","")),'dfl':'{}'.format(str(request.POST['dtf']).replace("-",""))},
#             locale='en_US'
#         )
#
#
#         return HttpResponse("true")
#     context = {"location": Flocation.objects.all().order_by('designation'),}
#
#     return render(request, 'gestionstock/rapportsortiecmp.html', context)
#
#
# def inventairecmp(request):
#
#     if request.method=="POST":
#
#
#         fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#         input_file = fn+"\{}".format("rapportinventairestock.jrxml")
#
#         # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")
#
#         output =fn+"\media"
#
#         con = {
#             'driver': 'generic',
#             'jdbc_driver':'net.sourceforge.jtds.jdbc.Driver',
#             'jdbc_url':'jdbc:sqlserver://localhost:1433;databaseName='+ str(settings.DATABASES['default']['NAME']),
#             'jdbc_dir':fn,
#             'username': settings.DATABASES['default']['USER'],
#             'password': settings.DATABASES['default']['PASSWORD']
#             # 'host': 'localhost',
#             # 'database': 'STOCKPRO',
#             # 'port': '1433'
#         }
#
#         jasper = JasperPy()
#         # jasper.compile("D:/test1.jrxml")
#         # jasper.path_executable = "D:/JasperStarter/bin/"
#
#
#
#         jasper.process(
#             input_file,
#             output,
#             format_list=["pdf"],
#             db_connection=con,
#             parameters={'taux':request.POST.get('taux'),'liblocation':request.POST.get('liblocation'),'location':request.POST.get('location'),'dd': '{}'.format(request.POST.get('dtd')),'ddl': '{}'.format(str(request.POST['dtd']).replace("-",""))},
#             locale='en_US'
#         )
#
#
#         return HttpResponse("true")
#     context = {"location": Flocation.objects.all().order_by('designation'),}
#
#     return render(request, 'gestionstock/rapportinventairecmp.html', context)
#
#
#
# def rapportentreecmpc(request):
#
# 	context = {"location": Flocation.objects.all().order_by('designation'),
# 			   # "magasinc": Magasin.objects.filter(depotcentral=True).order_by('designation'),
# 			   # "magasins": Magasin.objects.filter(depotcentral=False).order_by('designation'),
# 			   }
#
# 	# if request.method == "POST":
#     #     pass
# 		# from cnx import connexion
#         # return HttpResponse('')
#         # return HttpResponse(str(request.POST.get('dtd')).replace('-', ''))
#
#
#
#
# 		# try:
# 		# 	with transaction.atomic():
# 		# 		fac=Facture.objects.filter(numfac=request.POST.get('numfac'),user=request.user)
# 		# 		if fac:
# 		# 			pass
# 		# 		else:
# 		# 			fac=Facture.objects.create(
# 		# 				numfac=request.POST.get('numfac'),
# 		# 				datefac=datetime.today(),
# 		# 				user=request.user)
#
# 		# 		b= FactureArticle.objects.filter(facture__numfac=request.POST.get('numfac'),article_id=request.POST.get('article'))
# 		# 		if b:
#
# 		# 			b.update(
# 		# 				commentaire=request.POST.get(''),
# 		# 				magasinc_id=request.POST.get('magasinc'),
# 		# 				magasins_id=request.POST.get('magasins'),
# 		# 				mode="t",
# 		# 				qte=request.POST.get('qtet'),
# 		# 				taux=request.POST.get(''),
# 		# 			)
# 		# 		else:
# 		# 			FactureArticle.objects.create(
# 		# 			facture=fac,
# 		# 			article_id=request.POST.get('article'),
# 		# 			commentaire=request.POST.get(''),
# 		# 			magasinc_id=request.POST.get('magasinc'),
# 		# 			magasins_id=request.POST.get('magasins'),
# 		# 			mode = "t",
# 		# 			qte = request.POST.get('qtet'),
# 		# 			taux=request.POST.get(''),
# 		# 		)
# 		# 		return JsonResponse(
# 		# 			{"msg": "Opération effectuée",
# 		# 			 "id": "1"}, safe=False)
# 		# except Exception as e:
# 		# 	return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)
# 	# context['numfac'] = "FAC" + str(Facture.objects.count() + 1) + str(datetime.today().date()).replace("-", "")
# 	return render(request, 'gestionstock/rapportentreecmp.html', context)

@login_required
@permission_required('gestionstock.Produit',raise_exception=True)
def produit(request):


    if request.method == "POST":
        try:
            with transaction.atomic():
                if 'delete_' in request.POST:
                    Farticle.objects.filter(article=request.POST.get('idpro')).delete()
                else:

                    art=Farticle.objects.filter(article=request.POST.get('idpro'),LOCATION_id=request.session.get('idlocationuser'))

                    #pa=miseajourprix(f.article.article,f.emballage_id,request.POST.get('prix'),floc)


                    if request.POST.get('devise') == 'CDF':
                        pa = float(request.POST.get('pa1')) / float(str(request.POST.get('taux')).replace(",", "."))
                    else:
                        pa = float(request.POST.get('pa1'))

                    prix_achat_petit=pa/float(request.POST.get('qte1'))


                    if art:
                        art.update(
                            famille_id=request.POST.get('famille'),
                            classe_id=request.POST.get('classe'),


                            quantitee=request.POST.get('qte1'),
                            quantitea=0 if request.POST.get('qte3') == '' else request.POST.get('qte3'),
                            # quantiteu=0 if request.POST.get('qte2') == '' else request.POST.get('qte2'),
                            quantiteu=1,

                            emballagea=None if request.POST.get('emballage3') == '' else request.POST.get('emballage3'),
                            emballagee_id=request.POST.get('emballage1'),
                            emballageu_id=None if request.POST.get('emballage2') == '' else request.POST.get(
                                'emballage2'),

                            prix_vente=request.POST.get('pv1'),
                            prix_vente_cdf=0 if request.POST.get('pv2') == '' else request.POST.get('pv2'),
                            old_prix_vente=0 if request.POST.get('pv3') == '' else request.POST.get('pv3'),

                            prix_achat=request.POST.get('pa1'),
                            pa=prix_achat_petit, #if request.POST.get('pa2') == '' else request.POST.get('pa2'),
                            old_prix_achat=0 if request.POST.get('pa3') == '' else request.POST.get('pa3'),

                            qte_stock_minimal=request.POST.get('seuil'),

                            designation=request.POST.get('designation'),
                            # categorie=request.POST.get('categorie'),

                        )
                    else:
                        # recnumart = Farticle.objects.all().order_by('-article')[:1]

                        artx = Farticle.objects.filter(designation=str(request.POST.get('designation')).upper(),LOCATION_id=request.session.get('idlocationuser'))
                        if artx:
                            return JsonResponse({"msg": "Opération non effectuée .Produit existe déjà.", "id": "0"}, safe=False)

                        # recnumart = Farticle.objects.all()
                        recnumart = shortuuid.ShortUUID(alphabet="0123456789")
                        recnumart = recnumart.random(length=8)

                        f=Farticle.objects.filter(article=recnumart)
                        if f:
                            return JsonResponse({"msg": "Opération non effectuée .Error Connexion Recommencer SVP.", "id": "0"},
                                                safe=False)

                        # if recnumart:
                        #     # recnumart = recnumart.first().article
                        #     recnumart = recnumart.count()
                        #     # recnumart = int(''.join(filter(str.isdigit, recnumart)))
                        # else:
                        #     recnumart = 0
                        # # recnumart = str(request.session.get('idlocationuser'))+str(recnumart + 1)
                        # recnumart =  str(recnumart + 1)

                        # print(request.POST)
                        Farticle.objects.create(
                            article=recnumart,
                            famille_id=request.POST.get('famille'),
                            classe_id=request.POST.get('classe'),
                            # numcompte=request.POST.get('numcpt'),
                            #categorie=request.POST.get('categorie'),
                            #reference=datetime.today().date(),
                            qte_stock_minimal=request.POST.get('seuil'),

                            quantitee=request.POST.get('qte1'),
                            quantitea=0 if request.POST.get('qte3') == '' else request.POST.get('qte3'),
                            # quantiteu=0 if request.POST.get('qte2') == '' else request.POST.get('qte2'),
                            quantiteu=1,

                            emballagea=None if request.POST.get('emballage3') == '' else request.POST.get('emballage3'),
                            emballagee_id=request.POST.get('emballage1'),
                            emballageu_id=None if request.POST.get('emballage2') == '' else request.POST.get('emballage2'),

                            prix_vente=request.POST.get('pv1'),
                            prix_vente_cdf=0 if request.POST.get('pv2') == '' else request.POST.get('pv2'),
                            old_prix_vente=0 if request.POST.get('pv3') == '' else request.POST.get('pv3'),

                            prix_achat=request.POST.get('pa1'),
                            pa=prix_achat_petit,#if request.POST.get('pa2') == '' else request.POST.get('pa2'),
                            old_prix_achat=0 if request.POST.get('pa3') == '' else request.POST.get('pa3'),
                            # categorie=request.POST.get('categorie'),
                            designation=str(request.POST.get('designation')).upper()
                            ,LOCATION_id=request.session.get('idlocationuser')
                        )

                return JsonResponse(
                    {"msg": "Opération effectuée",
                    "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée "+str(e), "id": "0"}, safe=False)


    if 'q' in request.GET:
        p=0
        artists = Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser'),designation=str(request.GET.get("q")).strip())[:3]
        # artists = Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser'),designation__icontains=request.GET.get("q"))[:3]
        if artists:
            p=1
        else:
            p=0
        # html = render_to_string(
        #     template_name="gestionstock/artists-results-partial.html", context={"artists": artists}
        # )
        # if request.GET.get('q')=='':
        #     html=''
        # data_dict = {"html_from_view": html}
        # return JsonResponse(data=data_dict, safe=False)
        return JsonResponse({'data':str(p)}, safe=False)
    context = {
        "classe": Fclasse.objects.all().order_by('designation'),
        "famille": Ffamilles.objects.all().order_by('designation'),
        "emballage": Femballage.objects.all().order_by('designation'),
        "floc": Flocation.objects.get(location=request.session.get('idlocationuser')),
            }
    return render(request, 'gestionstock/produit.html', context)


@login_required
@permission_required('gestionstock.Produit',raise_exception=True)
def travaux(request):

    if request.method == "POST":

        for i in Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser')):
            i.prixachgro=arondir(math.trunc(float(i.prix_vente) * float(i.LOCATION.txchange)))
            i.prixvtegrosusd=arondir(math.trunc(float(i.prix_vente_cdf) * float(i.LOCATION.txchange)))
            i.prixvtegroscdf=arondir(math.trunc(float(i.old_prix_vente) * float(i.LOCATION.txchange)))
            i.save()

        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if 'full' in request.POST:
            input_file = os.path.join(fn,"etiquettePrix.jrxml")
        else:
            input_file = os.path.join(fn,"etiquette.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = os.path.join(fn, 'media')

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': f"jdbc:jtds:sqlserver://localhost/{settings.DATABASES['default']['NAME']}",
            'jdbc_dir': fn,
            'username': settings.DATABASES['default']['USER'],
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKPRO',
            # 'port': '1433'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"

        if 'full' in request.POST:
            parameters = {'liblocation': request.session.get('locationuser'),
                          'idlocation': request.session.get('idlocationuser'), 'dt': request.POST.get('dt')}
        #     parameters = {
        #                   'libdate1': request.POST.get('date1'), 'libdate2': request.POST.get('date2'),
        #                   'iddate1': str(request.POST.get('date1')).replace("/", "").replace("-", ""),
        #                   'iddate2': str(request.POST.get('date2')).replace("/", "").replace("-", "")}
        else:
            parameters = {'liblocation': request.session.get('locationuser'), 'idlocation': request.session.get('idlocationuser')}

        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters=parameters,
            locale='en_US'
        )


        return HttpResponse("true")


    context = {

    }
    return render(request, 'gestionstock/travaux.html', context)

@login_required
def fichiers(request):

    if request.method == "POST":
        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")



        if request.POST.get('code')=="1":
            input_file = os.path.join(fn, "emballage.jrxml")
        elif request.POST.get('code')=="2":
            input_file = os.path.join(fn, "classe.jrxml")
        elif request.POST.get('code')=="3":
            input_file = os.path.join(fn, "famille.jrxml")
        elif request.POST.get('code')=="4":
            input_file = os.path.join(fn, "magasin.jrxml")
        elif request.POST.get('code')=="5":
            input_file = os.path.join(fn, "articles.jrxml")
            


        

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = os.path.join(fn, 'media')
        
        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': f"jdbc:jtds:sqlserver://localhost/{settings.DATABASES['default']['NAME']}",
            'jdbc_dir': fn,
            'username': settings.DATABASES['default']['USER'],
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKPRO',
            # 'port': '1433'
        }
        
        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"


        if request.POST.get('code')=="4":
            jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            # parameters={'liblocation':request.session.get('locationuser')},
            locale='en_US'
            )
        elif request.POST.get('code')=="5":
            jasper.process(
                input_file,
                output,
                format_list=["pdf"],
                db_connection=con,
                parameters={'liblocation':request.session.get('locationuser'),'idlocation':request.session.get('idlocationuser')},
                locale='en_US'
            )
        else:
            jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            # parameters={'taux':request.POST.get('taux'),'liblocation':request.POST.get('liblocation'),'location':request.POST.get('location'),'dd': '{}'.format(request.POST.get('dtd')),'df': '{}'.format(request.POST.get('dtf')),'ddl': '{}'.format(str(request.POST['dtd']).replace("-","")),'dfl':'{}'.format(str(request.POST['dtf']).replace("-",""))},
            locale='en_US'
            )


        return HttpResponse("true")
    return render(request, 'gestionstock/fichiers.html')



@login_required
@permission_required('gestionstock.Delai_Inventaire',raise_exception=True)
def delaiinventaire(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                detail = DelaiInventaire.objects.filter(periode=request.POST.get('periode'),location_id=request.session.get('idlocationuser'))
                if detail:
                    detail.update(
                        # datedebutop=request.POST.get('datedebu'),
                        datefinop=request.POST.get('detefin'),
                        location_id=request.session.get('idlocationuser'),
                    )
                else:
                    DelaiInventaire.objects.create(
                    # datedebutop=request.POST.get('datedebu'),
                    datefinop=request.POST.get('detefin'),
                    periode=request.POST.get('periode'),
                    location_id=request.session.get('idlocationuser'),
                )

                return JsonResponse(
                    {"msg": "Opération effectuée",
                    "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée "+str(e), "id": "0"}, safe=False)
    context={
        "delai":DelaiInventaire.objects.filter(location_id=request.session.get('idlocationuser')).order_by("-periode")
    }
    return render(request, 'gestionstock/delaiinventaire.html',context)


@login_required
@permission_required('gestionstock.Bon_Commande_rapport',raise_exception=True)
def rapboncommande(request):
    if request.method == "POST":

        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = os.path.join(fn,"boncommande.jrxml")
        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = os.path.join(fn, 'media')

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': f"jdbc:jtds:sqlserver://localhost/{settings.DATABASES['default']['NAME']}",
            'jdbc_dir': fn,
            'username': settings.DATABASES['default']['USER'],
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKPRO',
            # 'port': '1433'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"

        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters={'numbon': request.POST.get('bon')},
            locale='en_US'
        )
        return HttpResponse("true")
    context={
        "bon":Fcommande.objects.filter(etatcde="1",location_id=request.session.get('idlocationuser')).order_by("-commande")
    }
    return render(request, 'gestionstock/rapboncommande.html',context)



@login_required
@permission_required('gestionstock.Bon_Livraison_rapport',raise_exception=True)
def rapbonlivraison(request):
    context={
        "bon":Flivraison.objects.filter(commande__location_id= request.session.get('idlocationuser'),etatliv="1").order_by('-serielivraison'),
    }
    return render(request, 'gestionstock/bonlivraison.html',context)







def periode(request):

   

    if request.method == "GET":
  
        try:
            with transaction.atomic():

                articles=Farticle.objects.filter(LOCATION_id=request.GET.get('location'))
                for i in articles:
                    one=Finventaire.objects.filter(periode=request.GET.get('periode'),location_id=request.GET.get('location'),
                                                   article_id=i.article)
                    if one:
                        pt=one.first().qte_u_phys
                        qte = getstockproduit(request.GET.get('location'), i.article,
                                              i.article.emballageu)
                        one.update(
                            qte_u_log=qte,
                            qte_u_ecart=float(pt) - float(qte)

                        )
                # else:
                #     qte=getstockproduit(request.session.get('idlocationuser'),request.POST.get('produit'),request.POST.get('emballage2'))
                #     Finventaire.objects.create(
                #         periode=request.POST.get('periode'),
                #         location_id=request.session.get('idlocationuser'),
                #         article_id=request.POST.get('produit'),
                #         emballage_e=request.POST.get('emballage1'),
                #         emballage_u=request.POST.get('emballage2'),
                #         quantitee=request.POST.get('qte1'),
                #         quantiteu=request.POST.get('qte2'),
                #         qte_u_phys=request.POST.get('qte2'),
                #         qte_u_log=qte,
                #         qte_u_ecart=float(request.POST.get('qte2'))-float(qte),
                #         dateinventaire=request.POST.get('dateop'),
                #         ndateinvent=str(request.POST.get('dateop')).replace("-","").replace("/",""),
                #     )

                # recnumart = Farticle.objects.all().order_by('-article')[:1]
                # if recnumart:
                #     recnumart = recnumart.first().article
                #     recnumart = int(''.join(filter(str.isdigit, recnumart)))
                # else:
                #     recnumart = 0
                # recnumart = recnumart + 1
                # Farticle.objects.create(
                #     article=recnumart,
                #     famille_id=request.POST.get('famille'),
                #     classe_id=request.POST.get('classe'),
                #     numcompte=request.POST.get('numcpt'),
                #     categorie=request.POST.get('taxe'),
                #     qte_stock_minimal=request.POST.get('seuil'),
                #     quantitee=request.POST.get('qte'),
                #     quantiteu=request.POST.get('qte1'),
                #     designation=request.POST.get('designation'),
                #     emballagee_id=request.POST.get('emballage1'),
                #     emballageu_id=request.POST.get('emballage2')
                # )

                return JsonResponse(
                    {"msg": "Opération effectuée",
                    "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée "+str(e), "id": "0"}, safe=False)
    return HttpResponse("true")

@login_required
@permission_required('gestionstock.Saisie_Stock',raise_exception=True)
def saisirphysique(request):



    if request.method == "POST":
  
        try:
            with transaction.atomic():

                delai=DelaiInventaire.objects.filter(periode=request.POST.get('periode'),location_id=request.session.get('idlocationuser'),
                                                   datefinop__gte=datetime.today().date())

                if delai:
                    pass
                else:
                    return JsonResponse(
                        {"msg": "Le délai de la saisie est expiré.",
                         "id": "0"}, safe=False)

                one=Finventaire.objects.filter(periode=request.POST.get('periode'),location_id=request.session.get('idlocationuser'),
                                               article_id=request.POST.get('produit'),emballage_e=request.POST.get('emballage'))

                # resultat1 = 0
                # resultat2 = 0
                # pa = 0
                # prix_achat_petit = 0
                #
                # art = Farticle.objects.filter(article=request.POST.get('produit'), emballagee_id=request.POST.get('emballage1'))
                #
                #
                # if art:
                #     resultat1 = float(request.POST.get('qte1'))
                #     resultat2 = float(request.POST.get('qte2')) / float(art.first().quantiteu)  # quantiteu
                #     resultat1=resultat1+resultat2
                #
                #
                #     if request.POST.get('devise') == 'CDF':
                #         pa = float(request.POST.get('pa')) / float(str(request.POST.get('taux')).replace(",", "."))
                #     else:
                #         pa = float(request.POST.get('pa'))
                #     prix_achat_petit = pa / float(art.first().quantiteu)

                pa = 0

                art = Farticle.objects.filter(article=request.POST.get('produit'), emballagee_id=request.POST.get('emballage'))
                art2 = Farticle.objects.filter(article=request.POST.get('produit'), emballageu_id=request.POST.get('emballage'))
                art3 = Farticle.objects.filter(article=request.POST.get('produit'), emballagea=request.POST.get('emballage'))

                st = 0

                qte = getstockproduit(request.session.get('idlocationuser'), request.POST.get('produit'),
                                      request.POST.get('emballage'), 1)
                if art:
                    pa = float(art.first().prix_achat)
                    st=qte[0]
                elif art2:
                    pa = float(art2.first().pa)
                    st = qte[1]
                elif art3:
                    pa = float(art3.first().old_prix_achat)
                    st = qte[2]

                if one:


                    one.update(

                        emballage_e=request.POST.get('emballage'),
                        # emballage_u=request.POST.get('emballage2'),
                        # quantitee=request.POST.get('qte1'),
                        # quantiteu=request.POST.get('qte2'),
                        qte_u_phys=request.POST.get('qte'),
                        qte_u_log=st,
                        prix_achat_u=pa,
                        prix_vente_u=0,
                        qte_u_ecart=float(request.POST.get('qte')) - float(st),
                        dateinventaire=request.POST.get('dateop'),
                        ndateinvent=str(request.POST.get('dateop')).replace("-", "").replace("/", ""),
                    )
                else:

                    Finventaire.objects.create(
                        periode=request.POST.get('periode'),
                        location_id=request.session.get('idlocationuser'),
                        article_id=request.POST.get('produit'),
                        emballage_e=request.POST.get('emballage'),
                        # emballage_u=request.POST.get('emballage2'),
                        # quantitee=request.POST.get('qte1'),
                        # quantiteu=request.POST.get('qte2'),
                        qte_u_phys=request.POST.get('qte'),
                        qte_u_log=st,
                        prix_achat_u=pa,
                        prix_vente_u=0,
                        qte_u_ecart=float(request.POST.get('qte'))-float(st),
                        dateinventaire=request.POST.get('dateop'),
                        ndateinvent=str(request.POST.get('dateop')).replace("-","").replace("/",""),
                    )


                # arti=Farticle.objects.get(article=request.POST.get('produit'))
                # arti.prix_achat = pa
                # arti.pa = prix_achat_petit
                # arti.save()


                return JsonResponse(
                    {"msg": "Opération effectuée",
                    "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée "+str(e), "id": "0"}, safe=False)

    if 'inventaire' in request.GET:
        rec = Finventaire.objects.filter(location_id=request.session.get('idlocationuser'),periode=request.GET.get('periode')).values(
          "emballage_e", "qte_u_phys",'article_id')
        rec = list(rec)
        return JsonResponse({'data': rec}, safe=False)

    if 'periode' in request.GET:

        rec2=Finventaire.objects.filter(location_id=request.session.get('idlocationuser'),periode=request.GET.get('periode')).order_by('article_id')

        list_d = []
        tot = '0'
        totid = '0'
        datafull={}
        for i in rec2:
            totid=i.article.article



            art = Farticle.objects.filter(article=i.article.article,
                                          emballagee_id=i.emballage_e)
            art2 = Farticle.objects.filter(article=i.article.article,
                                           emballageu_id=i.emballage_e)
            art3 = Farticle.objects.filter(article=i.article.article,
                                           emballagea=i.emballage_e)

            if tot!=i.article.article:
                if tot!='0':
                    xx = Farticle.objects.get(article=tot)

                    if 'emballagee_id' not in datafull:

                        if xx.emballagee_id is not None:
                            datafull['emballagee_id'] = xx.emballagee_id
                            datafull['qt1'] = '0'
                        else:
                            datafull['emballagee_id'] =None
                            datafull['qt1'] =None

                    if 'emballageu_id' not in datafull:

                        if xx.emballageu_id is not None:
                            datafull['emballageu_id'] =xx.emballageu_id
                            datafull['qt2'] = '0'
                        else:
                            datafull['emballageu_id'] = None
                            datafull['qt2'] = None

                    if 'emballagea' not in datafull:

                        if xx.emballagea is not None:
                            datafull['emballagea'] = xx.emballagea
                            datafull['qt3'] = '0'
                        else:
                            datafull['emballagea'] = None
                            datafull['qt3'] = None



                    list_d.append(datafull)
                    datafull = {}


            if art:
                emb =  art.first().emballagee_id
                datafull['emballagee_id'] = emb
                datafull['qt1'] = i.qte_u_phys

            elif art2:
                emb =  art2.first().emballageu_id
                datafull['emballageu_id'] = emb
                datafull['qt2'] = i.qte_u_phys

            elif art3:
                emb =  art3.first().emballagea
                datafull['emballagea'] = emb
                datafull['qt3'] = i.qte_u_phys

            datafull['article'] = i.article.article
            datafull['designation'] = i.article.designation
            tot = i.article.article




        if len(rec2)>0:
            xx = Farticle.objects.get(article=totid)

            if 'emballagee_id' not in datafull:

                if xx.emballagee_id is not None:
                    datafull['emballagee_id'] = xx.emballagee_id
                    datafull['qt1'] = '0'
                else:
                    datafull['emballagee_id'] = None
                    datafull['qt1'] = None

            if 'emballageu_id' not in datafull:

                if xx.emballageu_id is not  None:
                    datafull['emballageu_id'] = xx.emballageu_id
                    datafull['qt2'] = '0'
                else:
                    datafull['emballageu_id'] = None
                    datafull['qt2'] = None

            if 'emballagea' not in datafull:

                if xx.emballagea is not None:
                    datafull['emballagea'] = xx.emballagea
                    datafull['qt3'] = '0'
                else:
                    datafull['emballagea'] = None
                    datafull['qt3'] = None
            list_d.append(datafull)

        rec = Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser')).exclude(article__in=rec2.values('article_id')).annotate(
            qt1=Value('0', output_field=CharField()),
            qt2=Value('0', output_field=CharField()),
            qt3=Value('0', output_field=CharField()),
        ).values(
            "article", "designation", "emballagee_id","emballageu_id", "emballagea","qt1","qt2","qt3").order_by('designation')
        data = list(rec)
        data.extend(list_d)
        # print(data)
        return JsonResponse({'data': data}, safe=False)


    context = {
        # "taux": Flocation.objects.get(location=request.session.get('idlocationuser')).txchange,
        # "article": Farticle.objects.all().order_by('designation'),
        "periode": DelaiInventaire.objects.filter(location_id=request.session.get('idlocationuser'), ).order_by(
            '-periode'),
    }
    return render(request, 'gestionstock/saisirphysique.html', context)

@login_required
@permission_required('gestionstock.Rap_Prise_Inventaire',raise_exception=True)
def rapportlistepriseinventaire(request):
    if request.method == "POST":
        detail = DelaiInventaire.objects.filter(periode=request.POST.get('periode'),
                                                location_id=request.session.get('idlocationuser'))
        if detail:
            detail.update(
                # datedebutop=request.POST.get('datedebu'),
                datefinop=request.POST.get('detefin'),
                location_id=request.session.get('idlocationuser'),
            )
        else:
            DelaiInventaire.objects.create(
                # datedebutop=request.POST.get('datedebu'),
                datefinop=request.POST.get('detefin'),
                periode=request.POST.get('periode'),
                location_id=request.session.get('idlocationuser'),
            )
        # delai=DelaiInventaire.objects.filter(periode=request.POST.get('periode'),location_id=request.session.get('idlocationuser'),
        #                                    datefinop__lte=datetime.today())

        # if delai:
        #     pass
        # else:
        #     return HttpResponse("Cette Période n'est pas valide.")


        # art=Farticle.objects.all()
        # for i in art:
        #     tot=getstockproduit(request.session.get('idlocationuser'),i.article,i.emballageu_id)
        #     finven=Finventaire.objects.filter(location_id=request.session.get('idlocationuser')
        #                                       ,periode=request.POST.get('periode'),article_id=i.article)
        #     if finven:
        #         pass
        #     else:
        #         Finventaire.objects.create(location_id=request.session.get('idlocationuser')
        #                                    , periode=request.POST.get('periode'), article_id=i.article)
        #
        #     return

        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = os.path.join(fn,"priselisteinventaire.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = os.path.join(fn, 'media')

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': f"jdbc:jtds:sqlserver://localhost/{settings.DATABASES['default']['NAME']}",
            'jdbc_dir': fn,
            'username': settings.DATABASES['default']['USER'],
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKPRO',
            # 'port': '1433'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"

        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters={'idlocation': request.session.get('idlocationuser'),'liblocation': request.session.get('locationuser'),'periode':request.POST.get('periode')},
            locale='en_US'
        )

        return HttpResponse("true")
    return render(request, 'gestionstock/priseinventaire.html')


@login_required
@permission_required('gestionstock.Rap_Inventaire',raise_exception=True)
def inventaire(request):
    if request.method == "POST":
        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = os.path.join(fn,"inventaire.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = os.path.join(fn, 'media')

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': f"jdbc:jtds:sqlserver://localhost/{settings.DATABASES['default']['NAME']}",
            'jdbc_dir': fn,
            'username': settings.DATABASES['default']['USER'],
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKPRO',
            # 'port': '1433'
        }

        # finv=Finventaire.objects.filter(periode=request.POST.get('periode'))
        # date1=""
        # ndate1=""
        # if finv:
        #     finv=finv.first()
        #     date1 = finv.dateinventaire
        #     ndate1 = finv.ndateinvent

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"
        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters={'liblocation': request.session.get('locationuser'),'periode':request.POST.get('periode'),'idlocation':request.session.get('idlocationuser')},
            locale='en_US'
        )
        return HttpResponse("true")
    return render(request, 'gestionstock/inventaire.html',context={"periode":DelaiInventaire.objects.filter(location_id=request.session.get('idlocationuser')).order_by("-periode")})


@login_required
@permission_required('gestionstock.Rap_Mvt_Produit',raise_exception=True)
def rapmvtproduit(request):
    if request.method == "POST":
        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = os.path.join(fn,"rapmvtproduit.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = os.path.join(fn, 'media')

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': f"jdbc:jtds:sqlserver://localhost/{settings.DATABASES['default']['NAME']}",
            'jdbc_dir': fn,
            'username': settings.DATABASES['default']['USER'],
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKPRO',
            # 'port': '1433'
        }


        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"
        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters={'emblib': request.POST.get('emblib'),'emb': request.POST.get('emb'),'libdate2': request.POST.get('date2'),'iddate2': str(request.POST.get('date2')).replace("/","").replace("-",""),'libdate1': request.POST.get('date1'),'iddate1': str(request.POST.get('date1')).replace("/","").replace("-",""),'liblocation': request.session.get('locationuser'),'produit':request.POST.get('produit'),'idlocation':request.session.get('idlocationuser')},
            locale='en_US'
        )
        return HttpResponse("true")
    return render(request, 'gestionstock/rapmvtproduit.html',context={"article":Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser')).order_by("designation")})


@login_required
@permission_required('gestionstock.Rap_Logique_Physique',raise_exception=True)
def rapportlogiquephysique(request):
    if request.method == "POST":

        # delai=DelaiInventaire.objects.filter(periode=request.POST.get('periode'),location_id=request.session.get('idlocationuser'),
        #                                    datefinop__lte=datetime.today())

        # if delai:
        #     pass
        # else:
        #     return HttpResponse("Cette Période n'est pas valide.")

        try:
            with transaction.atomic():
                pass
                # for lox in Flocation.objects.filter(location__in=('1FIM','2FBM')):
                #
                #     art=Farticle.objects.filter(LOCATION_id=lox.location)
                #     for i in art:
                #
                #         pero=Finventaire.objects.filter(periode=request.POST.get('periode'),location_id=lox.location)
                #         finn=Finventaire.objects.filter(article=i,periode=request.POST.get('periode'),location_id=lox.location)
                #         if finn:
                #             qte=getstockproduit(lox.location,i.article,i.emballageu_id)
                #             finn=finn.first()
                #             finn.qte_u_log=qte
                #             finn.qte_u_ecart=float(finn.qte_u_phys)-float(qte)
                #             finn.save()
                #
                #
                #         else:
                #             qte=getstockproduit(lox.location,i.article,i.emballageu_id)
                #             Finventaire.objects.create(
                #                 periode=request.POST.get('periode'),
                #                 location_id=lox.location,
                #                 article=i,
                #                 emballage_e=i.emballagee_id,
                #                 emballage_u=i.emballageu_id,
                #                 quantitee=qte,
                #                 quantiteu=qte,
                #                 qte_u_phys=float(0),
                #                 qte_u_log=qte,
                #                 prix_vente_u=i.pa,
                #                 qte_u_ecart=float(0)-float(qte),
                #                 dateinventaire=pero.first().dateinventaire,
                #                 ndateinvent=pero.first().ndateinvent,
                #             )





        except Exception as e:
            print( str(e))

        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if 'id' in request.POST:
            input_file = os.path.join(fn,"logiquephysiquefull.jrxml")
        else:
            input_file = os.path.join(fn,"logiquephysique.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = os.path.join(fn, 'media')

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': f"jdbc:jtds:sqlserver://localhost/{settings.DATABASES['default']['NAME']}",
            'jdbc_dir': fn,
            'username': settings.DATABASES['default']['USER'],
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKPRO',
            # 'port': '1433'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"
        supo=int(str(request.POST.get('periode')).split("-")[1])-1
        if supo<=0:
            supo=12
            anne=int(str(request.POST.get('periode')).split("-")[0])-1
            supo=str(anne)+str(supo)+"31"
        else:
            if supo<10:
                supo=str("0")+str(supo)
                anne=int(str(request.POST.get('periode')).split("-")[0])
                supo=str(anne)+str(supo)+"31"

        print(supo,str(request.POST.get('periode')).replace("-","")+"31",str(request.POST.get('periode')).replace("-","")+"01")
        jasper.process(
            input_file,
            output,
            format_list=["pdf","xlsx"],
            db_connection=con,
            parameters={'liblocation': request.session.get('locationuser'),'idperiode':str(request.POST.get('periode')).replace("-","")+"01",'idperiode2':str(request.POST.get('periode')).replace("-","")+"31",'idperiode3':supo,'periode':request.POST.get('periode'),'idlocation':request.session.get('idlocationuser')},
            locale='en_US'
        )

        return HttpResponse("true")
    return render(request, 'gestionstock/raplogiquephysique.html',context={"periode":DelaiInventaire.objects.filter(location_id=request.session.get('idlocationuser')).order_by("-periode")})


@login_required
@permission_required('gestionstock.Rap_Inve_Theori',raise_exception=True)
def rapinventairethéoriqueval(request):
    if request.method == "POST":

        # delai=DelaiInventaire.objects.filter(periode=request.POST.get('periode'),location_id=request.session.get('idlocationuser'),
        #                                    datefinop__lte=datetime.today())

        # if delai:
        #     pass
        # else:
        #     return HttpResponse("Cette Période n'est pas valide.")



        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = os.path.join(fn,"theoriqueval.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = os.path.join(fn, 'media')

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': f"jdbc:jtds:sqlserver://localhost/{settings.DATABASES['default']['NAME']}",
            'jdbc_dir': fn,
            'username': settings.DATABASES['default']['USER'],
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKPRO',
            # 'port': '1433'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"
        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters={'liblocation': request.session.get('locationuser'),'dateop':request.POST.get('dateop'),'iddateop':str(request.POST.get('dateop')).replace("/","").replace("-",""),'idlocation':request.session.get('idlocationuser')},
            locale='en_US'
        )


        return HttpResponse("true")
    return render(request, 'gestionstock/rapinventairethéoriqueval.html')


@login_required
@permission_required('gestionstock.Rap_Inve_Theori',raise_exception=True)
def rapinventairethéorique(request):
    if request.method == "POST":

        # delai=DelaiInventaire.objects.filter(periode=request.POST.get('periode'),location_id=request.session.get('idlocationuser'),
        #                                    datefinop__lte=datetime.today())

        # if delai:
        #     pass
        # else:
        #     return HttpResponse("Cette Période n'est pas valide.")



        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = os.path.join(fn,"theorique.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = os.path.join(fn, 'media')

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': f"jdbc:jtds:sqlserver://localhost/{settings.DATABASES['default']['NAME']}",
            'jdbc_dir': fn,
            'username': settings.DATABASES['default']['USER'],
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKPRO',
            # 'port': '1433'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"
        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters={'liblocation': request.session.get('locationuser'),'dateop':request.POST.get('dateop'),'iddateop':str(request.POST.get('dateop')).replace("/","").replace("-",""),'idlocation':request.session.get('idlocationuser')},
            locale='en_US'
        )


        return HttpResponse("true")
    return render(request, 'gestionstock/rapinventairethéorique.html')



@login_required
@permission_required('gestionstock.Mise_Stock_Inventaire',raise_exception=True)
def misestockinventaire(request):


    if request.method == "POST":

        delai=DelaiInventaire.objects.filter(periode=request.POST.get('periode'),location_id=request.session.get('idlocationuser'),
                                           datefinop__gte=datetime.today().date())

        if delai:
            pass
        else:
            return JsonResponse({"msg": "Cette Période n'est pas valide.", "id": "0"}, safe=False)



        try:
            with transaction.atomic():
                artx=Finventaire.objects.filter(periode=request.POST.get('periode'),
                                           location_id=request.session.get('idlocationuser'))
                for i in artx:
                    finvv=Finventaire.objects.filter(article=i.article,emballage_e=i.emballage_e,periode=request.POST.get('periode'),location_id=request.session.get('idlocationuser'))
                    if finvv:
                        finvv=finvv.first()
                        tx=finvv.location.txchange
                        tempo1 = Fmvts.objects.filter(ndatemvt=finvv.ndateinvent,
                                                      location_id=request.session.get('idlocationuser'),
                                                      article=finvv.article,emballage_id=finvv.emballage_e,
                                                      ajustement_id="INV", periode=request.POST.get('periode'))


                        if finvv.qte_u_ecart>=0:
                            if tempo1:
                                tempo1.update(
                                    # requisition=i.serielivraison.serielivraison,

                                    # tiers_id=i.serielivraison.commande.tiers.tiers,

                                    # quantite=i.qte_u_ecart,
                                    qte_entree=finvv.qte_u_ecart,
                                    # qteunit_entree=resultat2,
                                    prix_achat=finvv.prix_achat_u,
                                    # pa=prix_achat_petit,
                                    prix_vente=0,
                                    # devise="",
                                    txchange=tx,
                                    codeuser_id=request.user.id,
                                )
                            else:
                                Fmvts.objects.create(
                                location_id=request.session.get('idlocationuser'),
                                periode=finvv.periode,
                                bordereau=datetime.now().time(),
                                datemvt=finvv.dateinventaire,
                                ndatemvt=str(finvv.dateinventaire).replace("-", "").replace("/", ""),
                                requisition="INV" + str(finvv.periode),
                                document="INV" + str(finvv.compteur),
                                ajustement_id="INV",
                                # tiers_id=i.serielivraison.commande.tiers.tiers,
                                article=finvv.article,
                                emballage_id=finvv.emballage_e,
                                qte_entree=finvv.qte_u_ecart,
                                # qteunit_entree=resultat2,
                                prix_achat=finvv.prix_achat_u,
                                # pa=prix_achat_petit,
                                prix_vente=0,
                                devise="USD",
                                txchange=tx,
                                codeuser_id=request.user.id,
                            )
                        elif finvv.qte_u_ecart < 0:
                            if tempo1:
                                tempo1.update(
                                # quantite=(i.qte_u_ecart),
                                qte_sortie=(finvv.qte_u_ecart)*(-1),
                                # qteunit_sortie=resultat2*(-1),
                                prix_achat=finvv.prix_achat_u,
                                # pa=prix_achat_petit,
                                prix_vente=0,
                                # devise="",
                                txchange=tx,
                                codeuser_id=request.user.id,
                            )
                            else:
                                Fmvts.objects.create(
                                    location_id=request.session.get('idlocationuser'),
                                    # periode=p,
                                    periode=finvv.periode,
                                    bordereau=datetime.now().time(),
                                    datemvt=finvv.dateinventaire,
                                    ndatemvt=str(finvv.dateinventaire).replace("-", "").replace("/", ""),
                                    requisition="INV" + str(finvv.periode),
                                    document="INV" + str(finvv.compteur),
                                    ajustement_id="INV",
                                    # tiers_id=i.serielivraison.commande.tiers.tiers,
                                    article=finvv.article,
                                    emballage_id=finvv.emballage_e,
                                    # quantite=(i.qte_u_ecart),
                                    qte_sortie=(finvv.qte_u_ecart)*(-1),
                                    # qteunit_sortie=resultat2*(-1),
                                    prix_achat=finvv.prix_achat_u,
                                    # pa=prix_achat_petit,
                                    prix_vente=0,
                                    devise="USD",
                                    txchange=tx,
                                    codeuser_id=request.user.id,
                                )


                return JsonResponse({"msg": "Opération effectuée ", "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée "+str(e), "id": "0"}, safe=False)




    return render(request, 'gestionstock/misestockinventaire.html',context={"periode":DelaiInventaire.objects.filter(location_id=request.session.get('idlocationuser')).order_by("-periode")})


@login_required
@permission_required('gestionstock.Rap_Stock',raise_exception=True)
def rapstock(request):
    if request.method == "POST":

        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = os.path.join(fn,"rapstock.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = os.path.join(fn, 'media')

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': f"jdbc:jtds:sqlserver://localhost/{settings.DATABASES['default']['NAME']}",
            'jdbc_dir': fn,
            'username': settings.DATABASES['default']['USER'],
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKPRO',
            # 'port': '1433'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"

        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters={'liblocation': request.session.get('locationuser'),'libdate1':request.POST.get('date1'),'libdate2':request.POST.get('date2'),'iddate1':str(request.POST.get('date1')).replace("/","").replace("-",""),'iddate2':str(request.POST.get('date2')).replace("/","").replace("-",""),'idlocation':request.session.get('idlocationuser')},
            locale='en_US'
        )


        return HttpResponse("true")
    return render(request, 'gestionstock/rapstock.html')


@login_required
@permission_required('gestionstock.Rap_varia',raise_exception=True)
def rapvariation(request):
    if request.method == "POST":

        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = os.path.join(fn,"extimation.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = os.path.join(fn, 'media')

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': f"jdbc:jtds:sqlserver://localhost/{settings.DATABASES['default']['NAME']}",
            'jdbc_dir': fn,
            'username': settings.DATABASES['default']['USER'],
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKPRO',
            # 'port': '1433'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"

        jasper.process(
            input_file,
            output,
            format_list=["pdf","xlsx"],
            db_connection=con,
            parameters={'libdate1':request.POST.get('date1'),'libdate2':request.POST.get('date2'),'iddate1':str(request.POST.get('date1')).replace("/","").replace("-",""),'iddate2':str(request.POST.get('date2')).replace("/","").replace("-","")},
            locale='en_US'
        )


        return HttpResponse("true")
    return render(request, 'gestionstock/rapvariation.html',context={"periode":DelaiInventaire.objects.filter(location_id=request.session.get('idlocationuser')).order_by("-periode")})


@login_required
@permission_required('gestionstock.Rap_Client_Co',raise_exception=True)
def rapclientco(request):
    if request.method == "POST":

        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if request.POST.get("cmp")=="1":
            input_file = os.path.join(fn,"rapclientcategorie.jrxml")
        elif request.POST.get("cmp")=="2":
            input_file = os.path.join(fn,"rapclientcategorie2.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = os.path.join(fn, 'media')

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': f"jdbc:jtds:sqlserver://localhost/{settings.DATABASES['default']['NAME']}",
            'jdbc_dir': fn,
            'username': settings.DATABASES['default']['USER'],
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKPRO',
            # 'port': '1433'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"

        idtva=0
        tvaero=0
        if len(request.POST.getlist('taxe[]')) > 0:
            for i in request.POST.getlist('taxe[]'):

                temp=Ftaxes.objects.get(taxe=i)
                if temp.taux==16:
                    idtva=1
                elif temp.taux==3:
                    tvaero = 1

        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters={'liblocation': request.session.get('locationuser'),'idlocation':request.session.get('idlocationuser'),'tvaero':str(tvaero),'idtva':str(idtva),'libdate1':request.POST.get('date1'),'libdate2':request.POST.get('date2'),'iddate1':str(request.POST.get('date1')).replace("/","").replace("-",""),'iddate2':str(request.POST.get('date2')).replace("/","").replace("-","")},
            locale='en_US'
        )



        return HttpResponse("true")

    context={

        "taxe":Ftaxes.objects.all().order_by("designation"),
    }
    return render(request, 'gestionstock/rapclientco.html',context)


# @login_required
# @permission_required('gestionstock.Rap_Client_Co',raise_exception=True)
# def rapclientco(request):
#     if request.method == "POST":
#
#         fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#         if request.POST.get("cmp")=="1":
#             input_file = os.path.join(fn,"rapclientcategorie.jrxml")
#         elif request.POST.get("cmp")=="2":
#             input_file = os.path.join(fn,"rapclientcategorie2.jrxml")
#
#         # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")
#
#         output = os.path.join(fn, 'media')
#
#         con = {
#             'driver': 'generic',
#             'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
#             'jdbc_url': f"jdbc:jtds:sqlserver://localhost/{settings.DATABASES['default']['NAME']}",
#             'jdbc_dir': fn,
#             'username': settings.DATABASES['default']['USER'],
#             'password': settings.DATABASES['default']['PASSWORD']
#             # 'host': 'localhost',
#             # 'database': 'STOCKPRO',
#             # 'port': '1433'
#         }
#
#         jasper = JasperPy()
#         # jasper.compile("D:/test1.jrxml")
#         # jasper.path_executable = "D:/JasperStarter/bin/"
#
#         idtva=0
#         tvaero=0
#         if len(request.POST.getlist('taxe[]')) > 0:
#             for i in request.POST.getlist('taxe[]'):
#
#                 temp=Ftaxes.objects.get(taxe=i)
#                 if temp.taux==16:
#                     idtva=1
#                 elif temp.taux==3:
#                     tvaero = 1
#
#         jasper.process(
#             input_file,
#             output,
#             format_list=["pdf"],
#             db_connection=con,
#             parameters={'liblocation': request.session.get('locationuser'),'idlocation':request.session.get('idlocationuser'),'tvaero':str(tvaero),'idtva':str(idtva),'libdate1':request.POST.get('date1'),'libdate2':request.POST.get('date2'),'iddate1':str(request.POST.get('date1')).replace("/","").replace("-",""),'iddate2':str(request.POST.get('date2')).replace("/","").replace("-","")},
#             locale='en_US'
#         )
#
#
#
#         return HttpResponse("true")
#
#     context={
#
#         "taxe":Ftaxes.objects.all().order_by("designation"),
#     }
#     return render(request, 'gestionstock/rapclientco.html',context)


@login_required
@permission_required('gestionstock.Rap_Client',raise_exception=True)
def rapclient(request):
    if request.method == "POST":
        if 'mvt' in request.POST:
            Fmvts.objects.filter(mvt=request.POST.get('mvt')).update(facture="1")
            return JsonResponse({"msg": "Opération effectuée","id":"1"}, safe=False)
        if 'numero' in request.POST:
            f=Fmvts.objects.filter(requisition=request.POST.get('numero'))
            totapayer=0
            totpaye=0
            for i in f:
                totpaye=i.prix_total
                totapayer+=(i.prix_achat*i.qte_sortie)
            try:
                totpaye=float(totpaye)+float(request.POST.get('mtn'))
                f.update(prix_total=totpaye)
                return JsonResponse({"msg": "Opération effectuée", "id": "1"}, safe=False)
            except:
                return JsonResponse({"msg": "Opération non effectuée", "id": "0"}, safe=False)



        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = os.path.join(fn,"rapclient.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = os.path.join(fn, 'media')

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': f"jdbc:jtds:sqlserver://localhost/{settings.DATABASES['default']['NAME']}",
            'jdbc_dir': fn,
            'username': settings.DATABASES['default']['USER'],
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKPRO',
            # 'port': '1433'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"

        idtva=0
        tvaero=0
        # if len(request.POST.getlist('taxe[]')) > 0:
        #     for i in request.POST.getlist('taxe[]'):
        #
        #         temp=Ftaxes.objects.get(taxe=i)
        #         if temp.taux==16:
        #             idtva=1
        #         elif temp.taux==3:
        #             tvaero = 1
        if "incremat" in request.POST:
            IncremaClient.objects.create(
                libelle="FCC"
            )
            numerofac = IncremaClient.objects.count()
        else:
            numerofac = IncremaClient.objects.count() + 1

        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters={'numerofac':"FCC000"+str(numerofac),'tvaero':str(tvaero),'idtva':str(idtva),'libdate1':request.POST.get('date1'),'libdate2':request.POST.get('date2'),'iddate1':str(request.POST.get('date1')).replace("/","").replace("-",""),'iddate2':str(request.POST.get('date2')).replace("/","").replace("-",""),'idclient':request.POST.get('client')},
            locale='en_US'
        )


        return HttpResponse("true")


    if 'affiche' in request.GET:

        mv=Fmvts.objects.filter(ajustement_id='FACT',tiers_id=request.GET.get('client'),datemvt__gte=request.GET.get('dtd'),datemvt__lte=request.GET.get('dtf'),prix_total__gte=0).order_by('requisition') #.values('mvt','datemvt','designation','location__designation','qteunit_sortie')
        datax=[]
        numero=''
        for i in mv:
            t={}
            if i.requisition == numero:

                for xx in datax:
                    if xx['numero']==i.requisition:
                        xx['paye'] += float("%.2f" %(i.prix_achat*i.qte_sortie))
                        xx['reste'] = float("%.2f" % (xx['paye']-i.prix_total))
                        break
            else:
                numero=i.requisition
                t = {
                    'numero': i.requisition,
                    'date': i.datemvt,
                    'paye': float("%.2f" %(i.prix_achat*i.qte_sortie)),
                    'totalgen': i.prix_total,
                    'reste': float("%.2f" % ((i.prix_achat*i.qte_sortie)-i.prix_total))
                }
                datax.append(t)

        return JsonResponse({"data": list(datax)}, safe=False)

    context={
        "client":Ftiers.objects.filter(nature="CLIENT").order_by("nompostnom"),
       # "taxe":Ftaxes.objects.all().order_by("designation"),
    }
    return render(request, 'gestionstock/rapclient.html',context)



@login_required
@permission_required('gestionstock.Rap_Sortie',raise_exception=True)
def rapsortie(request):
    if request.method == "POST":

        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if 'full' in request.POST:
            input_file = os.path.join(fn,"rapsortiefac.jrxml")
        elif 'con' in request.POST:
            if request.POST.get('con')=='1':
                input_file = os.path.join(fn, "rapcon.jrxml")
            elif request.POST.get('con')=='2':
                input_file = os.path.join(fn, "rapconlocal.jrxml")
        else:
            input_file = os.path.join(fn,"rapsortie.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = os.path.join(fn, 'media')

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': f"jdbc:jtds:sqlserver://localhost/{settings.DATABASES['default']['NAME']}",
            'jdbc_dir': fn,
            'username': settings.DATABASES['default']['USER'],
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKPRO',
            # 'port': '1433'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"

        # if 'full' in request.POST:
        #     parameters = {
        #                   'libdate1': request.POST.get('date1'), 'libdate2': request.POST.get('date2'),
        #                   'iddate1': str(request.POST.get('date1')).replace("/", "").replace("-", ""),
        #                   'iddate2': str(request.POST.get('date2')).replace("/", "").replace("-", "")}
        # else:
        parameters = {'liblocation': request.POST.get('locationlib'), 'location1': request.POST.get('location'),
                          'libdate1': request.POST.get('date1'), 'libdate2': request.POST.get('date2'),
                          'iddate1': str(request.POST.get('date1')).replace("/", "").replace("-", ""),
                          'iddate2': str(request.POST.get('date2')).replace("/", "").replace("-", "")}

        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters=parameters,
            locale='en_US'
        )


        return HttpResponse("true")

    context={
        "location":Flocation.objects.all().order_by("designation"),

    }
    return render(request, 'gestionstock/rapsortie.html',context)



@login_required
@permission_required('gestionstock.Rap_Sortie_full',raise_exception=True)
def rapsortiefull(request):
    if request.method == "POST":

        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = os.path.join(fn,"rapsortiefull.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = os.path.join(fn, 'media')

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': f"jdbc:jtds:sqlserver://localhost/{settings.DATABASES['default']['NAME']}",
            'jdbc_dir': fn,
            'username': settings.DATABASES['default']['USER'],
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKPRO',
            # 'port': '1433'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"




        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters={'liblocation':request.session.get('locationuser'),'location1':request.session.get('idlocationuser'),'libdate1':request.POST.get('date1'),'libdate2':request.POST.get('date2'),'iddate1':str(request.POST.get('date1')).replace("/","").replace("-",""),'iddate2':str(request.POST.get('date2')).replace("/","").replace("-","")},
            locale='en_US'
        )


        return HttpResponse("true")


    return render(request, 'gestionstock/rapsortiefull.html')


@login_required
@permission_required('gestionstock.Rap_achat',raise_exception=True)
def rapachat(request):
    if request.method == "POST":

        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if 'full' in request.POST:
            input_file = os.path.join(fn, "rapachatsy.jrxml")
        elif 'trans' in request.POST:
            input_file = os.path.join(fn, "rapachattrans.jrxml")
        else:
            input_file = os.path.join(fn,"rapachat.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = os.path.join(fn, 'media')

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': f"jdbc:jtds:sqlserver://localhost/{settings.DATABASES['default']['NAME']}",
            'jdbc_dir': fn,
            'username': settings.DATABASES['default']['USER'],
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKPRO',
            # 'port': '1433'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"

        # if 'full' in request.POST:
        #     parameters={'libdate1':request.POST.get('date1'),'libdate2':request.POST.get('date2'),'iddate1':str(request.POST.get('date1')).replace("/","").replace("-",""),'iddate2':str(request.POST.get('date2')).replace("/","").replace("-","")}
        # else:
        parameters = {'liblocation': request.POST.get('locationlib'), 'location1': request.POST.get('location'),
                          'libdate1': request.POST.get('date1'), 'libdate2': request.POST.get('date2'),
                          'iddate1': str(request.POST.get('date1')).replace("/", "").replace("-", ""),
                          'iddate2': str(request.POST.get('date2')).replace("/", "").replace("-", "")}
        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters=parameters,
            locale='en_US'
        )


        return HttpResponse("true")

    context={
        'location':Flocation.objects.all().order_by('designation')
    }
    return render(request, 'gestionstock/rapachat.html',context)


@login_required
@permission_required('gestionstock.recettesrapport',raise_exception=True)
def raprecette(request):
    if request.method == "POST":

        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        if request.POST.get('categorie')=="0":
            input_file = os.path.join(fn,"recettes.jrxml")
        else:
            input_file = os.path.join(fn,"plat.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = os.path.join(fn, 'media')

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': f"jdbc:jtds:sqlserver://localhost/{settings.DATABASES['default']['NAME']}",
            'jdbc_dir': fn,
            'username': settings.DATABASES['default']['USER'],
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKPRO',
            # 'port': '1433'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"

        # idtva=0
        # tvaero=0
        # if len(request.POST.getlist('taxe[]')) > 0:
        #     for i in request.POST.getlist('taxe[]'):
        #
        #         temp=Ftaxes.objects.get(taxe=i)
        #         if temp.taux==16:
        #             idtva=1
        #         elif temp.taux==3:
        #             tvaero = 1



        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            # parameters={'idlocation':request.session.get('idlocationuser'),'tvaero':str(tvaero),'idtva':str(idtva),'idclient':request.POST.get('client')},
            # parameters={},
            locale='en_US'
        )


        return HttpResponse("true")

    context={
        # "client":Ftiers.objects.filter(nature="CLIENT").order_by("nompostnom"),
        # "taxe":Ftaxes.objects.all().order_by("designation"),
    }
    return render(request, 'gestionstock/raprecette.html',context)


@login_required
@permission_required('gestionstock.Rap_Fourni',raise_exception=True)
def rapfournisseur(request):
    if request.method == "POST":

        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = os.path.join(fn,"rapfournisseur.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = os.path.join(fn, 'media')

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': f"jdbc:jtds:sqlserver://localhost/{settings.DATABASES['default']['NAME']}",
            'jdbc_dir': fn,
            'username': settings.DATABASES['default']['USER'],
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKPRO',
            # 'port': '1433'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"

        idtva=0
        tvaero=0
        if len(request.POST.getlist('taxe[]')) > 0:
            for i in request.POST.getlist('taxe[]'):

                temp=Ftaxes.objects.get(taxe=i)
                if temp.taux==16:
                    idtva=1
                elif temp.taux==3:
                    tvaero = 1
        if "incremat" in request.POST:
            IncremaClient.objects.create(
                libelle="FCC"
            )
            numerofac = IncremaClient.objects.count()
        else:
            numerofac = IncremaClient.objects.count() + 1


        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters={'numerofac':"FCC000"+str(numerofac),'tvaero':str(tvaero),'idtva':str(idtva),'numbon':request.POST.get('bon'),'libfou':request.POST.get('libfou'),'idclient':request.POST.get('client')},
            locale='en_US'
        )


        return HttpResponse("true")

    context={
        "client":Ftiers.objects.filter(nature="FOURNISSEUR").order_by("nompostnom"),
        "taxe":Ftaxes.objects.all().order_by("designation"),
    }
    return render(request, 'gestionstock/rapfournisseur.html',context)


@login_required
@permission_required('gestionstock.Entrer_Stock',raise_exception=True)
def entrestock(request):

    if request.method=="POST":
        p=0
        if 'idcode' in request.POST:
            e=etatbesoin.objects.filter(id=request.POST.get('idcode')).update(qteliv=request.POST.get('qte'))
        else:
            floc=Flocation.objects.get(location=request.session['idlocationuser'])
            for produit,qte,emb1,prix,devise,dt in zip(request.POST.getlist('produit[]'),request.POST.getlist('qte[]'),request.POST.getlist('emb'),request.POST.getlist('prix[]'),request.POST.getlist('devise[]'),request.POST.getlist('dt[]')):

                if produit!="" and qte!="" and qte!="0" and prix!="":
                    p=1
                    pa=miseajourprix(produit,emb1,prix,floc,devise,request.POST.get('tx'))

                    # art = Farticle.objects.filter(article=produit, emballagee_id=emb1)
                    # art2 = Farticle.objects.filter(article=produit, emballageu_id=emb1)
                    # art3 = Farticle.objects.filter(article=produit, emballagea=emb1)
                    #
                    # if art:
                    #     if devise == 'CDF':
                    #         pa = float(prix) / float(str(request.POST.get('tx')).replace(",", "."))
                    #     else:
                    #         pa = float(prix)
                    #     art=art.first()
                    #     art.prix_achat=pa
                    #     art.prix_vente=pa+((float(pa)*float(floc.cptetaxe))/100)
                    #     art.save()
                    # elif art2:
                    #     if devise == 'CDF':
                    #         pa = float(prix) / float(str(request.POST.get('tx')).replace(",", "."))
                    #     else:
                    #         pa = float(prix)
                    #     art2=art2.first()
                    #     art2.pa=pa
                    #     art.prix_vente_cdf = pa + ((float(pa) * float(floc.cptetaxev)) / 100)
                    #     art2.save()
                    # elif art3:
                    #     if devise == 'CDF':
                    #         pa = float(prix) / float(str(request.POST.get('tx')).replace(",", "."))
                    #     else:
                    #         pa = float(prix)
                    #     art3=art3.first()
                    #     art3.old_prix_achat=pa
                    #     art.old_prix_vente = pa + ((float(pa) * float(floc.cptechf)) / 100)
                    #     art3.save()


                    Fmvts.objects.create(
                        location_id=request.session['idlocationuser'],
                        datemvt=request.POST.get('dateop'),
                        ndatemvt=str(request.POST.get('dateop')).replace("-", "").replace("/", ""),
                        requisition=request.POST.get('code'),
                        reference=dt,
                        document=request.POST.get('numbonlivre'),
                        bordereau=datetime.now().time(),
                        ajustement_id='ACH',
                        article_id=produit,
                        emballage_id=emb1,
                        qte_entree=qte,
                        # qteunit_entree=resultat2,
                        prix_achat=pa,
                        # pa=prix_achat_petit,
                        prix_vente=0,
                        devise=devise,
                        txchange=str(request.POST.get('tx')).replace(",", "."),
                        codeuser_id=request.user.id,
                    )

        if p==1:
            return JsonResponse(
                {"msg": "Opération effectuée",
                 "id": "1","code":"E" + str(request.session['idlocationuser']) + random_char(6)}, safe=False)
        else:
            return JsonResponse(
                {"msg": "Opération noneffectuée",
                 "id": "0"}, safe=False)



    if request.session.get('idlocationuser') ==  'DSBB':
        context = {
            "article": Farticle.objects.all().order_by(
                'designation'),
            "taux": Flocation.objects.get(location=request.session.get('idlocationuser')).txchange,
        }
    else:
        context = {
            "article": Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser')).order_by(
                'designation'),
            "taux": Flocation.objects.get(location=request.session.get('idlocationuser')).txchange,
        }


    context['numtrans'] = "E" + str(request.session['idlocationuser']) + random_char(6)
    return render(request, 'gestionstock/entrestock.html', context)


@login_required
@permission_required('gestionstock.Entrer_Stock',raise_exception=True)
def entrestock2(request):


    context = {
    "taux":Flocation.objects.get(location=request.session.get('idlocationuser')).txchange,
    "bon":Fcommande.objects.filter(etatcde="1",location_id=request.session.get('idlocationuser'),cloture=False,validation=True).order_by('-commande'),
    "fournisseur":Ftiers.objects.all(),
    # "numentre":"BE000" + str(Flivraison.objects.filter(commande__location_id= request.session.get('idlocationuser')).count() + 1)
    }
    return render(request, 'gestionstock/entrestock2.html', context)




@login_required
@permission_required('gestionstock.Entrer_Stock',raise_exception=True)
def modistock(request):

    if request.method=="POST":
        f=Fmvts.objects.get(mvt=request.POST.get('mvt'))
        docmvt=f.document
        floc = Flocation.objects.get(location=request.session['idlocationuser'])

        pa=miseajourprix(f.article.article,f.emballage_id,request.POST.get('prix'),floc)

        # art = Farticle.objects.filter(article=f.article.article, emballagee_id=f.emballage_id)
        # art2 = Farticle.objects.filter(article=f.article.article, emballageu_id=f.emballage_id)
        # art3 = Farticle.objects.filter(article=f.article.article, emballagea=f.emballage_id)
        #
        # if art:
        #
        #     pa = float(request.POST.get('prix'))
        #     art = art.first()
        #     art.prix_achat = pa
        #     art.prix_vente = pa + ((float(pa) * float(floc.cptetaxe)) / 100)
        #     art.save()
        # elif art2:
        #     pa = float(request.POST.get('prix'))
        #     art2 = art2.first()
        #     art2.pa = pa
        #     art.prix_vente_cdf = pa + ((float(pa) * float(floc.cptetaxev)) / 100)
        #     art2.save()
        # elif art3:
        #     pa = float(request.POST.get('prix'))
        #     art3 = art3.first()
        #     art3.old_prix_achat = pa
        #     art.old_prix_vente = pa + ((float(pa) * float(floc.cptechf)) / 100)
        #     art3.save()


        if f.ajustement_id in ('ACH','TRFR'):
            Fmvts.objects.filter(mvt=request.POST.get('mvt')).update(
                qte_entree=request.POST.get('qte'),
                prix_achat=pa,
                codeuser_id=request.user.id,
            )
            Fmvts.objects.filter(document=docmvt,ajustement_id='TRTO').update(
                qte_sortie=request.POST.get('qte'),
                prix_achat=pa,
                codeuser_id=request.user.id,
            )
        else:
            Fmvts.objects.filter(mvt=request.POST.get('mvt')).update(
                qte_sortie=request.POST.get('qte'),
                prix_achat=pa,
                codeuser_id=request.user.id,
            )
            Fmvts.objects.filter(document=docmvt, ajustement_id='TRFR').update(
                qte_entree=request.POST.get('qte'),
                prix_achat=pa,
                codeuser_id=request.user.id,
            )
        return JsonResponse({"msg": "Opération effectuée ", "id": "1"}, safe=False)


    if 'mvt' in request.GET:
        if request.GET.get('ctrl')=="0":

            rec = Fmvts.objects.filter(requisition=request.GET.get('mvt'),ajustement_id='TRTO').values(
                "mvt", "article__designation","destination", "qte_sortie","qte_entree","datemvt","prix_achat", "emballage_id"
            ).order_by('-mvt')
        else:
            rec = Fmvts.objects.filter(requisition=request.GET.get('mvt'),ajustement__in=('TRFR','ACH')).values(
                "mvt", "article__designation", "location__designation", "qte_sortie", "qte_entree", "datemvt",
                "prix_achat", "emballage_id"
            ).order_by('-mvt')

        rec = list(rec)
        return JsonResponse({'data': rec}, safe=False)
    context = {
                "sortielist": Fmvts.objects.filter(ajustement_id="TRTO",location_id=request.session.get('idlocationuser')).values('requisition','datemvt','destination').annotate(Count('requisition')).order_by('-ndatemvt')[:150],
                "entrelist": Fmvts.objects.filter(ajustement__in=('TRFR','ACH'),location_id=request.session.get('idlocationuser')).values('requisition','datemvt','location__designation').annotate(Count('requisition')).order_by('-ndatemvt')[:150],

             }
    return render(request, 'gestionstock/modistock.html', context)



@login_required
@permission_required('gestionstock.view_stockrecettes',raise_exception=True)
def entrestockrecettes(request):

    if request.method == "POST":

        try:
            with transaction.atomic():

                if 'suppression' in request.POST:
                    one = StockRecettes.objects.filter(location_id=request.session.get('idlocationuser'),
                                                       bon=str(request.POST.get('bon')),
                                                       recette_id=str(request.POST.get('recette')), categorie='E')
                    if one:
                        if request.user.has_perm('gestionstock.delete_stockrecettes'):
                            one.delete()
                            #matieres premieres
                            rc = Fmvts.objects.filter(recette_id=str(request.POST.get('recette')),document=str(request.POST.get('bon')))
                            if rc:
                                rc.delete()
                            #matieres premieres
                            return JsonResponse(
                                {"msg": "Opération effectuée",
                                 "id": "1"}, safe=False)
                        else:
                            return JsonResponse(
                                {"msg": "Opération non effectuée.Vous avez pas ce droit",
                                 "id": "0"}, safe=False)
                    else:
                        return JsonResponse(
                            {"msg": "Opération non effectuée.Données invalides",
                             "id": "0"}, safe=False)

                one=StockRecettes.objects.filter(location_id=request.session.get('idlocationuser'),bon=str(request.POST.get('bon')),recette_id=str(request.POST.get('recette')),categorie='E')
                if one:
                    if request.user.has_perm('gestionstock.change_stockrecettes'):
                        one.update(
                            qte=request.POST.get('qte'),
                            prix=str(request.POST.get('pu')).replace(",", "."),
                            dateop=request.POST.get('dateop'),
                            user=request.user,
                        )
                        #matieres premieres
                        rc = Fmvts.objects.filter(recette_id=str(request.POST.get('recette')),
                                                  document=str(request.POST.get('bon')))
                        if rc:
                            for t in rc:
                                h = DetailRecettes.objects.filter(recettes_id=str(request.POST.get('recette')),produit_id=t.article.article)
                                if h:
                                    h=h.frist()
                                    p=Fmvts.objects.filter(recette_id=str(request.POST.get('recette')),
                                                  document=str(request.POST.get('bon')), article_id=t.article.article)
                                    p.update(
                                        datemvt=request.POST.get('dateop'),
                                        ndatemvt=str(request.POST.get('dateop')).replace("-", "").replace("/", ""),

                                        ajustement_id="TRTO",
                                        qte_sortie=float(h.qte) * float(request.POST.get('qte')),
                                        qteunit_sortie=float(h.qte) * float(request.POST.get('qte')),
                                        prix_achat=h.prix_achat,
                                        codeuser_id=request.user.id,
                                     )
                        #matieres premieres
                    else:
                        return JsonResponse(
                            {"msg": "Opération non effectuée.Vous avez pas ce droit",
                             "id": "0"}, safe=False)
                else:
                    if request.user.has_perm('gestionstock.add_stockrecettes'):
                        StockRecettes.objects.create(
                        recette_id=str(request.POST.get('recette')),
                        qte=request.POST.get('qte'),
                        bon=request.POST.get('bon'),
                        prix=str(request.POST.get('pu')).replace(",","."),
                        dateop=request.POST.get('dateop'),
                        user=request.user,
                        categorie='E',
                        location_id=request.session.get('idlocationuser')
                        )
                        #matieres premieres
                        rc=DetailRecettes.objects.filter(recettes_id=str(request.POST.get('recette')))
                        if rc:
                            for b in rc:
                                Fmvts.objects.create(
                                location_id=request.session.get('idlocationuser'),
                                datemvt=request.POST.get('dateop'),
                                ndatemvt=str(request.POST.get('dateop')).replace("-", "").replace("/", ""),

                                ajustement_id="TRTO",
                                article_id=b.produit.article,
                                recette_id=str(request.POST.get('recette')),

                                emballage_id=b.produit.emballagee.emballage,
                                qte_sortie=float(b.qte)*float(request.POST.get('qte')),
                                qteunit_sortie=float(b.qte)*float(request.POST.get('qte')),
                                document=request.POST.get('bon'),
                                prix_achat=b.produit.prix_achat,
                                # prix_vente=request.POST.get('privente'),
                                # devise=request.POST.get('devise'),
                                # txchange=str(request.POST.get('taux')).replace(",", "."),
                                codeuser_id=request.user.id,
                                #destinat_id=request.POST.get('locationbis'),
                            )
                        #matieres premieres
                    else:
                        return JsonResponse(
                            {"msg": "Opération non effectuée.Vous avez pas ce droit",
                             "id": "0"}, safe=False)
                return JsonResponse(
                    {"msg": "Opération effectuée",
                     "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)

    # clients=Ftiers.objects.all()
    #
    # datafull={}
    # datafullitem=[]
    # datafullitemtempo=[]
    # for i in clients:
    #     detal=DetailRecettes.objects.all()
    #     if detal:
    #         for x in detal:
    #             code= "_"+str(x.recettes_id)+ "_"+str(x.id)
    #             if code in datafullitemtempo:
    #                 pass
    #             else:
    #                 datafull={}
    #                 datafull['id']=code
    #                 datafull['libelle']= " => "+str(x.recettes.libelle)
    #                 datafullitem.append(datafull)
    #                 datafullitemtempo.append(code)
    #

    context = {
            "recette":Recettes.objects.all().order_by('libelle'),
                  }
    return render(request, 'gestionstock/entrerec.html', context)


@login_required
@permission_required('gestionstock.view_recettestocksortie',raise_exception=True)
def numerorectempodel(request):

    if request.method == "POST":

        try:
            with transaction.atomic():
                t=Fmvts.objects.filter(location_id=request.session['idlocationuser'],article__isnull=True,codeuser=request.user,ajustement__in=('FACT','SUP'),ndatemvt=str(datetime.today().date()).replace("-","").replace("/","")).order_by('-mvt')

                if t:
                    return JsonResponse(
                        {"tot": int(t.first().document) + 1}, safe=False)
                return JsonResponse({"tot": 1}, safe=False)

        except Exception as e:

            return JsonResponse({"tot": 1}, safe=False)




@login_required
#@permission_required('gestionstock.recettesrapportsys',raise_exception=True)
def etatbesoinn(request):

    if request.method=="POST":

        p=0
        if 'idcode' in request.POST:
            e=etatbesoin.objects.filter(id=request.POST.get('idcode')).update(qteliv=request.POST.get('qte'))
        else:
            floc=Flocation.objects.get(location=request.POST.get('location'))
            for produit,qte,emb1 in zip(request.POST.getlist('produit[]'),request.POST.getlist('qte[]'),request.POST.getlist('emb')):


                if produit!="" and qte!="" and qte!="0":
                    p=1
                    pa=0

                    art =  Farticle.objects.filter(article=produit, emballagee_id=emb1)
                    art2 = Farticle.objects.filter(article=produit, emballageu_id=emb1)
                    art3 = Farticle.objects.filter(article=produit, emballagea=emb1)

                    if art:
                        pa = float(art.first().prix_achat)
                    elif art2:
                        pa = float(art2.first().pa)
                    elif art3:
                        pa = float(art3.first().old_prix_achat)


                    Fmvts.objects.create(
                        destination=floc.designation,
                        location_id=request.session['idlocationuser'],
                        datemvt=datetime.today().date(),
                        ndatemvt=str(datetime.today().date()).replace("-", "").replace("/", ""),
                        requisition=request.POST.get('code'),
                        document=request.POST.get('code'),
                        bordereau=datetime.now().time(),
                        ajustement_id='TRTO',
                        article_id=produit,
                        emballage_id=emb1,
                        qte_sortie=qte,
                        prix_achat=pa,
                        prix_vente=0,
                        devise='USD',
                        txchange=str(request.POST.get('tx')).replace(",", "."),
                        codeuser_id=request.user.id,
                    )

                    Fmvts.objects.create(
                        destination=request.session.get('locationuser'),
                        location_id=request.POST.get('location'),
                        datemvt=datetime.today().date(),
                        ndatemvt=str(datetime.today().date()).replace("-", "").replace("/", ""),
                        requisition=request.POST.get('code'),
                        document=request.POST.get('code'),
                        bordereau=datetime.now().time(),
                        ajustement_id='TRFR',
                        article_id=produit,
                        emballage_id=emb1,
                        qte_entree=qte,
                        prix_achat=pa,
                        prix_vente=0,
                        devise='USD',
                        txchange=str(request.POST.get('tx')).replace(",", "."),
                        codeuser_id=request.user.id,
                    )
        if p==1:
            return JsonResponse(
            {"msg": "Opération effectuée",
             "id": "1","code":"T" + str(request.session['idlocationuser']) + random_char(6)}, safe=False)
        else:
            return JsonResponse(
                {"msg": "Opération non effectuée",
                 "id": "0"}, safe=False)



    context = {
        "article": Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser')).order_by('designation'),
        "taux": Flocation.objects.get(location=request.session.get('idlocationuser')).txchange,
        "locations": Flocation.objects.all().exclude(location=request.session.get('idlocationuser')).order_by('designation'),
    }
    context['numtrans'] = "T" + str(request.session['idlocationuser']) + random_char(6)
    return render(request, 'gestionstock/etatbesoinone.html',context)



@login_required
#@permission_required('gestionstock.recettesrapportsys',raise_exception=True)
def etatbesoinn2(request):

    if request.method=="POST":


        if 'idcode' in request.POST:
            e=etatbesoin.objects.filter(id=request.POST.get('idcode')).update(qteliv=request.POST.get('qte'))
        else:
            print(request.POST)
            for produit,qte,emb1 in zip(request.POST.getlist('produit[]'),request.POST.getlist('qte[]'),request.POST.getlist('emb')):

                e=etatbesoin.objects.filter(code=request.POST.get('code'),article_id = produit)
                if e:
                    pass
                else:
                    print(request.POST.get('location'))
                    etatbesoin.objects.create(
                    location_id=request.POST.get('location'),
                    locationfour_id="PHAR",
                    article_id = produit,
                    emb1_id = emb1,
                    code=request.POST.get('code'),
                    user = request.user,
                    dateop = datetime.today().date(),
                    qte = qte,
                    qteliv = qte
                )
        return JsonResponse(
            {"msg": "Opération effectuée",
             "id": "1","code":"T" + str(request.session['idlocationuser']) + random_char(6)}, safe=False)


    context = {
        "article": Farticle.objects.all().order_by('designation'),
        "locations": Flocation.objects.filter(typelocation='D').exclude(location=request.session.get('idlocationuser')).order_by('designation'),
    }
    context['numtrans'] = "T" + str(request.session['idlocationuser']) + random_char(6)
    return render(request, 'gestionstock/etatbesoinone2.html',context)


@login_required
@permission_required('gestionstock.recettesrapportsys',raise_exception=True)
def synthesepointvente(request):

    if request.method=="POST":


        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = fn+"\{}".format("rapsynthese.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output =fn+"\media"

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': 'jdbc:sqlserver://localhost;databaseName=' + str(settings.DATABASES['default']['NAME']),
            'jdbc_dir': fn,
            'username': settings.DATABASES['default']['USER'],
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKPRO',
            # 'port': '1433'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"



        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters={'liblocation': '{}'.format(request.session.get('locationuser')),'idlocation': '{}'.format(request.session.get('idlocationuser')),'d1': '{}'.format(request.POST.get('dtd')),'d2': '{}'.format(request.POST.get('dtf')),'datedb': '{}'.format(str(request.POST['dtd']).replace("-","")),'datefn':'{}'.format(str(request.POST['dtf']).replace("-",""))},
            locale='en_US'
        )


        return HttpResponse("true")

    return render(request, 'gestionstock/rapventesynthese.html')

@login_required
@permission_required('gestionstock.recettesrapportentree',raise_exception=True)
def pointventeentree(request):

    if request.method=="POST":


        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = fn+"\{}".format("rapentreerecette.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output =fn+"\media"

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': 'jdbc:sqlserver://localhost;databaseName=' + str(settings.DATABASES['default']['NAME']),
            'jdbc_dir': fn,
            'username': settings.DATABASES['default']['USER'],
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKPRO',
            # 'port': '1433'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"



        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters={'idlocation': '{}'.format(request.session.get('idlocationuser')),'liblocation': '{}'.format(request.session.get('locationuser')),'d1': '{}'.format(request.POST.get('dtd')),'d2': '{}'.format(request.POST.get('dtf'))},
            locale='en_US'
        )
        return HttpResponse("true")

    return render(request, 'gestionstock/rapentrearticle.html')


@login_required
@permission_required('gestionstock.recettesrapport',raise_exception=True)
def pointvente(request):

    if request.method=="POST":


        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = fn+"\{}".format("rapjournalier.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output =fn+"\media"

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': 'jdbc:sqlserver://localhost;databaseName=' + str(settings.DATABASES['default']['NAME']),
            'jdbc_dir': fn,
            'username': settings.DATABASES['default']['USER'],
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKPRO',
            # 'port': '1433'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml")
        # jasper.path_executable = "D:/JasperStarter/bin/"



        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters={'idlocation': '{}'.format(request.session.get('idlocationuser')),'liblocation': '{}'.format(request.session.get('locationuser')),'d1': '{}'.format(request.POST.get('dtd')),'d2': '{}'.format(request.POST.get('dtf')),'datedb': '{}'.format(str(request.POST['dtd']).replace("-","")),'datefn': '{}'.format(str(request.POST['dtf']).replace("-",""))},
            locale='en_US'
        )
        return HttpResponse("true")

    return render(request, 'gestionstock/rapvente.html')

@login_required
@permission_required('gestionstock.delete_recettestocksortie',raise_exception=True)
def annulation(request):

    if request.method=="POST":
        t = Fmvts.objects.filter(location=request.session['idlocationuser'],document=request.POST.get('document'),datemvt=request.POST.get('dt'))
        if t:
            t.update(
                ajustement_id='SUP'
            )
            return JsonResponse(
                {"msg": "Opération effectuée",
                 "id": "1"},
                safe=False)
        else:
            return JsonResponse(
                {"msg": "Opération non effectuée",
                 "id": "0"}),

    context={
        "mvts":Fmvts.objects.filter(ajustement='FACT',location=request.session.get('idlocationuser'),article__isnull=True).values('document','datemvt','ndatemvt').order_by('document','ndatemvt').annotate(somme=Sum('prix_achat')).order_by('-ndatemvt')[:1000]
    }
    return render(request, 'gestionstock/annulation.html',context)

@login_required
@permission_required('gestionstock.view_recettestocksortie',raise_exception=True)
def reimprimer(request):

    if request.method=="POST":
        t = Fmvts.objects.filter(location=request.session['idlocationuser'],document=request.POST.get('document'),datemvt=request.POST.get('dt'))
        if t:
            tbdata = []
            tbdata.append(['Article', 'Qte', 'Pu', 'Total'])
            tot = 0.0
            numcmd = ""
            b = t.first()

            codeb = b.requisition
            my_code = EAN13(codeb, writer=ImageWriter())
            my_code.save("barcode")


            Titretyle = ParagraphStyle(
                name='titre',
                fontName='Helvetica-Bold',
                fontSize=8,
                textColor='DarkGray',
                borderPadding=(2, 2, 7, 2),
                borderWidth=0,
                alignment=TA_CENTER
            )

            Headerstyle = ParagraphStyle(
                name='headesr',
                fontName='Helvetica-Bold',
                fontSize=8,
                # borderPadding=(2, 2, 7, 2),
                # borderWidth=0,
                # borderColor='Gray',
                alignment=TA_CENTER
            )

            Headerstyle2 = ParagraphStyle(
                name='headesrd',
                fontName='Helvetica-Bold',
                fontSize=16,
                # borderPadding=(2, 2, 7, 2),
                # borderWidth=0,
                # borderColor='Gray',
                alignment=TA_CENTER
            )

            styles = getSampleStyleSheet()
            styleN = styles["BodyText"]
            styleN.alignment = TA_LEFT
            styleN.fontSize = 8

            styleNN = styles["BodyText"]
            styleNN.alignment = TA_RIGHT
            styleNN.fontSize = 8

            styleB = styles["Normal"]
            styleB.alignment = TA_LEFT
            styleB.fontSize = 8

            autonum = 0
            nom=""
            for i in t:
                numcmd = i.document
                nom=i.description
                tbdata.append([

                    Paragraph(f"{i.designation}", styleB),
                    Paragraph(f"{int(i.qteunit_sortie)}", styleN),
                    Paragraph(f"{i.prix_achat}", styleNN),
                    Paragraph(f"{i.qteunit_sortie * i.prix_achat}", styleNN)
                ])
                tot += i.qteunit_sortie * i.prix_achat

            # rapport

            elements = []

            header = Table([[Paragraph(
                'Sté<br/>Est XX<br/>15 rue, xxxx C/Limete Kinshasa<br/>RCCM 14-99 ID NAT. N397108<br/>NIF A078A Tél:+243 81 209 90 09',
                style=Headerstyle)]])
            elements.append(header)

            header = Table([[Paragraph(f'N°:00{numcmd}', style=Headerstyle2)]])
            elements.append(header)

            elements.append(Spacer(1, 5))

            header = Table([[Paragraph(
                f'<u>Date: {request.POST.get("dt")} Client: {nom}</u>',
                style=Headerstyle)]])
            elements.append(header)

            # Items

            table = Table(tbdata, colWidths=[3 * cm, 0.8 * cm, 1.5 * cm, 1.5 * cm])
            table.setStyle([
                # ('FONT', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 7),
                # ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
                ('GRID', (0, 0), (-1, 0), 0, (0.7, 0.7, 0.7)),
                # ('GRID', (-2, -1), (-1, -1), 0, (0.7, 0.7, 0.7)),
                # ('ALIGN', (0, 0), (-3, -3), 'LEFT'),
                ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                # ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
            ])
            elements.append(table)

            header = Table([[Paragraph("--------------------------------", style=styleNN)]])
            elements.append(header)

            header = Table([[Paragraph("Total USD {:,.2f}".format(tot), style=styleNN)]])
            elements.append(header)

            header = Table([[Paragraph("--------------------------------", style=styleNN)]])
            elements.append(header)

            header = Table([[Paragraph(
                "Merci de votre visite. A la prochaine.<br/> Est XX",
                style=Headerstyle)]])
            elements.append(header)

            im = img(settings.BASE_DIR + '\\' + 'barcode.png', 2 * inch, 1 * inch)
            elements.append(im)
            # barcode = code39.Extended39(codeb, barWidth=0.01 * inch, barHeight=.5 * inch)
            # elements.append(barcode)

            elements.append(Spacer(1, 40))

            # elements.append(Spacer(1, 40))

            pagesize = (7.1967 * cm, 29.6686 * cm)

            doc = SimpleDocTemplate(settings.MEDIA_ROOT + "\\fac.pdf", pagesize=pagesize, rightMargin=1, leftMargin=1,
                                    topMargin=1, bottomMargin=1, )
            # doc.build(elements,onFirstPage=drawPageFrame)
            doc.multiBuild(elements)

            return JsonResponse(
                {"msg": "Opération effectuée",
                 "id": "1"},
                safe=False)
        else:
            return JsonResponse(
                {"msg": "Opération non effectuée",
                 "id": "0"}),

    context={
        "mvts":Fmvts.objects.filter(ajustement='FACT',location=request.session.get('idlocationuser'),article__isnull=True).values('document','datemvt','ndatemvt').order_by('document','ndatemvt').annotate(somme=Sum('prix_achat')).order_by('-ndatemvt')[:1000]
    }
    return render(request, 'gestionstock/reimprimer.html',context)

@login_required
@permission_required('gestionstock.view_recettestocksortie',raise_exception=True)
def sortistockrecettes(request):

    if request.method == "POST":

        try:
            with transaction.atomic():

                cmdlist = json.loads(request.POST.get('cart_list'))

                #totgen = sum([float(i['product_price']) * float(i['product_quantity']) for i in cmdlist])
                if request.user.has_perm('gestionstock.add_recettestocksortie'):

                    codeb = str(request.POST.get('autonum')) + str(
                        str(datetime.today().date()).replace("-", "").replace("/", ""))
                    if int(request.POST.get('autonum')) < 10:
                        codeb += '1111'
                    elif int(request.POST.get('autonum')) < 100:
                        codeb += '111'
                    elif int(request.POST.get('autonum')) < 1000:
                        codeb += '11'
                    elif int(request.POST.get('autonum')) < 10000:
                        codeb += '1'

                    my_code = EAN13(codeb, writer=ImageWriter())
                    my_code.save("barcode")
                    codeb = str(my_code.get_fullcode())
                    t=Ftiers.objects.get(tiers=request.POST.get("client"))
                    nom=t.nompostnom
                    for i in cmdlist:
                        Fmvts.objects.create(
                            location_id=request.session.get('idlocationuser'),
                            periode=str(datetime.today().date()).replace("-", "").replace("/", ""),
                            datemvt=datetime.today().date(),
                            ndatemvt=str(datetime.today().date()).replace("-", "").replace("/", ""),

                            ajustement_id="FACT",
                            recette_id=i['product_id'],
                            document=request.POST.get("autonum"),
                            txchange=request.POST.get("taux"),
                            # facture=request.POST.get("dette"),
                            prix_total=request.POST.get("mtnpaye"),
                            designation=i['product_name'],
                            qte_sortie=i['product_quantity'],
                            flag="0",
                            qteunit_sortie=i['product_quantity'],
                            prix_achat=i['product_price'],
                            tiers_id=request.POST.get("client"),
                            requisition=str(codeb),
                            description=nom,
                            devise='USD',
                            codeuser=request.user,
                        )

                    ########ticket
                    t = Fmvts.objects.filter(document=request.POST.get('autonum'),ndatemvt=str(datetime.today().date()).replace("-", "").replace("/", ""))
                    tbdata = []
                    tbdata.append(['Article', 'Qte', 'Pu', 'Total'])
                    tot = 0.0




                    Titretyle = ParagraphStyle(
                        name='titre',
                        fontName='Helvetica-Bold',
                        fontSize=8,
                        textColor='DarkGray',
                        borderPadding=(2, 2, 7, 2),
                        borderWidth=0,
                        alignment=TA_CENTER
                    )

                    Headerstyle = ParagraphStyle(
                        name='headesr',
                        fontName='Helvetica-Bold',
                        fontSize=8,
                        # borderPadding=(2, 2, 7, 2),
                        # borderWidth=0,
                        # borderColor='Gray',
                        alignment=TA_CENTER
                    )

                    Headerstyle2 = ParagraphStyle(
                        name='headesrd',
                        fontName='Helvetica-Bold',
                        fontSize=16,
                        # borderPadding=(2, 2, 7, 2),
                        # borderWidth=0,
                        # borderColor='Gray',
                        alignment=TA_CENTER
                    )

                    styles = getSampleStyleSheet()
                    styleN = styles["BodyText"]
                    styleN.alignment = TA_LEFT
                    styleN.fontSize = 8

                    styleNN = styles["BodyText"]
                    styleNN.alignment = TA_RIGHT
                    styleNN.fontSize = 8

                    styleB = styles["Normal"]
                    styleB.alignment = TA_LEFT
                    styleB.fontSize = 8



                    for i in t:
                        tbdata.append([

                            Paragraph(f"{i.recette.libelle}", styleB),
                            Paragraph(f"{int(i.qte_sortie)}", styleN),
                            Paragraph(f"{i.prix_achat}", styleNN),
                            Paragraph(f"{float(i.qte_sortie) * float(i.prix_achat)}", styleNN)
                        ])
                        tot += float(i.qte_sortie) * float(i.prix_achat)
                    # rapport
                    mtnpaye=float(request.POST.get("mtnpaye"))
                    elements = []

                    header = Table([[Paragraph(
                        'Sté<br/>Ets XX<br/>15 rue, xxxx C/Limete Kinshasa<br/>RCCM 14-99 ID NAT. N397108<br/>NIF A078A Tél:+243 81 209 90 09',
                        style=Headerstyle)]])
                    elements.append(header)
                    header = Table([[Paragraph(f'N°:00{request.POST.get("autonum")}', style=Headerstyle2)]])
                    elements.append(header)

                    elements.append(Spacer(1, 5))

                    header = Table([[Paragraph(
                        f'<u>Date: {datetime.now().strftime("%y/%m/%d %H:%M:%S")} Client: {nom}</u>',
                        style=Headerstyle)]])
                    elements.append(header)

                    # Items

                    table = Table(tbdata, colWidths=[3 * cm, 0.8 * cm, 1.5 * cm, 1.5 * cm])
                    table.setStyle([
                        # ('FONT', (0, 0), (-1, -1), 'Helvetica'),
                        ('FONTSIZE', (0, 0), (-1, -1), 7),
                        # ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
                        ('GRID', (0, 0), (-1, 0), 0, (0.7, 0.7, 0.7)),
                        # ('GRID', (-2, -1), (-1, -1), 0, (0.7, 0.7, 0.7)),
                        # ('ALIGN', (0, 0), (-3, -3), 'LEFT'),
                        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                        # ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
                    ])
                    elements.append(table)

                    header = Table([[Paragraph("--------------------------------", style=styleNN)]])
                    elements.append(header)

                    header = Table([[Paragraph("Total USD {:,.2f}".format(tot), style=styleNN)]])
                    elements.append(header)
                    header = Table([[Paragraph("Motant Payé USD {:,.2f}".format(mtnpaye), style=styleNN)]])
                    elements.append(header)
                    header = Table([[Paragraph("Reste  USD {:,.2f}".format(tot-mtnpaye), style=styleNN)]])
                    elements.append(header)

                    header = Table([[Paragraph("--------------------------------", style=styleNN)]])
                    elements.append(header)

                    header = Table([[Paragraph(
                        "Merci de votre visite. A la prochaine.<br/> Ets XX",
                        style=Headerstyle)]])
                    elements.append(header)

                    im = img(settings.BASE_DIR + '\\' + 'barcode.png', 2 * inch, 1 * inch)
                    elements.append(im)
                    # barcode = code39.Extended39(codeb, barWidth=0.01 * inch, barHeight=.5 * inch)
                    # elements.append(barcode)

                    elements.append(Spacer(1, 40))

                    pagesize = (7.1967 * cm, 29.6686 * cm)

                    doc = SimpleDocTemplate(settings.MEDIA_ROOT + "\\fac.pdf", pagesize=pagesize, rightMargin=1,
                                            leftMargin=1,
                                            topMargin=1, bottomMargin=1, )
                    # doc.build(elements,onFirstPage=drawPageFrame)
                    doc.multiBuild(elements)
                    ########ticket
                else:
                    return JsonResponse(
                        {"msg": "Opération non effectuée.Vous avez pas ce droit",
                         "id": "0"}, safe=False)
                return JsonResponse({"msg": "Opération effectuée ", "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)

    # clients=Ftiers.objects.all()
    #
    # datafull={}
    # datafullitem=[]
    # datafullitemtempo=[]
    # for i in clients:
    #     detal=DetailRecettes.objects.filter(client_id=i.tiers)
    #     if detal:
    #         for x in detal:
    #             code=str(i.tiers)+ "_"+str(x.recettes_id)+ "_"+str(x.id)
    #             if code in datafullitemtempo:
    #                 pass
    #             else:
    #                 datafull={}
    #                 datafull['id']=code
    #                 datafull['libelle']=str(i.nompostnom)+ " => "+str(x.recettes.libelle)
    #                 datafullitem.append(datafull)
    #                 datafullitemtempo.append(code)


    context = {
            "recettes":Recettes.objects.all().order_by('libelle'),
            "categories":CategorieArticle.objects.all().order_by('libelle'),
        "fournisseur": Ftiers.objects.filter(typetiers__in=("1", "2")).order_by('nompostnom'),
        }
    return render(request, 'gestionstock/commande.html', context)


@login_required
@permission_required('gestionstock.Entrer_Stock_valid',raise_exception=True)
def entrestockvalid(request):
    context = {
    "bon":Flivraison.objects.filter(commande__location_id= request.session.get('idlocationuser'),etatliv="0",validation=True).order_by('-serielivraison'),
        "taux":Flocation.objects.get(location=request.session.get('idlocationuser'))

    }
    if request.method=="POST":
        b = Fdetlivraison.objects.filter(serielivraison_id=request.POST.get('numbon'))
        if b:
            try:
                with transaction.atomic():

                    for i in b:




                        aj=Fajustement.objects.get(ajustement="ACH")
                        # p = int(str(request.POST.get('dateop'))[5:7])
                        #
                        # if p < 9:
                        #     p = str(p).replace("0", "")
                        # p = int(p)
                        libemb=""
                        emba=Fdetcde.objects.filter(commande=i.serielivraison.commande.commande,article_id=i.article.article)
                        if emba:
                            emba=emba.first()
                            libemb=emba.emballage.emballage
                        #----------------------------------
                        resultat1 = 0
                        resultat2 = 0
                        prixcmpgros=0
                        prixcmpdetail=0
                        idemb = ""

                        art = Farticle.objects.filter(article=i.article.article,emballagee_id=libemb)
                        art2 = Farticle.objects.filter(article=i.article.article,emballageu_id=libemb)

                        if art:
                            resultat1 = i.qtelivree
                            resultat2 = float(i.qtelivree) * art.first().quantiteu
                            # if art2:
                            #     resultat2 = i.qtelivree
                            # else:
                            #     resultat2 = float(i.qtelivree) * art.first().quantitee
                            # tot=getstockproduit(request.session.get('idlocationuser'),i.article.article,libemb)
                            # prixcmpdetail=((tot*art.first().prix_vente)+(resultat1*i.prixunitaire))/(resultat1+tot)
                        elif art2:
                            resultat2 = i.qtelivree
                            resultat1 = float(i.qtelivree) / art2.first().quantiteu
                            # prixcmpdetail=((tot*art.first().prix_vente)+(i.qtelivree*i.prixunitaire))/(resultat2+tot)

                        #################################################################CMP
                        artic = Farticle.objects.get(article=i.article.article)
                        tot=getstockproduit(request.session.get('idlocationuser'),i.article.article,artic.emballageu_id)
                        prixcmpdetail=((tot*art.first().prix_vente)+(resultat2*i.prixunitaire))/(resultat2+tot)




                        #################################################################


                        Fmvts.objects.create(
                        location_id=i.serielivraison.commande.location.location,
                        # periode=p,
                        datemvt=request.POST.get('dateop'),
                        ndatemvt=str(request.POST.get('dateop')).replace("-","").replace("/",""),
                        requisition=i.serielivraison.serielivraison,
                        document=i.serielivraison.document,
                        ajustement_id=aj.ajustement,
                        tiers_id=i.serielivraison.commande.tiers.tiers,
                        article_id=i.article.article,
                        emballage_id=libemb,
                        # quantite=i.qtelivree,
                        qte_entree=resultat1,
                        qteunit_entree=resultat2,
                        prix_achat=i.prixunitaire,
                        prix_vente=0,
                        # devise="",
                        txchange=str(request.POST.get('taux')).replace(",","."),
                        codeuser_id=request.user.id,
                        )


                        artic.prix_vente = prixcmpdetail
                        artic.prix_achat = i.prixunitaire
                        artic.pa = i.prixunitaire
                        artic.save()
                        # if art:
                        #     artic = Farticle.objects.get(article=i.article.article)
                        #     artic.prix_vente = prixcmpdetail
                        #     artic.prix_achat = i.prixunitaire
                        #     artic.save()
                        # elif art2:
                        #     artic = Farticle.objects.get(article=i.article.article)
                        #     artic.prix_vente = prixcmpdetail
                        #     artic.pa = i.prixunitaire
                        #     artic.save()
                    fliv=Flivraison.objects.get(serielivraison=request.POST.get('numbon'))
                    fliv.etatliv="1"
                    fliv.save()

                    return JsonResponse({"msg": "Opération effectuée ", "id": "1"}, safe=False)
            except Exception as e:
                return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)
        else:
            return JsonResponse({"msg": "Opération non effectuée ", "id": "0"}, safe=False)
    return render(request, 'gestionstock/entrestockvalid.html', context)



@login_required
@permission_required('gestionstock.Modifi_Produit_Prix_valide',raise_exception=True)
def modiproduitvalid(request):

    context = {"produit": TempoPrix.objects.filter(etat=False).order_by('designation'),

               }

    if request.method == "POST":

        try:
            with transaction.atomic():
                if "one" in request.POST:
                    tempo = TempoPrix.objects.get(id=request.POST.get('one'))
                    Farticle.objects.filter(article=tempo.article.article).update(prix_achat=tempo.prix1,
                                                                                  pa=tempo.prix2)
                    tempo.etat=True
                    tempo.save()
                else:
                    tempo = TempoPrix.objects.filter(etat=False)
                    for i in tempo:
                        Farticle.objects.filter(article=i.article.article).update(prix_achat=i.prix1,
                                                                                      pa=i.prix2)
                        i.etat=True
                        i.save()
                return JsonResponse(
                    {"msg": "Opération effectuée",
                     "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)
    return render(request, 'gestionstock/modiproduitvalid.html', context)


@login_required
@permission_required('gestionstock.Modifi_Produit_Prix',raise_exception=True)
def modiproduit(request):



    if request.method == "POST":
        if 'modi' in request.POST:
            try:
                with transaction.atomic():

                    pro = Fmvts.objects.filter(mvt=request.POST.get('id')).update(
                        prix_achat=request.POST.get('pa'),
                        prix_vente=0
                    )
                    return JsonResponse(
                        {"msg": "Opération effectuée",
                         "id": "1"}, safe=False)
            except Exception as e:
                return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)

        # else:
        #
        #     try:
        #         with transaction.atomic():
        #
        #             Farticle.objects.filter(article=request.POST.get('produit')).update(prix_vente=request.POST.get('prix1'),prix_achat=request.POST.get('prix1'),
        #                                                                           pa=request.POST.get('prix1'))
        #             return JsonResponse(
        #                 {"msg": "Opération effectuée",
        #                  "id": "1"}, safe=False)
        #     except Exception as e:
        #         return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)

    context = {
        "produit": Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser')).order_by('designation'),

        }
    return render(request, 'gestionstock/modiproduit.html', context)



@login_required
@permission_required('gestionstock.Bon_Commande_valide',raise_exception=True)
def boncommandevalide(request):

    context = {
               "bon": Fcommande.objects.filter(etatcde="0",validation=True,location_id=request.session.get('idlocationuser')).order_by('tiers__nompostnom'),
               }

    if request.method == "POST":

        try:
            with transaction.atomic():

                bon=Fcommande.objects.get(commande=request.POST.get('bon'),location_id=request.session.get('idlocationuser'))
                bon.etatcde="1"
                bon.typecommande=request.POST.get('mode')
                bon.datelivraison=request.POST.get('dateliv')
                bon.save()
                return JsonResponse(
                    {"msg": "Opération effectuée",
                     "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)

    return render(request, 'gestionstock/boncommandeval.html', context)




@login_required
@permission_required('gestionstock.supprimer_valide',raise_exception=True)
def supprimer(request):


    if request.method == "POST":

        try:
            with transaction.atomic():

                #modifier commande et livraison

                bon=Fcommande.objects.get(commande=request.POST.get('bon'),location_id=request.session.get('idlocationuser'))
                bon.etatcde="1"
                bon.typecommande=request.POST.get('mode')
                bon.datelivraison=request.POST.get('dateliv')
                bon.save()
                return JsonResponse(
                    {"msg": "Opération effectuée",
                     "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)

    return render(request, 'gestionstock/supprimer.html')



@login_required
# @permission_required('gestionstock.ajustementpro_valide',raise_exception=True)
def ajustementpro(request):


    if request.method == "POST":

        try:
            with transaction.atomic():


                # prixcmpdetail=0
                artic = Farticle.objects.get(article=request.POST.get('produit'))

                resultat2 = float(request.POST.get('qte'))
                art = Farticle.objects.filter(article=request.POST.get('produit'), emballagee_id=request.POST.get('emb'))
                art2 = Farticle.objects.filter(article=request.POST.get('produit'), emballageu_id=request.POST.get('emb'))
                art3 = Farticle.objects.filter(article=request.POST.get('produit'), emballagea=request.POST.get('emb'))

                if art:
                    pa = float(art.first().prix_achat)
                elif art2:
                    pa = float(art2.first().pa)
                elif art3:
                    pa = float(art3.first().old_prix_achat)

                if request.POST.get('qte')!='':
                    if str(request.POST.get('ajustement')).strip() == 'PAT':#ajustement positif


                        # tot=getstockproduit(request.session.get('idlocationuser'),request.POST.get('produit'),artic.emballageu_id)
                        #
                        # if (resultat2+tot) != 0:
                        #     prixcmpdetail=((tot*artic.prix_vente)+(resultat2*artic.pa))/(resultat2+tot)
                        # else:
                        #     prixcmpdetail=artic.prix_vente

                        Fmvts.objects.create(
                            location_id=request.session.get('idlocationuser'),
                            datemvt=request.POST.get('dateop'),
                            ndatemvt=str(request.POST.get('dateop')).replace("-","").replace("/",""),
                            requisition="AJUSTEMENT",
                            document="AJUSTEMENT",
                            ajustement_id=request.POST.get('ajustement'),
                            article_id=request.POST.get('produit'),
                            emballage_id=request.POST.get('emb'),
                            # quantite=i.qtelivree,
                            qte_entree=resultat2,
                            # qteunit_entree=resultat2,
                            prix_achat=pa,
                            prix_vente=0,
                            devise="USD",
                            txchange=artic.LOCATION.txchange,
                            codeuser_id=request.user.id,
                        )

                    else:#ajustement negatif

                        #################################################################CMP

                        # tot=getstockproduit(request.session.get('idlocationuser'),request.POST.get('produit'),artic.emballageu_id)
                        # tot=tot-resultat2
                        # if (tot) != 0:
                        #     prixcmpdetail=((tot*artic.pa))/(tot)
                        # else:
                        #     prixcmpdetail=artic.prix_vente


                        Fmvts.objects.create(
                            location_id=request.session.get('idlocationuser'),
                            datemvt=request.POST.get('dateop'),
                            ndatemvt=str(request.POST.get('dateop')).replace("-","").replace("/",""),
                            requisition="AJUSTEMENT",
                            document="AJUSTEMENT",
                            ajustement_id=request.POST.get('ajustement'),
                            article_id=request.POST.get('produit'),
                            emballage_id=request.POST.get('emb'),
                            # quantite=i.qtelivree,
                            qte_sortie=resultat2,
                            prix_achat=pa,
                            prix_vente=0,
                            devise="USD",
                            txchange=artic.LOCATION.txchange,
                            codeuser_id=request.user.id,
                        )
                        #################################################################


                ########################################"


                return JsonResponse({"msg": "Opération effectuée ", "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)

    context = {
        "produit": Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser')).order_by('designation'),
        "ajustement": Fajustement.objects.filter(ajustement__in=('DECL', 'PAT')).order_by('designation'),
    }
    return render(request, 'gestionstock/ajustementpro.html',context)

@login_required
@permission_required('gestionstock.ajustement_valide',raise_exception=True)
def ajustement(request):

    context = {
        "bon":Flivraison.objects.filter(commande__location_id= request.session.get('idlocationuser'),etatliv="1").order_by('-serielivraison'),
    }

    return render(request, 'gestionstock/ajustement.html',context)


@login_required
@permission_required('gestionstock.Bon_Commande_Interne',raise_exception=True)
def boncommandeinterne(request):

    context = {"produit": Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser')).order_by('designation'),
               "taux": Ftaxes.objects.get(taxe='001'),
               "location": Flocation.objects.filter(typelocation="D",location=request.session['idlocationuser']).order_by('designation'),
               "fournisseur": Ftiers.objects.filter(nature="FOURNISSEUR").order_by('nompostnom'),
               }

    if request.method == "POST":

        try:
            with transaction.atomic():

                bon=Fcommande.objects.filter(commande=request.POST.get('numbon'),userr_id=request.user.id,location_id=request.session.get('idlocationuser'))
                if bon:
                    bon=bon.first()
                else:
                    bon=Fcommande.objects.create(
                        commande=request.POST.get('numbon'),
                        datejour=request.POST.get('datebon'),
                        tiers_id=request.POST.get('fournisseur'),
                        # typecommande = request.POST.get('mode'),
                        location_id=request.POST.get('location'),
                        devise=request.POST.get('devise'),
                        userr_id=request.user.id,)
                # resultat1=0
                # resultat2=0
                # idemb=""
                # art=Farticle.objects.get(article=request.POST.get('produit'))
                #
                # if request.POST.get('emballage')=="1":
                #     resultat1=request.POST.get('qte')
                #     resultat2=float(request.POST.get('qte'))*art.quantitee
                #     idemb=art.emballagee_id
                # elif request.POST.get('emballage')=="2":
                #     resultat2=request.POST.get('qte')
                #     resultat1=float(request.POST.get('qte'))/art.quantitee
                #     idemb=art.emballageu_id


                b= Fdetcde.objects.filter(commande__commande=request.POST.get('numbon'),article_id=request.POST.get('produit'))
                if b:

                	b.update(
                        quantite=request.POST.get('qte'),
                        prix_unitaire=str(request.POST.get('prix')).replace(",", "."),
                        # qteunitaire=resultat2
                	)
                else:
                	Fdetcde.objects.create(commande=bon,
                	article_id=request.POST.get('produit'),
                	quantite = request.POST.get('qte'),
                	prix_unitaire = str(request.POST.get('prix')).replace(",","."),
                    # qteunitaire = resultat2
                    )
                return JsonResponse(
                    {"msg": "Opération effectuée",
                     "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)

    context['numbon'] = "BC000" + str(Fcommande.objects.count() + 1)
    return render(request, 'gestionstock/boncommandeinterne.html', context)

@login_required
@permission_required('gestionstock.Bon_Commande_Externe',raise_exception=True)
def boncommande(request):

    f=Flocation.objects.filter(typelocation='D',location=request.session['idlocationuser']).order_by('designation')
    if not f:
        messages.error(request, "Ce local n'est pas autorisé à établir la commande pour achats.")
        return redirect(reverse('gestionstock:home'))

    if request.session.get('idlocationuser') == 'DSBB':
        context = {"produit": Farticle.objects.all().order_by(
            'designation'),
                   "taux": Flocation.objects.get(location=request.session.get('idlocationuser')).txchange,
                   "location": f,
                   "fournisseur": Ftiers.objects.filter(nature="FOURNISSEUR").order_by('nompostnom'),
                   }
    else:
        context = {"produit": Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser')).order_by('designation'),
               "taux": Flocation.objects.get(location=request.session.get('idlocationuser')).txchange,
               "location":f ,
               "fournisseur": Ftiers.objects.filter(nature="FOURNISSEUR").order_by('nompostnom'),
               }

    if request.method == "POST":

        try:
            with transaction.atomic():


                if request.POST.get('devise') == 'CDF':
                    pa = float(request.POST.get('prix')) / float(str(request.POST.get('taux')).replace(",", "."))
                else:
                    pa = float(request.POST.get('prix'))

                bon=Fcommande.objects.filter(commande=request.POST.get('numbon'),userr_id=request.user.id,location_id=request.session.get('idlocationuser'))
                if bon:
                    bon=bon.first()
                else:
                    bon=Fcommande.objects.create(
                        commande=request.POST.get('numbon'),
                        observation=request.POST.get('numbont'),
                        datejour=request.POST.get('datebon'),
                        tiers_id=request.POST.get('fournisseur'),
                        # datelivraison=request.POST.get('dateliv'),
                        # typecommande = request.POST.get('mode'),
                        location_id=request.POST.get('location'),
                        # etatcde="0",
                        etatcde="1",
                        # devise=request.POST.get('devise'),
                        userr_id=request.user.id,)
                resultat=0
                idemb=""
                art=Farticle.objects.get(article=request.POST.get('produit'))

                if request.POST.get('emballage')=="1":
                    # resultat=request.POST.get('qte')
                    # resultat2=float(request.POST.get('qte'))*art.quantitee
                    idemb = art.emballagee_id
                elif request.POST.get('emballage')=="2":
                    # resultat2=request.POST.get('qte')
                    # resultat1=float(request.POST.get('qte'))/art.quantitee
                    idemb = art.emballageu_id




                b= Fdetcde.objects.filter(commande__commande=request.POST.get('numbon'),article_id=request.POST.get('produit'))
                if b:
                    k = b.first().quantite
                    b.update(
                        prix_unitaire=pa,
                        quantite=float(request.POST.get('qte')) + float(k),
                        # designation=request.POST.get('libunite'),
                        emballage_id=idemb,
                        ptusd=str(request.POST.get('taux')).replace(",", "."),
                        # emballage2_id=idemb2,
                	)
                else:
                	Fdetcde.objects.create(
                	commande=bon,
                	article_id=request.POST.get('produit'),
                	# designation=request.POST.get('libunite'),
                	emballage_id=idemb,
                        qte_livree=0,
                        ptusd=str(request.POST.get('taux')).replace(",", "."),
                	# emballage2_id=idemb2,
                	quantite = request.POST.get('qte'),
                	prix_unitaire = pa,
                    # qteunitaire = resultat2
                )
                return JsonResponse(
                    {"msg": "Opération effectuée",
                     "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)

    cmd=Fcommande.objects.all().order_by('-created_at')
    if cmd:
        cmd=cmd.first()
        cmd=str(cmd.commande).split("BC000")[1]
        context['numbon'] = "BC000" + str( int(cmd)+ 1)
    else:
        context['numbon'] = "BC000" + str( Fcommande.objects.all().count()+ 1)


    return render(request, 'gestionstock/boncommande.html', context)


@login_required
@permission_required('gestionstock.Bon_Commande_Modi',raise_exception=True)
def boncommandemodi(request):
    f = Flocation.objects.filter(typelocation='D', location=request.session['idlocationuser']).order_by('designation')
    if not f:
        messages.error(request, "Ce local n'est pas autorisé à établir la commande pour achats.")
        return redirect(reverse('gestionstock:home'))

    if request.session.get('idlocationuser') == 'DSBB':
        context = {
                "taux": Flocation.objects.get(location=request.session.get('idlocationuser')).txchange,
               # "commande": Fcommande.objects.filter(etatcde="1",validation=True,cloture=False,location_id=request.session.get('idlocationuser')).order_by('tiers__nompostnom'),
               "commande": Fcommande.objects.filter(etatcde="1",validation=False,location_id=request.session.get('idlocationuser')).order_by('tiers__nompostnom'),
               "produit": Farticle.objects.all().order_by('designation'),
               "location": f,
               "fournisseur": Ftiers.objects.filter(nature="FOURNISSEUR").order_by('nompostnom'),
               }
    else:
        context = {
            "taux": Flocation.objects.get(location=request.session.get('idlocationuser')).txchange,
            # "commande": Fcommande.objects.filter(etatcde="1",validation=True,cloture=False,location_id=request.session.get('idlocationuser')).order_by('tiers__nompostnom'),
            "commande": Fcommande.objects.filter(etatcde="1", validation=False,
                                                 location_id=request.session.get('idlocationuser')).order_by(
                'tiers__nompostnom'),
            "produit": Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser')).order_by(
                'designation'),
            "location": f,
            "fournisseur": Ftiers.objects.filter(nature="FOURNISSEUR").order_by('nompostnom'),
        }

    if request.method == "POST":

        try:
            with transaction.atomic():

                if 'qtecmd' in request.POST:
                    b = Fdetcde.objects.filter(id=request.POST.get('idcode'))
                    if b:
                        b.update(
                            quantite=request.POST.get('qte'),
                        )
                    return JsonResponse(
                        {"msg": "Opération effectuée",
                         "id": "1"}, safe=False)


                bon=Fcommande.objects.filter(commande=request.POST.get('numbon'),location_id=request.session.get('idlocationuser'))
                if bon:

                    bon.update(
                    datejour=request.POST.get('datebon'),
                    # datelivraison=request.POST.get('dateliv'),
                    # typecommande = request.POST.get('mode'),
                    )
                    bon=bon.first()
                # else:
                #     bon=Fcommande.objects.create(
                #         commande=request.POST.get('numbon'),
                #         datejour=request.POST.get('datebon'),
                #         tiers_id=request.POST.get('fournisseur'),
                #         datelivraison=request.POST.get('dateliv'),
                #         typecommande = request.POST.get('mode'),
                #         location_id=request.POST.get('location'),
                #         etatcde="0",
                #         # devise=request.POST.get('devise'),
                #         userr_id=request.user.id,)
                resultat=0
                idemb=""
                art=Farticle.objects.get(article=request.POST.get('produit'))

                if request.POST.get('emballage')=="1":
                    # resultat=request.POST.get('qte')
                    # resultat2=float(request.POST.get('qte'))*art.quantitee
                    idemb = art.emballagee_id
                elif request.POST.get('emballage')=="2":
                    # resultat2=request.POST.get('qte')
                    # resultat1=float(request.POST.get('qte'))/art.quantitee
                    idemb = art.emballageu_id



                if request.POST.get('devise') == 'CDF':
                    pa = float(request.POST.get('prix')) / float(str(request.POST.get('taux')).replace(",", "."))
                else:
                    pa = float(request.POST.get('prix'))

                b= Fdetcde.objects.filter(commande__commande=request.POST.get('numbon'),article_id=request.POST.get('produit'))
                if b:
                    k=b.first().quantite
                    b.update(
                        prix_unitaire=pa,
                        quantite=float(request.POST.get('qte'))+float(k),
                        designation=request.POST.get('libunite'),
                        emballage_id=idemb,
                        ptusd=str(request.POST.get('taux')).replace(",", "."),
                        # emballage2_id=idemb2,
                    )
                else:
                    Fdetcde.objects.create(
                        commande=bon,
                        article_id=request.POST.get('produit'),
                        designation=request.POST.get('libunite'),
                        ptusd=str(request.POST.get('taux')).replace(",", "."),
                        emballage_id=idemb,
                        qte_livree=0,
                        # emballage2_id=idemb2,
                        quantite = request.POST.get('qte'),
                        prix_unitaire = pa,
                        # qteunitaire = resultat2
                    )
                return JsonResponse(
                    {"msg": "Opération effectuée",
                     "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)

    return render(request, 'gestionstock/boncommandemodi.html', context)


@login_required
@permission_required('gestionstock.view_detailrecettes',raise_exception=True)
def fabproduction(request):

    if request.method == "POST":

        try:
            with transaction.atomic():

                r = Recettes.objects.filter(id=request.POST.get('idrecette'))

                if r:
                    if request.user.has_perm('gestionstock.change_recettes'):
                        r=r.last()
                        if 'img' not in request.FILES:
                            r.libelle=str(request.POST.get('designation')).upper()
                            r.prix=request.POST.get('prix')
                            r.location_id=request.session.get('idlocationuser')
                            r.categorie_id=request.POST.get('categorie')
                            r.user=request.user
                            r.save()
                        else:
                            r.libelle = str(request.POST.get('designation')).upper()
                            r.prix = request.POST.get('prix')
                            r.image=request.FILES["img"]
                            r.location_id = request.session.get('idlocationuser')
                            r.categorie_id = request.POST.get('categorie')
                            r.user = request.user
                            r.save()
                    else:
                        return JsonResponse({"msg": "Erreur !!!.Vous avez pas ce droit", "id": "0"}, safe=False)
                else:

                    if request.user.has_perm('gestionstock.add_recettes'):

                        if 'img' not in request.FILES:
                            Recettes.objects.create(
                                libelle=str(request.POST.get('designation')).upper(),
                                prix=request.POST.get('prix'),
                                location_id=request.session.get('idlocationuser'),
                                categorie_id=request.POST.get('categorie'),
                                user=request.user
                            )
                        else:
                            Recettes.objects.create(
                            libelle=str(request.POST.get('designation')).upper(),
                            prix=request.POST.get('prix'),
                            image=request.FILES["img"],
                            location_id=request.session.get('idlocationuser'),
                            categorie_id=request.POST.get('categorie'),
                            user=request.user
                            )
                    else:
                        return JsonResponse({"msg": "Erreur !!!.Vous avez pas ce droit", "id": "0"}, safe=False)

                return JsonResponse(
                    {"msg": "Opération effectuée",
                     "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)

    context={
        'produit':Farticle.objects.all().order_by('designation'),
        'recettes':Recettes.objects.all().order_by('libelle'),
    }
    return render(request, 'gestionstock/fabproduction.html',context)






@login_required
@permission_required('gestionstock.view_recettes',raise_exception=True)
def production(request):

    if request.method == "POST":

        try:
            with transaction.atomic():

                r = Recettes.objects.filter(id=request.POST.get('idrecette'))

                if r:
                    if request.user.has_perm('gestionstock.change_recettes'):
                        r=r.last()
                        if 'img' not in request.FILES:
                            r.libelle=str(request.POST.get('designation')).upper()
                            # r.prix=request.POST.get('prix')
                            # r.location_id=request.session.get('idlocationuser')
                            r.categorie=request.POST.get('categorie')
                            # r.user=request.user
                            r.save()
                        else:
                            r.libelle = str(request.POST.get('designation')).upper()
                            # r.prix = request.POST.get('prix')
                            # r.image=request.FILES["img"]
                            # r.location_id = request.session.get('idlocationuser')
                            # r.categorie_id = request.POST.get('categorie')
                            # r.user = request.user
                            r.categorie = request.POST.get('categorie')
                            r.save()
                    else:
                        return JsonResponse({"msg": "Erreur !!!.Vous avez pas ce droit", "id": "0"}, safe=False)
                else:

                    if request.user.has_perm('gestionstock.add_recettes'):

                        if 'img' not in request.FILES:
                            Recettes.objects.create(
                                libelle=str(request.POST.get('designation')).upper(),
                                categorie = request.POST.get('categorie')
                                # prix=request.POST.get('prix'),
                                # location_id=request.session.get('idlocationuser'),
                                # categorie_id=request.POST.get('categorie'),
                                # user=request.user
                            )
                        else:
                            Recettes.objects.create(
                            libelle=str(request.POST.get('designation')).upper(),
                                categorie=request.POST.get('categorie')
                            # prix=request.POST.get('prix'),
                            # image=request.FILES["img"],
                            # location_id=request.session.get('idlocationuser'),
                            # categorie_id=request.POST.get('categorie'),
                            # user=request.user
                            )
                    else:
                        return JsonResponse({"msg": "Erreur !!!.Vous avez pas ce droit", "id": "0"}, safe=False)

                return JsonResponse(
                    {"msg": "Opération effectuée",
                     "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)

    context={
        'categorie':CategorieArticle.objects.all().order_by('libelle'),
    }
    return render(request, 'gestionstock/production.html',context)


@require_POST
@login_required
@permission_required('gestionstock.delete_recettes',raise_exception=True)
def deleteproduction(request):

    if request.method == "POST":

        try:
            with transaction.atomic():

                r = Recettes.objects.get(id=request.POST.get('id'))
                r.delete()
                return JsonResponse(
                    {"msg": "Opération effectuée",
                     "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)


@login_required
@permission_required('gestionstock.recettesfiche',raise_exception=True)
def plat(request):
    if request.method == "POST":
        try:
            with transaction.atomic():

                if(request.POST.get('categorie') == "0"):  # produit
                    recd = PlatRecette.objects.filter(plat_id=request.POST.get('recette'),
                                                      produit_id=request.POST.get('produit'),recettes__isnull=True)
                else:
                    recd = PlatRecette.objects.filter(plat_id=request.POST.get('recette'),
                                                      recettes_id=request.POST.get('produit'))


                if recd:
                    if request.POST.get('suppression')=="non":
                        if (request.POST.get('categorie') == "0"):  # produit
                            recd.update(
                            qte=request.POST.get('qte'),
                            pu=request.POST.get('prix'),
                            emballage_id=request.POST.get('emballage')
                            )
                        else:
                            pass
                    else:
                        recd.delete()
                else:
                    if (request.POST.get('categorie')=="0"):#produit
                        PlatRecette.objects.create(
                            # recettes_id=request.POST.get('recette'),
                            plat_id=request.POST.get('recette'),
                            produit_id=request.POST.get('produit'),
                            pu=request.POST.get('prix'),
                            qte=request.POST.get('qte'),
                            emballage_id=request.POST.get('emballage')
                        )
                    else:#recettes
                        for i in DetailRecettes.objects.filter(recettes_id=request.POST.get('produit')):

                            PlatRecette.objects.create(
                                obs=i.recettes.libelle,
                                recettes_id=i.recettes.id,
                                plat_id=request.POST.get('recette'),
                                produit_id=i.produit_id,
                                pu=i.pu,
                                qte=i.qte,
                                emballage_id=i.emballage_id
                            )

                return JsonResponse(
                    {"msg": "Opération effectuée",
                     "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)
    else:
        context = {
                    'produit': Farticle.objects.all().order_by('designation'),
                    'recettes': Recettes.objects.filter(categorie=False).order_by('libelle'),
                    # 'client':Ftiers.objects.filter(nature="CLIENT").order_by('nompostnom'),
                   }
        return render(request, 'gestionstock/plat.html',context)


@login_required
@permission_required('gestionstock.view_detailrecettes',raise_exception=True)
def getrecettesdetail2(request):
    # cdz=str(request.GET.get("recette")).split("_")
    # if len(cdz)>=2:
    #     recx = DetailRecettes.objects.filter(client_id=cdz[0],recettes_id=cdz[1]).order_by('produit__designation')
    # else:
    if request.GET.get("recette")=='':
        return JsonResponse({'data': {}}, safe=False)
    else:

        recx = PlatRecette.objects.filter(plat_id=request.GET.get("recette")).order_by('produit__designation')
        rec=[]
        tot=0
        for i in recx:
            datafull = {}
            datafull['id']=i.id
            datafull['produit__designation']=i.produit.designation
            datafull['produit__id']=i.produit.article
            datafull['obs']=i.obs
            datafull['recette_id']=i.recettes_id
            datafull['produit__pa']=i.pu
            datafull['qte']=i.qte
            datafull['emballage__emballage']=i.emballage.emballage
            tot=tot+(float(i.pu)*float(i.qte))
            datafull['total']=tot
            rec.append(datafull)


        rec=list(rec)
        return JsonResponse({'data': rec}, safe=False)


@login_required
@permission_required('gestionstock.recettesfiche',raise_exception=True)
def fichetechnique(request):
    if request.method == "POST":
        try:
            with transaction.atomic():


                recd=DetailRecettes.objects.filter(recettes_id=request.POST.get('recette'),
                                                   produit_id=request.POST.get('produit'))
                if recd:
                    if request.POST.get('suppression')=="non":
                        recd.update(
                        qte=request.POST.get('qte'),
                        pu=request.POST.get('prix'),
                        emballage_id=request.POST.get('emballage')
                        )
                    else:
                        recd.delete()
                else:
                    DetailRecettes.objects.create(
                        recettes_id=request.POST.get('recette'),
                    produit_id=request.POST.get('produit'),
                    pu=request.POST.get('prix'),

                    qte=request.POST.get('qte'),
                    emballage_id=request.POST.get('emballage')
                    )

                return JsonResponse(
                    {"msg": "Opération effectuée",
                     "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)
    else:
        context = {
                    'produit': Farticle.objects.all().order_by('designation'),
                    # 'client':Ftiers.objects.filter(nature="CLIENT").order_by('nompostnom'),
                   }
        return render(request, 'gestionstock/productiontechnique.html',context)



@login_required
def facture(request):

    context = {"produit": Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser')).order_by('designation'),
               "tiers": Ftiers.objects.all().order_by('nompostnom'),
               "taux": Ftaxes.objects.get(taxe='001'),
               }

    if request.method == "POST":
        try:
            with transaction.atomic():

                fact=Fmvts.objects.filter(location_id=request.session['idlocationuser'],ajustement_id="FACT",document=request.POST.get('numfact'))
                if fact:
                    pass
                else:
                    emb=request.POST.get('emballage')
                    rqt=request.POST.get('qte')
                    if emb=="2":
                        art=Farticle.objects.get(article=request.POST.get('produit'))
                        rqt=(float(request.POST.get('qte')))/art.quantiteu

                    Fmvts.objects.create(

                        tiers_id=request.POST.get('fournisseur'),
                        location_id=request.session['idlocationuser'],
                        codeuser_id=request.user.id,
                        datemvt=request.POST.get('dateop'),
                        ndatemvt=str(request.POST.get('dateop')).replace("-", "").replace("/", ""),
                        ajustement_id="FACT",
                        article_id=request.POST.get('produit'),
                        qte_sortie=rqt,
                        document=request.POST.get('numfact'),
                        prix_vente=request.POST.get('prix'),
                        devise=request.POST.get('devise'),
                        txchange=str(request.POST.get('taux')).replace(",", "."),
                    )


                return JsonResponse(
                    {"msg": "Opération effectuée",
                     "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)

    context['numfactt'] = "FCT" + str(Fmvts.objects.filter(location_id=request.session['idlocationuser'],ajustement_id="FACT").count() + 1) + str(datetime.today().date()).replace("-", "")
    return render(request, 'gestionstock/facture.html', context)
@login_required
def deletearticle(request):

    if request.method == "POST":

        try:
            with transaction.atomic():
 
                b= Fdetcde.objects.filter(commande__commande=request.POST.get('numbon'),article__designation=request.POST.get('article'))
                if b:
                    b.delete()

                return JsonResponse(
                    {"msg": "Opération effectuée",
                     "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)

@login_required
def annulercommande(request):

    if request.method == "POST":

        try:
            with transaction.atomic():

                bon=Fcommande.objects.filter(commande=request.POST.get('numbon'),location_id=request.session.get('idlocationuser'))
                if bon:
                    b= Fdetcde.objects.filter(commande__commande=request.POST.get('numbon'))
                    if b:
                        b.delete()
                    bon.delete()

                cmd=Fcommande.objects.all().order_by('-created_at')
                if cmd:
                    cmd=cmd.first()
                    cmd=str(cmd.commande).split("BC000")[1]
                    return JsonResponse(
                        {"msg": "Opération effectuée",
                         "id": "1","bon":"BC000" + str( int(cmd)+ 1)}, safe=False)
                else:
                    return JsonResponse(
                    {"msg": "Opération effectuée",
                     "id": "1","bon":"BC000" + str( Fcommande.objects.all().count()+ 1)}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)





@login_required
def supprimerretour(request):

    if request.method == "POST":

        try:
            with transaction.atomic():

                bon=Fmvts.objects.filter(document=request.POST.get('numtrans'),article_id=request.POST.get('produit'))
                if bon:
                    bon.delete()
                    return JsonResponse(
                        {"msg": "Opération effectuée",
                         "id": "1"}, safe=False)
                else:
                    return JsonResponse(
                        {"msg": "Opération effectuée",
                         "id": "0"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)



@login_required
def cloturecommande(request):

    if request.method == "POST":

        try:
            with transaction.atomic():

                # bon=Fcommande.objects.get(commande=request.POST.get('numbon'),location_id=request.session.get('idlocationuser'),etatcde="0")
                bon=Fcommande.objects.get(commande=request.POST.get('numbon'),location_id=request.session.get('idlocationuser'),etatcde="1")
                bon.validation=True
                bon.save()
                cmd=Fcommande.objects.all().order_by('-created_at')
                if cmd:
                    cmd=cmd.first()
                    cmd=str(cmd.commande).split("BC000")[1]
                    return JsonResponse(
                        {"msg": "Opération effectuée",
                         "id": "1","bon":"BC000" + str( int(cmd)+ 1)}, safe=False)
                else:
                    return JsonResponse(
                        {"msg": "Opération effectuée",
                         "id": "1","bon":"BC000" + str( Fcommande.objects.all().count()+ 1)}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)


@login_required
def cloturecommande2(request):

    if request.method == "POST":

        try:
            with transaction.atomic():

                bon=Fcommande.objects.get(commande=request.POST.get('numbon'),location_id=request.session.get('idlocationuser'),etatcde="1")
                bon.cloture=True
                bon.save()
                return JsonResponse(
                        {"msg": "Opération effectuée",
                         "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)



@login_required
def validerlivraison(request):

    if request.method == "POST":

        try:
            with transaction.atomic():

                ###########################################insert les qte auto dans la tab livdetail
                b = Fdetcde.objects.filter(commande_id=request.POST.get('numbon'),
                                         commande__location_id=request.session.get('idlocationuser'))
                if b:
                    for ix in b:
                        try:
                            with transaction.atomic():
                                bpm = Flivraison.objects.filter(document=request.POST.get('numliv'),
                                                                commande=ix.commande, validation=True)
                                if bpm:
                                    return JsonResponse(
                                        {"msg": "Opération non effectuée.Veuillez changer le numero bon livraison ",
                                         "id": "0"}, safe=False)
                                else:
                                    bp = Flivraison.objects.filter(document=request.POST.get('numliv'),
                                                                   commande=ix.commande)
                                    if bp:
                                        bp = bp.first()
                                    else:
                                        liv = Flivraison.objects.filter(
                                            serielivraison=str(ix.commande.commande).replace("C", "E"))
                                        if liv:
                                            import time
                                            bp = Flivraison.objects.create(
                                                commande=ix.commande,
                                                serielivraison=str(ix.commande.commande).replace("C", "E") + str(
                                                    time.time()),
                                                document=request.POST.get('numliv'),
                                                datejour=request.POST.get('dateop'),
                                                tiers=request.POST.get('fournisseur'),
                                                # imputation=request.POST.get('mode'),
                                                etatliv="0",
                                                observation=request.POST.get('commentaire')
                                            )
                                        else:
                                            bp = Flivraison.objects.create(
                                                commande=ix.commande,
                                                serielivraison=str(ix.commande.commande).replace("C", "E"),
                                                document=request.POST.get('numliv'),
                                                datejour=request.POST.get('dateop'),
                                                tiers=request.POST.get('fournisseur'),
                                                # imputation=request.POST.get('mode'),
                                                etatliv="0",
                                                observation=request.POST.get('commentaire')
                                            )

                                    #     b.commande.serielivraison = request.POST.get('numbonentre')
                                    #     b.commande.save()
                                    # print(bp.serielivraison)

                                    #####################conversion
                                    # if request.POST.get('devise')=='CDF':
                                    #     pa=float(request.POST.get('pa'))/float(str(request.POST.get('taux')).replace(",","."))
                                    # else:
                                    #     pa=float(request.POST.get('pa'))
                                    pa = ix.prix_unitaire
                                    #####################conversion

                                    detaillivre = Fdetlivraison.objects.filter(article=ix.article,
                                                                               serielivraison_id=bp.serielivraison)
                                    if detaillivre:
                                        pass
                                    else:
                                        Fdetlivraison.objects.create(
                                            serielivraison_id=bp.serielivraison,
                                            article=ix.article,
                                            ptusd=ix.ptusd,
                                            qtelivree=ix.quantite,
                                            prixunitaire=pa
                                        )

                                    # b.qte_livree = b.qte_livree+ float(request.POST.get('qte'))
                                    somme = Fdetlivraison.objects.filter(serielivraison__commande=ix.commande,
                                                                         article=ix.article).aggregate(
                                        Sum('qtelivree')).get('qtelivree__sum')
                                    if somme is None:
                                        somme = 0
                                    ix.prix_unitaire = pa
                                    ix.qte_livree = float(somme)
                                    ix.save()
                        except Exception as e:
                            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)
                else:
                    return JsonResponse({"msg": "Opération non effectuée ", "id": "0"}, safe=False)

                ###########################################insert les qte auto dans la tab livdetail


                ##############################################333
                bon = Flivraison.objects.get(document=request.POST.get('numliv'),
                                             commande_id=request.POST.get('numbon'),
                                             commande__location_id=request.session.get('idlocationuser'))
                bon.validation = True
                bon.etatliv = "1"


                ###################################
                b = Fdetlivraison.objects.filter(serielivraison_id=bon.serielivraison)
                if b:
                    try:
                        with transaction.atomic():


                            for i in b:

                                aj = Fajustement.objects.get(ajustement="ACH")
                                # p = int(str(request.POST.get('dateop'))[5:7])
                                #
                                # if p < 9:
                                #     p = str(p).replace("0", "")
                                # p = int(p)
                                libemb = ""
                                emba = Fdetcde.objects.filter(commande=i.serielivraison.commande.commande,
                                                              article_id=i.article.article)
                                if emba:
                                    emba = emba.first()
                                    libemb = emba.emballage.emballage
                                # ----------------------------------
                                resultat1 = 0
                                resultat2 = 0
                                prixcmpgros = 0
                                prixcmpdetail = 0
                                idemb = ""

                                art = Farticle.objects.filter(article=i.article.article, emballagee_id=libemb)
                                art2 = Farticle.objects.filter(article=i.article.article, emballageu_id=libemb)

                                if art:
                                    resultat1 = i.qtelivree
                                    resultat2 = float(i.qtelivree) * art.first().quantiteu#quantiteu
                                    # if art2:
                                    #     resultat2 = i.qtelivree
                                    # else:
                                    #     resultat2 = float(i.qtelivree) * art.first().quantitee
                                    # tot=getstockproduit(request.session.get('idlocationuser'),i.article.article,libemb)
                                    # prixcmpdetail=((tot*art.first().prix_vente)+(resultat1*i.prixunitaire))/(resultat1+tot)
                                elif art2:
                                    resultat2 = i.qtelivree
                                    resultat1 = float(i.qtelivree) / art2.first().quantiteu#quantiteu
                                    # prixcmpdetail=((tot*art.first().prix_vente)+(i.qtelivree*i.prixunitaire))/(resultat2+tot)

                                #################################################################CMP
                                artic = Farticle.objects.get(article=i.article.article)
                                tot = getstockproduit(request.session.get('idlocationuser'), i.article.article,
                                                      artic.emballageu_id)
                                # prixcmpdetail = ((tot * art.first().prix_vente) + (resultat2 * i.prixunitaire)) / (
                                #             resultat2 + tot)

                                #################################################################

                                Fmvts.objects.create(
                                    location_id=i.serielivraison.commande.location.location,
                                    # periode=p,
                                    datemvt=request.POST.get('dateop'),
                                    ndatemvt=str(request.POST.get('dateop')).replace("-", "").replace("/", ""),
                                    requisition=i.serielivraison.serielivraison,
                                    document=i.serielivraison.document,
                                    ajustement_id=aj.ajustement,
                                    # tiers_id=i.serielivraison.commande.tiers.tiers,
                                    article_id=i.article.article,
                                    emballage_id=libemb,
                                    # quantite=i.qtelivree,
                                    qte_entree=resultat1,
                                    qteunit_entree=resultat2,
                                    txchange=i.ptusd,
                                    prix_achat=i.prixunitaire,
                                    prix_vente=0,
                                    # devise="",
                                    # txchange=str(request.POST.get('taux')).replace(",", "."),

                                    codeuser_id=request.user.id,
                                )

                                # artic.prix_vente = prixcmpdetail
                                artic.prix_achat = i.prixunitaire
                                artic.pa = i.prixunitaire
                                artic.save()
                                # if art:
                                #     artic = Farticle.objects.get(article=i.article.article)
                                #     artic.prix_vente = prixcmpdetail
                                #     artic.prix_achat = i.prixunitaire
                                #     artic.save()
                                # elif art2:
                                #     artic = Farticle.objects.get(article=i.article.article)
                                #     artic.prix_vente = prixcmpdetail
                                #     artic.pa = i.prixunitaire
                                #     artic.save()




                            bon.save()

                            return JsonResponse({"msg": "Opération effectuée ", "id": "1"}, safe=False)
                    except Exception as e:
                        return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)
                else:
                    return JsonResponse({"msg": "Opération non effectuée ", "id": "0"}, safe=False)
                ###################################
                # return JsonResponse(
                #     {"msg": "Opération effectuée",
                #      "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)


@login_required
@permission_required('gestionstock.Sortie_Stock',raise_exception=True)
def transfert(request):

    context = {
        "besoins": etatbesoin.objects.filter(etat=False,locationfour_id=request.session["idlocationuser"],dateop__gte=(datetime.today().date() - timedelta(days=1)),dateop__lte=datetime.today().date()).values('code','user__username','dateop','location__designation').annotate(Count('code')),
        # "fournisseur": Ftiers.objects.filter(typetiers__in=("1","2")).order_by('nompostnom'),
        # "sortielist": Fmvts.objects.filter(ajustement_id="TRTO",location_id=request.session.get('idlocationuser')).values('document','datemvt').annotate(Count('document')).order_by('-ndatemvt')[:10],
        # "article": Farticle.objects.all().order_by('designation'),
		# 	   "location": Flocation.objects.filter(typelocation="D",location=request.session["idlocationuser"]).order_by('designation'),
		# 	   "locationb": Flocation.objects.all().exclude(location=request.session["idlocationuser"]).order_by('designation'),
			   }
    if request.method == "POST":
        try:

            with transaction.atomic():
                # ----------------------------------

                e=etatbesoin.objects.filter(code=request.POST.get('besoins'),etat=False)
                if e:
                    for item in e:
                        # resultat1 = 0
                        # resultat2 = 0
                        # prix = 0
                        # art = Farticle.objects.filter(article=item.article_id,
                        #                               emballagee_id=item.emb1_id)
                        # art2 = Farticle.objects.filter(article=item.article_id,
                        #                                emballageu_id=item.emb1_id)
                        # if art:
                        #     resultat1 = item.qteliv
                        #     resultat2 = float(item.qteliv) * art.first().quantiteu
                        #     prix = art.first().pa
                        # elif art2:
                        #     resultat2 = item.qteliv
                        #     resultat1 = float(item.qteliv) / art2.first().quantiteu
                        #     prix = art.first().pa
                        #
                        # sortie = Fmvts.objects.filter(document=request.POST.get('besoins'),
                        #                               article_id=item.article_id)
                        # if sortie:
                        #     # sortie.filter(ajustement_id="TRFR").update(
                        #     #     datemvt=request.POST.get('dateop'),
                        #     #     ndatemvt=str(request.POST.get('dateop')).replace("-", "").replace("/", ""),
                        #     #     qte_entree=resultat1,
                        #     #     qteunit_entree=resultat2,
                        #     #     tiers_id=request.POST.get('client'),
                        #     #     emballage_id=request.POST.get('emballage'),
                        #     #     prix_achat=prix,
                        #     #     codeuser_id=request.user.id,
                        #     # )
                        #
                        #     sortie.filter(ajustement_id="TRTO").update(
                        #         datemvt=item.dateop,
                        #         ndatemvt=str(item.dateop).replace("-", "").replace("/", ""),
                        #         qte_sortie=resultat1,
                        #         qteunit_sortie=resultat2,
                        #         # tiers_id=request.POST.get('client'),
                        #         emballage_id=item.emb1_id,
                        #         prix_achat=prix,
                        #         codeuser_id=request.user.id,
                        #     )
                        # else:

                            # Fmvts.objects.create(
                            #     location_id=item.locationfour_id,
                            #     datemvt=item.dateop,
                            #     ndatemvt=str(item.dateop).replace("-", "").replace("/", ""),
                            #     ajustement_id="TRTO",
                            #     article_id=item.article_id,
                            #     # tiers_id=request.POST.get('client'),
                            #     emballage_id=item.emb1_id,
                            #     qte_sortie=resultat1,
                            #     qteunit_sortie=resultat2,
                            #     document=request.POST.get('besoins'),
                            #     prix_achat=prix,
                            #     # prix_vente=request.POST.get('privente'),
                            #     # devise=request.POST.get('devise'),
                            #     # txchange=str(request.POST.get('taux')).replace(",", "."),
                            #     codeuser_id=request.user.id,
                            #     destinat_id=item.location_id,
                            # )

                        art = Farticle.objects.filter(article=item.article_id, emballagee_id=item.emb1_id)
                        art2 = Farticle.objects.filter(article=item.article_id, emballageu_id=item.emb1_id)
                        art3 = Farticle.objects.filter(article=item.article_id, emballagea=item.emb1_id)

                        if art:
                            pa = float(art.first().prix_achat)
                        elif art2:
                            pa = float(art2.first().pa)
                        elif art3:
                            pa = float(art3.first().old_prix_achat)

                        Fmvts.objects.create(
                            destination=item.location.designation,
                            location_id=item.locationfour_id,
                            datemvt=datetime.today().date(),
                            ndatemvt=str(datetime.today().date()).replace("-", "").replace("/", ""),
                            requisition=request.POST.get('besoins'),
                            document=request.POST.get('besoins'),
                            bordereau=datetime.now().time(),
                            ajustement_id='TRTO',
                            article_id=item.article_id,
                            emballage_id=item.emb1_id,
                            qte_sortie=item.qteliv,
                            prix_achat=pa,
                            prix_vente=0,
                            devise='USD',
                            txchange=item.locationfour.txchange,
                            codeuser_id=request.user.id,
                        )

                        Fmvts.objects.create(
                            destination=item.locationfour.designation,
                            location_id=item.location_id,
                            datemvt=datetime.today().date(),
                            ndatemvt=str(datetime.today().date()).replace("-", "").replace("/", ""),
                            requisition=request.POST.get('besoins'),
                            document=request.POST.get('besoins'),
                            bordereau=datetime.now().time(),
                            ajustement_id='TRFR',
                            article_id=item.article_id,
                            emballage_id=item.emb1_id,
                            qte_entree=item.qteliv,
                            prix_achat=pa,
                            prix_vente=0,
                            devise='USD',
                            txchange=item.locationfour.txchange,
                            codeuser_id=request.user.id,
                        )
                    e.update(etat=True)
                    return JsonResponse({"msg": "Opération effectuée ", "id": "1"}, safe=False)
                else:
                    return JsonResponse({"msg": "Opération non effectuée ", "id": "0"}, safe=False)


                # pro2=Fmvts.objects.filter(document=request.POST.get('numtrans'),
                #                           location_id=request.POST.get('location'),
                #                           ajustement_id="TRFR",
                #                           article_id=request.POST.get('produit'),
                #                           tiers_id=request.POST.get('client'),destinat_id=request.POST.get('locationbis'))
                # if pro2:
                #     pro2.update(
                #         datemvt=request.POST.get('dateop'),
                #         ndatemvt=str(request.POST.get('dateop')).replace("-", "").replace("/", ""),
                #         qte_entree=resultat1+float(pro2.first().qte_entree),
                #         qteunit_entree=resultat2+float(pro2.first().qteunit_entree),
                #
                #         emballage_id=request.POST.get('emballage'),
                #         prix_achat=prix,
                #         # prix_vente=request.POST.get('privente'),
                #         # devise=request.POST.get('devise'),
                #         # txchange=str(request.POST.get('taux')).replace(",", "."),
                #         codeuser_id=request.user.id,
                #     )
                # else:
                #     Fmvts.objects.create(
                #     # location_id=request.POST.get('locationbis'),
                #     datemvt=request.POST.get('dateop'),
                #     ndatemvt=str(request.POST.get('dateop')).replace("-", "").replace("/", ""),
                #     document=request.POST.get('numtrans'),
                #     ajustement_id="TRFR",
                #     article_id=request.POST.get('produit'),
                #     qte_entree=resultat1,
                #     qteunit_entree=resultat2,
                #     tiers_id=request.POST.get('client'),
                #     emballage_id=request.POST.get('emballage'),
                #     prix_achat=prix,
                #     # prix_vente=request.POST.get('privente'),
                #     # devise=request.POST.get('devise'),
                #     # txchange=str(request.POST.get('taux')).replace(",", "."),
                #     codeuser_id=request.user.id,
                # )
            return JsonResponse({"msg": "Opération effectuée ", "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)

    # sortie=Fmvts.objects.filter(ajustement_id="TRTO").order_by('-mvt')
    # if sortie:
    #     sortie=sortie.first()
    # context['numtrans'] = "T" +str(request.session['idlocationuser'])+ random_char(6)
    # else:
    #     context['numtrans'] = "SRT0001"
    return render(request, 'gestionstock/transfert.html', context)

@login_required
@permission_required('gestionstock.Retour_Stock',raise_exception=True)
def retour(request):
    context = {"article": Farticle.objects.all().order_by('designation'),
               "location": Flocation.objects.all().exclude(typelocation="D").order_by('designation'),
               "locationb": Flocation.objects.filter(typelocation="D").order_by(
                   'designation'),
               "fournisseur": Ftiers.objects.filter(typetiers__in=("1", "2")).order_by('nompostnom'),
               }
    if request.method == "POST":
        try:

            with transaction.atomic():

                # ----------------------------------
                resultat1 = 0
                resultat2 = 0
                prix=0
                art = Farticle.objects.filter(article=request.POST.get('produit'),
                                              emballagee_id=request.POST.get('emballage'))
                art2 = Farticle.objects.filter(article=request.POST.get('produit'),
                                               emballageu_id=request.POST.get('emballage'))
                if art:
                    resultat1 = request.POST.get('qtet')
                    resultat2 = float(request.POST.get('qtet')) * art.first().quantiteu
                    prix = art.first().pa
                elif art2:
                    resultat2 = request.POST.get('qtet')
                    resultat1 = float(request.POST.get('qtet')) / art2.first().quantiteu
                    prix = art.first().pa
                Fmvts.objects.create(
                    location_id=request.POST.get('location'),
                    datemvt=request.POST.get('dateop'),
                    ndatemvt=str(request.POST.get('dateop')).replace("-", "").replace("/", ""),

                    ajustement_id="TRTO",
                    emballage_id=request.POST.get('emballage'),
                    tiers_id=request.POST.get('client'),
                    article_id=request.POST.get('produit'),
                    qte_sortie=resultat1,
                    qteunit_sortie=resultat2,
                    document=request.POST.get('numretour'),
                    prix_achat=prix,
                    # prix_vente=request.POST.get('privente'),
                    # devise=request.POST.get('devise'),
                    # txchange=str(request.POST.get('taux')).replace(",", "."),
                    codeuser_id=request.user.id,
                    destinat_id=request.POST.get('locationbis'),
                )

                Fmvts.objects.create(
                    location_id=request.POST.get('locationbis'),
                    datemvt=request.POST.get('dateop'),
                    ndatemvt=str(request.POST.get('dateop')).replace("-", "").replace("/", ""),
                    document=request.POST.get('numretour'),
                    ajustement_id="TRFR",
                    article_id=request.POST.get('produit'),
                    qte_entree=resultat1,
                    qteunit_entree=resultat2,
                    emballage_id=request.POST.get('emballage'),
                    prix_achat=prix,
                    # prix_vente=request.POST.get('privente'),
                    # devise=request.POST.get('devise'),
                    # txchange=str(request.POST.get('taux')).replace(",", "."),
                    codeuser_id=request.user.id,
                )
            return JsonResponse({"msg": "Opération effectuée ", "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)
    context['numretour'] = "R" +str(request.session['idlocationuser'])+ random_char(6)
    return render(request, 'gestionstock/retour.html',context)




@login_required
def getboncommande(request):
    if "validation" in request.GET:

        recc = Fdetlivraison.objects.filter(serielivraison_id=request.GET.get('validation'))
        rec=[]
        tot=0
        for i in recc:
            datafull = {}
            datafull['id']=i.id
            datafull['article__designation']=i.article.designation
            datafull['qtelivree']=i.qtelivree
            datafull['prixunitaire']=i.prixunitaire
            tot=tot+(i.prixunitaire*i.qtelivree)
            datafull['total']=tot


            # detail=Fdetcde.objects.filter(commande__flivraison__serielivraison=request.GET.get('validation'),article_id=i.article.article)
            detail=Fdetcde.objects.filter(commande_id=i.serielivraison.commande.commande,article_id=i.article.article)
            if detail:
                detail=detail.first()
                datafull['emballage'] = detail.emballage.emballage
                datafull['quantite'] = detail.quantite
                datafull['prix_unitaire'] = detail.prix_unitaire

            rec.append(datafull)

    # elif "validation2" in request.GET:
    #     rec = Fdetlivraison.objects.filter(serielivraison=request.GET.get('validation2')).values(
    #         "qtelivree", "prixunitaire"
    #     ).order_by('-id')
    elif "validation_boncmd" in request.GET:
        rec = Fdetcde.objects.filter(commande__etatcde="1",commande__commande=request.GET.get('validation_boncmd')).values(
            "id", "article__designation","designation", "emballage__emballage", "quantite", "commande__tiers__nompostnom",
            "commande__datejour", "qte_livree", "prix_unitaire", "commande__location__designation"
        ).order_by('-id')
    elif "impression" in request.GET:
        rec = Fdetcde.objects.filter(commande__etatcde="1",commande__commande=request.GET.get('impression')).annotate(somme=F('quantite')*F('prix_unitaire')).values(
            "id", "article__designation", "emballage__emballage", "quantite", "qteunitaire", "commande__tiers__nompostnom","somme",
            "commande__datejour", "qte_livree", "prix_unitaire", "commande__location__designation"
        ).order_by('-id')


    elif "livraison" in request.GET:
        rec = Fdetcde.objects.filter(commande__etatcde="1",commande__commande=request.GET.get('livraison')).annotate(difference=F('quantite')-F('qte_livree')).values(
            "id", "article__designation","prix_unitaire", "emballage__emballage","quantite", "commande__tiers__nompostnom",
            "commande__datejour", "commande__location__designation","qte_livree","difference"
        ).order_by('-id')
    else:
        rec = Fdetcde.objects.filter(commande__commande=request.GET.get('bon')).annotate(somme=F('quantite')*F('prix_unitaire')).values(
            "id","article__designation","article__qte_stock_minimal","article__article","designation","emballage__emballage","quantite","qteunitaire","commande__tiers__nompostnom","somme","commande__datejour","qte_livree","prix_unitaire","commande__location__designation"
        ).order_by('-id')
    rec=list(rec)
    return JsonResponse({'data': rec}, safe=False)

@login_required
def getpromodifier(request):
	rec = Fmvts.objects.filter(article_id=request.GET.get('id')).values(
            "mvt","datemvt","article__designation","emballage_id","prix_achat","qte_entree","qte_sortie","location__designation"
        ).order_by('-mvt')
	rec=list(rec)
	return JsonResponse({'data': rec}, safe=False)


@login_required
def getsupprimer(request):
    rec = Fcommande.objects.filter(location_id=request.session.get('idlocationuser')).values(
        "commande","tiers__nompostnom","etatcde","observation","userr__username","datejour","livraisoncmd__document","livraisoncmd__etatliv").order_by('-created_at')
    rec=list(rec)
    return JsonResponse({'data': rec}, safe=False)

@login_required
def fac(request):
    if request.method == 'POST':
        #imprimer__________________________


        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = os.path.join(fn,'facx.jrxml') #+ "\{}".format("fac.jrxml")

        # jdbc=os.path.join(fn, "\JasperStarter\jdbc\\")

        output = os.path.join(fn,'media') #+ "\media"

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': f"jdbc:jtds:sqlserver://localhost/{settings.DATABASES['default']['NAME']}",
            'jdbc_dir': fn,
            'username':f"{settings.DATABASES['default']['USER']}",
            'password': settings.DATABASES['default']['PASSWORD']
        }

        jasper = JasperPy()

        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters={'bon': str(request.POST.get('bon'))},
            locale='en_US'
        )

        #imprimer__________________________
        return HttpResponse("true")
@login_required
def getfacture(request):
    if 'besoins' in request.GET:
        rec=[]
        c = etatbesoin.objects.filter(code=request.GET.get('besoins'),etat=False) #.values("article__designation", "article_id", "emb1","qte","qteliv", "dateop","id", "locationfour__designation", "location__designation").order_by('article__designation')
        for i in c:
            rec.append(
                {"article__designation":i.article.designation,
                 "article_id":i.article.article,
                 "emb1":i.emb1.emballage,
                 "qte":i.qte,
                 "qteliv":i.qteliv,
                 "dateop":i.dateop,
                 "id":i.id,
                 "locationfour__designation":i.locationfour.designation,
                 "stock":getstockproduit(request.session.get('idlocationuser'),i.article.article,i.emb1.emballage),
                 "location__designation":i.location.designation
                 }
            )
    elif request.GET.get('id')!='':
        rec = Fmvts.objects.filter(document=request.GET.get('numtrans'),ajustement_id="TRTO").values(
            "mvt","article__designation","article_id","qte_sortie","datemvt","location__designation","tiers__nompostnom","destinat__designation").order_by('-mvt')
        rec = list(rec)
    else:
        rec = Fmvts.objects.filter(document=request.GET.get('numtrans'),ajustement_id="TRTO",ndatemvt=str(request.GET.get('dateop')).replace("-", "").replace("/", "")).values(
        #rec = Fmvts.objects.filter(document=request.GET.get('numtrans'),ajustement_id="TRFR",location_id=request.GET.get('locationbis'),ndatemvt=str(request.GET.get('dateop')).replace("-", "").replace("/", "")).values(
            "mvt","article__designation","article_id","qte_sortie","datemvt","location__designation","tiers__nompostnom","destinat__designation").order_by('-mvt')
        rec=list(rec)
    return JsonResponse({'data': rec}, safe=False)


@login_required
def getajustementpro(request):
    rec = Fmvts.objects.filter(ajustement__in=('DECL','PAT'),location_id=request.session.get('idlocationuser'),article_id=request.GET.get('produit')).values(
        "mvt","article__designation","ajustement__designation","emballage_id","qte_entree","qte_sortie","datemvt","codeuser__username").order_by('-mvt')
    rec=list(rec)
    return JsonResponse({'data': rec}, safe=False)

@login_required
def getfacture2(request):
	rec = Fmvts.objects.filter(document=request.GET.get('numretour'),ajustement_id="TRFR",location_id=request.GET.get('locationbis'),ndatemvt=str(request.GET.get('dateop')).replace("-", "").replace("/", "")).values(
            "mvt","article__designation","qte_entree","datemvt","location__designation").order_by('-mvt')
	rec=list(rec)
	return JsonResponse({'data': rec}, safe=False)


@login_required
def getfacture3(request):
	rec = Fmvts.objects.filter(document=request.GET.get('numfact'),ajustement_id="FACT",location_id=request.session.get('idlocationuser'),ndatemvt=str(request.GET.get('dateop')).replace("-", "").replace("/", "")).values(
            "mvt","article__designation","emballage__emballage","qte_sortie","datemvt","prix_vente").order_by('-mvt')
	rec=list(rec)
	return JsonResponse({'data': rec}, safe=False)

@require_POST
@login_required
@permission_required('gestionstock.view_recettes',raise_exception=True)
def getrecettes(request):
    rec = Recettes.objects.filter(categorie=False).values().order_by('libelle')
    rec=list(rec)
    return JsonResponse({'data': rec}, safe=False)


@login_required
@permission_required('gestionstock.view_detailrecettes',raise_exception=True)
def getrecettesdetail(request):
    # cdz=str(request.GET.get("recette")).split("_")
    # if len(cdz)>=2:
    #     recx = DetailRecettes.objects.filter(client_id=cdz[0],recettes_id=cdz[1]).order_by('produit__designation')
    # else:
    if request.GET.get("recette")=='':
        return JsonResponse({'data': {}}, safe=False)
    else:

        recx = DetailRecettes.objects.filter(recettes_id=request.GET.get("recette")).order_by('produit__designation')
        rec=[]
        tot=0
        for i in recx:
            datafull = {}
            datafull['id']=i.id
            datafull['produit__designation']=i.produit.designation
            datafull['produit__id']=i.produit.article
            datafull['article']=i.recettes.libelle
            datafull['produit__pa']=i.pu
            datafull['qte']=i.qte
            datafull['emballage__emballage']=i.emballage.emballage
            tot=tot+(float(i.pu)*float(i.qte))
            datafull['total']=tot
            rec.append(datafull)


        rec=list(rec)
        return JsonResponse({'data': rec}, safe=False)


@login_required
@permission_required('gestionstock.view_stockrecettes',raise_exception=True)
def getrecettesdetailstock(request):
    #.
    rec = StockRecettes.objects.filter(location_id=request.session.get('idlocationuser'),categorie="E",bon=request.GET.get('bon')).values("recette_id","dateop",'bon','recette__libelle','qte','prix')
    rec=list(rec)
    return JsonResponse({'data': rec}, safe=False)


@login_required
def getrecettesdetailstocksorti(request):
    #.
    rec = StockRecettes.objects.filter(location_id=request.session.get('idlocationuser'),categorie="S").annotate(_name=Concat('detail__recettes__libelle', Value ("/") ,'detail__client__nompostnom')).values("_name",'detail__recettes__libelle','detail__client__nompostnom').distinct().annotate(_sum=Sum("qte"))
    rec=list(rec)
    return JsonResponse({'data': rec}, safe=False)


@login_required
def getlistlivraison(request):
    rec = Flivraison.objects.filter(commande_id=request.POST.get('numbon'),validation=False).values("document","serielivraison")
    rec=list(rec)
    return JsonResponse({'data': rec},safe=False)


@login_required
def getproduit(request):
    st1=0
    st3=0
    st2=0
    qt1 = 0
    qt3 = 0
    qt2 = 0
    stn1 = ''
    stn3 = ''
    stn2 = ''
    if "id" in request.GET:
        i=Farticle.objects.get(article=request.GET.get('id'))
        if 'r' in request.GET:
            s=getstockproduit(request.session.get('idlocationuser'),i.article,i.emballagee_id,1)
            st1=s[0]
            st2=s[1]
            st3=s[2]
        else:
            st1 = getstockproduit(request.session.get('idlocationuser'), i.article, i.emballagee_id)
            st2 = getstockproduit(request.session.get('idlocationuser'), i.article, i.emballageu_id)
            st3 = getstockproduit(request.session.get('idlocationuser'), i.article, i.emballagea)
        stn1 =i.emballagee_id
        stn3 = i.emballagea
        stn2 = i.emballageu_id
        qt1 = i.quantitee
        qt2 = i.quantiteu
        qt3 = i.quantitea
        rec = Farticle.objects.filter(article=request.GET.get('id')).values(
       "article","designation","famille__designation","famille_id","quantitee","pa","prix_achat","old_prix_achat","old_prix_vente","prix_vente","prix_vente_cdf","quantitea","quantitee","quantiteu","classe__designation","emballagee_id","emballagea","emballageu_id","qte_stock_minimal","categorie").order_by('designation')
    elif 'location' in request.GET:
        rec = Farticle.objects.filter(LOCATION_id=request.GET.get('location')).values(
            "article", "designation").order_by('designation')
    else:
        rec = Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser')).values(
            "article","designation","famille__designation","quantitee","pa","prix_achat","old_prix_achat","old_prix_vente","prix_vente","prix_vente_cdf","quantitea","quantitee","quantiteu","classe__designation","emballagee_id","emballagea","emballageu_id","qte_stock_minimal","categorie").order_by('designation')
    rec=list(rec)
    return JsonResponse({'data': rec,'qt1':qt1,'qt2':qt2,'qt3':qt3,'st1':st1,'st2':st2,'st3':st3,'stn1':stn1,'stn2':stn2,'stn3':stn3}, safe=False)


@require_POST
@login_required
@permission_required('gestionstock.view_recettes',raise_exception=True)
def getrecettes2(request):
    rec = Recettes.objects.filter(categorie=True).values().order_by('libelle')
    rec=list(rec)
    return JsonResponse({'data': rec}, safe=False)

@login_required
@permission_required('gestionstock.view_recettes',raise_exception=True)
def getrecette(request):
    rec = Recettes.objects.all().values(
        "id","libelle","categorie").order_by('libelle')
    rec=list(rec)
    return JsonResponse({'data': rec}, safe=False)

@login_required
def gettiers(request):
    rec = Ftiers.objects.filter(tiers=request.GET.get('id')).values(
        "tiers","nompostnom","adresse","origine","idnational","raisonsoc")
    rec=list(rec)
    return JsonResponse({'data': rec}, safe=False)


@login_required
def getproduitinventaire(request):

    rec = Finventaire.objects.filter(location_id=request.session.get('idlocationuser'),periode=request.GET.get('periode')).values(
            "article__article","article__designation","emballage_e","emballage_u","qte_u_log","quantitee","quantiteu","qte_u_phys","qte_u_ecart").order_by('article__designation')
    rec=list(rec)
    return JsonResponse({'data': rec}, safe=False)

@require_POST
@login_required
@permission_required('gestionstock.Bon_Commande_valide',raise_exception=True)
def boncommandevalidemodi(request):
    try:
        with transaction.atomic():

            bon=Fdetcde.objects.get(id=request.POST.get('id'))
            bon.quantite=str(request.POST.get('qte')).replace(",",".")
            bon.prix_unitaire=str(request.POST.get('pa')).replace(",",".")
            bon.save()
            return JsonResponse(
                {"msg": "Opération effectuée",
                 "id": "1"}, safe=False)
    except Exception as e:
        return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)



@require_POST
@login_required
@permission_required('gestionstock.Bon_Commande_valide',raise_exception=True)
def boncommandevalidesup(request):
    try:
        with transaction.atomic():


            if request.POST.get('veri')=="1":
                Fdetcde.objects.filter(commande_id=request.POST.get('id')).delete()
                Fcommande.objects.filter(commande=request.POST.get('id')).delete()

            else:
                livrai=Flivraison.objects.filter(commande_id=request.POST.get('id'))
                if livrai:
                    return JsonResponse(
                        {"msg": "Opération non effectuée. La commande a déjà quelques livraisons ",
                         "id": "0"}, safe=False)
                else:
                    Fdetcde.objects.filter(commande_id=request.POST.get('id')).delete()
                    Fcommande.objects.filter(commande=request.POST.get('id')).delete()

            return JsonResponse(
                {"msg": "Opération effectuée",
                 "id": "1"}, safe=False)
    except Exception as e:
        return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)



@require_POST
@login_required
def getdetailboncommande(request):
    bon=Fcommande.objects.get(commande=request.POST.get('id'))
    return JsonResponse(
        {"dateliv":bon.datelivraison,
         "mode": bon.typecommande}, safe=False)


@require_POST
@login_required
@permission_required('gestionstock.Entrer_Stock',raise_exception=True)
def saveqte(request):


    b=Fdetcde.objects.get(id=request.POST.get('id'))
    if b:
        try:
            with transaction.atomic():
                bpm=Flivraison.objects.filter(document=request.POST.get('numbonlivre'), commande=b.commande,validation=True)
                if bpm:
                    return JsonResponse({"msg": "Opération non effectuée.Veuillez changer le numero bon livraison ", "id": "0"}, safe=False)
                else:
                    bp=Flivraison.objects.filter(document=request.POST.get('numbonlivre'), commande=b.commande)
                    #bp=Flivraison.objects.filter(document=request.POST.get('numbonlivre'))
                    if bp:
                        bp=bp.first()
                    else:
                        liv=Flivraison.objects.filter(serielivraison=str(b.commande.commande).replace("C","E"))
                        if liv:
                            import time
                            bp=Flivraison.objects.create(
                                commande=b.commande,
                                serielivraison=str(b.commande.commande).replace("C","E")+str(time.time()),
                                document=request.POST.get('numbonlivre'),
                                datejour=request.POST.get('dateop'),
                                tiers=request.POST.get('fournisseur'),
                                # imputation=request.POST.get('mode'),
                                etatliv="0",
                                observation=request.POST.get('commentaire')
                            )
                        else:
                            bp=Flivraison.objects.create(
                            commande=b.commande,
                            serielivraison=str(b.commande.commande).replace("C","E"),
                            document=request.POST.get('numbonlivre'),
                            datejour=request.POST.get('dateop'),
                                tiers=request.POST.get('fournisseur'),
                            # imputation=request.POST.get('mode'),
                            etatliv="0",
                            observation=request.POST.get('commentaire')
                            )

                    #     b.commande.serielivraison = request.POST.get('numbonentre')
                    #     b.commande.save()
                    # print(bp.serielivraison)


                    #####################conversion
                    # if request.POST.get('devise')=='CDF':
                    #     pa=float(request.POST.get('pa'))/float(str(request.POST.get('taux')).replace(",","."))
                    # else:
                    #     pa=float(request.POST.get('pa'))
                    pa = float(request.POST.get('pa'))
                    #####################conversion

                    detaillivre=Fdetlivraison.objects.filter(article=b.article,serielivraison_id=bp.serielivraison)
                    if detaillivre:
                        detaillivre.update(
                            qtelivree=request.POST.get('qte'),
                            prixunitaire=pa,
                            ptusd=b.ptusd,
                        )
                    else:
                        Fdetlivraison.objects.create(
                        serielivraison_id=bp.serielivraison,
                        article=b.article,
                        ptusd=b.ptusd,
                        qtelivree=request.POST.get('qte'),
                        prixunitaire=pa
                    )


                    # b.qte_livree = b.qte_livree+ float(request.POST.get('qte'))
                    somme=Fdetlivraison.objects.filter(serielivraison__commande=b.commande,article=b.article).aggregate(Sum('qtelivree')).get('qtelivree__sum')
                    if somme is None:
                        somme=0
                    b.prix_unitaire = pa
                    b.qte_livree = float(somme)
                    # b.quantite = float(request.POST.get('qtecmd'))

                    # b.prix_unitaire_livree = request.POST.get('pa')
                    b.save()


                    # aj=Fajustement.objects.get(ajustement="ACH")
                    # p = int(str(request.POST.get('dateop'))[5:7])
                    #
                    # if p < 9:
                    #     p = str(p).replace("0", "")
                    # p = int(p)

                    # Fmvts.objects.create(
                    # location_id=b.commande.location.location,
                    # # periode=p,
                    # datemvt=request.POST.get('dateop'),
                    # ndatemvt=str(request.POST.get('dateop')).replace("-","").replace("/",""),
                    # requisition=request.POST.get('numbonentre'),
                    # document=request.POST.get('numbonlivre'),
                    # ajustement_id=aj.ajustement,
                    # tiers_id=b.commande.tiers.tiers,
                    # article_id=b.article.article,
                    # quantite=request.POST.get('qte'),
                    # qte_entree=request.POST.get('qte'),
                    # prix_achat=request.POST.get('pa'),
                    # prix_vente=request.POST.get('privente'),
                    # devise=request.POST.get('devise'),
                    # txchange=str(request.POST.get('taux')).replace(",","."),
                    # codeuser_id=request.user.id,
                    # )

                    # art=Farticle.objects.get(article=b.article.article)
                    # art.prix_vente=request.POST.get('privente')
                    # art.prix_achat=request.POST.get('pa')
                    # art.save()
                    return JsonResponse({"msg": "Opération effectuée ", "id": "1", "qte": somme}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)
    else:
        return JsonResponse({"msg": "Opération non effectuée ", "id": "0"}, safe=False)



@require_POST
@login_required
@permission_required('gestionstock.Entrer_Stock_valid',raise_exception=True)
def modifyqte(request):

    b=Fdetlivraison.objects.get(id=request.POST.get('id'))
    if b:
        try:
            with transaction.atomic():

                commandeid=Fcommande.objects.get(commande=b.serielivraison.commande.commande)
                cmd=Fdetcde.objects.filter(article_id=b.article_id,commande=commandeid)
                if cmd:
                    cmd.update(
                        quantite=request.POST.get('qtecmd'),
                        prix_unitaire=request.POST.get('pa'),
                    )
                b.qtelivree = request.POST.get('qte')

                b.prixunitaire = request.POST.get('pa')
                b.save()


                # aj=Fajustement.objects.get(ajustement="ACH")
                # p = int(str(request.POST.get('dateop'))[5:7])
                #
                # if p < 9:
                #     p = str(p).replace("0", "")
                # p = int(p)

                # Fmvts.objects.create(
                # location_id=b.commande.location.location,
                # # periode=p,
                # datemvt=request.POST.get('dateop'),
                # ndatemvt=str(request.POST.get('dateop')).replace("-","").replace("/",""),
                # requisition=request.POST.get('numbonentre'),
                # document=request.POST.get('numbonlivre'),
                # ajustement_id=aj.ajustement,
                # tiers_id=b.commande.tiers.tiers,
                # article_id=b.article.article,
                # quantite=request.POST.get('qte'),
                # qte_entree=request.POST.get('qte'),
                # prix_achat=request.POST.get('pa'),
                # prix_vente=request.POST.get('privente'),
                # devise=request.POST.get('devise'),
                # txchange=str(request.POST.get('taux')).replace(",","."),
                # codeuser_id=request.user.id,
                # )

                # art=Farticle.objects.get(article=b.article.article)
                # art.prix_vente=request.POST.get('privente')
                # art.prix_achat=request.POST.get('pa')
                # art.save()
                return JsonResponse({"msg": "Opération effectuée ", "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)
    else:
        return JsonResponse({"msg": "Opération non effectuée ", "id": "0"}, safe=False)

@require_POST
@login_required
@permission_required('gestionstock.ajustement_valide',raise_exception=True)
def ajustementqte(request):


    b=Fdetlivraison.objects.get(id=request.POST.get('id'))
    if b:
        try:
            with transaction.atomic():
                #print(request.POST)
              
                commandeid=Fcommande.objects.get(commande=str(b.serielivraison.commande.commande))
                cmd=Fdetcde.objects.filter(article_id=b.article_id,commande=commandeid)
                if cmd:
                    emba=cmd.first()
                    libemb=emba.emballage.emballage
                    resultat1 = 0
                    resultat2 = 0
                    prixcmpdetail=0
                    artic=0

                    art = Farticle.objects.filter(article=b.article_id,emballagee_id=libemb)
                    art2 = Farticle.objects.filter(article=b.article_id,emballageu_id=libemb)
                    cot=0
                    cotv=0

                    if request.POST.get('qtecmd')!='':
                        cotv=1
                        if request.POST.get('ajustement1') == 'PAT':#ajustement positif

                            if request.POST.get('pa')!='':
                                cot=1
                                cmd.update(
                                    #quantite=float(request.POST.get('qtecmd'))+float(request.POST.get('qtecmd_')),
                                    prix_unitaire=float(request.POST.get('pa')),
                                    qte_livree=float(request.POST.get('qtecmd'))+float(request.POST.get('qtecmd_'))
                                )
                                b.qtelivree = float(request.POST.get('qtecmd'))+float(request.POST.get('qtecmd_'))
                                b.prixunitaire = float(request.POST.get('pa'))
                                b.save()
                            else:
                                cmd.update(
                                    #quantite=float(request.POST.get('qtecmd'))+float(request.POST.get('qtecmd_')),
                                    qte_livree=float(request.POST.get('qtecmd'))+float(request.POST.get('qtecmd_'))
                                )
                                b.qtelivree = float(request.POST.get('qtecmd'))+float(request.POST.get('qtecmd_'))
                                b.save()

                            if art:
                                resultat1 =request.POST.get('qtecmd')
                                resultat2 = float(request.POST.get('qtecmd')) * art.first().quantiteu
                            elif art2:
                                resultat2 = request.POST.get('qtecmd')
                                resultat1 = float(request.POST.get('qtecmd')) / art2.first().quantiteu

                            #################################################################CMP
                            artic = Farticle.objects.get(article=b.article.article)
                            tot=getstockproduit(request.session.get('idlocationuser'),b.article.article,artic.emballageu_id)
                            if request.POST.get('pa')!='':
                                prixcmpdetail=((tot*art.first().prix_vente)+(resultat2*float(request.POST.get('pa'))))/(resultat2+tot)
                                Fmvts.objects.create(
                                    location_id=b.serielivraison.commande.location.location,
                                    datemvt=request.POST.get('dateop'),
                                    ndatemvt=str(request.POST.get('dateop')).replace("-","").replace("/",""),
                                    requisition=b.serielivraison.serielivraison,
                                    document=b.serielivraison.document,
                                    ajustement_id=request.POST.get('ajustement1'),
                                    tiers_id=b.serielivraison.commande.tiers.tiers,
                                    article_id=b.article.article,
                                    emballage_id=libemb,
                                    # quantite=i.qtelivree,
                                    qte_entree=resultat1,
                                    qteunit_entree=resultat2,
                                    prix_achat=float(request.POST.get('pa')),
                                    prix_vente=0,
                                    # devise="",
                                    # txchange=str(request.POST.get('taux')).replace(",","."),
                                    codeuser_id=request.user.id,
                                )
                            else:
                                prixcmpdetail=((tot*art.first().prix_vente)+(resultat2*b.prixunitaire))/(resultat2+tot)
                                Fmvts.objects.create(
                                    location_id=b.serielivraison.commande.location.location,
                                    datemvt=request.POST.get('dateop'),
                                    ndatemvt=str(request.POST.get('dateop')).replace("-","").replace("/",""),
                                    requisition=b.serielivraison.serielivraison,
                                    document=b.serielivraison.document,
                                    ajustement_id=request.POST.get('ajustement1'),
                                    tiers_id=b.serielivraison.commande.tiers.tiers,
                                    article_id=b.article.article,
                                    emballage_id=libemb,
                                    # quantite=i.qtelivree,
                                    qte_entree=resultat1,
                                    qteunit_entree=resultat2,
                                    prix_achat=b.prixunitaire,
                                    prix_vente=0,
                                    # devise="",
                                    # txchange=str(request.POST.get('taux')).replace(",","."),
                                    codeuser_id=request.user.id,
                                )
                            #################################################################





                        else:#ajustement negatif
                            if request.POST.get('pa')!='':
                                cot=1
                                cmd.update(
                                    #quantite=float(request.POST.get('qtecmd_'))-float(request.POST.get('qtecmd')),
                                    prix_unitaire=float(request.POST.get('pa')),
                                    qte_livree=float(request.POST.get('qtecmd_'))-float(request.POST.get('qtecmd')),
                                )
                                b.qtelivree = float(request.POST.get('qtecmd_'))-float(request.POST.get('qtecmd'))
                                b.prixunitaire = float(request.POST.get('pa'))
                                b.save()
                            else:
                                cmd.update(
                                    #quantite=float(request.POST.get('qtecmd_'))-float(request.POST.get('qtecmd')),
                                    qte_livree=float(request.POST.get('qtecmd_'))-float(request.POST.get('qtecmd')),
                                )
                                b.qtelivree = float(request.POST.get('qtecmd_'))-float(request.POST.get('qtecmd'))
                                b.save()


                            if art:
                                resultat1 = float(request.POST.get('qtecmd'))
                                resultat2 = float(request.POST.get('qtecmd')) * art.first().quantiteu
                            elif art2:
                                resultat2 = float(request.POST.get('qtecmd'))
                                resultat1 = float(request.POST.get('qtecmd')) / art2.first().quantiteu

                            #################################################################CMP
                            artic = Farticle.objects.get(article=b.article.article)
                            tot=getstockproduit(request.session.get('idlocationuser'),b.article.article,artic.emballageu_id)
                            if request.POST.get('pa')!='':
                                tot=tot-resultat2
                                prixcmpdetail=((tot*float(request.POST.get('pa'))))/(tot)
                                Fmvts.objects.create(
                                    location_id=b.serielivraison.commande.location.location,
                                    datemvt=request.POST.get('dateop'),
                                    ndatemvt=str(request.POST.get('dateop')).replace("-","").replace("/",""),
                                    requisition=b.serielivraison.serielivraison,
                                    document=b.serielivraison.document,
                                    ajustement_id=request.POST.get('ajustement1'),
                                    tiers_id=b.serielivraison.commande.tiers.tiers,
                                    article_id=b.article.article,
                                    emballage_id=libemb,
                                    # quantite=i.qtelivree,
                                    qte_sortie=resultat1,
                                    qteunit_sortie=resultat2,
                                    prix_achat=float(request.POST.get('pa')),
                                    prix_vente=0,
                                    # devise="",
                                    # txchange=str(request.POST.get('taux')).replace(",","."),
                                    codeuser_id=request.user.id,
                                )
                            else:
                                tot=tot-resultat2
                                prixcmpdetail=((tot*art.first().pa))/(tot)
                                Fmvts.objects.create(
                                    location_id=b.serielivraison.commande.location.location,
                                    datemvt=request.POST.get('dateop'),
                                    ndatemvt=str(request.POST.get('dateop')).replace("-","").replace("/",""),
                                    requisition=b.serielivraison.serielivraison,
                                    document=b.serielivraison.document,
                                    ajustement_id=request.POST.get('ajustement1'),
                                    tiers_id=b.serielivraison.commande.tiers.tiers,
                                    article_id=b.article.article,
                                    emballage_id=libemb,
                                    # quantite=i.qtelivree,
                                    qte_sortie=resultat1,
                                    qteunit_sortie=resultat2,
                                    prix_achat=b.prixunitaire,
                                    prix_vente=0,
                                    # devise="",
                                    # txchange=str(request.POST.get('taux')).replace(",","."),
                                    codeuser_id=request.user.id,
                                )
                            #################################################################

                    if request.POST.get('pa')!='':
                        cotv=1
                        if cot==0:
                            cmd.update(
                                prix_unitaire=request.POST.get('pa'),
                            )
                            b.prixunitaire = request.POST.get('pa')
                            b.save()

                            #fmvt
                            p=Fmvts.objects.filter(article_id=b.article_id,requisition=b.serielivraison_id,ajustement_id='ACH')
                            if p:
                                p.update( prix_achat=request.POST.get('pa'))
                            #fmvt

                            #################################################################CMP
                            artic = Farticle.objects.get(article=b.article.article)
                            tot=getstockproduit(request.session.get('idlocationuser'),b.article.article,artic.emballageu_id)
                            if request.POST.get('pa')!='':
                                try:
                                    prixcmpdetail=((tot*float(request.POST.get('pa'))))/(tot)
                                except:
                                    prixcmpdetail=float(request.POST.get('pa'))

                            #################################################################

                    ########################################"

                    if cotv==1:
                        artic.prix_vente = prixcmpdetail
                        artic.prix_achat = b.prixunitaire
                        artic.pa = b.prixunitaire
                        artic.save()
                    return JsonResponse({"msg": "Opération effectuée ", "id": "1"}, safe=False)
                else:
                    return JsonResponse({"msg": "Opération non effectuée Commande non trouvée", "id": "0"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)
    else:
        return JsonResponse({"msg": "Opération non effectuée ", "id": "0"}, safe=False)



@login_required
def chargerappro(request):

    try:
        if 'id' in request.GET:
            a = Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser')).order_by('article').annotate(
                Count('article'))
            d = 0
            listpro = []
            for i in a:
                st1 = 0
                st2 =0
                st3 = 0

                if i.emballagee_id!= None and i.quantitee!=0:
                    s = getstockproduit(request.session.get('idlocationuser'),i.article,i.emballagee_id,1)
                    st1 = s[0]
                    st2 = s[1]
                    st3 = s[2]

                    if st1 <= i.qte_stock_minimal:
                        listpro.append(
                            {
                                'id':i.article,
                                'produit':i.designation,
                                'emb': i.emballagee_id,
                                'qte':st1,

                             }
                        )
                if i.emballageu_id != None and i.quantiteu != 0:
                    if st2 <= i.qte_stock_minimal:
                        listpro.append(
                            {
                                'id': i.article,
                                'produit': i.designation,
                                'emb': i.emballageu_id,
                                'qte': st2,

                            }
                        )

                if i.emballagea != None and i.quantitea != 0:

                    if st3 <= i.qte_stock_minimal:
                        listpro.append(
                            {
                                'id': i.article,
                                'produit': i.designation,
                                'emb': i.emballagea,
                                'qte': st3,

                            }
                        )
                #----------------------



            return JsonResponse({"data":listpro}, safe=False)
        elif 'peremption' in request.GET:
            from math import ceil
            a = Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser')).order_by('article')
            listpro = []
            for i in a:
                f=Fmvts.objects.filter(article=i.article,emballage_id=i.emballagee_id,ajustement_id='ACH').exclude(reference__isnull=True).order_by('reference')[:1]
                f1=Fmvts.objects.filter(article=i.article,emballage_id=i.emballageu_id,ajustement_id='ACH').exclude(reference__isnull=True).order_by('reference')[:1]
                f2=Fmvts.objects.filter(article=i.article,emballage_id=i.emballagea,ajustement_id='ACH').exclude(reference__isnull=True).order_by('reference')[:1]

                if f:

                    f=f.first()
                    if f.reference is not None:
                        dt=datetime.strptime(f.reference, '%Y-%m-%d').date()
                        dtoday=datetime.today().date()

                        c=ceil((dtoday - dt).days / 30)

                        if c>=1:
                            listpro.append(
                                {
                                    'id': i.article,
                                    'produit': i.designation,
                                    'emb': i.emballagee_id,
                                    'dt': f.reference,

                                })
                if f1:

                    f1 = f1.first()
                    if f1.reference is not None:
                        dt = datetime.strptime(f1.reference, '%Y-%m-%d').date()
                        dtoday = datetime.today().date()
                        c = ceil((dtoday - dt).days / 30)
                        if c>=1:
                            listpro.append(
                                {
                                    'id': i.article,
                                    'produit': i.designation,
                                    'emb': i.emballageu_id,
                                    'dt': f1.reference,

                                })
                if f2:
                    f2 = f2.first()
                    if f2.reference is not None:
                        dt = datetime.strptime(f2.reference, '%Y-%m-%d').date()
                        dtoday = datetime.today().date()
                        c = ceil((dtoday - dt).days / 30)
                        if c >= 1:
                            listpro.append(
                                {
                                    'id': i.article,
                                    'produit': i.designation,
                                    'emb': i.emballagea,
                                    'dt': f2.reference,

                                })


            return JsonResponse({"data":listpro}, safe=False)
        else:

            with transaction.atomic():
                # cmd = Fcommande.objects.filter(created_at__date==datetime.today().date(),location_id=request.session.get('idlocationuser'))
                # if cmd:
                #     return JsonResponse({"msg": "Opération non effectuée ", "id": "0"}, safe=False)
                ###################################
                cmd = Fcommande.objects.all().order_by('-created_at')
                if cmd:
                    cmd = cmd.first()
                    cmd = str(cmd.commande).split("BC000")[1]
                    numbon= "BC000" + str(int(cmd) + 1)
                else:
                    numbon= "BC000" + str(Fcommande.objects.all().count() + 1)

                listpro= {}

                f=Flocation.objects.filter(typelocation='D',location=request.session.get('idlocationuser'))
                if not f:
                    return JsonResponse({"msg": "Opération non effectuée ", "id": "0"}, safe=False)


                a = Farticle.objects.all()
                for i in a:
                    s = getstockproduit(request.session.get('idlocationuser'), i.article, i.emballagee_id,1)

                    if s == -1:
                        pass
                    elif s <= i.qte_stock_minimal:

                        fdx = Fdetcde.objects.filter(article_id=i.article)
                        veri=0
                        for xx in fdx:
                            if xx.commande.created_at.date()==datetime.today().date():
                                veri=1

                        if veri==0:
                            listpro[i.article] = s

                # listpro.update(listpro_)
                if 0==0:
                    for i in listpro:
                        bon = Fcommande.objects.filter(commande=numbon, userr_id=request.user.id,
                                                       location_id=request.session.get('idlocationuser'))
                        if bon:
                            bon = bon.first()
                        else:
                            bon = Fcommande.objects.create(
                                commande=numbon,
                                observation=numbon,
                                validation = False,
                                datejour=str(datetime.today().date()),
                                # tiers_id=1,
                                # datelivraison=request.POST.get('dateliv'),
                                # typecommande = request.POST.get('mode'),
                                location_id=request.session.get('idlocationuser'),
                                 # etatcde="0",
                                etatcde="1",
                                # devise=request.POST.get('devise'),
                                userr_id=request.user.id,
                            )

                        v=Farticle.objects.get(article=i)
                        idemb = v.emballagee_id
                        b = Fdetcde.objects.filter(commande__commande=numbon,article_id=v.article)
                        if b:
                            pass
                        else:
                            Fdetcde.objects.create(
                                commande=bon,
                                article_id=i,
                                # designation=request.POST.get('libunite'),
                                emballage_id=idemb,
                                qte_livree=0,
                                # emballage2_id=idemb2,
                                quantite=0,
                                qteunitaire=listpro[i],
                                prix_unitaire=v.prix_achat,
                                # qteunitaire = resultat2
                            )
                ###################################
                return JsonResponse({"msg": "Opération effectuée ", "id": "1"}, safe=False)
    except Exception as e:
        return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)



@require_POST
@login_required
@permission_required('gestionstock.ajustement_valide',raise_exception=True)
def ajustementqtesupprimer(request):  

    try:
        with transaction.atomic():
            b=Fdetlivraison.objects.get(id=request.POST.get('id'))
            arti=b.article_id
            livra=b.serielivraison_id
            b.delete()

            Fdetcde.objects.filter(article_id=arti,commande_id=str(livra).replace("E","C")).delete()

            Fmvts.objects.filter(article_id=arti,requisition=livra).delete()
            return JsonResponse({"msg": "Opération effectuée ", "id": "1"}, safe=False)
    except Exception as e:
        return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)


@require_POST
@login_required
def getqte(request):
    # b = Fmvts.objects.filter(location_id=,article_id=request.POST.get('produit'),ajustement_id__in=("ACH","PAT","TRFR"),emballage_id=request.POST.get('emballage')).aggregate(Sum("qte_entree")).get("qte_entree__sum")
    # if b is None:#entrer
    #     b = 0
    # c = Fmvts.objects.filter(location_id=request.POST.get('location'), article_id=request.POST.get('produit'),
    #                          ajustement_id__in=("VTE", "TRTO", "FACT","DECL"),emballage_id=request.POST.get('emballage')).aggregate(Sum("qte_sortie")).get("qte_sortie__sum")
    # if c is None:  # sortie
    #     c = 0


    tot=getstockproduit(request.POST.get('location'),request.POST.get('produit'),request.POST.get('emballage'))
    return JsonResponse({"tot": tot}, safe=False)

@require_POST
@login_required
def getprixemballage(request):
    if request.POST.get('emballage')=="1":
        b = Farticle.objects.get(article=request.POST.get('produit'))

        return JsonResponse({"prix": b.prix_achat}, safe=False)
    elif request.POST.get('emballage')=="2":
        b = Farticle.objects.get(article=request.POST.get('produit'))

        return JsonResponse({"prix": b.pa}, safe=False)
    else:
        one=Farticle.objects.filter(designation=request.POST.get('produit'),emballagee_id=request.POST.get('emballage'))
        if one:
            one=one.first()
            return JsonResponse({"prix": one.prix_achat}, safe=False)

        one = Farticle.objects.filter(designation=request.POST.get('produit'), emballageu_id=request.POST.get('emballage'))
        if one:
            one = one.first()
            return JsonResponse({"prix": one.pa}, safe=False)
        return JsonResponse({"prix": 0}, safe=False)


@require_POST
@login_required
def getlibemballage(request):
    b = Farticle.objects.get(article=request.POST.get('produit'))

    return JsonResponse({"prix_achat": b.prix_achat,"pa": b.pa,"emb1": b.emballagee_id,"emb2": b.emballageu_id,"qteseuil": b.qte_stock_minimal}, safe=False)


@login_required
def getbon(request):
    b = Flivraison.objects.filter(commande__tiers_id=request.GET.get('client')).values("serielivraison","datejour")
    return JsonResponse({"bon": list(b)}, safe=False)

@require_POST
@login_required
def ajoutfournisseur(request):

    cmp=Ftiers.objects.all().count()+1

    fou=Ftiers.objects.filter(tiers=request.POST.get('idtiers'))
    if fou:
        fou.update(
            nompostnom=request.POST.get('nom')
        ,nature=request.POST.get('nature')
        ,typetiers=request.POST.get('type')
        ,raisonsoc=request.POST.get('raison')
        ,idnational=request.POST.get('idnat')
        ,adresse=request.POST.get('adresse')
        ,origine=request.POST.get('tel'))
    else:
        Ftiers.objects.create(tiers=cmp
        ,nompostnom=request.POST.get('nom')
        ,nature=request.POST.get('nature')
        ,typetiers=request.POST.get('type')
        ,raisonsoc=request.POST.get('raison')
        ,idnational=request.POST.get('idnat')
        ,adresse=request.POST.get('adresse')
        ,origine=request.POST.get('tel')
        )
    return JsonResponse({"msg": "Opération effectuée ", "id": "1","idfou":cmp,"nom":request.POST.get('nom')}, safe=False)

@require_POST
@login_required
def getqteproduitfacture(request):

    if 'modi' in request.POST:
        prix = Farticle.objects.get(article=request.POST.get('produit'))
        return JsonResponse({"prix": prix.prix_achat,'emb':prix.emballagee_id}, safe=False)
    elif request.POST.get('ctrl')=="0":
        pro=Farticle.objects.get(article=request.POST.get('produit'))

        #
        # b = Fmvts.objects.filter(location_id=request.session.get('idlocationuser'),article_id=request.POST.get('produit'),emballage_id=pro.emballagee_id,ajustement_id__in=("ACH","PAT","TRFR","INV")).aggregate(Sum("qte_entree")).get("qte_entree__sum")
        # if b is None:#entrer
        #     b = 0
        # c = Fmvts.objects.filter(location_id=request.session.get('idlocationuser'), article_id=request.POST.get('produit'),emballage_id=pro.emballagee_id,
        #                          ajustement_id__in=("VTE", "TRTO", "FACT","DECL","INV")).aggregate(Sum("qte_sortie")).get("qte_sortie__sum")
        # if c is None:  # sortie
        #     c = 0
        #
        # tot=b-c
        #
        # b = Fmvts.objects.filter(location_id=request.session.get('idlocationuser'),
        #                          article_id=request.POST.get('produit'),emballage_id=pro.emballageu_id,
        #                          ajustement_id__in=("ACH", "PAT", "TRFR", "INV")).aggregate(Sum("qte_entree")).get(
        #     "qte_entree__sum")
        # if b is None:  # entrer
        #     b = 0
        # c = Fmvts.objects.filter(location_id=request.session.get('idlocationuser'),
        #                          article_id=request.POST.get('produit'),emballage_id=pro.emballageu_id,
        #                          ajustement_id__in=("VTE", "TRTO", "FACT", "DECL", "INV")).aggregate(
        #     Sum("qte_sortie")).get("qte_sortie__sum")
        # if c is None:  # sortie
        #     c = 0
        #
        # tot1 = b - c
        #
        # b = Fmvts.objects.filter(location_id=request.session.get('idlocationuser'),
        #                          article_id=request.POST.get('produit'),emballage_id=pro.emballagea,
        #                          ajustement_id__in=("ACH", "PAT", "TRFR", "INV")).aggregate(Sum("qte_entree")).get(
        #     "qte_entree__sum")
        # if b is None:  # entrer
        #     b = 0
        # c = Fmvts.objects.filter(location_id=request.session.get('idlocationuser'),
        #                          article_id=request.POST.get('produit'),emballage_id=pro.emballagea,
        #                          ajustement_id__in=("VTE", "TRTO", "FACT", "DECL", "INV")).aggregate(
        #     Sum("qte_sortie")).get("qte_sortie__sum")
        # if c is None:  # sortie
        #     c = 0
        #
        # tot2 = b - c
        # #--------------------------------------------
        emb=Farticle.objects.filter(article=request.POST.get('produit')).values('emballagee_id','emballageu_id','emballagea','emballageu__designation',
                                                                                'emballagee__designation','quantitee','quantiteu','quantitea')



        return JsonResponse({"emb":list(emb)}, safe=False)
    else:
        if request.POST.get('emb')=="1":
            b = Fmvts.objects.filter(location_id=request.session.get('idlocationuser'),
                                     article_id=request.POST.get('produit'),
                                     ajustement_id__in=("ACH", "PAT", "TRFR")).aggregate(
                Sum("qte_entree")).get("qte_entree__sum")
            if b is None:  # entrer
                b = 0
            c = Fmvts.objects.filter(location_id=request.session.get('idlocationuser'),
                                     article_id=request.POST.get('produit'),
                                     ajustement_id__in=("VTE", "TRTO", "FACT", "DECL")).aggregate(
                Sum("qte_sortie")).get("qte_sortie__sum")
            if c is None:  # sortie
                c = 0
            tot = b - c
            prix = Farticle.objects.get(article=request.POST.get('produit'),LOCATION_id=request.session.get('idlocationuser'))

            return JsonResponse({"tot": tot,"prix":prix.prix_vente}, safe=False)
        else:

            b = Fmvts.objects.filter(location_id=request.session.get('idlocationuser'),
                                     article_id=request.POST.get('produit'),
                                     ajustement_id__in=("ACH", "PAT", "TRFR")).aggregate(Sum("qte_entree")).get(
                "qte_entree__sum")
            if b is None:  # entrer
                b = 0
            c = Fmvts.objects.filter(location_id=request.session.get('idlocationuser'),
                                     article_id=request.POST.get('produit'),
                                     ajustement_id__in=("VTE", "TRTO", "FACT", "DECL")).aggregate(Sum("qte_sortie")).get(
                "qte_sortie__sum")
            if c is None:  # sortie
                c = 0

            tot = b - c
            # --------------------------------------------
            emb = Farticle.objects.get(article=request.POST.get('produit'),LOCATION_id=request.session.get('idlocationuser'))

            return JsonResponse({"tot": (tot*emb.quantitee),"prix":emb.prix_vente}, safe=False)



def arondir(x):
    try:
        v1 = str(x)[:-3]
        v2 = str(x)[-3:]
        p1 = v2[0]
        p2 = int(v2[1:3])
        if p2 >= 50:
            v2 = (int(p1) + 1) * 100
        else:
            if int(p1) == 0:
                v2 = '000'
            else:
                v2 = int(p1) * 100
        return (int(v1) * 1000) + int(v2)
    except:
        return 0


@login_required
def getproduitchangelocation(request):
    rec = Farticle.objects.filter(LOCATION_id=request.GET.get('location')).values(
        "article","designation").order_by('designation')
    rec=list(rec)
    return JsonResponse({'data': rec}, safe=False)


@login_required
def produitchange(request):
    context = {
        "location": Flocation.objects.filter(typelocation='D').order_by('designation'),
        }
    if request.method == "POST":
        try:
            with transaction.atomic():
                cmd = Farticle.objects.get(article=request.POST.get('produit'))
                rqt=Fmvts.objects.filter(article=request.POST.get('produit'),ajustement__in=('INV','ACH','TRTO'))
                rqt.update(
                    location_id=request.POST.get('location')
                )
                cmd.LOCATION_id=request.POST.get('location')
                cmd.save()
                return JsonResponse({"msg": "Opération effectuée ", "id": "1"}, safe=False)
        except Exception as e:
            # raise e
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)

    return render(request, 'gestionstock/produitchangelocation.html', context)
