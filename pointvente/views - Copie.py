from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,permission_required
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.db import IntegrityError, transaction
from datetime import datetime
import os

# Create your views here.
from django.urls import reverse
from django.views.decorators.http import require_POST


from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Image as img, Spacer, Paragraph, Table, TableStyle

from .models import *

from pyreportjasper import JasperPy

def colr(x,y,z):
    return (x/255,y/255,z/255)

def home(request):
    context={}

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


def situation(request):
    context = {"location": Flocation.objects.all().order_by('designation'),
               }

    if request.method=="POST":
        from .cnx import connexion

        cnxQ = connexion()  # creer instance connexion
        cnxQ2 = connexion()  # creer instance connexion
        cnxQ3 = connexion()  # creer instance connexion
        cnxQ4 = connexion()  # creer instance connexion
        cnxQ5 = connexion()  # creer instance connexion

        dbx = str(request.POST.get('dtd')).replace('-', '')
        dbfinx = str(request.POST.get('dtf')).replace('-', '')

        Titretyle = ParagraphStyle(
            name='titre',
            fontName='Helvetica-Bold',
            fontSize=14,
            textColor='DarkGray',
            borderPadding=(2, 2, 7, 2),
            borderWidth=0,
            borderColor='Gray',
            alignment=TA_CENTER
        )

        Paragraphstyle = ParagraphStyle(
            name='MyDoctorHeader',
            fontName='Helvetica',
            fontSize=12,
            textColor='Teal',
            leading=10,
            alignment=TA_LEFT
        )
        Headerstyle = ParagraphStyle(
            name='headesr',
            fontName='Helvetica-Bold',
            fontSize=15,
            textColor='Gray',
            # borderPadding=(2, 2, 7, 2),
            # borderWidth=0,
            # borderColor='Gray',
            alignment=TA_LEFT
        )

        styles = getSampleStyleSheet()
        styleN = styles["BodyText"]
        styleN.alignment = TA_LEFT

        styleB = styles["Normal"]
        styleB.alignment = TA_RIGHT

        elements = []

        header = Paragraph("""
                                                                   <b>%s</b><br/>
                                                                   %s<br/>
                                                                   <i>%s</i><br/>
                                                                   """ % (
            "République Democratique du Congo", "Miltex SARLU", "Kinshasa/Gombe"),
                           style=Headerstyle)
        #
        tab = Table([[header]], style=[('VALIGN', (0, 0), (-1, -1), 'TOP')],
                    colWidths=[25 * cm, 3 * cm])

        elements.append(tab)

        elements.append(Spacer(1, 20))

        rc = cnxQ.Selection([
            """
select * from(select  FMVTS.DESIGNATION,ARTICLE
from FMVTS
where FMVTS.LOCATION ='{}' and convert(Float,NDATEMVT)>=convert(Float,'{}')  and convert(Float,NDATEMVT)<=convert(Float,'{}') group by FMVTS.DESIGNATION,ARTICLE) as FMVTS order by DESIGNATION
               """.format(request.POST.get('location'),
                          dbx, dbfinx)])
        txt = 'STATISTIQUE COUT MOYEN PONDERE LOCATION {}<br/><br/><u>DU {} AU {}</u>'.format(request.POST.get('location'), request.POST.get('dtd'), request.POST.get('dtf'))
        data = [[Paragraph(txt,
                           style=Titretyle)]]
        titre = Table(data)

        elements.append(titre)
        elements.append(Spacer(1, 20))

        temp = ['#', 'Désignation', 'PUR', 'QTR', 'OP', 'PUE', 'QTE', 'VE', 'QTS', 'VS', 'QI', 'PUI', 'VI']
        diver_table = [temp]

        if rc:

            libpro = ''
            libstringDate = ''
            libstringPro = ''
            MVT = ''

            libstringDatex = ''
            libstringProx = ''

            libdate = 0
            compteur = 1
            sommepue = 0.0
            sommeqte = 0.0
            sommeqts = 0.0

            onepue = 0.0
            oneqte = 0.0
            oneqts = 0.0

            tempo = []


            for i in rc:

                tempo = []


                qteARTICLE = 0
                prixARTICLE = 0
                EmballageART1 = ''
                EmballageART2 = ''

                ####################################################qteinuit

                rqtART = cnxQ5.Selection([
                    """
                    SELECT QUANTITEE,EMBALLAGEE,EMBALLAGEU,PRIXREVIENTGRO FROM dbo.FARTICLE where ARTICLE='{}'
                    """.format(str(i[1]))

                ])

                if rqtART:
                    for b in rqtART:
                        qteARTICLE = b[0]
                        EmballageART1 = b[1]
                        EmballageART2 = b[2]
                        prixARTICLE = b[3]

                ####################################################
                # # # historik
                if qteARTICLE != 0:

                    rctempoE = cnxQ2.Selection(["""select sum(totpu) as totpu,sum(valori) as valori,sum(qte) as qte,sum(cmp) as cmp,NDATEMVT,sum(qteS) as qteS from(
        select totpu,0 as valori,qte,cmp,NDATEMVT,'' as qteS from(
        select qte,pu/cmp as totpu,cmp,NDATEMVT from(

        select sum(qte) as qte,sum(pu) as pu,COUNT(*) as cmp,NDATEMVT 

        from(
        select FMVTS.QTEUNIT_ENTREE/{} as qte,FMVTS.PRIX_ACHAT as pu,convert(Float,LEFT(Ltrim(rtrim(str(NDATEMVT))),6)) as NDATEMVT,DATEMVT,FMVTS.MVT,'' as qteS 
        from FMVTS  
        where convert(Float,NDATEMVT)<convert(Float,'{}')
        and  ARTICLE='{}' and LOCATION ={}
        and FMVTS.AJUSTEMENT='ACH'

        union

        select FMVTS.QTEUNIT_ENTREE/{} as qte,{} as pu,convert(Float,LEFT(Ltrim(rtrim(str(NDATEMVT))),6)) as NDATEMVT,DATEMVT,FMVTS.MVT,FMVTS.QTEUNIT_SORTIE/{} as qteS
        from FMVTS 
        where convert(Float,NDATEMVT)<convert(Float,'{}')
        and ARTICLE='{}' and LOCATION ={}
        and FMVTS.AJUSTEMENT='INV' and FMVTS.QTEUNIT_ENTREE is NOT NULL and FMVTS.QTEUNIT_SORTIE is NOT NULL 


        )as FMVTS group by NDATEMVT

        )as FMVTS
        )as FMVTS

        union

        select 0 as totpu ,0 as valori,0 as qte,0 as cmp,NDATEMVTE as NDATEMVT,sum(qteS) as qteS 

        from(
        select FMVTS.QTEUNIT_SORTIE/{} as qteS,convert(Float,LEFT(Ltrim(rtrim(str(NDATEMVT))),6)) as NDATEMVTE 
        from FMVTS   
        where convert(Float,NDATEMVT)<convert(Float,'{}')
        and ARTICLE='{}' and LOCATION ={}
        and AJUSTEMENT ='TRTO'

        )as FMVTS group by NDATEMVTE


        )as FMVTS group by NDATEMVT
                                """.format(qteARTICLE,
                                           dbx, str(i[1]), request.POST.get('location'), qteARTICLE, prixARTICLE, qteARTICLE, dbx,
                                           str(i[1]), request.POST.get('location'), qteARTICLE, dbx, str(i[1]), request.POST.get('location'))])

                    valorso = 0
                    valoren = 0
                    pue = 0
                    qts = 0
                    qte = 0
                    qti = 0
                    valorii = 0
                    Rpue = 0
                    Rqti = 0

                    for tempg in rctempoE:

                        if not tempg[0] is None:

                            if pue == 0:
                                pue = (pue + tempg[0])  # 0

                                qte = tempg[2] + qte  # 0

                                valoren = pue * qte  # 0000000
                                qts = tempg[5]  #
                                valorso = pue * qts  # 000000
                                qti = qte - qts
                                valorii = qti * pue  # 000000
                            else:
                                pue = (pue + tempg[0]) / 2

                                qte = tempg[2] + qti

                                valoren = pue * qte
                                qts = tempg[5]
                                valorso = pue * qts
                                qti = qte - qts
                                valorii = qti * pue

                            Rpue = pue
                            Rqti = qti

                    # for tempg in rctempoS:
                    #     if not tempg[0] is None:
                    #         qts = tempg[0]

                    # if pue==0:
                    #     compteur=0
                    #     diver_table.append(
                    #         [len(diver_table), 'Rep.', i[0], compteur, "%.2f" % pue, "%.2f" % qti,
                    #          "%.2f" % valorii, 0, 0,
                    #          0, 0, 0])
                    # else:
                    #     diver_table.append(
                    #     [len(diver_table), 'Rep.', i[0], compteur, "%.2f" % pue, "%.2f" % qti, "%.2f" % valorii, 0, 0,
                    #      0, 0, 0])

                    # # # historik
                    if pue == 0:
                        compteur = 0
                        tempo.append(len(diver_table))
                        tempo.append(i[0])
                        tempo.append("%.2f" % pue)
                        tempo.append("%.2f" % qti)

                    else:
                        tempo.append(len(diver_table))
                        tempo.append(i[0])
                        tempo.append("%.2f" % pue)
                        tempo.append("%.2f" % qti)

                    # # # historik

                    # # # Fin Periode

                    rqt = cnxQ4.Selection([
                        """ 
select sum(totpu) as totpu,sum(valori) as valori,sum(qte) as qte,sum(cmp) as cmp,NDATEMVT,sum(qteS) as qteS from(
select totpu,0 as valori,qte,cmp,NDATEMVT,'' as qteS from(
select qte,pu/cmp as totpu,cmp,NDATEMVT from(

select sum(qte) as qte,sum(pu) as pu,COUNT(*) as cmp,NDATEMVT 

from(
select FMVTS.QTEUNIT_ENTREE/{} as qte,FMVTS.PRIX_ACHAT as pu,convert(Float,LEFT(Ltrim(rtrim(str(NDATEMVT))),6)) as NDATEMVT,DATEMVT,FMVTS.MVT,'' as qteS 
from FMVTS  
where convert(Float,NDATEMVT)>=convert(Float,'{}')  and convert(Float,NDATEMVT)<=convert(Float,'{}')
and  ARTICLE='{}' and LOCATION ={}
and FMVTS.AJUSTEMENT='ACH'

union

select FMVTS.QTEUNIT_ENTREE/{} as qte,{} as pu,convert(Float,LEFT(Ltrim(rtrim(str(NDATEMVT))),6)) as NDATEMVT,DATEMVT,FMVTS.MVT,FMVTS.QTEUNIT_SORTIE/{} as qteS
from FMVTS 
where convert(Float,NDATEMVT)>=convert(Float,'{}')  and convert(Float,NDATEMVT)<=convert(Float,'{}')
and ARTICLE='{}' and LOCATION ={}
and FMVTS.AJUSTEMENT='INV' and FMVTS.QTEUNIT_ENTREE is NOT NULL and FMVTS.QTEUNIT_SORTIE is NOT NULL 


)as FMVTS group by NDATEMVT

)as FMVTS
)as FMVTS

union

select 0 as totpu ,0 as valori,0 as qte,0 as cmp,NDATEMVTE as NDATEMVT,sum(qteS) as qteS 

from(
select FMVTS.QTEUNIT_SORTIE/{} as qteS,convert(Float,LEFT(Ltrim(rtrim(str(NDATEMVT))),6)) as NDATEMVTE 
from FMVTS   
where convert(Float,NDATEMVT)>=convert(Float,'{}')  and convert(Float,NDATEMVT)<=convert(Float,'{}')
and ARTICLE='{}' and LOCATION ={}
and AJUSTEMENT ='TRTO'

)as FMVTS group by NDATEMVTE


)as FMVTS group by NDATEMVT
                    """.format(qteARTICLE,
                               dbx, dbfinx, str(i[1]), request.POST.get('location'), qteARTICLE, prixARTICLE, qteARTICLE, dbx, dbfinx,
                               str(i[1]), request.POST.get('location'), qteARTICLE, dbx, dbfinx, str(i[1]), request.POST.get('location'))])

                    if rqt:

                        valorsow = 0
                        valorenw = 0
                        puew = 0
                        qtsw = 0
                        qtew = 0
                        qtiw = 0
                        valoriiw = 0
                        cmpx = 0

                        for tempg in rqt:
                            if not tempg[0] is None:

                                if Rpue == 0:
                                    puew = (Rpue + tempg[0])
                                else:
                                    puew = (Rpue + tempg[0]) / 2

                                qtew = tempg[2] + Rqti
                                cmpx += tempg[3]
                                valorenw = puew * qtew
                                qtsw = tempg[5]
                                valorsow = puew * qtsw
                                qtiw = qtew - qtsw
                                Rqti = qtiw
                                Rpue = puew
                                valoriiw = qtiw * puew

                        tempo.append(cmpx)
                        tempo.append("%.2f" % puew)
                        tempo.append("%.2f" % qtew)
                        tempo.append("%.2f" % valorenw)
                        tempo.append("%.2f" % qtsw)
                        tempo.append("%.2f" % valorsow)
                        tempo.append("%.2f" % qtiw)
                        tempo.append("%.2f" % puew)
                        tempo.append("%.2f" % valoriiw)
                        diver_table.append(tempo)

            medstable = Table(diver_table, repeatRows=1,
                              colWidths=[1 * cm, 4 * cm, 2 * cm])
            medstable.setStyle(TableStyle([

                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, -1), 7),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('BACKGROUND', (0, 0), (-1, 0), colr(119, 136, 153)),
                ('GRID', (0, 0), (-1, 0), 0.5, '#CFEAD4'),
                ('INNERGRID', (0, 0), (-1, 0), 0.5, '#CFEAD4'),

                ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

                ('GRID', (0, 0), (-1, -1), 0.5, '#CFEAD4'),
                ('INNERGRID', (0, 0), (-1, -1), 0.5, '#CFEAD4'),
            ]))
            elements.append(medstable)


        doc = SimpleDocTemplate("situation.pdf", pagesize=landscape(letter), rightMargin=20, leftMargin=20,
                                topMargin=20, bottomMargin=20, allowSplitting=1,
                                )

        # doc.build(elements,onFirstPage=drawPageFrame)
        doc.multiBuild(elements)


        with open("situation.pdf") as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'inline;filename=rapportnew.pdf'
            return response

        return response
        # os.open('output.pdf')

        return HttpResponse(str(request.POST.get('dtd')).replace('-', ''))


    return render(request, 'gestionstock/situation.html', context)

def rapportentreecmp(request):

    if request.method=="POST":


        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = fn+"\{}".format("rapportentreestock.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")
    
        output =fn+"\media"
        
        con = {
            'driver': 'generic',
            'jdbc_driver':'com.microsoft.sqlserver.jdbc.SQLServerDriver',
            'jdbc_url':'jdbc:sqlserver://localhost:1433;databaseName=STOCKCFDB',
            'jdbc_dir':fn,
            'username': 'sa',
            'password': 'dev'
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
            parameters={'taux':request.POST.get('taux'),'liblocation':request.POST.get('liblocation'),'location':request.POST.get('location'),'dd': '{}'.format(request.POST.get('dtd')),'df': '{}'.format(request.POST.get('dtf')),'ddl': '{}'.format(str(request.POST['dtd']).replace("-","")),'dfl':'{}'.format(str(request.POST['dtf']).replace("-",""))},
            locale='en_US'
        )


        return HttpResponse("true")
    context = {"location": Flocation.objects.all().order_by('designation'),}

    return render(request, 'gestionstock/rapportentreecmp.html', context)


def rapportsortiecmp(request):

    if request.method=="POST":


        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = fn+"\{}".format("rapportsortiestock.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")
    
        output =fn+"\media"
        
        con = {
            'driver': 'generic',
            'jdbc_driver':'com.microsoft.sqlserver.jdbc.SQLServerDriver',
            'jdbc_url':'jdbc:sqlserver://localhost:1433;databaseName=STOCKCFDB',
            'jdbc_dir':fn,
            'username': 'sa',
            'password': 'dev'
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
            parameters={'taux':request.POST.get('taux'),'liblocation':request.POST.get('liblocation'),'location':request.POST.get('location'),'dd': '{}'.format(request.POST.get('dtd')),'df': '{}'.format(request.POST.get('dtf')),'ddl': '{}'.format(str(request.POST['dtd']).replace("-","")),'dfl':'{}'.format(str(request.POST['dtf']).replace("-",""))},
            locale='en_US'
        )


        return HttpResponse("true")
    context = {"location": Flocation.objects.all().order_by('designation'),}

    return render(request, 'gestionstock/rapportsortiecmp.html', context)


def inventairecmp(request):

    if request.method=="POST":


        fn = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        input_file = fn+"\{}".format("rapportinventairestock.jrxml")

        # jdbc=os.path.join(fn, "\mssql-jdbc-8.4.1.jre14.jar")
    
        output =fn+"\media"
        
        con = {
            'driver': 'generic',
            'jdbc_driver':'com.microsoft.sqlserver.jdbc.SQLServerDriver',
            'jdbc_url':'jdbc:sqlserver://localhost:1433;databaseName=STOCKCFDB',
            'jdbc_dir':fn,
            'username': 'sa',
            'password': 'dev'
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
            parameters={'taux':request.POST.get('taux'),'liblocation':request.POST.get('liblocation'),'location':request.POST.get('location'),'dd': '{}'.format(request.POST.get('dtd')),'ddl': '{}'.format(str(request.POST['dtd']).replace("-",""))},
            locale='en_US'
        )


        return HttpResponse("true")
    context = {"location": Flocation.objects.all().order_by('designation'),}

    return render(request, 'gestionstock/rapportinventairecmp.html', context)



def rapportentreecmpc(request):

	context = {"location": Flocation.objects.all().order_by('designation'),
			   # "magasinc": Magasin.objects.filter(depotcentral=True).order_by('designation'),
			   # "magasins": Magasin.objects.filter(depotcentral=False).order_by('designation'),
			   }

	# if request.method == "POST":
    #     pass
		# from cnx import connexion
        # return HttpResponse('')
        # return HttpResponse(str(request.POST.get('dtd')).replace('-', ''))




		# try:
		# 	with transaction.atomic():
		# 		fac=Facture.objects.filter(numfac=request.POST.get('numfac'),user=request.user)
		# 		if fac:
		# 			pass
		# 		else:
		# 			fac=Facture.objects.create(
		# 				numfac=request.POST.get('numfac'),
		# 				datefac=datetime.today(),
		# 				user=request.user)

		# 		b= FactureArticle.objects.filter(facture__numfac=request.POST.get('numfac'),article_id=request.POST.get('article'))
		# 		if b:

		# 			b.update(
		# 				commentaire=request.POST.get(''),
		# 				magasinc_id=request.POST.get('magasinc'),
		# 				magasins_id=request.POST.get('magasins'),
		# 				mode="t",
		# 				qte=request.POST.get('qtet'),
		# 				taux=request.POST.get(''),
		# 			)
		# 		else:
		# 			FactureArticle.objects.create(
		# 			facture=fac,
		# 			article_id=request.POST.get('article'),
		# 			commentaire=request.POST.get(''),
		# 			magasinc_id=request.POST.get('magasinc'),
		# 			magasins_id=request.POST.get('magasins'),
		# 			mode = "t",
		# 			qte = request.POST.get('qtet'),
		# 			taux=request.POST.get(''),
		# 		)
		# 		return JsonResponse(
		# 			{"msg": "Opération effectuée",
		# 			 "id": "1"}, safe=False)
		# except Exception as e:
		# 	return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)
	# context['numfac'] = "FAC" + str(Facture.objects.count() + 1) + str(datetime.today().date()).replace("-", "")
	return render(request, 'gestionstock/rapportentreecmp.html', context)

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
                art=Farticle.objects.filter(article=request.POST.get('idpro'))

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
                    recnumart = Farticle.objects.all().order_by('-article')[:1]
                    if recnumart:
                        recnumart = recnumart.first().article
                        recnumart = int(''.join(filter(str.isdigit, recnumart)))
                    else:
                        recnumart = 0
                    recnumart = recnumart + 1
                    Farticle.objects.create(
                        article=recnumart,
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
            'password': 'dev'
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
def saisirphysique(request):

    context = {
  "classe": Fclasse.objects.all().order_by('designation'),
  "famille": Ffamilles.objects.all().order_by('designation'),
  "emballage": Femballage.objects.all().order_by('designation'),
             }

    if request.method == "POST":
  
        try:
            with transaction.atomic():
                recnumart = Farticle.objects.all().order_by('-article')[:1]
                if recnumart:
                    recnumart = recnumart.first().article
                    recnumart = int(''.join(filter(str.isdigit, recnumart)))
                else:
                    recnumart = 0
                recnumart = recnumart + 1
                Farticle.objects.create(
                    article=recnumart,
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

                return JsonResponse(
                    {"msg": "Opération effectuée",
                    "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée "+str(e), "id": "0"}, safe=False)
    return render(request, 'gestionstock/saisirphysique.html', context)


def rapportlistepriseinventaire(request):

    context = {
  "classe": Fclasse.objects.all().order_by('designation'),
  "famille": Ffamilles.objects.all().order_by('designation'),
  "emballage": Femballage.objects.all().order_by('designation'),
             }

    if request.method == "POST":
  
        try:
            with transaction.atomic():
                recnumart = Farticle.objects.all().order_by('-article')[:1]
                if recnumart:
                    recnumart = recnumart.first().article
                    recnumart = int(''.join(filter(str.isdigit, recnumart)))
                else:
                    recnumart = 0
                recnumart = recnumart + 1
                Farticle.objects.create(
                    article=recnumart,
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

                return JsonResponse(
                    {"msg": "Opération effectuée",
                    "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée "+str(e), "id": "0"}, safe=False)
    return render(request, 'gestionstock/rapportlistepriseinventaire.html', context)


def entrestock(request):
    context = {
    "taux":Ftaxes.objects.get(taxe='001'),
    "bon":Fcommande.objects.all().order_by('-commande'),
    "numentre":"BE" + str(Fmvts.objects.filter(ajustement_id="ACH",location_id= request.session.get('idlocationuser')).count() + 1) + str(datetime.today().date()).replace("-", "")
    }
    return render(request, 'gestionstock/entrestock.html', context)


@login_required
@permission_required('gestionstock.Bon_Commande',raise_exception=True)
def boncommande(request):

	context = {"produit": Farticle.objects.all().order_by('designation'),
			   "location": Flocation.objects.filter(typelocation="D",location=request.session['idlocationuser']).order_by('designation'),
			   "fournisseur": Ftiers.objects.filter(nature="FOURNISSEUR").order_by('nompostnom'),
			   }

	if request.method == "POST":

		try:
			with transaction.atomic():

				bon=Fcommande.objects.filter(commande=request.POST.get('numbon'),userr_id=request.user.id)
				if bon:
					bon=bon.first()
				else:
					bon=Fcommande.objects.create(
						commande=request.POST.get('numbon'),
						datejour=request.POST.get('datebon'),
                        tiers_id=request.POST.get('fournisseur'),
                        # typecommande = request.POST.get('mode'),
                        location_id=request.POST.get('location'),
						userr_id=request.user.id,)
                resultat1=0 
                resultat2=0
                idemb=""
                art=Farticle.objects.get(article=request.POST.get('produit'))

                if request.POST.get('emballage')=="1":
                    resultat1=request.POST.get('qte')
                    resultat2=float(request.POST.get('qte'))*art.quantitee
                    idemb=art.emballagee_id
                elif request.POST.get('emballage')=="2":
                    resultat2=request.POST.get('qte')
                    resultat1=float(request.POST.get('qte'))/art.quantitee
                    idemb=art.emballageu_id


                b= Fdetcde.objects.filter(commande__commande=request.POST.get('numbon'),article_id=request.POST.get('produit'))
                if b:

                	b.update(
                		quantite = request.POST.get('qte')
                	)
                else:
                	Fdetcde.objects.create(
                	commande=bon,
                	article_id=request.POST.get('produit'),
                	quantite = resultat1
                    qteunitaire = resultat2
                )
				return JsonResponse(
					{"msg": "Opération effectuée",
					 "id": "1"}, safe=False)
		except Exception as e:
			return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)

	context['numbon'] = "BCD" + str(Fcommande.objects.count() + 1) + str(datetime.today().date()).replace("-", "")
	return render(request, 'gestionstock/boncommande.html', context)
def facture(request):

    context = {"produit": Farticle.objects.all().order_by('designation'),
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


def annulercommande(request):

    if request.method == "POST":

        try:
            with transaction.atomic():

                bon=Fcommande.objects.filter(commande=request.POST.get('numbon'))
                if bon:
                    b= Fdetcde.objects.filter(commande__commande=request.POST.get('numbon'))
                    if b:
                        b.delete()
                    bon.delete()

                return JsonResponse(
                    {"msg": "Opération effectuée",
                     "id": "1","bon":"BCD" + str(Fcommande.objects.count() + 1) + str(datetime.today().date()).replace("-", "")}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)

def transfert(request):

    context = {"article": Farticle.objects.all().order_by('designation'),
			   "location": Flocation.objects.filter(typelocation="D",location=request.session["idlocationuser"]).order_by('designation'),
			   "locationb": Flocation.objects.all().exclude(location=request.session["idlocationuser"]).order_by('designation'),
			   }
    if request.method == "POST":
        try:

            with transaction.atomic():
                Fmvts.objects.create(
                location_id=request.POST.get('location'),
                datemvt=request.POST.get('dateop'),
                ndatemvt=str(request.POST.get('dateop')).replace("-", "").replace("/", ""),

                ajustement_id="TRTO",
                article_id=request.POST.get('produit'),
                qte_sortie=request.POST.get('qtet'),
                    document=request.POST.get('numtrans'),
                # prix_achat=request.POST.get('pa'),
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
                    document=request.POST.get('numtrans'),
                    ajustement_id="TRFR",
                    article_id=request.POST.get('produit'),
                    qte_sortie=request.POST.get('qtet'),
                    # prix_achat=request.POST.get('pa'),
                    # prix_vente=request.POST.get('privente'),
                    # devise=request.POST.get('devise'),
                    # txchange=str(request.POST.get('taux')).replace(",", "."),
                    codeuser_id=request.user.id,
                )
            return JsonResponse({"msg": "Opération effectuée ", "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)
    context['numtrans'] = "TRF" + str(Fmvts.objects.filter(location_id=request.session["idlocationuser"],ajustement_id="TRTO").count() + 1) + str(datetime.today().date()).replace("-", "")
    return render(request, 'gestionstock/transfert.html', context)


def retour(request):
    context = {"article": Farticle.objects.all().order_by('designation'),
               "location": Flocation.objects.filter(location=request.session["idlocationuser"]).exclude(typelocation="D").order_by('designation'),
               "locationb": Flocation.objects.filter(typelocation="D").order_by(
                   'designation'),
               }
    if request.method == "POST":
        try:

            with transaction.atomic():
                Fmvts.objects.create(
                    location_id=request.POST.get('location'),
                    datemvt=request.POST.get('dateop'),
                    ndatemvt=str(request.POST.get('dateop')).replace("-", "").replace("/", ""),

                    ajustement_id="TRTO",
                    article_id=request.POST.get('produit'),
                    qte_sortie=request.POST.get('qtet'),
                    document=request.POST.get('numtrans'),
                    # prix_achat=request.POST.get('pa'),
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
                    document=request.POST.get('numtrans'),
                    ajustement_id="TRFR",
                    article_id=request.POST.get('produit'),
                    qte_sortie=request.POST.get('qtet'),
                    # prix_achat=request.POST.get('pa'),
                    # prix_vente=request.POST.get('privente'),
                    # devise=request.POST.get('devise'),
                    # txchange=str(request.POST.get('taux')).replace(",", "."),
                    codeuser_id=request.user.id,
                )
            return JsonResponse({"msg": "Opération effectuée ", "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)
    context['numretour'] = "RT" + str(
        Fmvts.objects.filter(location_id=request.session["idlocationuser"], ajustement_id="TRTO").count() + 1) + str(
        datetime.today().date()).replace("-", "")
    return render(request, 'gestionstock/retour.html',context)




@login_required
# @permission_required('banking.Consultations',raise_exception=True)#echange
def getboncommande(request):
	rec = Fdetcde.objects.filter(commande=request.GET.get('bon')).values(
            "id","article__designation","quantite","commande__tiers__nompostnom","commande__datejour","qte_livree","commande__location__designation"
        ).order_by('-id')
	rec=list(rec)
	return JsonResponse({'data': rec}, safe=False)


@login_required
def getfacture(request):
	rec = Fmvts.objects.filter(document=request.GET.get('numtrans'),ajustement_id="TRFR",location_id=request.GET.get('locationbis'),ndatemvt=str(request.GET.get('dateop')).replace("-", "").replace("/", "")).values(
            "mvt","article__designation","qte_sortie","datemvt","location__designation").order_by('-mvt')
	rec=list(rec)
	return JsonResponse({'data': rec}, safe=False)

@login_required
def getfacture2(request):
	rec = Fmvts.objects.filter(document=request.GET.get('numretour'),ajustement_id="TRFR",location_id=request.GET.get('locationbis'),ndatemvt=str(request.GET.get('dateop')).replace("-", "").replace("/", "")).values(
            "mvt","article__designation","qte_sortie","datemvt","location__designation").order_by('-mvt')
	rec=list(rec)
	return JsonResponse({'data': rec}, safe=False)


@login_required
def getfacture3(request):
	rec = Fmvts.objects.filter(document=request.GET.get('numfact'),ajustement_id="FACT",location_id=request.session.get('idlocationuser'),ndatemvt=str(request.GET.get('dateop')).replace("-", "").replace("/", "")).values(
            "mvt","article__designation","emballage__emballage","qte_sortie","datemvt","prix_vente").order_by('-mvt')
	rec=list(rec)
	return JsonResponse({'data': rec}, safe=False)


@login_required
def getproduit(request):
    if "id" in request.GET:
        rec = Farticle.objects.filter(article=request.GET.get('id')).values(
       "article","designation","famille__famille","classe__classe","numcompte","categorie","qte_stock_minimal","emballagee__emballage","emballageu__emballage","quantiteu","quantitee","qte_stock_minimal").order_by('designation')
    else:
        rec = Farticle.objects.all().values(
            "article","designation","famille__designation","classe__designation","emballagee__designation","emballageu__designation","qte_stock_minimal").order_by('designation')
    rec=list(rec)
    return JsonResponse({'data': rec}, safe=False)


@require_POST
@login_required
def saveqte(request):

    b=Fdetcde.objects.get(id=request.POST.get('id'))
    if b:
        try:
            with transaction.atomic():

                if request.POST.get('cmp')=="1":
                    if b.qte_livree:
                        b.qte_livree=int(b.qte_livree)+int(request.POST.get('qte'))
                    else:
                        b.qte_livree = request.POST.get('qte')
                    b.save()

                else:
                    b.qte_livree = request.POST.get('qte')
                    b.save()



                b.commande.observation=request.POST.get('commentaire')
                b.commande.serielivraison=request.POST.get('mode')
                b.commande.save()
                aj=Fajustement.objects.get(ajustement="ACH")
                # p = int(str(request.POST.get('dateop'))[5:7])
                #
                # if p < 9:
                #     p = str(p).replace("0", "")
                # p = int(p)
                Fmvts.objects.create(
                location_id=b.commande.location.location,
                # periode=p,
                datemvt=request.POST.get('dateop'),
                ndatemvt=str(request.POST.get('dateop')).replace("-","").replace("/",""),
                requisition=request.POST.get('numbonentre'),
                document=request.POST.get('numbonlivre'),
                ajustement_id=aj.ajustement,
                tiers_id=b.commande.tiers.tiers,
                article_id=b.article.article,
                quantite=request.POST.get('qte'),
                qte_entree=request.POST.get('qte'),
                prix_achat=request.POST.get('pa'),
                prix_vente=request.POST.get('privente'),
                devise=request.POST.get('devise'),
                txchange=str(request.POST.get('taux')).replace(",","."),
                codeuser_id=request.user.id,
                )

                art=Farticle.objects.get(article=b.article.article)
                art.prix_vente=request.POST.get('privente')
                art.prix_achat=request.POST.get('pa')
                art.save()
                return JsonResponse({"msg": "Opération effectuée ", "id": "1"}, safe=False)
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée " + str(e), "id": "0"}, safe=False)
    else:
        return JsonResponse({"msg": "Opération non effectuée ", "id": "0"}, safe=False)

@require_POST
@login_required
def getqte(request):

    b = Fmvts.objects.filter(location_id=request.POST.get('location'),article_id=request.POST.get('produit'),ajustement_id__in=("ACH","PAT","TRFR")).aggregate(Sum("qte_entree")).get("qte_entree__sum")
    if b is None:#entrer
        b = 0
    c = Fmvts.objects.filter(location_id=request.POST.get('location'), article_id=request.POST.get('produit'),
                             ajustement_id__in=("VTE", "TRTO", "FACT","DECL")).aggregate(Sum("qte_sortie")).get("qte_sortie__sum")
    if c is None:  # sortie
        c = 0

    tot=b-c
    return JsonResponse({"tot": tot}, safe=False)

@require_POST
@login_required
def ajoutfournisseur(request):

    cmp=Ftiers.objects.all().count()+1
    Ftiers.objects.create(tiers=cmp
        ,nompostnom=request.POST.get('nom')
        ,nature="FOURNISSEUR"
        ,raisonsoc=request.POST.get('raison')
        ,idnational=request.POST.get('idnat')
        ,adresse=request.POST.get('adresse')
        )
    return JsonResponse({"msg": "Opération effectuée ", "id": "1","idfou":cmp,"nom":request.POST.get('nom')}, safe=False)

@require_POST
@login_required
def getqteproduitfacture(request):

    if request.POST.get('ctrl')=="0":

        b = Fmvts.objects.filter(location_id=request.session.get('idlocationuser'),article_id=request.POST.get('produit'),ajustement_id__in=("ACH","PAT","TRFR")).aggregate(Sum("qte_entree")).get("qte_entree__sum")
        if b is None:#entrer
            b = 0
        c = Fmvts.objects.filter(location_id=request.session.get('idlocationuser'), article_id=request.POST.get('produit'),
                                 ajustement_id__in=("VTE", "TRTO", "FACT","DECL")).aggregate(Sum("qte_sortie")).get("qte_sortie__sum")
        if c is None:  # sortie
            c = 0

        tot=b-c
        #--------------------------------------------
        emb=Farticle.objects.filter(article=request.POST.get('produit')).values('emballagee_id','emballageu_id','emballageu__designation',
                                                                                'emballagee__designation')

        prix=Farticle.objects.get(article=request.POST.get('produit'))


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
            prix = Farticle.objects.get(article=request.POST.get('produit'))

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
            emb = Farticle.objects.get(article=request.POST.get('produit'))

            return JsonResponse({"tot": (tot*emb.quantitee),"prix":emb.prix_vente}, safe=False)




