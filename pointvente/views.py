from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,permission_required
from django.core.management import call_command
from django.db.models import Func, F, Value,Sum,Q
from django.db.models.functions import Concat
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.db import IntegrityError, transaction
import datetime
import time
import os
import random
import string
# Create your views here.
from django.urls import reverse
from django.views.decorators.http import require_POST

from django.utils.text import Truncator

from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Image as img, Spacer, Paragraph, Table, TableStyle
from reportlab.graphics.barcode import code39

from .models import *
from gestionstock.models import *
from gestionstock.views import getstockproduit
from parametrage.models import Paramet,CustomUser

from pyreportjasper import JasperPy

from django.template.defaulttags import register



@login_required
@register.filter
def to_get_name_serveur(value):
    try:
        return Serveur.objects.get(id=value).nom
    except:
        return ""

@login_required
# @register.filter
@register.simple_tag
def to_get_table_serveur(value,user_):
    try:
        txt = f"""<div class="row">
                                        <div class="col-md-6">
                                            <p class="no-margin"><button id="#" type="button" class="btn btn-outline btn-info mb-5 btn_nouvelle" data-serveur="{value}">Nouvelle</button></p>
                                        </div>"""
        if user_.is_superuser:
            rec = Tattente.objects.filter(serveur_id=value).order_by('table_id')
        else:
            rec = Tattente.objects.filter(serveur_id=value,indsuspect=user_.id).order_by('table_id')
        tab=[]
        for i in rec:
            if i.table.id not in tab:
                tab.append(i.table.id)
                txt += f"""<div class="col-md-6"><p class="no-margin"><a type="button" class="btn btn-warning mb-5 btn_nouvelle_one" data-table="{i.table.id}" data-tablelib="{i.table.numero}" data-serveur="{i.serveur.id}">Table {i.table.numero}</a></p></div>"""
        txt+='</div>'
        return txt
    except:
        return ""


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


def home(request):

    # if Flocation.objects.filter(location=request.session.get('idlocationuser'),extra=True):
    #     from .cnx import connexion
    #     cnxQ = connexion()
    #     rc = cnxQ.Selection(["""select count(*) from TArticle"""])
    #     tot=0
    #     for i in rc:
    #         tot=i[0]
    #     context={
    #         "totproduit":tot,
    #         # "totclientnon":Ftiers.objects.filter(typetiers="2").count(),
    #         "totclientoui":DelaiInventaire.objects.count(),
    #         # "totcmd":Fcommande.objects.filter(etatcde="0",location_id=request.session.get('idlocationuser')).count(),
    #         # "totprix":TempoPrix.objects.filter(etat=0).count(),
    #         # "totproalerte":Farticle.objects.filter(etat=0).count(),
    #     }
    # else:
    #     context={
    #     "totproduit":Farticle.objects.count(),
    #     # "totclientnon":Ftiers.objects.filter(typetiers="2").count(),
    #     "totclientoui":DelaiInventaire.objects.count(),
    #     # "totcmd":Fcommande.objects.filter(etatcde="0",location_id=request.session.get('idlocationuser')).count(),
    #     # "totprix":TempoPrix.objects.filter(etat=0).count(),
    #     # "totproalerte":Farticle.objects.filter(etat=0).count(),
    # }

    t=0
    if request.session.get('check') == '1':  # Restaurent
        t_ = Fmvts.objects.filter(location=request.session.get('idlocationuser'), stckused=1, ndatemvt=str(
            str(datetime.datetime.today().date()).replace("-", "").replace("/", ""))).exclude(
            classe__isnull=False).exclude(destination__isnull=False).values("utilisateur", "datemvt",
                                                                            "ajustement").annotate(
            t=Sum(F("qte_sortie") * F("prix_achat"))).order_by("utilisateur")
        data = []
        detail = ''
        nom = ''
        for i in t_:
            if nom != i['utilisateur']:
                if nom != '':
                    offre = Fmvts.objects.filter(location=request.session.get('idlocationuser'), utilisateur=nom, stckused=1,
                                                 ndatemvt=str(
                                                     str(datetime.datetime.today().date()).replace("-", "").replace("/",
                                                                                                                    "")),
                                                 classe__isnull=False).values("utilisateur", "datemvt",
                                                                              "ajustement").aggregate(
                        t=Sum(F("qte_sortie") * F("prix_achat"))).get('t')
                    if offre is None:
                        offre = 0
                    detail += '<pclass ="no-margin"><span class ="text-white" style="font-size: 30px">Offre CDF {:,.2f}</span></p>'.format(
                        offre)

                    hebergement = Fmvts.objects.filter(location=request.session.get('idlocationuser'), utilisateur=nom,
                                                       stckused=1,
                                                       ndatemvt=str(
                                                           str(datetime.datetime.today().date()).replace("-",
                                                                                                         "").replace(
                                                               "/",
                                                               "")),
                                                       destination__isnull=False).values("utilisateur", "datemvt",
                                                                                         "ajustement").aggregate(
                        t=Sum(F("qte_sortie") * F("prix_achat"))).get('t')
                    if hebergement is None:
                        hebergement = 0
                    detail += '<p class ="no-margin"> <span class ="text-white" style="font-size: 30px">Hebergement CDF {:,.2f}</span></p>'.format(
                        hebergement)

                    nonvalide = Fmvts.objects.filter(location=request.session.get('idlocationuser'), utilisateur=nom,
                                                     stckused=0,
                                                     ajustement='FACT',
                                                     ndatemvt=str(
                                                         str(datetime.datetime.today().date()).replace("-",
                                                                                                       "").replace(
                                                             "/",
                                                             ""))).values("utilisateur", "datemvt").aggregate(
                        t=Sum(F("qte_sortie") * F("prix_achat"))).get('t')
                    if nonvalide is None:
                        nonvalide = 0
                    detail += '<p class ="no-margin"> <span class ="text-white" style="font-size: 30px">Non Valide {}</span></p>'.format(
                        nonvalide)

                    data.append(
                        {
                            'user': nom,
                            'detail': detail,
                        }
                    )
                nom = i['user']
                detail = ''
            if i['ajustement'] == "FACT":
                detail += '<p class ="no-margin"> <span class ="text-white" style="font-size:30px">Cash CDF {:,.2f}</span></p>'.format(
                    i["t"])

            if i['ajustement'] == "SUP":
                detail += '<p class ="no-margin"> <span class ="text-white" style="font-size: 30px">Annuler CDF {:,.2f}</span></p>'.format(
                    i["t"])

        if nom != '':
            offre = Fmvts.objects.filter(location=request.session.get('idlocationuser'), utilisateur=nom, stckused=1,
                                         ndatemvt=str(
                                             str(datetime.datetime.today().date()).replace("-", "").replace("/", "")),
                                         classe__isnull=False).values("utilisateur", "datemvt", "ajustement").aggregate(
                t=Sum(F("qte_sortie") * F("prix_achat"))).get('t')
            if offre is None:
                offre = 0
            detail += '<pclass ="no-margin"><span class ="text-white" style="font-size: 30px">Offre CDF {:,.2f}</span></p>'.format(
                offre)

            hebergement = Fmvts.objects.filter(location=request.session.get('idlocationuser'), utilisateur=nom, stckused=1,
                                               ndatemvt=str(
                                                   str(datetime.datetime.today().date()).replace("-", "").replace("/",
                                                                                                                  "")),
                                               destination__isnull=False).values("utilisateur", "datemvt",
                                                                                 "ajustement").aggregate(
                t=Sum(F("qte_sortie") * F("prix_achat"))).get('t')
            if hebergement is None:
                hebergement = 0
            detail += '<p class ="no-margin"> <span class ="text-white" style="font-size: 30px">Hebergement CDF {:,.2f}</span></p>'.format(
                hebergement)

            nonvalide = Fmvts.objects.filter(location=request.session.get('idlocationuser'), utilisateur=nom,
                                             stckused=0,
                                             ajustement='FACT',
                                             ndatemvt=str(
                                                 str(datetime.datetime.today().date()).replace("-",
                                                                                               "").replace(
                                                     "/",
                                                     ""))).values("utilisateur", "datemvt").aggregate(
                t=Sum(F("qte_sortie") * F("prix_achat"))).get('t')
            if nonvalide is None:
                nonvalide = 0
            detail += '<p class ="no-margin"> <span class ="text-white" style="font-size: 30px">Non Valide {}</span></p>'.format(
                nonvalide)

            data.append(
                {
                    'user': nom,
                    'detail': detail,
                }
            )

        context = {
            # "totclientnon": Ftiers.objects.filter(typetiers="1").count(),
            # "totarticl": Recettes.objects.filter(location_id=request.session.get('idlocationuser')).count(),
            "tot": data,
        }
    else:
        t = Fmvts.objects.filter(location=request.session.get('idlocationuser'), ajustement='FACT',
                                 ndatemvt=str(str(datetime.datetime.today().date()).replace("-", "").replace("/",
                                                                                                             ""))).aggregate(
            t=Sum(F("qte_sortie") * F("prix_achat"))).get('t')

        context = {
            # "totclientnon": Ftiers.objects.filter(typetiers="1").count(),
            "totarticl": Recettes.objects.filter(location_id=request.session.get('idlocationuser')).count(),
            "totcmd": t,
        }

    if 'locationuser' not in request.session:
        logout(request)

    if not request.user.is_authenticated:
        context['location']=Flocation.objects.all().order_by("designation")

    return render(request, 'main.html',context)

def check(request):

    username = request.POST['username']
    password = request.POST['pass']
    user = authenticate(username=username, password=password)
    if user is not None:

        veri=LocationUser.objects.filter(user=user,location_id=request.POST.get('location'))
        if veri:

            request.session['locationuser']=veri.first().location.designation
            request.session['idlocationuser']=veri.first().location.location
            request.session['check']=veri.first().location.categorie
            login(request, user)

    return redirect(reverse('pointvente:home'))

def uncheck(request):
    if 'locationuser' in request.session:
        del request.session['locationuser']
        del request.session['idlocationuser']
        del request.session['check']
    logout(request)
    return redirect(reverse('pointvente:home'))



@login_required
@permission_required('pointvente.facturation',raise_exception=True)
def commande(request):
    if request.method == "POST":
        t = 0
        try:
            with transaction.atomic():

                for produit, qte, emb1, prix,remise in zip(request.POST.getlist('produit[]'), request.POST.getlist('qte[]'),
                                                    request.POST.getlist('emb'), request.POST.getlist('prix[]'), request.POST.getlist('remise[]')):

                    if produit != "" and qte != "" and qte != "0" and prix != "":

                        pa=0

                        art = Farticle.objects.filter(article=produit, emballagee_id=emb1)
                        art2 = Farticle.objects.filter(article=produit, emballageu_id=emb1)
                        art3 = Farticle.objects.filter(article=produit, emballagea=emb1)
                        if art:
                            pa = float(art.first().prix_achat)
                        elif art2:
                            pa = float(art2.first().pa)
                        elif art3:
                            pa = float(art3.first().old_prix_achat)

                        art = Farticle.objects.get(article=produit)


                        f=Fmvts.objects.filter( location_id=art.LOCATION_id,document=request.POST.get('numfact'), article_id=produit, emballage_id=emb1, ajustement_id="FACT")
                        if f:
                            f.update(
                                location_id=art.LOCATION_id,
                                periode=str(datetime.date.today()).replace("-", "").replace("/", ""),
                                datemvt=datetime.date.today(),
                                ndatemvt=str(datetime.date.today()).replace("-", "").replace("/", ""),
                                ajustement_id="FACT",
                                article_id=produit,
                                emballage_id=emb1,
                                document=request.POST.get('numfact'),
                                designation=art.designation,
                                qte_sortie=qte,
                                flag="0",
                                prix_vente=prix,
                                bordereau=datetime.datetime.now().time(),
                                prix_achat=pa,
                                description=request.POST.get('client'),
                                imputation=request.POST.get('operation'),
                                txchange=str(request.POST.get('tx')).replace(",", "."),
                                requisition=str(request.POST.get('numfact')),
                                reference=art.famille.designation,
                                devise='CDF',
                                codeuser_id=request.user.id,
                                remise=remise,
                                destination=request.user.username,
                            )
                        else:

                            Fmvts.objects.create(
                                location_id=art.LOCATION_id,
                                periode=str(datetime.date.today()).replace("-","").replace("/",""),
                                datemvt=datetime.date.today(),
                                ndatemvt=str(datetime.date.today()).replace("-","").replace("/",""),
                                ajustement_id="FACT",
                                article_id=produit,
                                emballage_id=emb1,
                                document=request.POST.get('numfact'),
                                designation=art.designation,
                                qte_sortie=qte,
                                flag="0",
                                prix_vente=prix,
                                bordereau=datetime.datetime.now().time(),
                                prix_achat=pa,
                                description=request.POST.get('client'),
                                imputation=request.POST.get('operation'),
                                txchange=str(request.POST.get('tx')).replace(",","."),
                                requisition=str(request.POST.get('numfact')),
                                reference=art.famille.designation,
                                devise='CDF',
                                codeuser_id=request.user.id,
                                remise=remise,
                                destination=request.user.username,
                                )
                        t=1


                # #rapport
                # elements = []
                #
                # header = Table([[Paragraph(
                #     f'{request.session["locationuser"]}<br/>{para.libelle}<br/>{para.adresse}<br/>{para.cdpostal}<br/>Tél:{para.telephone}',
                #     style=Headerstyle)]])
                #
                # elements.append(header)
                #
                # header = Table([[Paragraph(f'FACT:{numcmd}', style=Headerstyle2)]])
                # elements.append(header)
                # elements.append(Spacer(1, 5))
                #
                # header = Table([[Paragraph(
                #     f'Date: {datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")}<br/><u>Client:{request.POST.get("client")} {request.POST.get("operation")}</u>',
                #     style=Headerstyle)]])
                #
                #
                # elements.append(header)
                # # Items
                #
                # table = Table(tbdata, colWidths=[2.3 * cm, 1.4 * cm, 1.8 * cm, 1.8 * cm])
                # table.setStyle([
                #     #('FONT', (0, 0), (-1, -1), 'Helvetica'),
                #     ('FONTSIZE', (0, 0), (-1, -1), 8),
                #     #('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
                #     ('GRID', (0, 0), (-1, 0), 0, (0.7, 0.7, 0.7)),
                #     # ('GRID', (-2, -1), (-1, -1), 0, (0.7, 0.7, 0.7)),
                #     # ('ALIGN', (0, 0), (-3, -3), 'LEFT'),
                #     ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                #     #('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
                # ])
                # elements.append(table)
                #
                # header = Table([[Paragraph("--------------------------------", style=styleNN)]])
                # elements.append(header)
                #
                # if tremise!=0:
                #     header = Table([[Paragraph("Total CDF {:,.2f}".format(tot+tremise), style=styleNN)]])
                #     elements.append(header)
                #
                #     header = Table([[Paragraph("Remise CDF {:,.2f}".format(tremise), style=styleNN)]])
                #     elements.append(header)
                #
                #     header = Table([[Paragraph("Total Gen. CDF {:,.2f}".format(tot), style=styleNN)]])
                #     elements.append(header)
                # else:
                #     header = Table([[Paragraph("Total CDF {:,.2f}".format(tot), style=styleNN)]])
                #     elements.append(header)
                #
                # header = Table([[Paragraph("--------------------------------", style=styleNN)]])
                # elements.append(header)
                #
                # header = Table([[Paragraph(f"Facture etablie par {request.user.username}", style=styleNN)]])
                # elements.append(header)
                #
                # header = Table([[Paragraph(
                #     "Merci de votre visite. A la prochaine.<br/>Les marchandises vendues ne sont ni Reprises ni echangees",
                #     style=Headerstyle)]])
                # elements.append(header)
                #
                #
                # barcode = code39.Extended39(codeb, barWidth=0.01 * inch, barHeight=.5 * inch)
                # elements.append(barcode)
                #
                # # elements.append(Spacer(1, 40))
                #
                # pagesize = (7.1967 * cm, 29.6686 * cm)
                #
                # # fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                # # output_file = os.path.join(fn, 'fac.pdf')
                # doc = SimpleDocTemplate(os.path.join(settings.MEDIA_ROOT, f'fac{request.user.id}.pdf') , pagesize=pagesize, rightMargin=1, leftMargin=1,
                #                         topMargin=1, bottomMargin=1, )
                # # doc.build(elements,onFirstPage=drawPageFrame)
                # doc.multiBuild(elements)



                ####################IMPRESSION
               # impression(request,t)
                ####################IMPRESSION
            # else:
            #     return JsonResponse({"msg": "Opération non effectuée ", "id": "0"}, safe=False)
        except Exception as e:
            print(str(e))
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)

        if t == 1:
            fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            input_file = os.path.join(fn, 'fac.jrxml')

            # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

            output = os.path.join(fn, 'media')

            con = {
                'driver': 'generic',
                'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
                'jdbc_url': f'jdbc:jtds:sqlserver://localhost/{settings.DATABASES["default"]["NAME"]}',
                'jdbc_dir': fn,
                'username': 'sa',
                'password': settings.DATABASES['default']['PASSWORD']
                # 'host': 'localhost',
                # 'database': 'STOCKCF',
                # 'port': '1433'
            }

            jasper = JasperPy()

            jasper.process(
                input_file,
                output,
                format_list=["pdf"],
                db_connection=con,
                parameters={'bon': request.POST.get('numfact')},
                locale='en_US'
            )

            return HttpResponse("1")
        else:
            return HttpResponse("0")


    if 'rqt' in request.GET:

        rec = Farticle.objects.filter(article=request.GET.get('produit')).values(
            "emballagee_id","emballageu_id", "emballagea", "prix_vente", "prix_vente_cdf", "old_prix_vente",'quantitee','quantiteu','quantitea')
        recx = list(rec)


        return JsonResponse({'data': recx,
                             'stock1':getstockproduit(request.session.get('idlocationuser'),request.GET.get('produit'),rec[0]['emballagee_id'],1),
                             'stock2':getstockproduit(request.session.get('idlocationuser'),request.GET.get('produit'),rec[0]['emballageu_id'],1),
                             'stock3':getstockproduit(request.session.get('idlocationuser'),request.GET.get('produit'),rec[0]['emballagea'],1)
                             }, safe=False)
    elif 'modi' in request.GET:

        rec = Fmvts.objects.filter(document=request.GET.get('id')).values()
        recx = list(rec)
        return JsonResponse({'data':recx},safe=False)
    context={
        "recettes":Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser')).order_by('designation'),
        "location":Flocation.objects.filter(location=request.session.get('idlocationuser')),
        "taux": Flocation.objects.get(location=request.session.get('idlocationuser')).txchange,
    }
    # context['numtrans'] = "F" + str(request.session['idlocationuser']) + random_char(6)

    return render(request, 'pointvente/commande.html',context)

@login_required
#@permission_required('pointvente.Rap_Stock',raise_exception=True)
def valcmd(request):

    ######################################################################
    if request.method == "POST":
        code=request.POST.get('code')

        if request.POST.get('code') is not None:

            f=Fmvts.objects.filter(location="028",ajustement='FACT',requisition=str(code))

            if f:
                f.update(flag="1")
                #code speaker



                #code speaker
                return JsonResponse("true", safe=False)
            else:
                return JsonResponse("false", safe=False)
        return JsonResponse("false", safe=False)
    # import os, sys
    # import win32print
    #
    # printer_name = win32print.GetDefaultPrinter()
    # hPrinter = win32print.OpenPrinter(printer_name)
    #
    # def prn_txt(text):
    #     if sys.version_info >= (3,):
    #         raw_data = bytes(text, "utf-8")
    #     else:
    #         raw_data = text
    #     try:
    #         hJob = win32print.StartDocPrinter(hPrinter, 1, ("test of raw data", None, "TEXT"))
    #         try:
    #             win32print.StartPagePrinter(hPrinter)
    #             win32print.WritePrinter(hPrinter, raw_data)
    #             win32print.EndPagePrinter(hPrinter)
    #         finally:
    #             win32print.EndDocPrinter(hPrinter)
    #     finally:
    #         win32print.ClosePrinter(hPrinter)
    #
    # txt =  "              LEON HOTEL \n"
    # txt += "               take way\n"
    # txt += "  41,Luambo Makiadi C/Gombe Kinshasa\n"
    # txt += "  Tel:0820044887    NO:FAC0019      \n"
    # txt += "  Date:2021-01-12   Client:Cash     \n"
    # txt += "  ----------------------------------\n"
    # txt += "\n"
    # txt += "Article     Qte   Prix       Montant\n"
    # txt += "------------------------------------\n"
    # txt += "BROKEN      1     28000          800\n"
    # txt += "BROKEN      1     28000          800\n"
    # txt += "BROKEN      1     28000          800\n"
    # txt += "------------------------------------\n"
    # txt += "                Total(Fc)       5600\n"
    # txt += "------------------------------------\n"
    # txt += "Merci de votre visite à la prochaine\n"
    # txt += "Les marchandises vendues ne sont ni \n"
    # txt += "Reprises ni echangees \n"
    # prn_txt(txt)

    # import os, sys
    # import win32print
    #
    # printer_name = win32print.GetDefaultPrinter()
    # print(printer_name)
    # #
    # # raw_data could equally be raw PCL/PS read from
    # #  some print-to-file operation
    # #
    # if sys.version_info >= (3,):
    #     print(1)
    #     raw_data = bytes("This is a test", "utf-8")
    # else:
    #     print(2)
    #     raw_data = "This is a test"
    #
    # hPrinter = win32print.OpenPrinter(printer_name)
    # try:
    #     print(3)
    #     hJob = win32print.StartDocPrinter(hPrinter, 1, ("test of raw data", None, "RAW"))
    #     try:
    #         print(4)
    #         win32print.StartPagePrinter(hPrinter)
    #         a = win32print.WritePrinter(hPrinter, raw_data)
    #         print(a)
    #         win32print.EndPagePrinter(hPrinter)
    #     finally:
    #         print(5)
    #         win32print.EndDocPrinter(hPrinter)
    # finally:
    #     print(6)
    #     win32print.ClosePrinter(hPrinter)







    # import os, sys
    # import win32print
    #
    # printer_name = win32print.GetDefaultPrinter ()
    #
    # #----------------------------------------------------------------------------------------------
    # import six
    # #create some raw data
    # #for i in range(2):
    #
    # rawdata = b'\x1b\x40'
    #
    # import time
    # from django.conf import settings
    # from reportlab.lib.pagesizes import landscape, letter
    # from reportlab.lib import colors
    # from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    # from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    # from reportlab.lib.units import inch, cm
    # from reportlab.platypus import SimpleDocTemplate, Image as img, Spacer, Paragraph, Table, TableStyle
    # strings = time.strftime("%Y:%m:%d %H:%M:%S")
    #
    #
    # # rawdata = bytes('Miltex SARLU','utf-8') + b'\n'+bytes('Agence E-money       Date : '+strings, 'utf-8') + b'\n'+bytes(txt, 'utf-8') + b'\n'+ b'\n' + bytes('---------------------Operation-----------------', 'utf-8') +b'\n'+b'\n'+ bytes(categorie, 'utf-8') +b'\n'+b'\n'+bytes( 'Caisse C. --> '+provin, 'utf-8') +b'\n' + bytes('-----------------------------------------------', 'utf-8') +b'\n'+b'\n'+bytes('Montant : '+request.POST.get('montant') +" "+monnaiee, 'utf-8') + b'\n'+b'\n'+ bytes('Autorise par '+request.user.username, 'utf-8') +b'\n'+b'\n'+ bytes('Visa Beneficier :', 'utf-8') +b'\n'+b'\n'+b'\n'+b'\n'+b'\n'+b'\n'+b'\n'+b'\x1d\x56' + six.int2byte(66) + b'\x00'
    # # printer = win32print.OpenPrinter(printer_name)
    # # hJob = win32print.StartDocPrinter(printer, 1, ("Leon Hotel", None, "RAW"))
    # # win32print.WritePrinter(printer, rawdata)
    # # win32print.EndPagePrinter(printer)
    # # win32print.ClosePrinter(printer)
    #
    # doc = SimpleDocTemplate(settings.MEDIA_ROOT+"/ticket.pdf", pagesize=letter,
    #                         rightMargin=0, leftMargin=0,
    #                         topMargin=0, bottomMargin=0)
    # Story = []
    # styles = getSampleStyleSheet()
    # styleN = styles["Normal"]
    # styleH = styles['Heading1']
    # Story.append(
    #     Paragraph("<b>Miltex SARLU<br/>Agence E-money<br/>" + 'txt' + " ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------</b>",
    #               styleN))
    # Story.append(Spacer(1 * inch, .5 * inch))
    # Story.append(Paragraph("Operation: %s" % ("categorie"), styleN))
    # Story.append(Spacer(1 * inch, .10 * inch))
    # Story.append(Paragraph("Libelle: %s" % ('Caisse C. --> '+"provin"), styleN))
    # Story.append(Spacer(1 * inch, .10 * inch))
    # Story.append(Paragraph("Montant: %s %s" % ("request.POST.get('montant')", "monnaiee"), styleN))
    # Story.append(Spacer(1 * inch, .10 * inch))
    # Story.append(Paragraph("Date: %s" % ("strings"), styleN))
    # Story.append(Spacer(1 * inch, .10 * inch))
    # Story.append(Paragraph("Autorise par: %s" % ("request.user.username"), styleN))
    # Story.append(Spacer(1 * inch, .10 * inch))
    # Story.append(Paragraph("Visa Beneficier : ", styleN))
    # Story.append(Spacer(1 * inch, .25 * inch))
    # doc.build(Story)
    ######################################################################
    return render(request, 'pointvente/valcmd.html')


@login_required
@permission_required('pointvente.recettesrapport',raise_exception=True)
def raprecette(request):
    if request.method == "POST":

        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = os.path.join(fn,'recettes.jrxml')

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = os.path.join(fn,'media')

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': f'jdbc:jtds:sqlserver://localhost/{settings.DATABASES["default"]["NAME"]}',
            'jdbc_dir': fn,
            'username': 'sa',
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKCF',
            # 'port': '1433'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml')
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
            parameters={'idlocation':request.session.get('idlocationuser'),'tvaero':str(tvaero),'idtva':str(idtva),'idclient':request.POST.get('client')},
            locale='en_US'
        )


        return HttpResponse("true")

    context={
        "client":Ftiers.objects.filter(nature="CLIENT").order_by("nompostnom"),
        "taxe":Ftaxes.objects.all().order_by("designation"),
    }
    return render(request, 'pointvente/raprecette.html',context)




@login_required
@permission_required('pointvente.sessionuser',raise_exception=True)
def sessionuser(request):
    if request.method == "POST":
        c=SessionUser.objects.filter(user=request.user,dateop=request.POST.get('dt'),etat=False)
        if c:
            c.update(user=request.user,
                                       etat=True
                                       )
        else:
            c = SessionUser.objects.filter(user=request.user, dateop=request.POST.get('dt'), etat=True)
            if c:
                messages.error(request, 'Il faut changer la date d\'ouverture, cette date existe déjà.')
            else:
                c = SessionUser.objects.filter(user=request.user, dateop__lt=request.POST.get('dt'))
                if c:
                    SessionUser.objects.create(user=request.user,
                                               etat=False,
                                               dateop=request.POST.get('dt')
                                               )
                    request.session['sesio'] = str(request.POST.get('dt'))

                else:
                    c = SessionUser.objects.filter(user=request.user)
                    if c:
                        messages.error(request, 'La date d\'ouverture doit être superieur aux dates antérieures.')
                    else:
                        SessionUser.objects.create(user=request.user,
                                                   etat=False,
                                                   dateop=request.POST.get('dt')
                                                   )
                        request.session['sesio'] = str(request.POST.get('dt'))
        return redirect(reverse('pointvente:sessionuser'))

    context={
        'users_':SessionUser.objects.filter(user=request.user,etat=False)
    }
    return render(request, 'pointvente/sessionuser.html',context)


#@login_required
#@permission_required('pointvente.recettesfiche',raise_exception=True)
def client(request):

    context={
        "recettes":Recettes.objects.filter(promotion=True).order_by('libelle')[:15]
    }
    return render(request, 'pointvente/client.html',context)



#def impression(request,numcmd,nom,"switch":0,table):
def bar(request):
    para = Paramet.objects.filter(location_id=request.session['idlocationuser'])
    if para:
        para = para.first()
    if request.user.is_superuser:
        t = Tattente.objects.filter(location=request.session['idlocationuser'],
                                    serveur_id=request.GET.get('serveur'), table_id=request.GET.get('table'))
    else:
        t = Tattente.objects.filter(location=request.session['idlocationuser'], indsuspect=request.user.id,
                                     serveur_id=request.GET.get('serveur'), table_id=request.GET.get('table'))


    if t:
        tbdata = []
        tbdata.append(['Article', 'Qte', 'Pu', 'Total'])
        tot = 0.0
        numcmd = ""
        b = t.first()

        codeb = str(int(int(''.join(filter(str.isdigit, b.facture))))) + str(
            str(datetime.date.today()).replace("-", "").replace("/", ""))
        if int((''.join(filter(str.isdigit, b.facture)))) < 10:
            codeb += '1111'
        elif int((''.join(filter(str.isdigit, b.facture)))) < 100:
            codeb += '111'
        elif int((''.join(filter(str.isdigit, b.facture)))) < 1000:
            codeb += '11'
        elif int((''.join(filter(str.isdigit, b.facture)))) < 10000:
            codeb += '1'

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


        for i in t:
            autonum = i.facture

            articl_=Recettes.objects.filter(id=i.article,cuisine=2)
            if articl_ and i.taux==0:
                numcmd = i.facture
                tbdata.append([

                    Paragraph(f"{str(i.designation).upper()} =>{i.famille} {i.client}", styleB),
                    Paragraph(f"{int(i.qte)}", styleN),
                    Paragraph(f"{i.puht}", styleNN),
                    Paragraph(f"{i.qte * i.puht}", styleNN)

                ])
                tot += i.qte * i.puht


        # rapport
        elements = []

        header = Table([[Paragraph(
            f'BON DE COMMANDE BAR<br/>{para.libelle}<br/>{para.adresse}<br/>{para.cdpostal}<br/>Tél:{para.telephone}',
            style=Headerstyle)]])

        elements.append(header)

        header = Table([[Paragraph(f'CDE:{numcmd}', style=Headerstyle2)]])
        elements.append(header)

        elements.append(Spacer(1, 5))

        header = Table([[Paragraph(
            f'<u>Date: {datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")} Client:Cash \nRéf.:{str(request.POST.get("reference"))} - Serveur : {b.serveur.nom} - table : {b.table.numero}</u>',
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

        header = Table([[Paragraph("Total CDF {:,.2f}".format(tot), style=styleNN)]])
        elements.append(header)

        header = Table([[Paragraph("--------------------------------", style=styleNN)]])
        elements.append(header)

        # header = Table([[Paragraph(
        #     "Merci de votre visite. A la prochaine.<br/>Les marchandises vendues ne sont ni Reprises ni echangees",
        #     style=Headerstyle)]])
        # elements.append(header)

        barcode = code39.Extended39(codeb, barWidth=0.01 * inch, barHeight=.5 * inch)
        elements.append(barcode)

        # elements.append(Spacer(1, 40))

        pagesize = (7.1967 * cm, 29.6686 * cm)

        # fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # output_file = os.path.join(fn, 'fac.pdf')
        doc = SimpleDocTemplate(os.path.join(settings.MEDIA_ROOT, 'facbar.pdf'), pagesize=pagesize, rightMargin=1,
                                leftMargin=1,
                                topMargin=1, bottomMargin=1, )
        # doc.build(elements,onFirstPage=drawPageFrame)
        doc.multiBuild(elements)
        t.update(taux=1)


    return JsonResponse({"msg": "Opération effectuée ", "id": "1"}, safe=False)
def cuisinetempo(request):
    para = Paramet.objects.filter(location_id=request.session['idlocationuser'])
    if para:
        para = para.first()
    if request.user.is_superuser:
        t = Tattente.objects.filter(location=request.session['idlocationuser'],
                                    serveur_id=request.GET.get('serveur'), table_id=request.GET.get('table'))
    else:
        t = Tattente.objects.filter(location=request.session['idlocationuser'], indsuspect=request.user.id,
                                     serveur_id=request.GET.get('serveur'), table_id=request.GET.get('table'))


    if t:
        tbdata = []
        tbdata.append(['Article', 'Qte', 'Pu', 'Total'])
        tot = 0.0
        numcmd = ""
        b = t.first()

        codeb = str(int(int(''.join(filter(str.isdigit, b.facture))))) + str(
            str(datetime.date.today()).replace("-", "").replace("/", ""))
        if int((''.join(filter(str.isdigit, b.facture)))) < 10:
            codeb += '1111'
        elif int((''.join(filter(str.isdigit, b.facture)))) < 100:
            codeb += '111'
        elif int((''.join(filter(str.isdigit, b.facture)))) < 1000:
            codeb += '11'
        elif int((''.join(filter(str.isdigit, b.facture)))) < 10000:
            codeb += '1'

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


        for i in t:
            autonum = i.facture

            articl_=Recettes.objects.filter(id=i.article,cuisine=1)
            if articl_ and i.taux==0:
                numcmd = i.facture
                tbdata.append([

                    Paragraph(f"{str(i.designation).upper()} =>{i.famille} {i.client}", styleB),
                    Paragraph(f"{int(i.qte)}", styleN),
                    Paragraph(f"{i.puht}", styleNN),
                    Paragraph(f"{i.qte * i.puht}", styleNN)

                ])
                tot += i.qte * i.puht


        # rapport
        elements = []

        header = Table([[Paragraph(
            f'BON DE COMMANDE CUISINE<br/>{para.libelle}<br/>{para.adresse}<br/>{para.cdpostal}<br/>Tél:{para.telephone}',
            style=Headerstyle)]])

        elements.append(header)

        header = Table([[Paragraph(f'CDE:{numcmd}', style=Headerstyle2)]])
        elements.append(header)

        elements.append(Spacer(1, 5))

        header = Table([[Paragraph(
            f'<u>Date: {datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")} Client:Cash \nRéf.:{str(request.POST.get("reference"))} - Serveur : {b.serveur.nom} - table : {b.table.numero}</u>',
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

        header = Table([[Paragraph("Total CDF {:,.2f}".format(tot), style=styleNN)]])
        elements.append(header)

        header = Table([[Paragraph("--------------------------------", style=styleNN)]])
        elements.append(header)

        # header = Table([[Paragraph(
        #     "Merci de votre visite. A la prochaine.<br/>Les marchandises vendues ne sont ni Reprises ni echangees",
        #     style=Headerstyle)]])
        # elements.append(header)

        barcode = code39.Extended39(codeb, barWidth=0.01 * inch, barHeight=.5 * inch)
        elements.append(barcode)

        # elements.append(Spacer(1, 40))

        pagesize = (7.1967 * cm, 29.6686 * cm)

        # fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # output_file = os.path.join(fn, 'fac.pdf')
        doc = SimpleDocTemplate(os.path.join(settings.MEDIA_ROOT, 'faccuisine.pdf'), pagesize=pagesize, rightMargin=1,
                                leftMargin=1,
                                topMargin=1, bottomMargin=1, )
        # doc.build(elements,onFirstPage=drawPageFrame)
        doc.multiBuild(elements)
        t.update(taux=1)

    return JsonResponse({"msg": "Opération effectuée ", "id": "1"}, safe=False)


def impression(request):

    # try:

    from escpos import NetworkConnection
    from escpos.impl.epson import GenericESCPOS
    # from escpos.printer import Usb
    # p = Usb(0x04b8, 0x0202, 0)
    # p.text("Hello World\n")
    # #p.image("logo.gif")
    # p.barcode('1324354657687', 'EAN13', 64, 2, '', '')
    # p.cut()
    #
    dtx = Tattente.objects.filter(location=request.session['idlocationuser'], indsuspect=request.user.id,
                          serveur_id=request.GET.get('serveur'), table_id=request.GET.get('table'))
    d=dtx.first()
    conn = NetworkConnection.create('192.168.123.100:9100')
    printer = GenericESCPOS(conn)
    printer.init()
    printer.text_center(' RESTAURANT ')
    printer.text_center(request.session.get("locationuser"))
    printer.text_center('41,Luambo Makiadi C/Gombe Kinshasa')
    printer.text_center(f'NO:CMD{d.facture}')
    printer.text_center(f'Date:{datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")}')
    printer.text_center('------------------------------------------')
    printer.text_center('Article                                Qte')
    printer.text_center('------------------------------------------')
    printer.justify_left()
    dtx=Tattente.objects.filter(location=request.session['idlocationuser'], indsuspect=request.user.id,serveur_id=request.GET.get('serveur'),table_id=request.GET.get('table'))
    for i in dtx:
        if Recettes.objects.get(id=i.article).cuisine:
            printer.textout(f'{str(i.designation)}               {str(int(i.qte))}')
            printer.lf(lines=1)

    printer.justify_right()
    # printer.lf(lines=1)
    # printer.text_center('Merci de votre visite à la prochaine')
    # printer.text_center('Les marchandises vendues ne sont ni')
    # printer.text_center('Reprises ni echangees')
    printer.lf(lines=15)
    printer.cut()
    return HttpResponse("ok")
    # except:
    #     pass

# def win_print(filename, printer_name = None):
#     font = {
#         "height": 8,
#     }
#     from win32 import win32print, win32api
#
#     Printer.text("title1", font_config=font)
#     Printer.text("title2", font_config=font)
#     Printer.text("title3", font_config=font)
#     Printer.text("title4", font_config=font)
#     # if not printer_name:
#     #     printer_name = win32print.GetDefaultPrinter()
#     # out = '/d:"%s"' % (printer_name)
#     # win32api.ShellExecute(0, "print", filename, out, ".", 0)

@login_required
@permission_required('pointvente.createrecette',raise_exception=True)
def prosnack(request):

    # win_print('test')
    # win_print('test.txt', 'PDFCreator')
#    impression(request,dtx={})

    if request.method == "POST":

        try:
            with transaction.atomic():

                art=Recettes.objects.filter(article_id=request.POST.get('produit'))

                if art:
                    art.update(
                        pu=str(request.POST.get('prix')).replace(",","."),
                        pu2=str(request.POST.get('prix2')).replace(",","."),
                        pu3=str(request.POST.get('prix3')).replace(",","."),
                        qte=str(request.POST.get('qte')).replace(",", "."),
                        qte2=str(request.POST.get('qte2')).replace(",", "."),
                        qte3=str(request.POST.get('qte3')).replace(",", "."),
                        embpu=request.POST.get('emb'),
                        embpu2=request.POST.get('emb2'),
                        embpu3=request.POST.get('emb3'),
                    )
                else:

                    Recettes.objects.create(
                        article_id=request.POST.get('produit'),
                        pu=str(request.POST.get('prix')).replace(",","."),
                        pu2=str(request.POST.get('prix2')).replace(",","."),
                        pu3=str(request.POST.get('prix3')).replace(",","."),
                        qte=str(request.POST.get('qte')).replace(",", "."),
                        qte2=str(request.POST.get('qte2')).replace(",", "."),
                        qte3=str(request.POST.get('qte3')).replace(",", "."),
                        embpu=request.POST.get('emb'),
                        embpu2=request.POST.get('emb2'),
                        embpu3=request.POST.get('emb3'),
                    )

                return JsonResponse(
                    {"msg": "Opération effectuée",
                     "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)
    context={
        "produit":Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser')),
        "emb":Femballage.objects.all()
    }
    return render(request, 'pointvente/productionsnack.html',context)

@login_required
@permission_required('pointvente.createcatrecette',raise_exception=True)
def catprosnack(request):

    if request.method == "POST":

        try:
            with transaction.atomic():
                print(request.POST)


                art=Ffamilles.objects.filter(famille=request.POST.get('idrecette'),codesocie=request.session.get('idlocationuser'))

                if art:
                    art.update(
                        designation=request.POST.get('designation'),
                    )
                else:
                    recnumart = Ffamilles.objects.filter(location_id=request.session.get('idlocationuser'))
                    if recnumart:
                        recnumart = recnumart.count()
                    else:
                        recnumart = 0
                    recnumart = str(recnumart + 1)

                    Ffamilles.objects.create(
                        famille=recnumart,
                        location_id=request.session['idlocationuser'],
                        codesocie=request.session.get('idlocationuser'),
                        designation=request.POST.get('designation'),
                    )

                return JsonResponse(
                    {"msg": "Opération effectuée",
                     "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)

    return render(request, 'pointvente/catproductionsnack.html')

@login_required
def deletearticle(request):

    if request.method == "POST":

        try:
            with transaction.atomic():

                b= Fmvts.objects.filter(requisition=request.POST.get('numbon'),designation=request.POST.get('article'),mvt=request.POST.get('id'))
                if b:
                    b.delete()

                return JsonResponse(
                    {"msg": "Opération effectuée",
                     "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)


@login_required
def deletearticle2(request):

    if request.method == "POST":

        try:
            with transaction.atomic():

                b= Fmvts.objects.filter(document=request.POST.get('numbon'),designation=request.POST.get('article'))
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

                bon=Fmvts.objects.filter(requisition=request.POST.get('numbon'))
                if bon:
                    bon.delete()

                # cmd=Fmvts.objects.all().order_by('-mvt')
                # if cmd:
                #     cmd=cmd.first()
                #     cmd=str(cmd.mvt)
                return JsonResponse(
                        {"msg": "Opération effectuée",
                         "id": "1","bon":"BC" +str(request.session['idlocationuser'])+ random_char(6)}, safe=False)
                # else:
                #     return JsonResponse(
                #     {"msg": "Opération effectuée",
                #      "id": "1","bon":"BC000" + str( Fmvts.objects.all().count()+ 1)}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)


@login_required
def addrectempodel(request):

    if request.method == "POST":

        try:
            with transaction.atomic():
                if request.session.get('check') == '1':  # Restaurent
                    t = Tattente.objects.filter(article=request.POST.get('produit'),
                                                location=request.session['idlocationuser'], id=request.POST.get('id')).exclude(colnet=1)

                    if t:
                        t.delete()

                        return JsonResponse(
                            {"msg": "Opération effectuée",
                             "id": "1"}, safe=False)
                    else:
                        return JsonResponse({"msg": "Opération non effectuée ", "id": "0"}, safe=False)
                else:
                    t=Tattente.objects.filter(article=request.POST.get('produit'),location=request.session['idlocationuser'],id=request.POST.get('id'))

                    if t:
                        t.delete()

                        return JsonResponse(
                        {"msg": "Opération effectuée",
                         "id": "1"}, safe=False)
                    else:
                        return JsonResponse({"msg": "Opération non effectuée ", "id": "0"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)

@login_required
def numerorectempodel(request):

    if request.method == "POST":

        try:
            with transaction.atomic():
                mois=datetime.date.today().month
                if mois<=9:
                    mois="0"+str(mois)

                jour=datetime.date.today().day
                if jour<=9:
                    jour="0"+str(jour)
                yg=1
                t=Fmvts.objects.filter(location=request.session['idlocationuser'],ajustement__in=('FACT','SUP'),codeuser=request.user.id,ndatemvt=str(datetime.date.today()).replace("-","").replace("/","")).values('document').distinct()
                if t:
                    yg = t.count() + 1
                    if yg <= 9:
                        yg = "00" + str(yg)
                    elif yg <= 99:
                        yg = "0" + str(yg)
                    elif yg <= 999:
                        yg = str(yg)
                    return JsonResponse({"tot": str(request.user.matricule)+str(datetime.date.today().year)[2:4]+str(mois)+str(jour)+str(yg)}, safe=False)

                if yg <= 9:
                    yg = "00" + str(yg)
                elif yg <= 99:
                    yg = "0" + str(yg)
                elif yg <= 999:
                    yg = str(yg)
                return JsonResponse({"tot": str(request.user.matricule)+str(datetime.date.today().year)[2:4]+str(mois)+str(jour)+str(yg)}, safe=False)

        except Exception as e:
            return JsonResponse({"tot": str(request.user.matricule)+str(datetime.date.today().year)[2:4]+str(mois)+str(jour)+str(yg)}, safe=False)


@login_required
@permission_required('pointvente.facturation',raise_exception=True)
def validerrec(request):
    if request.method == "POST":
        #
        # if 'imprimer' in request.POST:
        #
        #     # import win32api
        #     # import win32print
        #     from glob import glob
        #     # from docx import Document
        #     # from docx.shared import Inches, Cm,Mm
        #     # from docx.enum.text import WD_ALIGN_PARAGRAPH
        #     #
        #     # from docx.enum.section import WD_SECTION
        #     # #from barcode import EAN13
        #     # import barcode
        #     # from barcode.writer import ImageWriter
        #     # from docx2pdf import convert as ff
        #     #
        #     # document = Document()
        #     #
        #     # # document.add_heading('Document Title', 0)
        #     #
        #     # #sections = document.sections
        #     # section = document.sections[0]
        #     # section.page_height = Mm(297)
        #     # section.page_width = Mm(72)
        #     # section.left_margin = Cm(0.1)
        #     # section.right_margin = Cm(0.1)
        #     # section.top_margin = Cm(0.1)
        #     # section.bottom_margin = Cm(0.1)
        #     # # section.header_distance = Mm(12.7)
        #     # # section.footer_distance = Mm(12.7)
        #     #
        #     # # for section in sections:
        #     # #     section.top_margin = Cm(2.5)
        #     # #     section.bottom_margin = Cm(2.5)
        #     # #     section.left_mar&éàé&àçéè&&&è
        #     # #     gin = Cm(2.5)
        #     # #     section.right_margin = Cm(2.5)
        #     #
        #     # p = document.add_paragraph('TAKE AWAY\nLEON HOTEL')
        #     # p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        #     #
        #     # p1 = document.add_paragraph(
        #     #     '41,Luambo Makiadi C/Gombe Kinshasa\nRCCM 14-B-2299 ID NAT. N397108 \nNIF A0705328A Tél:+243 81 219 90 09\nCDE:00{}\nDate:{}   Client:Cash\n--------------------------------------------------'.format(request.POST.get('imprimer'),str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
        #     # p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        #     #
        #     #
        #     # table = document.add_table(rows=1, cols=4,)
        #     # hdr_cells = table.rows[0].cells
        #     # hdr_cells[0].text = 'Article'
        #     # hdr_cells[1].text = 'Qte'
        #     # hdr_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        #     # hdr_cells[2].text = 'Pu'
        #     # hdr_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        #     # hdr_cells[3].text = 'Montant'
        #     # hdr_cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        #     records=Fmvts.objects.filter(document=request.POST.get('imprimer'),ndatemvt=request.POST.get('bon'),ajustement='FACT',location=request.session['idlocationuser'])
        #     # tot=0
        #     # for i in records:
        #     #     row_cells = table.add_row().cells
        #     #     row_cells[0].text = str(i.designation)
        #     #     row_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
        #     #
        #     #     row_cells[1].text = str(i.qte_sortie)
        #     #     row_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        #     #     row_cells[2].text = str(i.prix_achat)
        #     #     row_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        #     #     row_cells[3].text = str(i.qte_sortie*i.prix_achat)
        #     #     tot+=(i.qte_sortie*i.prix_achat)
        #     #     row_cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        #     #
        #     # p1 = document.add_paragraph(f'Total(Fc)  {tot}')
        #     # p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        #     #
        #     # p1 = document.add_paragraph(
        #     #     'Merci de votre visite à la prochaine\nLes marchandises vendues ne sont ni \nReprises ni echangees')
        #     # p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        #     codeb=str(request.POST.get("imprimer"))+str(request.POST.get("bon"))
        #     if int(request.POST.get("imprimer"))<10:
        #         codeb+='1111'
        #     elif int(request.POST.get("imprimer"))<100:
        #         codeb+='111'
        #     elif int(request.POST.get("imprimer"))<1000:
        #         codeb+='11'
        #     elif int(request.POST.get("imprimer"))<10000:
        #         codeb+='1'
        #
        #     if records:
        #         records.update(
        #                 requisition=str(codeb)  # [:-2]
        #             )
        #
        #     # barCodeImage = barcode.get('ean13', f'{codeb}', writer=ImageWriter())
        #
        #
        #     #filename = barCodeImage.save('barcode')
        #
        #
        #     # with open('barcode.png', 'wb') as f:
        #     #     EAN13(f'1234567891234', writer=ImageWriter()).write(f)
        #
        #     # document.add_picture(settings.BASE_DIR+'\\'+'barcode.png', width=Inches(2.25))
        #     # last_paragraph = document.paragraphs[-1]
        #     # last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        #     #
        #     # document.add_page_break()
        #     #
        #     # document.save(settings.MEDIA_ROOT+"\demo.docx")
        #     #
        #     # #convert to pdf
        #     # ff(settings.MEDIA_ROOT+"\demo.docx")
        #
        #     # from keyboard import press
        #     #
        #     # # # A List containing the system printers
        #     # # all_printers = [printer[2] for printer in win32print.EnumPrinters(2)]
        #     # # # Ask the user to select a printer
        #     # # printer_num = int(input("Choose a printer:\n"+"\n".join([f"{n} {p}" for n, p in enumerate(all_printers)])+"\n"))
        #     # # # set the default printer
        #     # # win32print.SetDefaultPrinter(all_printers[printer_num])
        #     # name = win32print.GetDefaultPrinter()
        #     # pdf_dir = settings.BASE_DIR+"\demo.docx"
        #     # # for f in glob(pdf_dir, recursive=True):
        #     # win32api.ShellExecute(0, "print", pdf_dir, None, ".", 0)
        #     #press('enter')
        #
        #     fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        #     input_file = os.path.join(fn,'fac.jrxml')
        #     output = os.path.join(fn,'media')
        #
        #     con = {
        #         'driver': 'generic',
        #         'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
        #         'jdbc_url': f'jdbc:jtds:sqlserver://localhost/{settings.DATABASES["default"]["NAME"]}',
        #         'jdbc_dir': fn,
        #         'username': 'sa',
        #         'password': 'dev'
        #         # 'host': 'localhost',
        #         # 'database': 'STOCKCF',
        #         # 'port': '1433'
        #     }
        #
        #     jasper = JasperPy()
        #
        #     jasper.process(
        #         input_file,
        #         output,
        #         format_list=["pdf"],
        #         db_connection=con,
        #         parameters={'codebarre':codeb,'ndatemvt':request.POST.get('bon'),'location': request.session.get('idlocationuser'), 'document':request.POST.get('imprimer')},
        #         locale='en_US'
        #     )
        #
        #     return HttpResponse("true")



        try:
            valcheckpoint = 0
            checkpoint = request.session['check']
            if checkpoint == '1':
                valcheckpoint = 1  # restaurent

                #Check Serveur/Table
                serveur=Serveur.objects.filter(id=request.POST.get('serveur'))
                if serveur:
                    serveur=serveur.first()
                else:
                    return JsonResponse({"msg": "Opération non effectuée.Serveur n'existe Pas", "id": "0"}, safe=False)
                #Check Serveur/Table

            with transaction.atomic():
                para = Paramet.objects.filter(location_id=request.session['idlocationuser'])
                if para:
                    para = para.first()

                if valcheckpoint == 1:  # Restaurent
                    if request.user.is_superuser:
                        t=Tattente.objects.filter(location=request.session['idlocationuser'],serveur_id=request.POST.get('serveur'),table_id=request.POST.get('table'))
                    else:
                        t=Tattente.objects.filter(location=request.session['idlocationuser'],indsuspect=request.user.id,serveur_id=request.POST.get('serveur'),table_id=request.POST.get('table'))
                else:
                    t=Tattente.objects.filter(location=request.session['idlocationuser'],indsuspect=request.user.id)
                if t:
                    tbdata=[]
                    tbdata.append(['Article', 'Qte', 'Pu', 'Total'])
                    tot=0.0
                    numcmd=""
                    b=t.first()

                    codeb = str(int(int(''.join(filter(str.isdigit, b.facture))) ) ) + str(str(datetime.date.today()).replace("-","").replace("/",""))
                    if int((''.join(filter(str.isdigit, b.facture)))) < 10:
                        codeb += '1111'
                    elif int((''.join(filter(str.isdigit, b.facture)))) < 100:
                        codeb += '111'
                    elif int((''.join(filter(str.isdigit, b.facture)))) < 1000:
                        codeb += '11'
                    elif int((''.join(filter(str.isdigit, b.facture)))) < 10000:
                        codeb += '1'



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

                    autonum=0



                    for i in t:
                        autonum = i.facture

                        if valcheckpoint==1:#Restaurent
                            f=Fmvts.objects.filter(location=i.location,datemvt=datetime.date.today(),article=i.article,
                                document=i.facture)
                            if f:
                                qte_=f.first().qte_sortie
                                f.update(
                                    location=i.location,
                                    periode=str(request.session['sesio']).replace("-", "").replace("/", ""),
                                    datemvt=request.session['sesio'],
                                    ndatemvt=str(request.session['sesio']).replace("-", "").replace("/", ""),

                                    ajustement="FACT",
                                    article=i.article,
                                    tiers=i.classe,
                                    document=i.facture,
                                    designation=i.designation,
                                    qte_sortie=(i.qte+qte_),
                                    flag="0",
                                    qteunit_sortie=(i.qte+qte_),
                                    prix_achat=i.puht,
                                    description=i.client,
                                    requisition=str(codeb),
                                    reference=i.famille,
                                    devise='CDF',
                                    codeuser=request.user.id,
                                    stckused=0,
                                    imputation=f"{str(request.POST.get('reference'))} - Serveur : {i.serveur.nom} - table : {i.table.numero}",
                                    table=i.table.numero,
                                    utilisateur=request.user.username,
                                    serveur=i.serveur.nom
                                )
                            else:
                                Fmvts.objects.create(
                                location=i.location,
                                periode=str(request.session['sesio']).replace("-", "").replace("/", ""),
                                datemvt=request.session['sesio'],
                                ndatemvt=str(request.session['sesio']).replace("-", "").replace("/", ""),

                                ajustement="FACT",
                                article=i.article,
                                tiers=i.classe,
                                document=i.facture,
                                designation=i.designation,
                                qte_sortie=i.qte,
                                flag="0",
                                qteunit_sortie=i.qte,
                                prix_achat=i.puht,
                                description=i.client,
                                requisition=str(codeb),
                                reference=i.famille,
                                devise='CDF',
                                codeuser=request.user.id,
                                stckused=0,
                                imputation=f"{str(request.POST.get('reference'))} - table : {i.table.numero}",
                                table=i.table.numero,
                                utilisateur=request.user.username,
                                serveur = i.serveur.nom
                            )

                        else:
                            f = Fmvts.objects.filter(location=i.location, datemvt=datetime.date.today(),
                                                     article=i.article,
                                                     document=i.facture)
                            if f:
                                qte_ = f.first().qte_sortie
                                f.update(
                                    location=i.location,
                                    periode=str(datetime.date.today()).replace("-", "").replace("/", ""),
                                    datemvt=datetime.date.today(),
                                    ndatemvt=str(datetime.date.today()).replace("-", "").replace("/", ""),

                                    ajustement="FACT",
                                    article=i.article,
                                    tiers=i.classe,
                                    document=i.facture,
                                    designation=i.designation,
                                    qte_sortie=(i.qte+qte_),
                                    flag="0",
                                    qteunit_sortie=(i.qte+qte_),
                                    prix_achat=i.puht,
                                    description=i.client,
                                    requisition=str(codeb),
                                    reference=i.famille,
                                    devise='CDF',
                                    codeuser=request.user.id,
                                    utilisateur=request.user.username,
                                )
                            else:
                                Fmvts.objects.create(
                            location=i.location,
                            periode=str(datetime.date.today()).replace("-","").replace("/",""),
                            datemvt=datetime.date.today(),
                            ndatemvt=str(datetime.date.today()).replace("-","").replace("/",""),

                            ajustement="FACT",
                            article=i.article,
                                    tiers=i.classe,
                            document=i.facture,
                            designation=i.designation,
                            qte_sortie=i.qte,
                            flag="0",
                            qteunit_sortie=i.qte,
                            prix_achat=i.puht,
                            description=i.client,
                            requisition=str(codeb),
                            reference=i.famille,
                            devise='CDF',
                            codeuser=request.user.id,
                            utilisateur=request.user.username,
                            )
                        numcmd=i.facture
                        tbdata.append([

                            Paragraph(f"{str(i.designation).upper()} =>{i.famille} {i.client}", styleB),
                            Paragraph(f"{int(i.qte)}", styleN),
                            Paragraph(f"{i.puht}", styleNN),
                            Paragraph(f"{i.qte*i.puht}", styleNN)

                        ])
                        tot+=i.qte*i.puht

                    if valcheckpoint == 1:  # Restaurent
                        ##################Remote
                        # call_command('synchronize')
                        # try:
                        #     call_command('synchronize')
                        # except:
                        #     pass
                        ##################Remote
                        if request.user.is_superuser:
                            Tattente.objects.filter(location=request.session['idlocationuser'],serveur_id=request.POST.get('serveur'),table_id=request.POST.get('table')).delete()
                        else:
                            Tattente.objects.filter(location=request.session['idlocationuser'],indsuspect=request.user.id,serveur_id=request.POST.get('serveur'),table_id=request.POST.get('table')).delete()
                    else:
                        Tattente.objects.filter(location=request.session['idlocationuser'],indsuspect=request.user.id).delete()

                    #rapport
                    elements = []

                    header = Table([[Paragraph(
                        f'TAKE AWAY<br/>{para.libelle}<br/>{para.adresse}<br/>{para.cdpostal}<br/>Tél:{para.telephone}',
                        style=Headerstyle)]])

                    elements.append(header)

                    header = Table([[Paragraph(f'FACT:{numcmd}', style=Headerstyle2)]])
                    elements.append(header)

                    elements.append(Spacer(1, 5))


                    if valcheckpoint == 1:
                        header = Table([[Paragraph(
                            f'<u>Date: {datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")} Client:Cash \nRéf.:{str(request.POST.get("reference"))} - Serveur : {b.serveur.nom} - table : {b.table.numero}</u>',
                            style=Headerstyle)]])
                    else:
                        header = Table([[Paragraph(
                            f'<u>Date: {datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")} Client:Cash</u>',
                            style=Headerstyle)]])


                    elements.append(header)

                    # Items


                    table = Table(tbdata, colWidths=[3 * cm, 0.8 * cm, 1.5 * cm, 1.5 * cm])
                    table.setStyle([
                        #('FONT', (0, 0), (-1, -1), 'Helvetica'),
                        ('FONTSIZE', (0, 0), (-1, -1), 7),
                        #('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
                        ('GRID', (0, 0), (-1, 0), 0, (0.7, 0.7, 0.7)),
                        # ('GRID', (-2, -1), (-1, -1), 0, (0.7, 0.7, 0.7)),
                        # ('ALIGN', (0, 0), (-3, -3), 'LEFT'),
                        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                        #('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
                    ])
                    elements.append(table)

                    header = Table([[Paragraph("--------------------------------", style=styleNN)]])
                    elements.append(header)

                    header = Table([[Paragraph("Total CDF {:,.2f}".format(tot), style=styleNN)]])
                    elements.append(header)

                    header = Table([[Paragraph("--------------------------------", style=styleNN)]])
                    elements.append(header)

                    header = Table([[Paragraph(
                        "Merci de votre visite. A la prochaine.<br/>Les marchandises vendues ne sont ni Reprises ni echangees",
                        style=Headerstyle)]])
                    elements.append(header)


                    barcode = code39.Extended39(codeb, barWidth=0.01 * inch, barHeight=.5 * inch)
                    elements.append(barcode)

                    # elements.append(Spacer(1, 40))

                    pagesize = (7.1967 * cm, 29.6686 * cm)

                    # fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    # output_file = os.path.join(fn, 'fac.pdf')
                    doc = SimpleDocTemplate(os.path.join(settings.MEDIA_ROOT, 'fac.pdf') , pagesize=pagesize, rightMargin=1, leftMargin=1,
                                            topMargin=1, bottomMargin=1, )
                    # doc.build(elements,onFirstPage=drawPageFrame)
                    doc.multiBuild(elements)



                    ####################IMPRESSION
                   # impression(request,t)
                    ####################IMPRESSION
                    return JsonResponse(
                            {"msg": "Opération effectuée",
                             "id": "1","autonum":autonum,"bon":str(datetime.date.today()).replace("-","").replace("/","")}, safe=False)
                else:
                    return JsonResponse({"msg": "Opération non effectuée ", "id": "0"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)




# @login_required
# @permission_required('pointvente.facturation',raise_exception=True)
# def addition(request):
#     if request.method == "POST":
#
#         try:
#             valcheckpoint = 0
#             checkpoint = request.session['check']
#             if checkpoint == '1':
#                 valcheckpoint = 1  # restaurent
#
#                 #Check Serveur/Table
#                 serveur=Serveur.objects.filter(id=request.POST.get('serveur'))
#                 if serveur:
#                     serveur=serveur.first()
#                 else:
#                     return JsonResponse({"msg": "Opération non effectuée.Serveur n'existe Pas", "id": "0"}, safe=False)
#                 #Check Serveur/Table
#
#
#
#
#
#
#
#
#
#             with transaction.atomic():
#                 para = Paramet.objects.all()
#                 if para:
#                     para = para.first()
#                 t=Tattente.objects.filter(location=request.session['idlocationuser'],indsuspect=request.user.id)
#                 if t:
#                     tbdata=[]
#                     tbdata.append(['Article', 'Qte', 'Pu', 'Total'])
#                     tot=0.0
#                     numcmd=""
#                     b=t.first()
#
#                     codeb = str(int(int(''.join(filter(str.isdigit, b.facture))) ) ) + str(str(datetime.date.today()).replace("-","").replace("/",""))
#                     if int((''.join(filter(str.isdigit, b.facture)))) < 10:
#                         codeb += '1111'
#                     elif int((''.join(filter(str.isdigit, b.facture)))) < 100:
#                         codeb += '111'
#                     elif int((''.join(filter(str.isdigit, b.facture)))) < 1000:
#                         codeb += '11'
#                     elif int((''.join(filter(str.isdigit, b.facture)))) < 10000:
#                         codeb += '1'
#
#
#
#                     Titretyle = ParagraphStyle(
#                         name='titre',
#                         fontName='Helvetica-Bold',
#                         fontSize=8,
#                         textColor='DarkGray',
#                         borderPadding=(2, 2, 7, 2),
#                         borderWidth=0,
#                         alignment=TA_CENTER
#                     )
#
#                     Headerstyle = ParagraphStyle(
#                         name='headesr',
#                         fontName='Helvetica-Bold',
#                         fontSize=8,
#                         # borderPadding=(2, 2, 7, 2),
#                         # borderWidth=0,
#                         # borderColor='Gray',
#                         alignment=TA_CENTER
#                     )
#
#                     Headerstyle2 = ParagraphStyle(
#                         name='headesrd',
#                         fontName='Helvetica-Bold',
#                         fontSize=16,
#                         # borderPadding=(2, 2, 7, 2),
#                         # borderWidth=0,
#                         # borderColor='Gray',
#                         alignment=TA_CENTER
#                     )
#
#                     styles = getSampleStyleSheet()
#                     styleN = styles["BodyText"]
#                     styleN.alignment = TA_LEFT
#                     styleN.fontSize = 8
#
#                     styleNN = styles["BodyText"]
#                     styleNN.alignment = TA_RIGHT
#                     styleNN.fontSize = 8
#
#                     styleB = styles["Normal"]
#                     styleB.alignment = TA_LEFT
#                     styleB.fontSize = 8
#
#                     autonum=0
#
#
#
#                     for i in t:
#                         autonum = i.facture
#
#                         numcmd=i.facture
#                         tbdata.append([
#
#                             Paragraph(f"{str(i.designation).upper()} =>{i.famille} {i.client}", styleB),
#                             Paragraph(f"{int(i.qte)}", styleN),
#                             Paragraph(f"{i.puht}", styleNN),
#                             Paragraph(f"{i.qte*i.puht}", styleNN)
#
#                         ])
#                         tot+=i.qte*i.puht
#                     Tattente.objects.filter(location=request.session['idlocationuser'],indsuspect=request.user.id).delete()
#
#                     #rapport
#                     elements = []
#
#                     header = Table([[Paragraph(
#                         f'TAKE AWAY<br/>{para.libelle}<br/>{para.adresse}<br/>{para.cdpostal}<br/>Tél:{para.telephone}',
#                         style=Headerstyle)]])
#
#                     elements.append(header)
#
#                     header = Table([[Paragraph(f'CDE:{numcmd}', style=Headerstyle2)]])
#                     elements.append(header)
#
#                     elements.append(Spacer(1, 5))
#
#                     header = Table([[Paragraph(
#                         f'<u>Date: {datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")} Client:Cash \nRéf.:{request.POST.get("reference")}</u>',
#                         style=Headerstyle)]])
#
#
#                     elements.append(header)
#
#                     # Items
#
#
#                     table = Table(tbdata, colWidths=[3 * cm, 0.8 * cm, 1.5 * cm, 1.5 * cm])
#                     table.setStyle([
#                         #('FONT', (0, 0), (-1, -1), 'Helvetica'),
#                         ('FONTSIZE', (0, 0), (-1, -1), 7),
#                         #('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
#                         ('GRID', (0, 0), (-1, 0), 0, (0.7, 0.7, 0.7)),
#                         # ('GRID', (-2, -1), (-1, -1), 0, (0.7, 0.7, 0.7)),
#                         # ('ALIGN', (0, 0), (-3, -3), 'LEFT'),
#                         ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
#                         #('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
#                     ])
#                     elements.append(table)
#
#                     header = Table([[Paragraph("--------------------------------", style=styleNN)]])
#                     elements.append(header)
#
#                     header = Table([[Paragraph("Total CDF {:,.2f}".format(tot), style=styleNN)]])
#                     elements.append(header)
#
#                     header = Table([[Paragraph("--------------------------------", style=styleNN)]])
#                     elements.append(header)
#
#                     header = Table([[Paragraph(
#                         "Merci de votre visite. A la prochaine.<br/>Les marchandises vendues ne sont ni Reprises ni echangees",
#                         style=Headerstyle)]])
#                     elements.append(header)
#
#
#                     barcode = code39.Extended39(codeb, barWidth=0.01 * inch, barHeight=.5 * inch)
#                     elements.append(barcode)
#
#                     # elements.append(Spacer(1, 40))
#
#                     pagesize = (7.1967 * cm, 29.6686 * cm)
#
#                     # fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#                     # output_file = os.path.join(fn, 'fac.pdf')
#                     doc = SimpleDocTemplate(os.path.join(settings.MEDIA_ROOT, 'fac.pdf') , pagesize=pagesize, rightMargin=1, leftMargin=1,
#                                             topMargin=1, bottomMargin=1, )
#                     # doc.build(elements,onFirstPage=drawPageFrame)
#                     doc.multiBuild(elements)
#                     return JsonResponse(
#                             {"msg": "Opération effectuée",
#                              "id": "1","autonum":autonum,"bon":str(datetime.date.today()).replace("-","").replace("/","")}, safe=False)
#                 else:
#                     return JsonResponse({"msg": "Opération non effectuée ", "id": "0"}, safe=False)
#         except Exception as e:
#             return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)




@login_required
def addrectempo(request):

    if request.method == "POST":

        try:
            with transaction.atomic():

                # print(request.POST.getlist('commentaire[]'))
                # return JsonResponse(
                #     {"msg": "Opération effectuée",
                #      "id": "1"}, safe=False)
                # t=Tattente.objects.filter(article=request.POST.get('id'),location=request.session['idlocationuser'])
                #
                # if t:
                #     t.update(
                #         client=request.POST.getlist('commentaire[]'),
                #         qte=str(request.POST.get('qte')).replace(",","."),
                #         famille=request.POST.get('categorie'),
                #         puht=str(request.POST.get('pa')).replace(",","."),
                #         ptht=float(str(request.POST.get('pa')).replace(",","."))*float(str(request.POST.get('qte')).replace(",","."))
                #     )
                # else:
                checkpoint = request.session['check']
                if checkpoint == '1':
                    # t=Tattente.objects.filter(
                    #     article=request.POST.get('id'),
                    #     facture=request.POST.get('autonum'),
                    #     location=request.session['idlocationuser'],
                    #     datemvt=datetime.datetime.today().date(),
                    #     indsuspect=request.user.id
                    #         )
                    # if t:
                    #     qte=t.first().qte+int(str(request.POST.get('qte')).replace(",", "."))
                    #     t.update(
                    #         qte=qte,
                    #         ptht=float(str(request.POST.get('pa')).replace(",", ".")) * float(qte)
                    #     )
                    # else:
                    Tattente.objects.create(
                        article=request.POST.get('id'),
                            taux=0,
                        facture=request.POST.get('autonum'),
                        designation=request.POST.get('designation'),
                        client=request.POST.getlist('commentaire[]'),
                        famille=request.POST.get('categorie'),
                        classe=request.POST.get('famille'),
                        qte=str(request.POST.get('qte')).replace(",", "."),
                        location=request.session['idlocationuser'],
                        puht=str(request.POST.get('pa')).replace(",", "."),
                        indsuspect=request.user.id,
                        serveur_id=request.POST.get('serveur'),
                        table_id=request.POST.get('table'),
                        # datemvt=datetime.datetime.today().date(),
                        datemvt=request.session['sesio'],
                        ptht=float(str(request.POST.get('pa')).replace(",", ".")) * float(
                            str(request.POST.get('qte')).replace(",", "."))
                    )
                else:

                    Tattente.objects.create(
                    article=request.POST.get('id'),
                        taux=0,
                    facture=request.POST.get('autonum'),
                        classe=request.POST.get('famille'),
                    designation=request.POST.get('designation'),
                    client=request.POST.getlist('commentaire[]'),
                    famille=request.POST.get('categorie'),
                    qte=str(request.POST.get('qte')).replace(",","."),
                    location=request.session['idlocationuser'],
                    puht=str(request.POST.get('pa')).replace(",","."),
                        datemvt=datetime.datetime.today().date(),
                    indsuspect=request.user.id,
                    ptht=float(str(request.POST.get('pa')).replace(",","."))*float(str(request.POST.get('qte')).replace(",","."))
                )
                return JsonResponse(
                    {"msg": "Opération effectuée",
                     "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)

@login_required
def addrectempoaff(request):
    checkpoint = request.session['check']
    if checkpoint == '1':
        if request.user.is_superuser:
            rec = Tattente.objects.filter(location=request.session['idlocationuser'],serveur_id=request.GET.get('serveur'),table_id=request.GET.get('table'))
        else:
            rec = Tattente.objects.filter(location=request.session['idlocationuser'], indsuspect=request.user.id,serveur_id=request.GET.get('serveur'),table_id=request.GET.get('table'))
        htmltxt = ""
        tot = 0
        numerofac = ""
        for i in rec:
            numerofac = i.facture
            tot += i.ptht

            if i.colnet is not None and int(i.colnet) == 1:

                htmltxt += """
                                <div class="media">
                                                       <div class="media-body">

                                                            <p>
                                                            <nav class="nav no-gutters gap-2 font-size-16 media-show">

                                                                    <a class="nav-link text-danger" href="#" data-toggle="tooltip" ><strong>{}</strong></a>
                                                                </nav>
                                                            </p>
                                                            <div class="media-block-actions">

                                                                <nav class="nav nav-dot-separated no-gutters">
                                                                    <div class="nav-item">
                                                                        <a class="nav-link text-success" href="#" style="font-size: 20px"> Qte={}</a>
                                                                    </div>
                                                                    <div class="nav-item">
                                                                        <a class="nav-link text-danger" href="#" style="font-size: 20px"> <strong>Pu={}</strong> </a>
                                                                    </div>
                                                                    <div class="nav-item">
                                                                        <a class="nav-link text-info" href="#"style="font-size: 20px"> Tot={}</a>
                                                                    </div>
                                                                </nav>

                                                            </div>
                                                            <label>{}</label> 
                                                        </div>
                                                    </div>
                                """.format(i.designation, i.qte,i.puht, i.ptht,['Cuisine' if Recettes.objects.get(id=i.article).cuisine else ''][0])
            else:

                htmltxt += """
                <div class="media">
                                       <div class="media-body">

                                            <p>
                                            <nav class="nav no-gutters gap-2 font-size-16 media-show">

                                                    <a class="nav-link text-danger" href="#" onclick="supprimer('{}','{}')" data-toggle="tooltip" title="Supprimer"><i class="ion-close"> <strong>{}</strong> </i></a>
                                                </nav>
                                            </p>
                                            <div class="media-block-actions">

                                                <nav class="nav nav-dot-separated no-gutters">
                                                    <div class="nav-item">
                                                        <a class="nav-link text-success" href="#" onclick="supprimer('{}','{}')" style="font-size: 20px"> Qte={}</a>
                                                    </div>
                                                    <div class="nav-item">
                                                        <a class="nav-link text-danger" href="#" onclick="supprimer('{}','{}')" style="font-size: 20px"> <strong>Pu={}</strong> </a>
                                                    </div>
                                                    <div class="nav-item">
                                                        <a class="nav-link text-info" href="#" onclick="supprimer('{}','{}')" style="font-size: 20px"> Tot={}</a>
                                                    </div>
                                                </nav>

                                            </div>
                                            <label>{}</label> 
                                        </div>
                                    </div>
                """.format(i.article, i.id, i.designation, i.article, i.id, i.qte, i.article, i.id, i.puht, i.article,
                           i.id, i.ptht, ['Cuisine' if Recettes.objects.get(id=i.article).cuisine else ''][0])


    else:
        rec = Tattente.objects.filter(location=request.session['idlocationuser'], indsuspect=request.user.id)
        htmltxt = ""
        tot = 0
        numerofac = ""
        for i in rec:
            numerofac = i.facture
            tot += i.ptht
            htmltxt += """
                <div class="media">
                                       <div class="media-body">

                                            <p>
                                            <nav class="nav no-gutters gap-2 font-size-16 media-show">

                                                    <a class="nav-link text-danger" href="#" onclick="supprimer('{}','{}')" data-toggle="tooltip" title="Supprimer"><i class="ion-close"> <strong>{}</strong> </i></a>
                                                </nav>
                                            </p>
                                            <div class="media-block-actions">

                                                <nav class="nav nav-dot-separated no-gutters">
                                                    <div class="nav-item">
                                                        <a class="nav-link text-success" href="#" onclick="supprimer('{}','{}')" style="font-size: 20px"> Qte={}</a>
                                                    </div>
                                                    <div class="nav-item">
                                                        <a class="nav-link text-danger" href="#" onclick="supprimer('{}','{}')" style="font-size: 20px"> <strong>Pu={}</strong> </a>
                                                    </div>
                                                    <div class="nav-item">
                                                        <a class="nav-link text-info" href="#" onclick="supprimer('{}','{}')" style="font-size: 20px"> Tot={}</a>
                                                    </div>
                                                </nav>

                                            </div>
                                            <label>{}</label> 
                                        </div>
                                    </div>
                """.format(i.article, i.id, i.designation, i.article, i.id, i.qte, i.article, i.id, i.puht, i.article,
                           i.id, i.ptht, ['Cuisine' if Recettes.objects.get(id=i.article).cuisine else ''][0])

    if checkpoint == '1':
        return JsonResponse({'numerofac': numerofac,'data': htmltxt,'tot':str("Total Gen = ")+str(tot),'totcdf':str(tot)}, safe=False)
    else:
        return JsonResponse({'data': htmltxt,'tot':str("Total Gen = ")+str(tot),'totcdf':str(tot)}, safe=False)

def getclienttakedetele(request):

    recc = Fmvts.objects.filter(location="028",ajustement='FACT',flag="1",ndatemvt=str(datetime.date.today()).replace("-","").replace("/","")).values('document').order_by('mvt')
    rec=list(recc)
    return JsonResponse({'data': rec}, safe=False)

def getclienttake(request):

    recc = Fmvts.objects.filter(location="028",ajustement='FACT',flag="0",ndatemvt=str(datetime.date.today()).replace("-","").replace("/","")).order_by('-mvt')
    doc=""
    txtfull=""
    for i in recc:
        if doc!=i.document:
            doc=i.document
            recette=Recettes.objects.get(id=i.article)


            txtfull+=f"""<li class="carousel-item" data-document={i.document} data-commande={i.mvt}>
                    <div class="card" align="center">
                        <h2 class="card-title" style="font-weight: bold;font-size:25px">{Truncator(i.designation).chars(16)}</h2>
                        <img style="border-radius:5%;" width="400px" height="400px" src="{ recette.image.url if recette.image else "/media/images/recettes/logovide.png"}" />
                        <div class="card-content">
                            <a href="#" class="button">Commande N° {i.document}</a>
                        </div>
                    </div>
                </li>"""

    return JsonResponse({'data': txtfull}, safe=False)


def getclienttakeone(request):
    if request.GET.get('id') is not None:
        recc = Fmvts.objects.filter(location="028",ajustement='FACT',flag="0",mvt__gt=request.GET.get('id'),ndatemvt=str(datetime.date.today()).replace("-","").replace("/","")).exclude(document=request.GET.get('commande')).order_by('mvt')
    else:
        recc = Fmvts.objects.filter(location="028", ajustement='FACT', flag="0", mvt__gt=0,ndatemvt=str(datetime.date.today()).replace("-","").replace("/","")).order_by('mvt')
    doc=""
    cmd=0
    txtfull=""
    for i in recc:
        cmd=i.document
        if doc!=i.document:
            doc=i.document
            recette=Recettes.objects.get(id=i.article)

            txtfull+=f"""<li class="carousel-item" data-document={i.document} data-commande={i.mvt}>
                    <div class="card" align="center">
                        <h2 class="card-title" style="font-weight: bold;font-size:25px">{Truncator(i.designation).chars(16)}</h2>
                        <img style="border-radius:5%;" width="400px" height="400px" src="{ recette.image.url if recette.image else "/media/images/recettes/logovide.png"}" />
                        <div class="card-content">
                            <a href="#" class="button">Commande N° {i.document}</a>
                        </div>
                    </div>
                </li>"""

    return JsonResponse({'data': txtfull,'cmd':cmd}, safe=False)


@login_required
def getfacture(request):
	rec = Fmvts.objects.filter(document=request.GET.get('numtrans'),ajustement="TRFR",location=request.GET.get('locationbis').replace("-", "").replace("/", "")).values(
            "mvt","designation","qteunit_entree","qte_entree","emballage","imputation","datemvt","location").order_by('-mvt')
	rec=list(rec)
	return JsonResponse({'data': rec}, safe=False)


@require_POST
@login_required
def getrecettes(request):
    rec = Recettes.objects.filter(location_id=request.session.get('idlocationuser')).values().order_by('libelle')
    rec=list(rec)
    return JsonResponse({'data': rec}, safe=False)


@login_required
def getrecette(request):
    rec = Recettes.objects.filter(location_id=request.session.get('idlocationuser')).values(
        "id","libelle").order_by('libelle')
    rec=list(rec)
    return JsonResponse({'data': rec}, safe=False)

@login_required
def getrecettesnack(request):
    rec = Recettes.objects.filter(article__LOCATION_id=request.session.get('idlocationuser')).values(
        "article_id","article__designation","qte","qte2","qte3","pu","embpu","pu2","embpu2","pu3","embpu3").order_by('article__designation')
    rec=list(rec)
    return JsonResponse({'data': rec}, safe=False)

@login_required
def gettabledispo(request):
    txt='<div class="row">'
    rec = TableRestaurent.objects.filter(etat=True,location_id=request.session.get('idlocationuser')).exclude(tattente__isnull=False)
    for i in rec:
        txt+=f"""<div class="col-md-3"><p class="no-margin"><button type="button" class="btn btn-warning mb-5 btn_nouvelle_one" data-table="{i.id}" data-tablelib="{i.numero}" data-serveur="{request.GET.get('serveur')}">Table {i.numero}</button></p></div>"""
    txt+='</div>'
    return JsonResponse({'data': txt}, safe=False)

@login_required
def getrecettecatsnack(request):
    rec = Ffamilles.objects.filter(codesocie=request.session.get('idlocationuser')).values(
        "famille","designation").order_by('designation')
    rec=list(rec)
    return JsonResponse({'data': rec}, safe=False)

@login_required
def gettiers(request):
    rec = Ftiers.objects.filter(tiers=request.GET.get('id')).values(
        "tiers","nompostnom","adresse","origine","idnational","raisonsoc")
    rec=list(rec)
    return JsonResponse({'data': rec}, safe=False)


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

    if request.POST.get('ctrl')=="0":

        # b = Fmvts.objects.filter(location_id=request.session.get('idlocationuser'),article_id=request.POST.get('produit'),ajustement_id__in=("ACH","PAT","TRFR","INV")).aggregate(Sum("qte_entree")).get("qte_entree__sum")
        # if b is None:#entrer
        #     b = 0
        # c = Fmvts.objects.filter(location_id=request.session.get('idlocationuser'), article_id=request.POST.get('produit'),
        #                          ajustement_id__in=("VTE", "TRTO", "FACT","DECL","INV")).aggregate(Sum("qte_sortie")).get("qte_sortie__sum")
        # if c is None:  # sortie
        #     c = 0
        #
        # tot=b-c
        #--------------------------------------------
        if Flocation.objects.filter(location=request.session.get('idlocationuser'),extra=True):
            from .cnx import connexion
            cnxQ = connexion()
            b = cnxQ.Selection(["""select EmbV,EmbU,Pa from TArticle where CodeArt='{}'""".format(request.POST.get('produit'))])
            b1=''
            b2=''
            b3=''
            for tempg in b:
                b1=tempg[0]
                b2=tempg[1]
                b3=tempg[2]
            return JsonResponse({"emb1": b1,"emb2": b2,"prix": b3}, safe=False)
        else:
            b = Farticle.objects.get(article=request.POST.get('produit'))

            return JsonResponse({"emb1": b.emballagee,"emb2": b.emballageu,"prix": b.prix_achat,"prix1": b.prixachgro}, safe=False)

            # emb=Farticle.objects.filter(article=request.POST.get('produit'),LOCATION_id=request.session.get('idlocationuser')).values('emballagee_id','emballageu_id','emballageu__designation',
                                                                               # 'emballagee__designation')

        # prix=Farticle.objects.get(article=request.POST.get('produit'),LOCATION_id=request.session.get('idlocationuser'))


        # return JsonResponse({"tot": tot,"emb":list(emb),"prix":prix.prix_vente}, safe=False)
        # return JsonResponse({"tot": tot,"emb":list(emb),"prix":prix.prix_vente}, safe=False)
    else:

        if request.POST.get('emb')=="1":
            b = Fmvts.objects.filter(location_id=request.session.get('idlocationuser'),
                                     article_id=request.POST.get('produit'),
                                     ajustement_id__in=("ACH", "PAT", "TRFR")).aggregate(
                Sum("qte_entree")).get(
                "qte_entree__sum")
            if b is None:  # entrer
                b = 0
            c = Fmvts.objects.filter(location_id=request.session.get('idlocationuser'),
                                     article_id=request.POST.get('produit'),
                                     ajustement_id__in=("VTE", "TRTO", "FACT", "DECL")).aggregate(
                Sum("qte_sortie")).get(
                "qte_sortie__sum")
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


@login_required
def pointvente(request):

    if request.method=="POST":


        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        if 'categorie' in request.POST:
            if request.POST.get("utilisateur") != "":
                input_file = os.path.join(fn, 'rapjournalierCatUtil.jrxml')
            else:
                input_file = os.path.join(fn, 'rapjournalierCat.jrxml')

            # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

            output = os.path.join(fn, 'media')

            con = {
                'driver': 'generic',
                'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
                'jdbc_url': f'jdbc:jtds:sqlserver://localhost/{settings.DATABASES["default"]["NAME"]}',
                'jdbc_dir': fn,
                'username': 'sa',
                'password': settings.DATABASES['default']['PASSWORD']
                # 'host': 'localhost',
                # 'database': 'STOCKCF',
                # 'port': '1433'
            }

            jasper = JasperPy()
            # jasper.compile("D:/test1.jrxml')
            # jasper.path_executable = "D:/JasperStarter/bin/"

            if request.POST.get('utilisateur') != "":
                p = {'utilisateur': '{}'.format(request.POST.get('utilisateur')),
                     'nom': '{}'.format(request.POST.get('nom')),
                     'idlocation': '{}'.format(request.POST.get('idlocationuser')),
                     'liblocation': '{}'.format(request.POST.get('locationuser')),
                     'd1': '{}'.format(request.POST.get('dtd')), 'd2': '{}'.format(request.POST.get('dtf')),
                     'datedb': '{}'.format(str(request.POST['dtd']).replace("-", "")),
                     'datefn': '{}'.format(str(request.POST['dtf']).replace("-", ""))}
            else:
                p = {'idlocation': '{}'.format(request.POST.get('idlocationuser')),
                     'liblocation': '{}'.format(request.POST.get('locationuser')),
                     'd1': '{}'.format(request.POST.get('dtd')), 'd2': '{}'.format(request.POST.get('dtf')),
                     'datedb': '{}'.format(str(request.POST['dtd']).replace("-", "")),
                     'datefn': '{}'.format(str(request.POST['dtf']).replace("-", ""))}
            jasper.process(
                input_file,
                output,
                format_list=["pdf"],
                db_connection=con,
                parameters=p,
                locale='en_US'
            )
        else:

            if request.POST.get("utilisateur")!="":
                input_file = os.path.join(fn,'rapjournalierUtil.jrxml')
            else:
                input_file = os.path.join(fn,'rapjournalier_.jrxml')

            # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

            output =os.path.join(fn,'media')

            con = {
                'driver': 'generic',
                'jdbc_driver':'net.sourceforge.jtds.jdbc.Driver',
                'jdbc_url':f'jdbc:jtds:sqlserver://localhost/{settings.DATABASES["default"]["NAME"]}',
                'jdbc_dir':fn,
                'username': 'sa',
                'password': settings.DATABASES['default']['PASSWORD']
                # 'host': 'localhost',
                # 'database': 'STOCKCF',
                # 'port': '1433'
            }

            jasper = JasperPy()
            # jasper.compile("D:/test1.jrxml')
            # jasper.path_executable = "D:/JasperStarter/bin/"


            if request.POST.get('utilisateur')!="":
                p={'utilisateur': '{}'.format(request.POST.get('utilisateur')),'nom': '{}'.format(request.POST.get('nom')),'idlocation': '{}'.format(request.POST.get('idlocationuser')),'liblocation': '{}'.format(request.POST.get('locationuser')),'d1': '{}'.format(request.POST.get('dtd')),'d2': '{}'.format(request.POST.get('dtf')),'datedb': '{}'.format(str(request.POST['dtd']).replace("-","")),'datefn': '{}'.format(str(request.POST['dtf']).replace("-",""))}
            else:
                p={'idlocation': '{}'.format(request.POST.get('idlocationuser')),'liblocation': '{}'.format(request.POST.get('locationuser')),'d1': '{}'.format(request.POST.get('dtd')),'d2': '{}'.format(request.POST.get('dtf')),'datedb': '{}'.format(str(request.POST['dtd']).replace("-","")),'datefn': '{}'.format(str(request.POST['dtf']).replace("-",""))}
            jasper.process(
                input_file,
                output,
                format_list=["pdf"],
                db_connection=con,
                parameters=p,
                locale='en_US'
            )
        return HttpResponse("true")

    context={
    	'noms':CustomUser.objects.all(),
    	'location':Flocation.objects.all()
    }

    return render(request, 'pointvente/rapvente.html',context)


@login_required
def pointvente1(request):

    if request.method=="POST":
        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        input_file = os.path.join(fn, 'rapjournalierH.jrxml')

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = os.path.join(fn, 'media')

        con = {
            'driver': 'generic',
            'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url': f'jdbc:jtds:sqlserver://localhost/{settings.DATABASES["default"]["NAME"]}',
            'jdbc_dir': fn,
            'username': 'sa',
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKCF',
            # 'port': '1433'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml')
        # jasper.path_executable = "D:/JasperStarter/bin/"

        p = {'idlocation': '{}'.format(request.POST.get('idlocationuser')),
             'liblocation': '{}'.format(request.POST.get('locationuser')), 'd1': '{}'.format(request.POST.get('dtd')),
             'd2': '{}'.format(request.POST.get('dtf')),
             'datedb': '{}'.format(str(request.POST['dtd']).replace("-", "")),
             'datefn': '{}'.format(str(request.POST['dtf']).replace("-", ""))}
        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters=p,
            locale='en_US'
        )
        return HttpResponse("true")

    context={

    	'location':Flocation.objects.all()
    }

    return render(request, 'pointvente/rapvente1.html',context)

@login_required
def pointvente2(request):

    if request.method=="POST":

        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        input_file = os.path.join(fn,'rapjournalierO.jrxml')

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output =os.path.join(fn,'media')

        con = {
            'driver': 'generic',
            'jdbc_driver':'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url':f'jdbc:jtds:sqlserver://localhost/{settings.DATABASES["default"]["NAME"]}',
            'jdbc_dir':fn,
            'username': 'sa',
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKCF',
            # 'port': '1433'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml')
        # jasper.path_executable = "D:/JasperStarter/bin/"

        p={'idlocation': '{}'.format(request.POST.get('idlocationuser')),'liblocation': '{}'.format(request.POST.get('locationuser')),'d1': '{}'.format(request.POST.get('dtd')),'d2': '{}'.format(request.POST.get('dtf')),'datedb': '{}'.format(str(request.POST['dtd']).replace("-","")),'datefn': '{}'.format(str(request.POST['dtf']).replace("-",""))}
        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters=p,
            locale='en_US'
        )
        return HttpResponse("true")

    context={
    	'location':Flocation.objects.all()
    }

    return render(request, 'pointvente/rapvente2.html',context)


@login_required
def pointvente3(request):

    if request.method=="POST":

        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        input_file = os.path.join(fn,'rapjournalierBouillard.jrxml')

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output =os.path.join(fn,'media')

        con = {
            'driver': 'generic',
            'jdbc_driver':'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url':f'jdbc:jtds:sqlserver://localhost/{settings.DATABASES["default"]["NAME"]}',
            'jdbc_dir':fn,
            'username': 'sa',
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKCF',
            # 'port': '1433'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml')
        # jasper.path_executable = "D:/JasperStarter/bin/"

        p={'idlocation': '{}'.format(request.POST.get('idlocationuser')),'liblocation': '{}'.format(request.POST.get('locationuser')),'d1': '{}'.format(request.POST.get('dtd')),'d2': '{}'.format(request.POST.get('dtf')),'datedb': '{}'.format(str(request.POST['dtd']).replace("-","")),'datefn': '{}'.format(str(request.POST['dtf']).replace("-",""))}
        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters=p,
            locale='en_US'
        )
        return HttpResponse("true")

    context={
    	'location':Flocation.objects.all()
    }

    return render(request, 'pointvente/rapvente3.html',context)


@login_required
def pointvente4(request):

    if request.method=="POST":

        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        input_file = os.path.join(fn,'rapjournalierReg.jrxml')

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output =os.path.join(fn,'media')

        con = {
            'driver': 'generic',
            'jdbc_driver':'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url':f'jdbc:jtds:sqlserver://localhost/{settings.DATABASES["default"]["NAME"]}',
            'jdbc_dir':fn,
            'username': 'sa',
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKCF',
            # 'port': '1433'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml')
        # jasper.path_executable = "D:/JasperStarter/bin/"

        p={'idlocation': '{}'.format(request.session.get('idlocationuser')),'d1': '{}'.format(request.POST.get('dtd')),'d2': '{}'.format(request.POST.get('dtf')),'datedb': '{}'.format(str(request.POST['dtd']).replace("-","")),'datefn': '{}'.format(str(request.POST['dtf']).replace("-",""))}
        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters=p,
            locale='en_US'
        )
        return HttpResponse("true")

    return render(request, 'pointvente/rapvente4.html')


@login_required
def pointvente5(request):

    if request.method=="POST":

        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        input_file = os.path.join(fn,'rapjournalierA.jrxml')

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output =os.path.join(fn,'media')

        con = {
            'driver': 'generic',
            'jdbc_driver':'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url':f'jdbc:jtds:sqlserver://localhost/{settings.DATABASES["default"]["NAME"]}',
            'jdbc_dir':fn,
            'username': 'sa',
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKCF',
            # 'port': '1433'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml')
        # jasper.path_executable = "D:/JasperStarter/bin/"

        p={'idlocation': '{}'.format(request.session.get('idlocationuser')),'d1': '{}'.format(request.POST.get('dtd')),'d2': '{}'.format(request.POST.get('dtf')),'datedb': '{}'.format(str(request.POST['dtd']).replace("-","")),'datefn': '{}'.format(str(request.POST['dtf']).replace("-",""))}
        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters=p,
            locale='en_US'
        )
        return HttpResponse("true")

    return render(request, 'pointvente/rapvente5.html')





@login_required
@permission_required('pointvente.validation_facture',raise_exception=True)
def validation(request):

    if request.method=="POST":
        t = Fmvts.objects.filter(location=request.session['idlocationuser'],document=request.POST.get('document'),stckused=0,datemvt=request.POST.get('dt'))
        if t:
            if 'client' in request.POST:
                for i in t:
                    i.stckused=1
                    i.codeuser=request.user.id
                    i.utilisateur=request.user.username
                    i.destination=request.POST.get('client')
                    i.save()
            elif 'offre' in request.POST:
                for i in t:
                    i.stckused=1
                    i.codeuser = request.user.id
                    i.utilisateur = request.user.username
                    i.classe=request.POST.get('offre')
                    i.save()
            elif 'regula' in request.POST:
                for i in t:
                    i.location = "REGULA"
                    i.stckused = 1
                    i.classe = request.POST.get('nom')
                    i.save()
            else:
                for i in t:
                    i.stckused = 1
                    i.codeuser = request.user.id
                    i.utilisateur = request.user.username
                    i.save()
             # t.update(destionation=1)
            ##################Remote
            # try:
            #     call_command('synchronize')
            # except:
            #     pass
            ##################Remote
            return JsonResponse(
                {"msg": "Opération effectuée",
                 "id": "1"},
                safe=False)
        else:
            return JsonResponse(
                {"msg": "Opération non effectuée",
                 "id": "0"}),

    if request.user.is_superuser:
        context = {
            "mvts": Fmvts.objects.filter(ajustement='FACT', location=request.session.get('idlocationuser'),
                                         stckused=0).values('document', 'datemvt', 'imputation', 'ndatemvt', 'utilisateur',
                                                            'serveur').order_by('document', 'ndatemvt').annotate(
                somme=Sum(F('prix_achat') * F('qte_sortie'))).order_by('-ndatemvt')
        }
    else:

        context={
            "mvts":Fmvts.objects.filter(ajustement='FACT',location=request.session.get('idlocationuser'),stckused=0).values('document','datemvt','imputation','ndatemvt','utilisateur','serveur').order_by('document','ndatemvt').annotate(somme=Sum(F('prix_achat') * F('qte_sortie'))).order_by('-ndatemvt')
        }
    return render(request, 'pointvente/validation.html',context)

@login_required
@permission_required('pointvente.reimprimer',raise_exception=True)
def reimprimer(request):

    if request.method=="POST":
        para=Paramet.objects.all()
        if para:
            para=para.first()

        t = Fmvts.objects.filter(location_id=request.POST.get('idlocationuser'),document=request.POST.get('document'),datemvt=request.POST.get('dt'))
        if t:
            fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            input_file = os.path.join(fn, 'fac.jrxml')

            # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

            output = os.path.join(fn, 'media')

            con = {
                'driver': 'generic',
                'jdbc_driver': 'net.sourceforge.jtds.jdbc.Driver',
                'jdbc_url': f'jdbc:jtds:sqlserver://localhost/{settings.DATABASES["default"]["NAME"]}',
                'jdbc_dir': fn,
                'username': 'sa',
                'password': settings.DATABASES['default']['PASSWORD']
                # 'host': 'localhost',
                # 'database': 'STOCKCF',
                # 'port': '1433'
            }

            jasper = JasperPy()

            jasper.process(
                input_file,
                output,
                format_list=["pdf"],
                db_connection=con,
                parameters={'bon': request.POST.get('document')},
                locale='en_US'
            )

            return HttpResponse("true")
            # tbdata = []
            # tbdata.append(['Article', 'Qte', 'Pu', 'Total'])
            # tot = 0.0
            #
            # b = t.first()
            # numcmd =b.document
            #
            # codeb = b.requisition
            #
            # Titretyle = ParagraphStyle(
            #     name='titre',
            #     fontName='Helvetica-Bold',
            #     fontSize=8,
            #     textColor='DarkGray',
            #     borderPadding=(2, 2, 7, 2),
            #     borderWidth=0,
            #     alignment=TA_CENTER
            # )
            #
            # Headerstyle = ParagraphStyle(
            #     name='headesr',
            #     fontName='Helvetica-Bold',
            #     fontSize=8,
            #     # borderPadding=(2, 2, 7, 2),
            #     # borderWidth=0,
            #     # borderColor='Gray',
            #     alignment=TA_CENTER
            # )
            #
            # Headerstyle2 = ParagraphStyle(
            #     name='headesrd',
            #     fontName='Helvetica-Bold',
            #     fontSize=16,
            #     # borderPadding=(2, 2, 7, 2),
            #     # borderWidth=0,
            #     # borderColor='Gray',
            #     alignment=TA_CENTER
            # )
            #
            # styles = getSampleStyleSheet()
            # styleN = styles["BodyText"]
            # styleN.alignment = TA_LEFT
            # styleN.fontSize = 8
            #
            # styleNN = styles["BodyText"]
            # styleNN.alignment = TA_RIGHT
            # styleNN.fontSize = 8
            #
            # styleB = styles["Normal"]
            # styleB.alignment = TA_LEFT
            # styleB.fontSize = 8
            #
            # tremise = 0
            # tot =0
            #
            # elements = []
            #
            # for txx in t:
            #     txre = ((float(txx.qte_sortie) * float(txx.prix_vente)) * float(txx.remise)) / 100
            #     tbdata.append([
            #         Paragraph(f"{str(txx.article.designation).upper()}", styleB),
            #         Paragraph(f"{int(txx.qte_sortie)} {txx.emballage_id}", styleN),
            #         Paragraph("{:,.2f}".format((float(txx.prix_vente))), styleNN),
            #         Paragraph("{:,.2f}".format((float(txx.qte_sortie) * float(txx.prix_vente)) - txre), styleNN)
            #     ])
            #     tremise += txre
            #     tot += (float(txx.qte_sortie) * float(txx.prix_vente))
            # tot = tot - tremise
            #
            #
            #
            # header = Table([[Paragraph(
            #     f'{request.session["locationuser"]}<br/>{para.libelle}<br/>{para.adresse}<br/>{para.cdpostal}<br/>Tél:{para.telephone}',
            #     style=Headerstyle)]])
            #
            # elements.append(header)
            #
            # header = Table([[Paragraph(f'FACT:{numcmd}', style=Headerstyle2)]])
            # elements.append(header)
            # elements.append(Spacer(1, 5))
            #
            # header = Table([[Paragraph(
            #     f'Date: {b.datemvt}{b.bordereau}<br/><u>Client:{b.description} {b.imputation}</u>',
            #     style=Headerstyle)]])
            #
            # elements.append(header)
            # # Items
            #
            # table = Table(tbdata, colWidths=[2.3 * cm, 1.4 * cm, 1.8 * cm, 1.8 * cm])
            # table.setStyle([
            #     # ('FONT', (0, 0), (-1, -1), 'Helvetica'),
            #     ('FONTSIZE', (0, 0), (-1, -1), 8),
            #     # ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
            #     ('GRID', (0, 0), (-1, 0), 0, (0.7, 0.7, 0.7)),
            #     # ('GRID', (-2, -1), (-1, -1), 0, (0.7, 0.7, 0.7)),
            #     # ('ALIGN', (0, 0), (-3, -3), 'LEFT'),
            #     ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            #     # ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
            # ])
            # elements.append(table)
            #
            # header = Table([[Paragraph("--------------------------------", style=styleNN)]])
            # elements.append(header)
            #
            # if tremise != 0:
            #     header = Table([[Paragraph("Total CDF {:,.2f}".format(tot + tremise), style=styleNN)]])
            #     elements.append(header)
            #
            #     header = Table([[Paragraph("Remise CDF {:,.2f}".format(tremise), style=styleNN)]])
            #     elements.append(header)
            #
            #     header = Table([[Paragraph("Total Gen. CDF {:,.2f}".format(tot), style=styleNN)]])
            #     elements.append(header)
            # else:
            #     header = Table([[Paragraph("Total CDF {:,.2f}".format(tot), style=styleNN)]])
            #     elements.append(header)
            #
            # header = Table([[Paragraph("--------------------------------", style=styleNN)]])
            # elements.append(header)
            #
            # header = Table([[Paragraph(f"Facture etablie par {b.destination}", style=styleNN)]])
            # elements.append(header)
            #
            # header = Table([[Paragraph(
            #     "Merci de votre visite. A la prochaine.<br/>Les marchandises vendues ne sont ni Reprises ni echangees",
            #     style=Headerstyle)]])
            # elements.append(header)
            #
            # barcode = code39.Extended39(codeb, barWidth=0.01 * inch, barHeight=.5 * inch)
            # elements.append(barcode)
            #
            # # elements.append(Spacer(1, 40))
            #
            # pagesize = (7.1967 * cm, 29.6686 * cm)
            #
            # # fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            # # output_file = os.path.join(fn, 'fac.pdf')
            # doc = SimpleDocTemplate(os.path.join(settings.MEDIA_ROOT, f'fac{b.codeuser_id}.pdf'), pagesize=pagesize,
            #                         rightMargin=1, leftMargin=1,
            #                         topMargin=1, bottomMargin=1, )
            # # doc.build(elements,onFirstPage=drawPageFrame)
            # doc.multiBuild(elements)
            #
            # return JsonResponse(
            #     {"msg": "Opération effectuée",
            #      "id": "1","utilisateur":str(b.codeuser_id)},
            #     safe=False)
        else:
            return JsonResponse(
                {"msg": "Opération non effectuée",
                 "id": "0"}),

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        rec=Fmvts.objects.filter(ajustement='FACT',location_id=request.GET.get('idlocationuser'),ndatemvt__lte=str(request.GET.get('db1')).replace("-",""),ndatemvt__gte=str(request.GET.get('db2')).replace("-","")).values('document','datemvt','description','ndatemvt').order_by('document','ndatemvt').annotate(somme=Sum(F('prix_vente') * F('qte_sortie'))).order_by('-ndatemvt')
        return JsonResponse({"data": list(rec)},safe=False)

    context={
        # "mvts":Fmvts.objects.filter(ajustement='FACT',location=request.session.get('idlocationuser'),ndatemvt=str(datetime.date.today()).replace("-","")).values('document','datemvt','ndatemvt').order_by('document','ndatemvt').annotate(somme=Sum(F('prix_achat') * F('qte_sortie'))).order_by('-ndatemvt')[:1000],
        "location":Flocation.objects.all()
    }
    return render(request, 'pointvente/reimprimer.html',context)

@login_required
@permission_required('pointvente.annulation',raise_exception=True)
def annulation(request):

    if request.method=="POST":
        t = Fmvts.objects.filter(location_id=request.POST.get('idlocationuser'),document=request.POST.get('document'),datemvt=request.POST.get('dt'))
        if t:
            for i in t:
                i.ajustement='SUP'
                i.save()
            return JsonResponse(
                {"msg": "Opération effectuée",
                 "id": "1"},
                safe=False)
        else:
            return JsonResponse(
                {"msg": "Opération non effectuée",
                 "id": "0"}),

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        rec=Fmvts.objects.filter(ajustement='FACT',location_id=request.GET.get('idlocationuser'),ndatemvt__lte=str(request.GET.get('db1')).replace("-",""),ndatemvt__gte=str(request.GET.get('db2')).replace("-","")).values('document','datemvt','description','ndatemvt').order_by('document','ndatemvt').annotate(somme=Sum(F('prix_vente') * F('qte_sortie'))).order_by('-ndatemvt')
        return JsonResponse({"data": list(rec)},safe=False)
    context={
        "location": Flocation.objects.all()
        # "mvts":Fmvts.objects.filter(ajustement='FACT',location=request.session.get('idlocationuser'),ndatemvt=str(datetime.date.today()).replace("-","")).values('document','datemvt','ndatemvt').order_by('document','ndatemvt').annotate(somme=Sum(F('prix_achat') * F('qte_sortie'))).order_by('-ndatemvt')
    }
    return render(request, 'pointvente/annulation.html',context)


@login_required
@permission_required('pointvente.transferttable',raise_exception=True)
def transferttable(request):

    if request.method=="POST":

        if request.POST.get('table1')!=request.POST.get('table2'):
            t=Tattente.objects.filter(location=request.session.get('idlocationuser'),facture=request.POST.get('table2'))
            if t:
                t=t.first()
                Tattente.objects.filter(location=request.session.get('idlocationuser'),
                                        facture=request.POST.get('table1')).update(
                    facture=t.facture,
                    table_id=t.table_id,
                    serveur_id=t.serveur_id
                )
                return JsonResponse(
                    {"msg": "Opération effectuée",
                     "id": "1"},
                    safe=False)
            else:
                return JsonResponse(
                    {"msg": "Opération non effectuée",
                     "id": "0"})

        else:
            return JsonResponse(
                {"msg": "Opération non effectuée.Les Tables sont egaux.",
                 "id": "0"})
    context={
        "mvts": Tattente.objects.filter(location=request.session.get('idlocationuser'),indsuspect=request.user.id).values('facture','datemvt','table__numero').order_by('facture','datemvt','table__numero').annotate(somme=Sum(F('puht') * F('qte'))).order_by('facture')
        # "mvts":Fmvts.objects.filter(ajustement='FACT',location=request.session.get('idlocationuser'),ndatemvt=str(datetime.date.today()).replace("-","")).values('document','datemvt','ndatemvt').order_by('document','ndatemvt').annotate(somme=Sum(F('prix_achat') * F('qte_sortie'))).order_by('-ndatemvt')
    }
    return render(request, 'pointvente/transferttable.html',context)


@login_required
@permission_required('pointvente.transfertserveur',raise_exception=True)
def transfertserveur(request):

    if request.method=="POST":

        if request.POST.get('serveur1')!=request.POST.get('serveur2'):

            Tattente.objects.filter(location=request.session.get('idlocationuser'),
                                    serveur_id=request.POST.get('serveur1')).update(
                serveur_id=request.POST.get('serveur2')
            )
            return JsonResponse(
                {"msg": "Opération effectuée",
                 "id": "1"},
                safe=False)

        else:
            return JsonResponse(
                {"msg": "Opération non effectuée.Les serveurs sont egaux.",
                 "id": "0"})
    context={
        "mvts": Serveur.objects.filter(etat=True)

    }
    return render(request, 'pointvente/transfertserveur.html',context)


def getnumeroauto(request,nom):
    ##################################################
    numero = ''
    t = Fmvts.objects.filter(location=request.session['idlocationuser'], ajustement__in=('FACT', 'SUP'),
                             codeuser=request.POST.get('user2'),
                             ndatemvt=str(request.session['sesio']).replace("-", "").replace("/",
                                                                                          "")).order_by(
        '-mvt')
    if t:

        tabnumero = []
        for tempo in t:
            xar = int(''.join(filter(str.isdigit, tempo.document)))
            if xar not in tabnumero:
                tabnumero.append(xar)
        tabnumero.sort()
        doc = str(nom)[0].upper() + str(tabnumero[-1] + 1)

        attentf = Tattente.objects.filter(facture=doc, location=request.session['idlocationuser'],
                                          indsuspect=request.POST.get('user2'),
                                          datemvt=request.session['sesio']).order_by('-id')
        if attentf:
            tx = Tattente.objects.filter(location=request.session['idlocationuser'],
                                         indsuspect=request.POST.get('user2'),
                                         datemvt=request.session['sesio']).order_by('-id')
            if tx:
                tabnumero = []
                for tempo in tx:
                    xar = int(''.join(filter(str.isdigit, tempo.facture)))
                    if xar not in tabnumero:
                        tabnumero.append(xar)
                tabnumero.sort()
                numero = str(nom)[0].upper() + str(int(tabnumero[-1]) + 1)

        else:
            numero = str(nom)[0].upper() + str(int(tabnumero[-1]) + 1)
    else:
        tx = Tattente.objects.filter(location=request.session['idlocationuser'],
                                     indsuspect=request.POST.get('user2'),
                                     datemvt=request.session['sesio']).order_by('-id')
        if tx:
            tabnumero = []
            for tempo in tx:
                xar = int(''.join(filter(str.isdigit, tempo.facture)))
                if xar not in tabnumero:
                    tabnumero.append(xar)
            tabnumero.sort()
            numero = str(nom)[0].upper() + str(int(tabnumero[-1]) + 1)
        else:
            numero = str(nom)[0].upper() + str(1)

    ##################################################
    return numero


@login_required
@permission_required('pointvente.transfertproduit',raise_exception=True)
def transfertproduit(request):

    if request.method=="POST":
        tx=Tattente.objects.filter(location=request.session.get('idlocationuser'),facture=request.POST.get('facture'),article=request.POST.get('article')).delete()
        return JsonResponse(
            {"msg": "Opération effectuée",
             "id": "1"},
            safe=False)

    if 'facture' in request.GET:
        t=Tattente.objects.filter(location=request.session.get('idlocationuser'),facture=request.GET.get('facture')).values('article','designation')

        return JsonResponse({"data": list(t)},safe=False)
    context={
        "tables": Tattente.objects.filter(location=request.session.get('idlocationuser')).values('facture').order_by('facture').annotate(somme=Sum('puht')).order_by('facture'),
            }
    return render(request, 'pointvente/transfertproduit.html',context)

@login_required
@permission_required('pointvente.transfertcompte',raise_exception=True)
def transfertcompte(request):

    if request.method=="POST":

        if request.POST.get('user1')!=request.POST.get('user2'):


            numero=getnumeroauto(request,request.POST.get('user2nom'))

            numerotempo=''
            tx=Tattente.objects.filter(location=request.session.get('idlocationuser'), indsuspect=request.POST.get('user1')).order_by('id')
            for ix in tx:
                if numerotempo!=ix.facture:
                    numerotempo=ix.facture
                    Tattente.objects.filter(location=request.session.get('idlocationuser'),
                                            indsuspect=request.POST.get('user1'),facture=numerotempo).update(
                        facture=numero,
                        indsuspect=request.POST.get('user2')
                    )
                    numero = getnumeroauto(request, request.POST.get('user2nom'))

            tx_ = Fmvts.objects.filter(location=request.session.get('idlocationuser'),ajustement='FACT',stckused=0,codeuser=request.POST.get('user1')).order_by('mvt')

            for ix in tx_:
                ix.codeuser=request.POST.get('user2')
                ix.utilisateur=request.POST.get('user2nom')
                ix.save()

            return JsonResponse(
                {"msg": "Opération effectuée",
                 "id": "1"},
                safe=False)

        else:
            return JsonResponse(
                {"msg": "Opération non effectuée.Les Caissiers sont egaux.",
                "id": "0"})

    m=Tattente.objects.filter(location=request.session.get('idlocationuser')).values('indsuspect').order_by('indsuspect').annotate(somme=Sum(F('puht') * F('qte'))).order_by('indsuspect')
    m_=Fmvts.objects.filter(location=request.session.get('idlocationuser'),ajustement='FACT',stckused=0).values('codeuser').order_by('codeuser').annotate(somme=Sum(F('qte_sortie') * F('prix_achat'))).order_by('codeuser')

    context={
        "users": User.objects.filter(Q(id__in=m.values_list('indsuspect'))|Q(id__in=m_.values_list('codeuser'))),
        "users_": User.objects.all()
            }
    return render(request, 'pointvente/transfertcompte.html',context)

@login_required
def synthesepointvente(request):

    if request.method=="POST":


        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        #print(request.POST)
        #input_file = os.path.join(fn,'rapsynthese.jrxml')
        if 'pro' in request.POST:
        	input_file= os.path.join(fn,'rapsynthesepro.jrxml')
        elif 'totaux' in request.POST:
        	input_file= os.path.join(fn,'raptotaux.jrxml')
        else:
            input_file=os.path.join(fn,'rapsynthese.jrxml')

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output =os.path.join(fn,'media')
        #print(input_file)


        con = {
            'driver': 'generic',
            'jdbc_driver':'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url':f'jdbc:jtds:sqlserver://localhost/{settings.DATABASES["default"]["NAME"]}',
            'jdbc_dir':fn,
            'username': 'sa',
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKCF',
            # 'port': '1433'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml')
        # jasper.path_executable = "D:/JasperStarter/bin/"



        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters={'liblocation': '{}'.format(request.POST.get('locationuser')),'idlocation': '{}'.format(request.POST.get('idlocationuser')),'d1': '{}'.format(request.POST.get('dtd')),'d2': '{}'.format(request.POST.get('dtf')),'datedb': '{}'.format(str(request.POST['dtd']).replace("-","")),'datefn':'{}'.format(str(request.POST['dtf']).replace("-",""))},
            locale='en_US'
        )


        return HttpResponse("true")

    context = {"location": Flocation.objects.all().order_by('designation'), }
    return render(request, 'pointvente/rapventesynthese.html',context)


@login_required
def profit(request):

    if request.method=="POST":


        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        #print(request.POST)
        #input_file = os.path.join(fn,'rapsynthese.jrxml')
        input_file= os.path.join(fn,'rapprofit.jrxml')


        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output =os.path.join(fn,'media')
        #print(input_file)


        con = {
            'driver': 'generic',
            'jdbc_driver':'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url':f'jdbc:jtds:sqlserver://localhost/{settings.DATABASES["default"]["NAME"]}',
            'jdbc_dir':fn,
            'username': 'sa',
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKCF',
            # 'port': '1433'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml')
        # jasper.path_executable = "D:/JasperStarter/bin/"



        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters={'liblocation': '{}'.format(request.POST.get('locationuser')),'idlocation': '{}'.format(request.POST.get('idlocationuser')),'d1': '{}'.format(request.POST.get('dtd')),'d2': '{}'.format(request.POST.get('dtf')),'datedb': '{}'.format(str(request.POST['dtd']).replace("-","")),'datefn':'{}'.format(str(request.POST['dtf']).replace("-",""))},
            locale='en_US'
        )


        return HttpResponse("true")

    context = {"location": Flocation.objects.all().order_by('designation'), }
    return render(request, 'pointvente/profit.html',context)

@login_required
def pointventeliste(request):

    if request.method=="POST":


        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = os.path.join(fn,'rapcapliste.jrxml')

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output =os.path.join(fn,'media')

        con = {
            'driver': 'generic',
            'jdbc_driver':'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url':f'jdbc:jtds:sqlserver://localhost/{settings.DATABASES["default"]["NAME"]}',
            'jdbc_dir':fn,
            'username': 'sa',
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKCF',
            # 'port': '1433'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml')
        # jasper.path_executable = "D:/JasperStarter/bin/"



        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters={'liblocation': '{}'.format(request.session.get('locationuser')),'idlocation': '{}'.format(request.POST.get('location')),'d1': '{}'.format(request.POST.get('dtd')),'d2': '{}'.format(request.POST.get('dtf')),'datedb': '{}'.format(str(request.POST['dtd']).replace("-","")),'datefn':'{}'.format(str(request.POST['dtf']).replace("-",""))},
            locale='en_US'
        )


        return HttpResponse("true")

    context = {"location": Flocation.objects.all().order_by('designation'),}
    return render(request, 'pointvente/rapventeliste.html',context)

@login_required
def liste(request):

    if request.method=="POST":

        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = os.path.join(fn,'liste.jrxml')

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output =os.path.join(fn,'media')

        con = {
            'driver': 'generic',
            'jdbc_driver':'net.sourceforge.jtds.jdbc.Driver',
            'jdbc_url':f'jdbc:jtds:sqlserver://localhost/{settings.DATABASES["default"]["NAME"]}',
            'jdbc_dir':fn,
            'username': 'sa',
            'password': settings.DATABASES['default']['PASSWORD']
            # 'host': 'localhost',
            # 'database': 'STOCKCF',
            # 'port': '1433'
        }

        jasper = JasperPy()
        # jasper.compile("D:/test1.jrxml')
        # jasper.path_executable = "D:/JasperStarter/bin/"



        jasper.process(
            input_file,
            output,
            format_list=["pdf"],
            db_connection=con,
            parameters={'liblocation': '{}'.format(request.session.get('locationuser')),'idlocation': '{}'.format(request.session.get('idlocationuser')),'utilisateur': '{}'.format(request.user.id),'nom': '{}'.format(request.user.username)},
            locale='en_US'
        )


        return HttpResponse("true")

    context = {"location": Flocation.objects.all().order_by('designation'),}
    return render(request, 'pointvente/liste.html',context)





