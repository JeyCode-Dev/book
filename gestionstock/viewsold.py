from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,permission_required
from django.db.models import Sum, F, Value, Count
from django.db.models.functions import Concat
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.db import IntegrityError, transaction
from datetime import datetime
import os

# Create your views here.
from django.urls import reverse
from django.views.decorators.http import require_POST


# from reportlab.lib.pagesizes import landscape, letter
# from reportlab.lib import colors
# from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.units import inch, cm
# from reportlab.platypus import SimpleDocTemplate, Image as img, Spacer, Paragraph, Table, TableStyle

from .models import *

from pyreportjasper import JasperPy

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
                famille_id=2,
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
                periode='2020-12',
                location_id=location,
                article_id=cmp,
                emballage_e='UNIT',
                emballage_u='UNIT',
                quantitee=physique,
                quantiteu=physique,
                qte_u_phys=physique,
                qte_u_log=0,
                qte_u_ecart=float(physique)-float(0),
                dateinventaire=datetime.today().date(),
                ndateinvent=str(datetime.today().date()).replace("-","").replace("/",""),
            )
            #----------------------mouvement
            Fmvts.objects.create(
                location_id=location,
                periode='2020-12',
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

def getstockproduit(location,produit,emballage):
    # ----------------------------------
    art = Farticle.objects.filter(article=produit, emballagee_id=emballage)
    art2 = Farticle.objects.filter(article=produit, emballageu_id=emballage)
    if art:
        b = Fmvts.objects.filter(location_id=location, article_id=produit,
                                 ajustement_id__in=("ACH", "PAT", "TRFR", "INV")).aggregate(Sum("qte_entree")).get("qte_entree__sum")
        if b is None:  # entrer
            b = 0
        c = Fmvts.objects.filter(location_id=location, article_id=produit,
                                 ajustement_id__in=("VTE", "TRTO", "FACT", "DECL", "INV")).aggregate(Sum("qte_sortie")).get("qte_sortie__sum")
        if c is None:  # sortie
            c = 0

        tot = b - c
        return tot
    elif art2:
        b = Fmvts.objects.filter(location_id=location, article_id=produit,
                                 # ajustement_id__in=("ACH", "PAT", "TRFR", "INV")).aggregate(Sum("qteunit_entree")).get(
                                 ajustement_id__in=("ACH", "PAT", "TRFR", "INV")).aggregate(Sum("qteunit_entree")).get(
            "qteunit_entree__sum")
        if b is None:  # entrer
            b = 0
        c = Fmvts.objects.filter(location_id=location, article_id=produit,
                                 ajustement_id__in=("VTE", "TRTO", "FACT", "DECL", "INV")).aggregate(
            Sum("qteunit_sortie")).get("qteunit_sortie__sum")
        if c is None:  # sortie
            c = 0

        tot = b - c
        return tot


def colr(x,y,z):
    return (x/255,y/255,z/255)

def home(request):

    context={
        "totproduit":Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser')).count(),
        "totclientnon":Ftiers.objects.filter(typetiers="2").count(),
        "totclientoui":Ftiers.objects.filter(typetiers="1").count(),
        "totcmd":Fcommande.objects.filter(etatcde="0",location_id=request.session.get('idlocationuser')).count(),
        "totprix":TempoPrix.objects.filter(etat=0).count(),
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

        veri=LocationUser.objects.filter(user=user,location_id=request.POST.get('location'))
        if veri:
            # veri=veri.first().location.designation
            request.session['locationuser']=veri.first().location.designation
            request.session['idlocationuser']=veri.first().location.location
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
#             'jdbc_driver':'com.microsoft.sqlserver.jdbc.SQLServerDriver',
#             'jdbc_url':'jdbc:sqlserver://localhost:1433;databaseName=STOCKCFDB',
#             'jdbc_dir':fn,
#             'username': 'sa',
#             'password': 'dev12345'
#             # 'host': 'localhost',
#             # 'database': 'STOCKCFDB',
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
#             'jdbc_driver':'com.microsoft.sqlserver.jdbc.SQLServerDriver',
#             'jdbc_url':'jdbc:sqlserver://localhost:1433;databaseName=STOCKCFDB',
#             'jdbc_dir':fn,
#             'username': 'sa',
#             'password': 'dev12345'
#             # 'host': 'localhost',
#             # 'database': 'STOCKCFDB',
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
#             'jdbc_driver':'com.microsoft.sqlserver.jdbc.SQLServerDriver',
#             'jdbc_url':'jdbc:sqlserver://localhost:1433;databaseName=STOCKCFDB',
#             'jdbc_dir':fn,
#             'username': 'sa',
#             'password': 'dev12345'
#             # 'host': 'localhost',
#             # 'database': 'STOCKCFDB',
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

    context = {
  "classe": Fclasse.objects.all().order_by('designation'),
  "famille": Ffamilles.objects.all().order_by('designation'),
  "emballage": Femballage.objects.all().order_by('designation'),
             }

    if request.method == "POST":
  
        try:
            with transaction.atomic():
                art=Farticle.objects.filter(article=request.POST.get('idpro'),LOCATION_id=request.session.get('idlocationuser'))

                if art:
                    art.update(
                        famille_id=request.POST.get('famille'),
                        classe_id=request.POST.get('classe'),
                        numcompte=request.POST.get('numcpt'),
                        categorie=request.POST.get('taxe'),

                        qte_stock_minimal=request.POST.get('seuil'),
                        quantitee=request.POST.get('qte'),
                        quantiteu=request.POST.get('qte1'),
                        designation=request.POST.get('designation'),
                        emballagee_id=request.POST.get('emballage1'),
                        emballageu_id=request.POST.get('emballage2')
                    )
                else:                        
                    # recnumart = Farticle.objects.all().order_by('-article')[:1]
                    recnumart = Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser'))
                    if recnumart:
                        # recnumart = recnumart.first().article
                        recnumart = recnumart.count()
                        # recnumart = int(''.join(filter(str.isdigit, recnumart)))
                    else:

                        recnumart = 0
                    recnumart = str(request.session.get('idlocationuser'))+str(recnumart + 1)
                    Farticle.objects.create(
                        article=recnumart,
                        famille_id=request.POST.get('famille'),
                        classe_id=request.POST.get('classe'),
                        numcompte=request.POST.get('numcpt'),
                        categorie=request.POST.get('taxe'),
                        qte_stock_minimal=request.POST.get('seuil'),
                        quantitee=request.POST.get('qte'),
                        quantiteu=request.POST.get('qte1'),
                        prix_vente=0,
                        designation=request.POST.get('designation'),
                        emballagee_id=request.POST.get('emballage1'),
                        emballageu_id=request.POST.get('emballage2')
                    ,LOCATION_id=request.session.get('idlocationuser')
                    )

                return JsonResponse(
                    {"msg": "Opération effectuée",
                    "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée "+str(e), "id": "0"}, safe=False)
    return render(request, 'gestionstock/produit.html', context)

@login_required
def fichiers(request):

    if request.method == "POST":
        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if request.POST.get('code')=="1":
            input_file = fn+"\{}".format("emballage.jrxml")
        elif request.POST.get('code')=="2":
            input_file = fn+"\{}".format("classe.jrxml")
        elif request.POST.get('code')=="3":
            input_file = fn+"\{}".format("famille.jrxml")
        elif request.POST.get('code')=="4":
            input_file = fn+"\{}".format("magasin.jrxml")
        elif request.POST.get('code')=="5":
            input_file = fn+"\{}".format("articles.jrxml")
            


        

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")
    
        output =fn+"\media"
        
        con = {
            'driver': 'generic',
            'jdbc_driver':'com.microsoft.sqlserver.jdbc.SQLServerDriver',
            'jdbc_url':'jdbc:sqlserver://localhost;databaseName=STOCK',
            'jdbc_dir':fn,
            'username': 'sa',
            'password': 'dev12345'
            # 'host': 'localhost',
            # 'database': 'STOCKCFDB',
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
            parameters={'liblocation':request.session.get('liblocation')},
            locale='en_US'
            )
        elif request.POST.get('code')=="5":
            jasper.process(
                input_file,
                output,
                format_list=["pdf"],
                db_connection=con,
                parameters={'liblocation':request.session.get('liblocation'),'idlocation':request.session.get('idlocationuser')},
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
        input_file = fn + "\{}".format("boncommande.jrxml")
        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = fn + "\media"

        con = {
            'driver': 'generic',
            'jdbc_driver': 'com.microsoft.sqlserver.jdbc.SQLServerDriver',
            'jdbc_url': 'jdbc:sqlserver://localhost;databaseName=STOCK',
            'jdbc_dir': fn,
            'username': 'sa',
            'password': 'dev12345'
            # 'host': 'localhost',
            # 'database': 'STOCKCFDB',
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
                                              i.emballageu_id)
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

    context = {
  "article": Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser')).order_by('designation'),
  "periode": DelaiInventaire.objects.filter(location_id=request.session.get('idlocationuser'),).order_by('-periode'),
             }

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
                                               article_id=request.POST.get('produit'))
                if one:
                    qte = getstockproduit(request.session.get('idlocationuser'), request.POST.get('produit'),
                                          request.POST.get('emballage2'))

                    one.update(

                        emballage_e=request.POST.get('emballage1'),
                        emballage_u=request.POST.get('emballage2'),
                        quantitee=request.POST.get('qte1'),
                        quantiteu=request.POST.get('qte2'),
                        qte_u_phys=request.POST.get('qte2'),
                        qte_u_log=qte,
                        qte_u_ecart=float(request.POST.get('qte2')) - float(qte),
                        dateinventaire=request.POST.get('dateop'),
                        ndateinvent=str(request.POST.get('dateop')).replace("-", "").replace("/", ""),
                    )
                else:
                    qte=getstockproduit(request.session.get('idlocationuser'),request.POST.get('produit'),request.POST.get('emballage2'))
                    Finventaire.objects.create(
                        periode=request.POST.get('periode'),
                        location_id=request.session.get('idlocationuser'),
                        article_id=request.POST.get('produit'),
                        emballage_e=request.POST.get('emballage1'),
                        emballage_u=request.POST.get('emballage2'),
                        quantitee=request.POST.get('qte1'),
                        quantiteu=request.POST.get('qte2'),
                        qte_u_phys=request.POST.get('qte2'),
                        qte_u_log=qte,
                        qte_u_ecart=float(request.POST.get('qte2'))-float(qte),
                        dateinventaire=request.POST.get('dateop'),
                        ndateinvent=str(request.POST.get('dateop')).replace("-","").replace("/",""),
                    )

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
    return render(request, 'gestionstock/saisirphysique.html', context)

@login_required
@permission_required('gestionstock.Rap_Prise_Inventaire',raise_exception=True)
def rapportlistepriseinventaire(request):
    if request.method == "POST":

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
        input_file = fn + "\{}".format("priselisteinventaire.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = fn + "\media"

        con = {
            'driver': 'generic',
            'jdbc_driver': 'com.microsoft.sqlserver.jdbc.SQLServerDriver',
            'jdbc_url': 'jdbc:sqlserver://localhost;databaseName=STOCK',
            'jdbc_dir': fn,
            'username': 'sa',
            'password': 'dev12345'
            # 'host': 'localhost',
            # 'database': 'STOCKCFDB',
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
        input_file = fn + "\{}".format("inventaire.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = fn + "\media"

        con = {
            'driver': 'generic',
            'jdbc_driver': 'com.microsoft.sqlserver.jdbc.SQLServerDriver',
            'jdbc_url': 'jdbc:sqlserver://localhost;databaseName=STOCK',
            'jdbc_dir': fn,
            'username': 'sa',
            'password': 'dev12345'
            # 'host': 'localhost',
            # 'database': 'STOCKCFDB',
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
        input_file = fn + "\{}".format("rapmvtproduit.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = fn + "\media"

        con = {
            'driver': 'generic',
            'jdbc_driver': 'com.microsoft.sqlserver.jdbc.SQLServerDriver',
            'jdbc_url': 'jdbc:sqlserver://localhost;databaseName=STOCK',
            'jdbc_dir': fn,
            'username': 'sa',
            'password': 'dev12345'
            # 'host': 'localhost',
            # 'database': 'STOCKCFDB',
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
            parameters={'libdate2': request.POST.get('date2'),'iddate2': str(request.POST.get('date2')).replace("/","").replace("-",""),'libdate1': request.POST.get('date1'),'iddate1': str(request.POST.get('date1')).replace("/","").replace("-",""),'liblocation': request.session.get('locationuser'),'produit':request.POST.get('produit'),'idlocation':request.session.get('idlocationuser')},
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



        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if 'id' in request.POST:
            input_file = fn + "\{}".format("logiquephysiquefull.jrxml")
        else:
            input_file = fn + "\{}".format("logiquephysique.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = fn + "\media"

        con = {
            'driver': 'generic',
            'jdbc_driver': 'com.microsoft.sqlserver.jdbc.SQLServerDriver',
            'jdbc_url': 'jdbc:sqlserver://localhost;databaseName=STOCK',
            'jdbc_dir': fn,
            'username': 'sa',
            'password': 'dev12345'
            # 'host': 'localhost',
            # 'database': 'STOCKCFDB',
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
            parameters={'liblocation': request.session.get('locationuser'),'periode':request.POST.get('periode'),'idlocation':request.session.get('idlocationuser')},
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
        input_file = fn + "\{}".format("theoriqueval.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = fn + "\media"

        con = {
            'driver': 'generic',
            'jdbc_driver': 'com.microsoft.sqlserver.jdbc.SQLServerDriver',
            'jdbc_url': 'jdbc:sqlserver://localhost;databaseName=STOCK',
            'jdbc_dir': fn,
            'username': 'sa',
            'password': 'dev12345'
            # 'host': 'localhost',
            # 'database': 'STOCKCFDB',
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
        input_file = fn + "\{}".format("theorique.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = fn + "\media"

        con = {
            'driver': 'generic',
            'jdbc_driver': 'com.microsoft.sqlserver.jdbc.SQLServerDriver',
            'jdbc_url': 'jdbc:sqlserver://localhost;databaseName=STOCK',
            'jdbc_dir': fn,
            'username': 'sa',
            'password': 'dev12345'
            # 'host': 'localhost',
            # 'database': 'STOCKCFDB',
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
                art=Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser'))
                for i in art:
                    pero=Finventaire.objects.filter(periode=request.POST.get('periode'),location_id=request.session.get('idlocationuser'))
                    finn=Finventaire.objects.filter(article=i,periode=request.POST.get('periode'),location_id=request.session.get('idlocationuser'))
                    if finn:
                        pass
                    else:
                        qte=getstockproduit(request.session.get('idlocationuser'),i.article,i.emballageu_id)
                        Finventaire.objects.create(
                            periode=request.POST.get('periode'),
                            location_id=request.session.get('idlocationuser'),
                            article=i,
                            emballage_e=i.emballagee_id,
                            emballage_u=i.emballageu_id,
                            quantitee=qte,
                            quantiteu=qte,
                            qte_u_phys=float(0),
                            qte_u_log=qte,
                            qte_u_ecart=float(0)-float(qte),
                            dateinventaire=pero.first().dateinventaire,
                            ndateinvent=pero.first().ndateinvent,
                        )


                    finvv=Finventaire.objects.filter(article=i,periode=request.POST.get('periode'),location_id=request.session.get('idlocationuser'))
                    if finvv:
                        finvv=finvv.first()
                        tempo1 = Fmvts.objects.filter(ndatemvt=finvv.ndateinvent,
                                                      location_id=request.session.get('idlocationuser'),
                                                      article=i,
                                                      ajustement_id="INV", periode=request.POST.get('periode'))

                        resultat1 = 0
                        resultat2 = 0
                        prix = 0
                        art = Farticle.objects.filter(article=i.article,emballagee_id=finvv.emballage_e)
                        art2 = Farticle.objects.filter(article=i.article,emballageu_id=finvv.emballage_u)
                        if art:
                            resultat1 = finvv.qte_u_ecart
                            prix = art.first().pa
                            resultat2 = float(finvv.qte_u_ecart) * art.first().quantitee
                        elif art2:
                            resultat2 = finvv.qte_u_ecart
                            prix = art2.first().pa
                            resultat1 = float(finvv.qte_u_ecart) / art2.first().quantitee


                        if finvv.qte_u_ecart>=0:

                            if tempo1:
                                tempo1.update(
                                    # requisition=i.serielivraison.serielivraison,

                                    # tiers_id=i.serielivraison.commande.tiers.tiers,

                                    # quantite=i.qte_u_ecart,
                                    qte_entree=resultat1,
                                    qteunit_entree=resultat2,
                                    prix_achat=0,
                                    prix_vente=0,
                                    # devise="",
                                    # txchange="",
                                    codeuser_id=request.user.id,
                                )
                            else:
                                Fmvts.objects.create(
                                location_id=request.session.get('idlocationuser'),
                                    periode=finvv.periode,
                                datemvt=finvv.dateinventaire,
                                ndatemvt=str(finvv.dateinventaire).replace("-", "").replace("/", ""),
                                # requisition=i.serielivraison.serielivraison,
                                document="INV" + str(finvv.compteur),
                                ajustement_id="INV",
                                # tiers_id=i.serielivraison.commande.tiers.tiers,
                                article=i,
                                emballage_id=i.emballageu.emballage,
                                    qte_entree=resultat1,
                                    qteunit_entree=resultat2,
                                prix_achat=0,
                                prix_vente=0,
                                # devise="",
                                # txchange="",
                                codeuser_id=request.user.id,
                            )
                        elif finvv.qte_u_ecart < 0:
                            if tempo1:
                                tempo1.update(
                                # quantite=(i.qte_u_ecart),
                                qte_sortie=(resultat1)*(-1),
                                    qteunit_sortie=resultat2*(-1),
                                prix_achat=0,
                                prix_vente=0,
                                # devise="",
                                # txchange="",
                                codeuser_id=request.user.id,
                            )
                            else:
                                Fmvts.objects.create(
                                    location_id=request.session.get('idlocationuser'),
                                    # periode=p,
                                    periode=finvv.periode,
                                    datemvt=finvv.dateinventaire,
                                    ndatemvt=str(finvv.dateinventaire).replace("-", "").replace("/", ""),
                                    # requisition=i.serielivraison.serielivraison,
                                    document="INV" + str(finvv.compteur),
                                    ajustement_id="INV",
                                    # tiers_id=i.serielivraison.commande.tiers.tiers,
                                    article=i,
                                    emballage_id=i.emballageu.emballage,
                                    # quantite=(i.qte_u_ecart),
                                    qte_sortie=(resultat1)*(-1),
                                    qteunit_sortie=resultat2*(-1),
                                    prix_achat=0,
                                    prix_vente=0,
                                    # devise="",
                                    # txchange="",
                                    codeuser_id=request.user.id,
                                )
                        finvv.prix_vente_u=prix
                        finvv.save()

                    # else:
                    #     qte=getstockproduit(request.session.get('idlocationuser'),i.article,i.emballageu_id)
                    #     Finventaire.objects.create(
                    #             periode=request.POST.get('periode'),
                    #             location_id=request.session.get('idlocationuser'),
                    #             article=i,
                    #             emballage_e=i.emballagee_id,
                    #             emballage_u=i.emballageu_id,
                    #             quantitee=qte,
                    #             quantiteu=qte,
                    #             qte_u_phys=float(0),
                    #             qte_u_log=qte,
                    #             qte_u_ecart=float(0)-float(qte),
                    #             dateinventaire=request.POST.get('dateop'),
                    #             ndateinvent=str(request.POST.get('dateop')).replace("-","").replace("/",""),
                    #         )


                #somme inventaire
                #Foo.objects.extra(where=["i1 + i2 + i3 > 200"])
                sommefood=Finventaire.objects.filter(periode=request.POST.get('periode'),location_id=request.session.get('idlocationuser'),article__famille_id=1).annotate(total=F('qte_u_phys') * F('prix_vente_u')).aggregate(Sum('total')).get('total__sum')
                sommelessi=Finventaire.objects.filter(periode=request.POST.get('periode'),location_id=request.session.get('idlocationuser'),article__famille_id=2).annotate(total=F('qte_u_phys') * F('prix_vente_u')).aggregate(Sum('total')).get('total__sum')

                if sommefood is None:
                    sommefood=0

                if sommelessi is None:
                    sommelessi=0

                som=SommeInventaire.objects.filter(periode=request.POST.get('periode'),location_id=request.session.get('idlocationuser'))
                if som:
                    v=som.filter(famille_id=1)
                    if v:
                        v.update(somme=sommefood,famille_id=1,periode=request.POST.get('periode'),location_id=request.session.get('idlocationuser'))

                    b=som.filter(famille_id=2)
                    if b:
                        b.update(somme=sommelessi,famille_id=2,periode=request.POST.get('periode'),location_id=request.session.get('idlocationuser'))

                else:
                    SommeInventaire.objects.create(somme=sommefood,famille_id=1,periode=request.POST.get('periode'),location_id=request.session.get('idlocationuser'))
                    SommeInventaire.objects.create(somme=sommelessi,famille_id=2,periode=request.POST.get('periode'),location_id=request.session.get('idlocationuser'))


                return JsonResponse({"msg": "Opération effectuée ", "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée "+str(e), "id": "0"}, safe=False)




    return render(request, 'gestionstock/misestockinventaire.html',context={"periode":DelaiInventaire.objects.filter(location_id=request.session.get('idlocationuser')).order_by("-periode")})


@login_required
@permission_required('gestionstock.Rap_Stock',raise_exception=True)
def rapstock(request):
    if request.method == "POST":

        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = fn + "\{}".format("rapstock.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = fn + "\media"

        con = {
            'driver': 'generic',
            'jdbc_driver': 'com.microsoft.sqlserver.jdbc.SQLServerDriver',
            'jdbc_url': 'jdbc:sqlserver://localhost;databaseName=STOCK',
            'jdbc_dir': fn,
            'username': 'sa',
            'password': 'dev12345'
            # 'host': 'localhost',
            # 'database': 'STOCKCFDB',
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
        input_file = fn + "\{}".format("extimation.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = fn + "\media"

        con = {
            'driver': 'generic',
            'jdbc_driver': 'com.microsoft.sqlserver.jdbc.SQLServerDriver',
            'jdbc_url': 'jdbc:sqlserver://localhost;databaseName=STOCK',
            'jdbc_dir': fn,
            'username': 'sa',
            'password': 'dev12345'
            # 'host': 'localhost',
            # 'database': 'STOCKCFDB',
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
            parameters={'periode':request.POST.get('periode'),'libdate1':request.POST.get('date1'),'libdate2':request.POST.get('date2'),'iddate1':str(request.POST.get('date1')).replace("/","").replace("-",""),'iddate2':str(request.POST.get('date2')).replace("/","").replace("-","")},
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
            input_file = fn + "\{}".format("rapclientcategorie.jrxml")
        elif request.POST.get("cmp")=="2":
            input_file = fn + "\{}".format("rapclientcategorie2.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = fn + "\media"

        con = {
            'driver': 'generic',
            'jdbc_driver': 'com.microsoft.sqlserver.jdbc.SQLServerDriver',
            'jdbc_url': 'jdbc:sqlserver://localhost;databaseName=STOCK',
            'jdbc_dir': fn,
            'username': 'sa',
            'password': 'dev12345'
            # 'host': 'localhost',
            # 'database': 'STOCKCFDB',
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


@login_required
@permission_required('gestionstock.Rap_Client_Co',raise_exception=True)
def rapclientco(request):
    if request.method == "POST":

        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if request.POST.get("cmp")=="1":
            input_file = fn + "\{}".format("rapclientcategorie.jrxml")
        elif request.POST.get("cmp")=="2":
            input_file = fn + "\{}".format("rapclientcategorie2.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = fn + "\media"

        con = {
            'driver': 'generic',
            'jdbc_driver': 'com.microsoft.sqlserver.jdbc.SQLServerDriver',
            'jdbc_url': 'jdbc:sqlserver://localhost;databaseName=STOCK',
            'jdbc_dir': fn,
            'username': 'sa',
            'password': 'dev12345'
            # 'host': 'localhost',
            # 'database': 'STOCKCFDB',
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


@login_required
@permission_required('gestionstock.Rap_Client',raise_exception=True)
def rapclient(request):
    if request.method == "POST":

        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = fn + "\{}".format("rapclient.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = fn + "\media"

        con = {
            'driver': 'generic',
            'jdbc_driver': 'com.microsoft.sqlserver.jdbc.SQLServerDriver',
            'jdbc_url': 'jdbc:sqlserver://localhost;databaseName=STOCK',
            'jdbc_dir': fn,
            'username': 'sa',
            'password': 'dev12345'
            # 'host': 'localhost',
            # 'database': 'STOCKCFDB',
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
            parameters={'numerofac':"FCC000"+str(numerofac),'tvaero':str(tvaero),'idtva':str(idtva),'libdate1':request.POST.get('date1'),'libdate2':request.POST.get('date2'),'iddate1':str(request.POST.get('date1')).replace("/","").replace("-",""),'iddate2':str(request.POST.get('date2')).replace("/","").replace("-",""),'idclient':request.POST.get('client')},
            locale='en_US'
        )


        return HttpResponse("true")

    context={
        "client":Ftiers.objects.filter(nature="CLIENT").order_by("nompostnom"),
        "taxe":Ftaxes.objects.all().order_by("designation"),
    }
    return render(request, 'gestionstock/rapclient.html',context)



@login_required
@permission_required('gestionstock.Rap_Sortie',raise_exception=True)
def rapsortie(request):
    if request.method == "POST":

        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = fn + "\{}".format("rapsortie.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = fn + "\media"

        con = {
            'driver': 'generic',
            'jdbc_driver': 'com.microsoft.sqlserver.jdbc.SQLServerDriver',
            'jdbc_url': 'jdbc:sqlserver://localhost;databaseName=STOCK',
            'jdbc_dir': fn,
            'username': 'sa',
            'password': 'dev12345'
            # 'host': 'localhost',
            # 'database': 'STOCKCFDB',
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
            parameters={'liblocation':request.session.get('locationuser'),'location1':request.session.get('idlocationuser'),'libdate1':request.POST.get('date1'),'libdate2':request.POST.get('date2'),'iddate1':str(request.POST.get('date1')).replace("/","").replace("-",""),'iddate2':str(request.POST.get('date2')).replace("/","").replace("-",""),'location':request.POST.get('location')},
            locale='en_US'
        )


        return HttpResponse("true")

    context={
        "local":Flocation.objects.exclude(location=request.session.get('idlocationuser')).order_by("designation"),

    }
    return render(request, 'gestionstock/rapsortie.html',context)



@login_required
@permission_required('gestionstock.recettesrapport',raise_exception=True)
def raprecette(request):
    if request.method == "POST":

        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = fn + "\{}".format("recettes.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = fn + "\media"

        con = {
            'driver': 'generic',
            'jdbc_driver': 'com.microsoft.sqlserver.jdbc.SQLServerDriver',
            'jdbc_url': 'jdbc:sqlserver://localhost;databaseName=STOCK',
            'jdbc_dir': fn,
            'username': 'sa',
            'password': 'dev12345'
            # 'host': 'localhost',
            # 'database': 'STOCKCFDB',
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
            parameters={'idlocation':request.session.get('idlocationuser'),'tvaero':str(tvaero),'idtva':str(idtva),'idclient':request.POST.get('client')},
            locale='en_US'
        )


        return HttpResponse("true")

    context={
        "client":Ftiers.objects.filter(nature="CLIENT").order_by("nompostnom"),
        "taxe":Ftaxes.objects.all().order_by("designation"),
    }
    return render(request, 'gestionstock/raprecette.html',context)


@login_required
@permission_required('gestionstock.Rap_Fourni',raise_exception=True)
def rapfournisseur(request):
    if request.method == "POST":

        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = fn + "\{}".format("rapfournisseur.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")

        output = fn + "\media"

        con = {
            'driver': 'generic',
            'jdbc_driver': 'com.microsoft.sqlserver.jdbc.SQLServerDriver',
            'jdbc_url': 'jdbc:sqlserver://localhost;databaseName=STOCK',
            'jdbc_dir': fn,
            'username': 'sa',
            'password': 'dev12345'
            # 'host': 'localhost',
            # 'database': 'STOCKCFDB',
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

    context = {
    "taux":Ftaxes.objects.get(taxe='001'),
    "bon":Fcommande.objects.filter(etatcde="1",location_id=request.session.get('idlocationuser'),cloture=False).order_by('-commande'),
    # "numentre":"BE000" + str(Flivraison.objects.filter(commande__location_id= request.session.get('idlocationuser')).count() + 1)
    }
    return render(request, 'gestionstock/entrestock.html', context)

@login_required
@permission_required('gestionstock.recettestock',raise_exception=True)
def entrestockrecettes(request):

    if request.method == "POST":

        try:
            with transaction.atomic():
                # one=StockRecettes.objects.filter(location_id=request.session.get('idlocationuser'),detail_id=str(request.POST.get('recette')).split("_")[2],categorie='E')
                # if one:
                #     one.update(
                #         qte=request.POST.get('qte')
                #     )
                # else:
                StockRecettes.objects.create(
                detail_id=str(request.POST.get('recette')).split("_")[2],
                qte=request.POST.get('qte'),
                categorie='E',
                location_id=request.session.get('idlocationuser')
                )
                return JsonResponse(
                    {"msg": "Opération effectuée",
                     "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)

    clients=Ftiers.objects.all()

    datafull={}
    datafullitem=[]
    datafullitemtempo=[]
    for i in clients:
        detal=DetailRecettes.objects.filter(client_id=i.tiers)
        if detal:
            for x in detal:
                code=str(i.tiers)+ "_"+str(x.recettes_id)+ "_"+str(x.id)
                if code in datafullitemtempo:
                    pass
                else:
                    datafull={}
                    datafull['id']=code
                    datafull['libelle']=str(i.nompostnom)+ " => "+str(x.recettes.libelle)
                    datafullitem.append(datafull)
                    datafullitemtempo.append(code)


        context = {
            "recette":datafullitem,
                  }
    return render(request, 'gestionstock/entrerec.html', context)


@login_required
@permission_required('gestionstock.recettestocksortie',raise_exception=True)
def sortistockrecettes(request):

    if request.method == "POST":

        try:
            with transaction.atomic():
                # one=StockRecettes.objects.filter(location_id=request.session.get('idlocationuser'),detail_id=str(request.POST.get('recette')).split("_")[2],categorie='E')
                # if one:
                #     one.update(
                #         qte=request.POST.get('qte')
                #     )
                # else:
                StockRecettes.objects.create(
                    detail_id=str(request.POST.get('recette')).split("_")[2],
                    qte=request.POST.get('qte'),
                    categorie='S',
                    location_id=request.session.get('idlocationuser')
                )
                return JsonResponse(
                    {"msg": "Opération effectuée",
                     "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)

    clients=Ftiers.objects.all()

    datafull={}
    datafullitem=[]
    datafullitemtempo=[]
    for i in clients:
        detal=DetailRecettes.objects.filter(client_id=i.tiers)
        if detal:
            for x in detal:
                code=str(i.tiers)+ "_"+str(x.recettes_id)+ "_"+str(x.id)
                if code in datafullitemtempo:
                    pass
                else:
                    datafull={}
                    datafull['id']=code
                    datafull['libelle']=str(i.nompostnom)+ " => "+str(x.recettes.libelle)
                    datafullitem.append(datafull)
                    datafullitemtempo.append(code)


        context = {
            "recette":datafullitem,
        }
    return render(request, 'gestionstock/sortirec.html', context)

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
                            resultat2 = float(i.qtelivree) * art.first().quantitee
                            # if art2:
                            #     resultat2 = i.qtelivree
                            # else:
                            #     resultat2 = float(i.qtelivree) * art.first().quantitee
                            # tot=getstockproduit(request.session.get('idlocationuser'),i.article.article,libemb)
                            # prixcmpdetail=((tot*art.first().prix_vente)+(resultat1*i.prixunitaire))/(resultat1+tot)
                        elif art2:
                            resultat2 = i.qtelivree
                            resultat1 = float(i.qtelivree) / art2.first().quantitee
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

    context = {"produit": Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser')).order_by('designation'),

               }

    if request.method == "POST":

        try:
            with transaction.atomic():

                pro=TempoPrix.objects.filter(article_id=request.POST.get('produit'),etat=False)
                if pro:
                    pro.update(
                        dateop=request.POST.get('dateop'),
                        emb1_id=request.POST.get('emballage1'),
                        emb2_id=request.POST.get('emballage2'),
                        prix1=request.POST.get('prix1'),
                        prix2=request.POST.get('prix2'),
                        devise=request.POST.get('devise'),
                        user_id=request.user.id, )
                else:
                    TempoPrix.objects.create(
                    article_id=request.POST.get('produit'),
                    dateop=request.POST.get('dateop'),
                    emb1_id=request.POST.get('emballage1'),
                    emb2_id=request.POST.get('emballage2'),
                    prix1=request.POST.get('prix1'),
                    prix2=request.POST.get('prix2'),
                    devise=request.POST.get('devise'),
                    user_id=request.user.id,)
                return JsonResponse(
                    {"msg": "Opération effectuée",
                     "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)
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
@permission_required('gestionstock.ajustementpro_valide',raise_exception=True)
def ajustementpro(request):

    context = {
        "produit":Farticle.objects.filter(LOCATION_id= request.session.get('idlocationuser')).order_by('designation'),
        "ajustement":Fajustement.objects.filter(ajustement__in=('DECL','PAT')).order_by('designation'),
    }
    if request.method == "POST":

        try:
            with transaction.atomic():


                prixcmpdetail=0
                artic = Farticle.objects.get(article=request.POST.get('produit'))

                resultat2 = float(request.POST.get('qte'))
                resultat1 = float(request.POST.get('qte')) / artic.quantitee

                if request.POST.get('qte')!='':
                    if str(request.POST.get('ajustement')).strip() == 'PAT':#ajustement positif


                        tot=getstockproduit(request.session.get('idlocationuser'),request.POST.get('produit'),artic.emballageu_id)

                        if (resultat2+tot) != 0:
                            prixcmpdetail=((tot*artic.prix_vente)+(resultat2*artic.pa))/(resultat2+tot)
                        else:
                            prixcmpdetail=artic.prix_vente

                        Fmvts.objects.create(
                            location_id=request.session.get('idlocationuser'),
                            datemvt=request.POST.get('dateop'),
                            ndatemvt=str(request.POST.get('dateop')).replace("-","").replace("/",""),
                            requisition="AJUSTEMENT",
                            document="AJUSTEMENT",
                            ajustement_id=request.POST.get('ajustement'),
                            article_id=request.POST.get('produit'),
                            emballage_id=artic.emballageu_id,
                            # quantite=i.qtelivree,
                            qte_entree=resultat1,
                            qteunit_entree=resultat2,
                            prix_achat=artic.pa,
                            prix_vente=0,
                            # devise="",
                            # txchange=str(request.POST.get('taux')).replace(",","."),
                            codeuser_id=request.user.id,
                        )

                    else:#ajustement negatif

                        #################################################################CMP

                        tot=getstockproduit(request.session.get('idlocationuser'),request.POST.get('produit'),artic.emballageu_id)
                        tot=tot-resultat2
                        if (tot) != 0:
                            prixcmpdetail=((tot*artic.pa))/(tot)
                        else:
                            prixcmpdetail=artic.prix_vente


                        Fmvts.objects.create(
                            location_id=request.session.get('idlocationuser'),
                            datemvt=request.POST.get('dateop'),
                            ndatemvt=str(request.POST.get('dateop')).replace("-","").replace("/",""),
                            requisition="AJUSTEMENT",
                            document="AJUSTEMENT",
                            ajustement_id=request.POST.get('ajustement'),
                            article_id=request.POST.get('produit'),
                            emballage_id=artic.emballageu_id,
                            # quantite=i.qtelivree,
                            qte_sortie=resultat1,
                            qteunit_sortie=resultat2,
                            prix_achat=artic.pa,
                            prix_vente=0,
                            # devise="",
                            # txchange=str(request.POST.get('taux')).replace(",","."),
                            codeuser_id=request.user.id,
                        )
                        #################################################################


                ########################################"

                    artic.prix_vente = prixcmpdetail
                    artic.save()
                return JsonResponse({"msg": "Opération effectuée ", "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)




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
                	Fdetcde.objects.create(
                	commande=bon,
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
                        observation=request.POST.get('numbont'),
                        datejour=request.POST.get('datebon'),
                        tiers_id=request.POST.get('fournisseur'),
                        datelivraison=request.POST.get('dateliv'),
                        typecommande = request.POST.get('mode'),
                        location_id=request.POST.get('location'),
                        etatcde="0",
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

                	b.update(
                        prix_unitaire=str(request.POST.get('prix')).replace(",", "."),
                        quantite=request.POST.get('qte'),
                        designation=request.POST.get('libunite'),
                        emballage_id=idemb,
                        # emballage2_id=idemb2,
                	)
                else:
                	Fdetcde.objects.create(
                	commande=bon,
                	article_id=request.POST.get('produit'),
                	designation=request.POST.get('libunite'),
                	emballage_id=idemb,
                        qte_livree=0,
                	# emballage2_id=idemb2,
                	quantite = request.POST.get('qte'),
                	prix_unitaire = str(request.POST.get('prix')).replace(",","."),
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

    context = {"commande": Fcommande.objects.filter(etatcde="0",validation=False,location_id=request.session.get('idlocationuser')).order_by('tiers__nompostnom'),
               "produit": Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser')).order_by('designation'),
               "location": Flocation.objects.filter(typelocation="D",location=request.session['idlocationuser']).order_by('designation'),
               "fournisseur": Ftiers.objects.filter(nature="FOURNISSEUR").order_by('nompostnom'),
               }

    if request.method == "POST":

        try:
            with transaction.atomic():

                bon=Fcommande.objects.filter(commande=request.POST.get('numbon'),location_id=request.session.get('idlocationuser'))
                if bon:

                    bon.update(
                    datejour=request.POST.get('datebon'),
                    datelivraison=request.POST.get('dateliv'),
                    typecommande = request.POST.get('mode'),
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




                b= Fdetcde.objects.filter(commande__commande=request.POST.get('numbon'),article_id=request.POST.get('produit'))
                if b:

                    b.update(
                        prix_unitaire=str(request.POST.get('prix')).replace(",", "."),
                        quantite=request.POST.get('qte'),
                        designation=request.POST.get('libunite'),
                        emballage_id=idemb,
                        # emballage2_id=idemb2,
                    )
                else:
                    Fdetcde.objects.create(
                        commande=bon,
                        article_id=request.POST.get('produit'),
                        designation=request.POST.get('libunite'),
                        emballage_id=idemb,
                        qte_livree=0,
                        # emballage2_id=idemb2,
                        quantite = request.POST.get('qte'),
                        prix_unitaire = str(request.POST.get('prix')).replace(",","."),
                        # qteunitaire = resultat2
                    )
                return JsonResponse(
                    {"msg": "Opération effectuée",
                     "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)

    return render(request, 'gestionstock/boncommandemodi.html', context)



@login_required
@permission_required('gestionstock.recettesfiche',raise_exception=True)
def production(request):

    if request.method == "POST":

        try:
            with transaction.atomic():



                if request.POST.get('idrecette')!='':
                    bon=Recettes.objects.get(id=request.POST.get('idrecette'))
                    bon.libelle=request.POST.get('designation')
                    bon.save()
                else:
                    Recettes.objects.create(
                        libelle=request.POST.get('designation'))

                return JsonResponse(
                    {"msg": "Opération effectuée",
                     "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)

    context={
        'produit':Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser')).order_by('designation'),
        'client':Ftiers.objects.filter(nature="CLIENT").order_by('nompostnom'),
    }
    return render(request, 'gestionstock/production.html',context)

@require_POST
@login_required
@permission_required('gestionstock.recettesfiche',raise_exception=True)
def fichetechnique(request):


    try:
        with transaction.atomic():


            recd=DetailRecettes.objects.filter(recettes_id=request.POST.get('recette'),
                                               produit_id=request.POST.get('produit'),
                                               client_id=request.POST.get('client'))
            if recd:
                if request.POST.get('suppression')=="non":
                    recd.update(
                    qte=request.POST.get('qte'),
                    emballage_id=request.POST.get('emballage')
                    )
                else:
                    recd.delete()
            else:
                DetailRecettes.objects.create(
                    recettes_id=request.POST.get('recette'),
                produit_id=request.POST.get('produit'),
                client_id=request.POST.get('client'),
                qte=request.POST.get('qte'),
                emballage_id=request.POST.get('emballage')
                )

            return JsonResponse(
                {"msg": "Opération effectuée",
                 "id": "1"}, safe=False)
    except Exception as e:
        return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)




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
                        rqt=(art.quantiteu*float(request.POST.get('qte')))/art.quantitee

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

                bon=Fcommande.objects.get(commande=request.POST.get('numbon'),location_id=request.session.get('idlocationuser'),etatcde="0")
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

                bon=Flivraison.objects.get(document=request.POST.get('numliv'),commande_id=request.POST.get('numbon'),commande__location_id=request.session.get('idlocationuser'))
                bon.validation=True
                bon.save()
                return JsonResponse(
                    {"msg": "Opération effectuée",
                     "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)


@login_required
@permission_required('gestionstock.Sortie_Stock',raise_exception=True)
def transfert(request):

    context = {
        "fournisseur": Ftiers.objects.filter(typetiers__in=("1","2")).order_by('nompostnom'),
        "sortielist": Fmvts.objects.filter(ajustement_id="TRTO",location_id=request.session.get('idlocationuser')).values('document','datemvt').annotate(Count('document')).order_by('-ndatemvt'),
        "article": Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser')).order_by('designation'),
			   "location": Flocation.objects.filter(typelocation="D",location=request.session["idlocationuser"]).order_by('designation'),
			   "locationb": Flocation.objects.all().exclude(location=request.session["idlocationuser"]).exclude(typelocation="D").order_by('designation'),
			   }
    if request.method == "POST":
        try:

            with transaction.atomic():
                # ----------------------------------
                resultat1 = 0
                resultat2 = 0
                prix = 0
                art = Farticle.objects.filter(article=request.POST.get('produit'), emballagee_id=request.POST.get('emballage'))
                art2 = Farticle.objects.filter(article=request.POST.get('produit'), emballageu_id=request.POST.get('emballage'))
                if art:
                    resultat1 = request.POST.get('qtet')
                    resultat2 = float(request.POST.get('qtet')) * art.first().quantitee
                    prix=art.first().pa
                elif art2:
                    resultat2 = request.POST.get('qtet')
                    resultat1 = float(request.POST.get('qtet')) / art2.first().quantitee
                    prix = art.first().pa

                sortie=Fmvts.objects.filter(document=request.POST.get('numtrans'),article_id=request.POST.get('produit'))
                if sortie:
                    sortie.filter(ajustement_id="TRFR").update(
                        datemvt=request.POST.get('dateop'),
                        ndatemvt=str(request.POST.get('dateop')).replace("-", "").replace("/", ""),
                        qte_entree=resultat1,
                        qteunit_entree=resultat2,
                        tiers_id=request.POST.get('client'),
                        emballage_id=request.POST.get('emballage'),
                        prix_achat=prix,
                        codeuser_id=request.user.id,
                    )

                    sortie.filter(ajustement_id="TRTO").update(
                        datemvt=request.POST.get('dateop'),
                        ndatemvt=str(request.POST.get('dateop')).replace("-", "").replace("/", ""),
                        qte_sortie=resultat1,
                        qteunit_sortie=resultat2,
                        tiers_id=request.POST.get('client'),
                        emballage_id=request.POST.get('emballage'),
                        prix_achat=prix,
                        codeuser_id=request.user.id,
                    )
                else:
                    Fmvts.objects.create(
                location_id=request.POST.get('location'),
                datemvt=request.POST.get('dateop'),
                ndatemvt=str(request.POST.get('dateop')).replace("-", "").replace("/", ""),

                ajustement_id="TRTO",
                article_id=request.POST.get('produit'),
                    tiers_id=request.POST.get('client'),
                emballage_id=request.POST.get('emballage'),
                qte_sortie=resultat1,
                qteunit_sortie=resultat2,
                    document=request.POST.get('numtrans'),
                prix_achat=prix,
                # prix_vente=request.POST.get('privente'),
                # devise=request.POST.get('devise'),
                # txchange=str(request.POST.get('taux')).replace(",", "."),
                codeuser_id=request.user.id,
                destinat_id=request.POST.get('locationbis'),
            )

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
                    Fmvts.objects.create(
                    location_id=request.POST.get('locationbis'),
                    datemvt=request.POST.get('dateop'),
                    ndatemvt=str(request.POST.get('dateop')).replace("-", "").replace("/", ""),
                    document=request.POST.get('numtrans'),
                    ajustement_id="TRFR",
                    article_id=request.POST.get('produit'),
                    qte_entree=resultat1,
                    qteunit_entree=resultat2,
                    tiers_id=request.POST.get('client'),
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

    sortie=Fmvts.objects.filter(ajustement_id="TRTO").order_by('-mvt')
    if sortie:
        sortie=sortie.first()
        context['numtrans'] = "SRT000" + str(int(str(sortie.document).split("SRT000")[1]) + 1)
    else:
        context['numtrans'] = "SRT0001"
    return render(request, 'gestionstock/transfert.html', context)

@login_required
@permission_required('gestionstock.Retour_Stock',raise_exception=True)
def retour(request):
    context = {"article": Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser')).order_by('designation'),
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
                    resultat2 = float(request.POST.get('qtet')) * art.first().quantitee
                    prix = art.first().pa
                elif art2:
                    resultat2 = request.POST.get('qtet')
                    resultat1 = float(request.POST.get('qtet')) / art2.first().quantitee
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
    context['numretour'] = "RT000" + str(
        Fmvts.objects.filter(location_id=request.session["idlocationuser"], ajustement_id="TRTO").count() + 1)
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
        rec = Fdetcde.objects.filter(commande__etatcde="0",commande__commande=request.GET.get('validation_boncmd')).values(
            "id", "article__designation","designation", "emballage__emballage", "quantite", "commande__tiers__nompostnom",
            "commande__datejour", "qte_livree", "prix_unitaire", "commande__location__designation"
        ).order_by('-id')
    elif "impression" in request.GET:
        rec = Fdetcde.objects.filter(commande__etatcde="1",commande__commande=request.GET.get('impression')).values(
            "id", "article__designation", "emballage__emballage", "quantite", "commande__tiers__nompostnom",
            "commande__datejour", "qte_livree", "prix_unitaire", "commande__location__designation"
        ).order_by('-id')
    elif "livraison" in request.GET:
        rec = Fdetcde.objects.filter(commande__etatcde="1",commande__commande=request.GET.get('livraison')).annotate(difference=F('quantite')-F('qte_livree')).values(
            "id", "article__designation","prix_unitaire", "emballage__emballage","quantite", "commande__tiers__nompostnom",
            "commande__datejour", "commande__location__designation","qte_livree","difference"
        ).order_by('-id')
    else:
        rec = Fdetcde.objects.filter(commande__commande=request.GET.get('bon')).values(
            "id","article__designation","article__article","designation","emballage__emballage","quantite","commande__tiers__nompostnom","commande__datejour","qte_livree","prix_unitaire","commande__location__designation"
        ).order_by('-id')
    rec=list(rec)
    return JsonResponse({'data': rec}, safe=False)

@login_required
def getpromodifier(request):
	rec = TempoPrix.objects.filter(etat=False,article__LOCATION_id=request.session.get('idlocationuser')).values(
            "id","article__designation","emb1__emballage","prix1","emb2__emballage","prix2"
        ).order_by('-id')
	rec=list(rec)
	return JsonResponse({'data': rec}, safe=False)


@login_required
def getsupprimer(request):
    rec = Fcommande.objects.filter(location_id=request.session.get('idlocationuser')).values(
        "commande","tiers__nompostnom","etatcde","observation","userr__username","datejour","livraisoncmd__document","livraisoncmd__etatliv").order_by('-created_at')
    rec=list(rec)
    return JsonResponse({'data': rec}, safe=False)


@login_required
def getfacture(request):
    if request.GET.get('id')!='':
        rec = Fmvts.objects.filter(document=request.GET.get('numtrans'),ajustement_id="TRFR").values(
            "mvt","article__designation","article_id","qte_entree","datemvt","location__designation","tiers__nompostnom").order_by('-mvt')
    else:
        rec = Fmvts.objects.filter(document=request.GET.get('numtrans'),ajustement_id="TRFR",location_id=request.GET.get('locationbis'),ndatemvt=str(request.GET.get('dateop')).replace("-", "").replace("/", "")).values(
            "mvt","article__designation","article_id","qte_entree","datemvt","location__designation","tiers__nompostnom").order_by('-mvt')
    rec=list(rec)
    return JsonResponse({'data': rec}, safe=False)


@login_required
def getajustementpro(request):
    rec = Fmvts.objects.filter(ajustement__in=('DECL','PAT'),location_id=request.session.get('idlocationuser'),article_id=request.GET.get('produit')).values(
        "mvt","article__designation","ajustement__designation","emballage_id","qteunit_entree","qteunit_sortie","datemvt","codeuser__username").order_by('-mvt')
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
def getrecettes(request):
    rec = Recettes.objects.all().values().order_by('libelle')
    rec=list(rec)
    return JsonResponse({'data': rec}, safe=False)


@login_required
def getrecettesdetail(request):
    cdz=str(request.GET.get("recette")).split("_")
    if len(cdz)>=2:
        recx = DetailRecettes.objects.filter(client_id=cdz[0],recettes_id=cdz[1]).order_by('produit__designation')
    else:
        recx = DetailRecettes.objects.filter(client_id=request.GET.get("client"),recettes_id=request.GET.get("recette")).order_by('produit__designation')
    rec=[]
    tot=0
    for i in recx:
        datafull = {}
        datafull['id']=i.id
        datafull['produit__designation']=i.produit.designation
        datafull['produit__pa']=i.produit.pa
        datafull['qte']=i.qte
        datafull['emballage__emballage']=i.emballage.emballage
        tot=tot+(float(i.produit.pa)*float(i.qte))
        datafull['total']=tot
        rec.append(datafull)


    rec=list(rec)
    return JsonResponse({'data': rec}, safe=False)


@login_required
def getrecettesdetailstock(request):
    #.
    rec = StockRecettes.objects.filter(location_id=request.session.get('idlocationuser'),categorie="E").annotate(_name=Concat('detail__recettes__libelle', Value ("/") ,'detail__client__nompostnom')).values("_name",'detail__recettes__libelle','detail__client__nompostnom').distinct().annotate(_sum=Sum("qte"))
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
    if "id" in request.GET:
        rec = Farticle.objects.filter(article=request.GET.get('id'),LOCATION_id=request.session.get('idlocationuser')).values(
       "article","designation","famille__famille","classe__classe","numcompte","categorie","qte_stock_minimal","emballagee__emballage","emballageu__emballage","quantiteu","quantitee","qte_stock_minimal").order_by('designation')
    else:

        rec = Farticle.objects.filter(LOCATION_id=request.session.get('idlocationuser')).values(
            "article","designation","famille__designation","quantitee","quantiteu","classe__designation","emballagee__designation","emballageu__designation","qte_stock_minimal").order_by('designation')
    rec=list(rec)
    return JsonResponse({'data': rec}, safe=False)


@login_required
def getrecette(request):
    rec = Recettes.objects.all().values(
        "id","libelle").order_by('libelle')
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
            "article__article","article__designation","emballage_e","emballage_u","qte_u_log","qte_u_phys","qte_u_ecart").order_by('article__designation')
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
                                imputation=request.POST.get('mode'),
                                etatliv="0",
                                observation=request.POST.get('commentaire')
                            )
                        else:
                            bp=Flivraison.objects.create(
                            commande=b.commande,
                            serielivraison=str(b.commande.commande).replace("C","E"),
                            document=request.POST.get('numbonlivre'),
                            datejour=request.POST.get('dateop'),
                            imputation=request.POST.get('mode'),
                            etatliv="0",
                            observation=request.POST.get('commentaire')
                            )

                    #     b.commande.serielivraison = request.POST.get('numbonentre')
                    #     b.commande.save()
                    # print(bp.serielivraison)
                    detaillivre=Fdetlivraison.objects.filter(article=b.article,serielivraison_id=bp.serielivraison)
                    if detaillivre:
                        detaillivre.update(
                            qtelivree=request.POST.get('qte'),
                            prixunitaire=request.POST.get('pa')
                        )
                    else:
                        Fdetlivraison.objects.create(
                        serielivraison_id=bp.serielivraison,
                        article=b.article,
                        qtelivree=request.POST.get('qte'),
                        prixunitaire=request.POST.get('pa')
                    )


                    # b.qte_livree = b.qte_livree+ float(request.POST.get('qte'))
                    somme=Fdetlivraison.objects.filter(serielivraison__commande=b.commande,article=b.article).aggregate(Sum('qtelivree')).get('qtelivree__sum')
                    if somme is None:
                        somme=0
                    b.prix_unitaire = float(request.POST.get('pa'))
                    b.qte_livree = float(somme)
                    b.quantite = float(request.POST.get('qtecmd'))

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
                    return JsonResponse({"msg": "Opération effectuée ", "id": "1"}, safe=False)
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
                                resultat2 = float(request.POST.get('qtecmd')) * art.first().quantitee
                            elif art2:
                                resultat2 = request.POST.get('qtecmd')
                                resultat1 = float(request.POST.get('qtecmd')) / art2.first().quantitee

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
                                resultat2 = float(request.POST.get('qtecmd')) * art.first().quantitee
                            elif art2:
                                resultat2 = float(request.POST.get('qtecmd'))
                                resultat1 = float(request.POST.get('qtecmd')) / art2.first().quantitee

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
        b = Farticle.objects.get(article=request.POST.get('produit'),LOCATION_id=request.session.get('idlocationuser'))

        return JsonResponse({"prix": b.prix_achat}, safe=False)
    elif request.POST.get('emballage')=="2":
        b = Farticle.objects.get(article=request.POST.get('produit'),LOCATION_id=request.session.get('idlocationuser'))

        return JsonResponse({"prix": b.pa}, safe=False)
    else:
        one=Farticle.objects.filter(designation=request.POST.get('produit'),emballagee_id=request.POST.get('emballage'),LOCATION_id=request.session.get('idlocationuser'))
        if one:
            one=one.first()
            return JsonResponse({"prix": one.prix_achat}, safe=False)

        one = Farticle.objects.filter(designation=request.POST.get('produit'), emballageu_id=request.POST.get('emballage'),LOCATION_id=request.session.get('idlocationuser'))
        if one:
            one = one.first()
            return JsonResponse({"prix": one.pa}, safe=False)
        return JsonResponse({"prix": 0}, safe=False)


@require_POST
@login_required
def getlibemballage(request):
    b = Farticle.objects.get(article=request.POST.get('produit'),LOCATION_id=request.session.get('idlocationuser'))
    return JsonResponse({"emb1": b.emballagee_id,"emb2": b.emballageu_id}, safe=False)


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

    if request.POST.get('ctrl')=="0":

        b = Fmvts.objects.filter(location_id=request.session.get('idlocationuser'),article_id=request.POST.get('produit'),ajustement_id__in=("ACH","PAT","TRFR","INV")).aggregate(Sum("qte_entree")).get("qte_entree__sum")
        if b is None:#entrer
            b = 0
        c = Fmvts.objects.filter(location_id=request.session.get('idlocationuser'), article_id=request.POST.get('produit'),
                                 ajustement_id__in=("VTE", "TRTO", "FACT","DECL","INV")).aggregate(Sum("qte_sortie")).get("qte_sortie__sum")
        if c is None:  # sortie
            c = 0

        tot=b-c
        #--------------------------------------------
        emb=Farticle.objects.filter(article=request.POST.get('produit'),LOCATION_id=request.session.get('idlocationuser')).values('emballagee_id','emballageu_id','emballageu__designation',
                                                                                'emballagee__designation')

        prix=Farticle.objects.get(article=request.POST.get('produit'),LOCATION_id=request.session.get('idlocationuser'))


        return JsonResponse({"tot": tot,"emb":list(emb),"prix":prix.prix_vente}, safe=False)
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




