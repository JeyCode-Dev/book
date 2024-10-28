from django.db import models
from gestionstock.models import Femballage,Ffamilles
# Create your models here.
from parametrage.models import CustomUser,Flocation,CategorieArticle,TimespantedModel
from django.utils import timezone
cat_medical=(
    ('L', 'Local'),
    ('E', 'Externe'),
)

devise = (
     ('USD', 'USD'),
    ('FC', 'FC'),
)

sexe = (
     ('M', 'MASCULIN'),
    ('F', 'FEMININ'),
)
statuts = (
     ('A', 'AGENT'),
    ('E', 'EXTERNE'),
)
etat = (
     ('C', 'CELIBATAIRE'),
    ('M', 'MARIEE'),
)



class TimespantedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

class Patient(TimespantedModel):
    date = models.DateField(blank=True, null=True,default=timezone.now)
    nom = models.CharField(db_column='NOM', max_length=50,blank=True, null=True)
    sexe = models.CharField(db_column='SEXE', max_length=50,blank=True, null=True)
    statut = models.CharField(db_column='STATUT', max_length=50, blank=True, null=True)
    date_nais = models.CharField( max_length=50,blank=True, null=True)
    etat_civil = models.CharField(db_column='ETATCIVIL', max_length=50,blank=True, null=True)
    adresse = models.CharField(db_column='ADRESSE', max_length=50,blank=True, null=True)
    telephone = models.CharField(db_column='TELEPHONE',max_length=50,blank=True, null=True)
    taille = models.CharField(max_length=50,blank=True, null=True)
    email =  models.CharField(max_length=50,blank=True, null=True)

    class Meta:
        verbose_name = ("Patient")
        verbose_name_plural = ("Patients")

    def __str__(self):
        return self.nom
    

class Consultation(TimespantedModel):
    numeFiche = models.CharField(max_length=50,blank=True, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL,null=True,blank=True)
    #user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    temperature = models.CharField(max_length=50,blank=True, null=True)
    tention = models.CharField(max_length=50,blank=True, null=True)
    poids = models.CharField(max_length=50,blank=True, null=True)
    

    def __str__(self):
            return self.patient

class Diagnostique(TimespantedModel):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL,null=True,blank=True)
    diagnostique = models.CharField(max_length=1000,blank=True, null=True)
    
    def __str__(self):
            return self.patient
