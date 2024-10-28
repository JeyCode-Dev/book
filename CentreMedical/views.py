from django.shortcuts import render
from django.db import transaction
from gestionstock.models import Femballage,Ffamilles,Farticle,Fclasse,etatbesoin,Fmvts
from gestionstock.views import random_char
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required,permission_required
from .models import *
import shortuuid as shortuuid
from pyreportjasper import JasperPy
from datetime import datetime, timedelta
import os
import random
from django.views import View
import json
from django.db.models import Sum, F, Value, Count, Q,CharField
from django.utils import timezone
# Create your views here.
@login_required
def produit(request):

    if request.method == "POST":
            print(request.POST)
            with transaction.atomic():
                if 'delete_' in request.POST:
                    Farticle.objects.filter(article=request.POST.get('idpro')).delete()
                else:

                    art=Farticle.objects.filter(article=request.POST.get('idpro'),LOCATION_id=request.session.get('idlocationuser'))

                    #pa=miseajourprix(f.article.article,f.emballage_id,request.POST.get('prix'),floc)


                    if request.POST.get('devise') == 'CDF':
                        pa = float(request.POST.get('pa1')) / float(str(request.POST.get('taux')).replace(",", "."))
                        print(request.POST.get('pa1'))
                    else:
                        print('-------')
                        print(request.POST.get('pa1'))
                        pa = float(request.POST.get('pa1'))

                    ##prix_achat_petit=pa/float(request.POST.get('qte1'))


                    if art:
                        art.update(
                            famille_id=request.POST.get('famille'),
                            classe_id=request.POST.get('classe'),


                            #quantitee=request.POST.get('qte1'),
                            quantitea=0 if request.POST.get('qte3') == '' else request.POST.get('qte3'),
                            # quantiteu=0 if request.POST.get('qte2') == '' else request.POST.get('qte2'),
                            quantiteu=1,

                            emballagea=1, #None if request.POST.get('emballage3') == '' else request.POST.get('emballage3'),
                            emballagee_id=request.POST.get('emballage1'),
                            emballageu_id=None if request.POST.get('emballage2') == '' else request.POST.get(
                                'emballage2'),

                            #prix_vente=request.POST.get('pv1'),
                            #prix_vente_cdf=0 if request.POST.get('pv2') == '' else request.POST.get('pv2'),
                            #old_prix_vente=0 if request.POST.get('pv3') == '' else request.POST.get('pv3'),

                            prix_achat=request.POST.get('pa1'),
                            #pa=prix_achat_petit, #if request.POST.get('pa2') == '' else request.POST.get('pa2'),
                            #old_prix_achat=0 if request.POST.get('pa3') == '' else request.POST.get('pa3'),

                            #qte_stock_minimal=request.POST.get('seuil'),

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

                            #quantitee=request.POST.get('qte1'),
                            quantitea=0 if request.POST.get('qte3') == '' else request.POST.get('qte3'),
                            # quantiteu=0 if request.POST.get('qte2') == '' else request.POST.get('qte2'),
                            quantiteu=1,

                            emballagea=1, #None if request.POST.get('emballage3') == '' else request.POST.get('emballage3'),
                            emballagee_id=request.POST.get('emballage1'),
                            emballageu_id=None if request.POST.get('emballage2') == '' else request.POST.get('emballage2'),

                            prix_vente=request.POST.get('pv1'),
                            prix_vente_cdf=0 if request.POST.get('pv2') == '' else request.POST.get('pv2'),
                            old_prix_vente=0 if request.POST.get('pv3') == '' else request.POST.get('pv3'),

                            prix_achat=request.POST.get('pa1'),
                            #pa=prix_achat_petit,#if request.POST.get('pa2') == '' else request.POST.get('pa2'),
                            old_prix_achat=0 if request.POST.get('pa3') == '' else request.POST.get('pa3'),
                            # categorie=request.POST.get('categorie'),
                            designation=str(request.POST.get('designation')).upper()
                            ,LOCATION_id=request.session.get('idlocationuser')
                        )

                return JsonResponse(
                    {"msg": "Opération effectuée",
                    "id": "1"}, safe=False)
        


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
    return render(request, 'produit.html', context)


"""
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


                           

                            #emballagea=None if request.POST.get('emballage3') == '' else request.POST.get('emballage3'),
                            emballagee_id=request.POST.get('emballage1'),
                            #emballageu_id=None if request.POST.get('emballage2') == '' else request.POST.get('emballage2'),

                            prix_vente=request.POST.get('pv1'),
                            prix_vente_cdf=0 if request.POST.get('pv2') == '' else request.POST.get('pv2'),
                            #old_prix_vente=0 if request.POST.get('pv3') == '' else request.POST.get('pv3'),

                            prix_achat=request.POST.get('pa1'),
                            #pa=prix_achat_petit, #if request.POST.get('pa2') == '' else request.POST.get('pa2'),
                            #old_prix_achat=0 if request.POST.get('pa3') == '' else request.POST.get('pa3'),

                            #qte_stock_minimal=request.POST.get('seuil'),

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
                            #qte_stock_minimal=request.POST.get('seuil'),

                            #quantitee=request.POST.get('qte1'),
                            #quantitea=0 if request.POST.get('qte3') == '' else request.POST.get('qte3'),
                            # quantiteu=0 if request.POST.get('qte2') == '' else request.POST.get('qte2'),
                            quantiteu=1,

                            #emballagea=None if request.POST.get('emballage3') == '' else request.POST.get('emballage3'),
                            emballagee_id=request.POST.get('emballage1'),
                            #emballageu_id=None if request.POST.get('emballage2') == '' else request.POST.get('emballage2'),

                            prix_vente=request.POST.get('pv1'),
                            prix_vente_cdf=0 if request.POST.get('pv2') == '' else request.POST.get('pv2'),
                            #old_prix_vente=0 if request.POST.get('pv3') == '' else request.POST.get('pv3'),

                            prix_achat=request.POST.get('pa1'),
                            #pa=prix_achat_petit,#if request.POST.get('pa2') == '' else request.POST.get('pa2'),
                            #old_prix_achat=0 if request.POST.get('pa3') == '' else request.POST.get('pa3'),
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
    return render(request, 'produit2.html', context)
""" 

@login_required
def CreationPatient(request):
    
    pt = Patient.objects.all()
    context = {
        'liste': pt
    }
    if request.method == "POST" and request.POST.get('nom') and request.POST.get('adresse'):
        
        try:
           
            pt = Patient.objects.filter(nom=str(request.POST.get('nom'))).first()
            print('---------obj-----')
            print(pt)
            if pt:
                    print('--------IL EXISTE------------')
                    context['error'] = "Opération non effectuée ce patient existe déjà"
                    print(context['error'] )
                    #return JsonResponse({"msg": "Opération non effectuée cet utilisateur existe déjà "}, safe=False)
            else:
                    with transaction.atomic():
                        obj = Patient.objects.create(
                                nom =str(request.POST.get('nom')).upper(),
                                sexe = request.POST.get('sexe'),
                                statut = request.POST.get('statut'),
                                etat_civil = request.POST.get('etat'),
                                date_nais = request.POST.get('date'),
                                adresse =str( request.POST.get('adresse')).upper(),
                                telephone = request.POST.get('telephone'),
                                email = request.POST.get('email'),
                                taille = request.POST.get('taille')
                                )
                        print(obj.id)
                        print(obj.id)
                        print(datetime.today().date())
                        location = Flocation.objects.create(
                        location = obj.id,
                        designation = str(obj.nom).upper(),
                        typelocation = obj.statut,
                        datejour = datetime.today().date()
                        )        
                        
                        context['message'] = "opération éffectuée"
        except Exception as e:
            return JsonResponse({"msg": "Opération non effectuée "+str(e), "id": "0"}, safe=False)
            
    return render(request,'create_patient.html',context)
"""
def Ordonance(request):
    print('------ ordonance-------')
    if request.method=="POST":
        print('------ MESSAGE-------')
        p=0
        if 'idcode' in request.POST:
            print('------ ICODE-------')
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

                    print('------------------')
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
        "article": Farticle.objects.all(),
        "taux": Flocation.objects.get(location=request.session.get('idlocationuser')).txchange,
        "locations": Flocation.objects.filter(typelocation__in=['A', 'E']).order_by('designation'),
    }
    context['numtrans'] = "T" + str(request.session['idlocationuser']) + random_char(6)
    #context['numtrans'] = "T" + str(request.session['idlocationuser']) + random_char(6)

    return render(request,'ordonance.html', context)
"""
@login_required
def InsertDate(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
                # Charger les données JSON
                if request.method == "POST":
                    data = json.loads(request.body)
                    #pt = Patient.objects.get(id=1)
                    print('--------------------')
                    #print(list(data))
                    # Créer une nouvelle consultation
                    required_fields = ['num', 'id_patient', 'temperature', 'tension', 'poids']
                    for field in required_fields:
                        if field not in data or data[field] is None:
                            return JsonResponse({'error': f'{field} est requis.'}, safe=False)
                    if  data['id_patient']  is not None:
                            print("------------------------")
                            print(data['id_patient'])
                            consultation = Consultation.objects.create(
                                        numeFiche =data['num'],
                                        patient_id=data['id_patient'],
                                        temperature=data['temperature'],
                                        tention=data['tension'],
                                        poids=data['poids']
                                        ) 
                            print("donner------------ enregistrer")
                            #print(consultation)
                            return JsonResponse({'message': 'Signes Vitaux enregistrés avec succès!'},  safe=False)
            
        except Exception as e:
                return JsonResponse({'error': str(e)},  safe=False)
    else:
         return JsonResponse({'error': 'La requête doit être une requête AJAX.'},  safe=False)
    
@login_required
#@transaction.atomic
def Consult(request):
    tab = []
    c = Consultation.objects.all()
    date = timezone.now().date()
    
    for val in c:
        if val.created_at.date() == date:
             print(val.created_at.date())
             tab.append(val)
    
    context = {
        'tab': tab,
        'current_date': date
    } 
    try:
        if request.method == "POST":
           user = Patient.objects.get(id=str(request.POST.get('user_id')))
           diagnost = request.POST.get('diag')
           if user and diagnost:
            #print(user.nom)
                obj = Diagnostique.objects.create(
                                patient = user,
                                diagnostique = str(diagnost).upper() 
                            )
                context['message'] = "Opération réussit"
            #return JsonResponse({'msg': str(context['message'])}, safe=False)
    except Exception as e:
                return render(request, 'erreur.html', {'erreur_message': str(e)})
    
    

    return render(request,'consultation.html', context)


def getPatient(request):
    try: 
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                #Charger les données JSON
                if request.method == "GET":
                    resp = Patient.objects.get(id=str(request.GET.get('id')))
                    pt_consulter = Consultation.objects.filter(patient_id=resp.id).order_by('-id').first()
                    #print(pt_consulter)
                    nombre = Consultation.objects.all().count()
                    numfiche = "/".join(["CMBB",str(datetime.now().year)[-2:],str(f"00{nombre}")])
                    
                    tp = pt_consulter.temperature if pt_consulter else ""
                    tt = pt_consulter.tention if pt_consulter else ""
                    pd = pt_consulter.poids if pt_consulter else "" 

                    return JsonResponse({
                    'name': str(resp.nom),
                    'num': str(numfiche),
                    'tp': tp,
                    'tt': tt,
                    'pd': pd,
                    'msg': "Mis à jour de prélèvement du patient déjà éxistant"
                }, safe=False)
    except Exception as e:
            return JsonResponse({'error': str(e)}, safe=False)



@login_required
def fac(request):
        pass
        """ if request.method == 'POST':
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
 """
        #imprimer__________________________
        return HttpResponse("true")
    
@login_required
def GetConsultPatient(request):
    
    try: 
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                print(request.GET)
                # Charger les données JSON
                if request.method == "GET":
                    consult = Consultation.objects.get(id=str(request.GET.get('q')))
                    val = [
                        consult.patient.nom,
                        consult.patient.sexe,consult.patient.statut,
                        consult.temperature,
                        consult.poids,
                        consult.tention,
                        consult.patient.id,
                        consult.numeFiche
                        ]
                    if val:
                       return JsonResponse({'data': str(val), 'msg': 'Patient Trouvé'}, safe=False)
    except Exception as e:
            return JsonResponse({'error': str(e)}, safe=False)
    
   
@login_required
def Pharmacie(request):
    
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
    return render(request, 'pharmacie.html', context)

@login_required
def Ordonance(request):

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
        "locations": Flocation.objects.filter(typelocation__in=['A', 'E']).order_by('designation') #Flocation.objects.filter(typelocation='D').exclude(location=request.session.get('idlocationuser')).order_by('designation'),
    }
    context['numtrans'] = "/".join(["CMBB",str(datetime.now().year)[-2:],str(random_char(6))]) 
    return render(request, 'ordonance.html',context)


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
                
                print(f'val quantiteu: {pro.quantiteu}---- val quantitee: {pro.quantitee}---- val quantitea: {pro.quantitea}')
                b=b1+((pro.quantiteu/1.0)*b2)+((1.0/1.0)*b3)
                c=c1+((pro.quantiteu/1.0)*c2)+((1.0/1.0)*c3)
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