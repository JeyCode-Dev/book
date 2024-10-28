from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TimespantedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

# class Monnaie(TimespantedModel):
#     libelle=models.CharField(max_length=255,unique=True)

#     def __str__(self):
#         return "Devise " + self.libelle
# class Emballage(TimespantedModel):
#     libelle=models.CharField(max_length=255,unique=True)

#     def __str__(self):
#         return "Emballage " + self.libelle
# class FamilleArticle(TimespantedModel):
#     libelle=models.CharField(max_length=255,unique=True)

#     def __str__(self):
#         return "Famille Article " + self.libelle
# class ClasseArticle(TimespantedModel):
#     code=models.CharField(max_length=255,unique=True)
#     libelle=models.CharField(max_length=255,unique=True)

#     def __str__(self):
#         return "Classe Article " + self.libelle

# sorte = (
#         ('E', 'Entre'),
#         ('S', 'Sortie'),

#  )
# class CodeOperation(TimespantedModel):
#     code=models.CharField(max_length=255,unique=True)
#     libelle=models.CharField(max_length=255,unique=True)
#     type = models.CharField(max_length=1, choices=sorte)

#     def __str__(self):
#         return "Code Operation Article " + self.libelle
# class Magasin(TimespantedModel):
#     designation=models.CharField(max_length=255)
#     adresse=models.CharField(max_length=255)
#     depotcentral = models.BooleanField(default=False)
#     taux = models.DecimalField(max_digits=20, decimal_places=2, default=0)
#     caissecdf = models.CharField(max_length=6)
#     caisseusd = models.CharField(max_length=6)

#     def __str__(self):
#         return "Magasin " + self.designation
# class Article(TimespantedModel):
#     numcompt = models.CharField(max_length=255)
#     designation=models.CharField(max_length=255,unique=True)
#     famille=models.ForeignKey(FamilleArticle,on_delete=models.SET_NULL,null=True)
#     classe=models.ForeignKey(ClasseArticle,on_delete=models.SET_NULL,null=True)
#     avectaxe = models.BooleanField(default=False)
#     seuil = models.IntegerField(default=1)
#     emballageachat = models.ForeignKey(Emballage, on_delete=models.SET_NULL, null=True)
#     emballagevente = models.ForeignKey(Emballage,related_name="emballageventearticle", on_delete=models.SET_NULL, null=True)
#     qteemballageachat = models.DecimalField(max_digits=20, decimal_places=2, default=0)
#     qteemballagevente = models.DecimalField(max_digits=20, decimal_places=2, default=0)

#     def __str__(self):
#         return "Article " + self.designation

# categorie = (
#         ('F', 'Fournisseur'),
#         ('C', 'Client'),

#  )
# class FournisseurClient(TimespantedModel):
#     noms = models.CharField(max_length=255)
#     adresse=models.CharField(max_length=255)
#     raisonsocial=models.CharField(max_length=255)
#     idnation=models.CharField(max_length=255)
#     numcompt=models.CharField(max_length=255)
#     type=models.CharField(max_length=1,choices=categorie)

#     def __str__(self):
#         return "Fournisseur/Client " + self.noms

# applic = (
#         ('oui', 'Oui'),
#         ('non', 'Non'),

#  )
# class Taux(TimespantedModel):
#     dateop = models.DateField(unique=True)
#     taux= models.DecimalField(max_digits=20, decimal_places=2, default=0)

#     def __str__(self):
#         return "Taux " + str(self.dateop) +" => "+str(self.taux)
# class Taxe(TimespantedModel):
#     designation = models.CharField(max_length=255)
#     taux = models.ForeignKey(Taux, on_delete=models.SET_NULL, null=True)
#     applicable=models.CharField(max_length=3,choices=applic)

#     def __str__(self):
#         return "Taxe " + self.designation

# modeachat = (
#         ('c', 'Comptant'),
#         ('r', 'Crédit'),
#         ('t', 'transfert'),
#         ('s', 'retour'),

#  )
# class BonCommande(TimespantedModel):
#     numbon = models.CharField(max_length=255,unique=True)
#     datebon=models.DateField()


#     # article = models.ManyToManyField(Article,through='BonCommandeArticle')
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     # article = models.ManyToManyField(Article, related_name='articlecommander', null=True, blank=True)


# class Facture(TimespantedModel):
#     numfac = models.CharField(max_length=255,unique=True)
#     datefac=models.DateField()
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

# class FactureArticle(models.Model):
#     article = models.ForeignKey(Article, models.SET_NULL, null = True, blank = True)
#     taux = models.ForeignKey(Taux, on_delete=models.SET_NULL, null=True)
#     magasinc = models.ForeignKey(Magasin,related_name="magasinmere", on_delete=models.SET_NULL, null=True)
#     magasins = models.ForeignKey(Magasin, on_delete=models.SET_NULL, null=True)
#     facture = models.ForeignKey(Facture, models.SET_NULL, null = True, blank = True)
#     commentaire = models.CharField(max_length=255, null=True, blank=True)
#     mode = models.CharField(max_length=1, choices=modeachat)
#     qte = models.IntegerField()
#     prix = models.DecimalField(max_digits=20, decimal_places=2,default=0)

# class BonCommandeArticle(models.Model):
#     article = models.ForeignKey(Article, models.SET_NULL, null = True, blank = True)
#     taux = models.ForeignKey(Taux, on_delete=models.SET_NULL, null=True)
#     magasin = models.ForeignKey(Magasin, on_delete=models.SET_NULL, null=True)
#     boncommande = models.ForeignKey(BonCommande, models.SET_NULL, null = True, blank = True)
#     fournisseur = models.ForeignKey(FournisseurClient, on_delete=models.SET_NULL, null=True)
#     commentaire = models.CharField(max_length=255, null=True, blank=True)
#     mode = models.CharField(max_length=1, choices=modeachat)
#     qtecmd = models.IntegerField()
#     qtelivre = models.IntegerField(default=0)
#     # fraisacha = models.DecimalField(max_digits=20, decimal_places=2)


# class BonLivraison(TimespantedModel):
#     numliv = models.CharField(max_length=255,unique=True)
#     dateliv=models.DateField()
#     taux = models.ForeignKey(Taux, on_delete=models.SET_NULL, null=True)
#     boncommande = models.ForeignKey(BonCommande, on_delete=models.SET_NULL, null=True)
#     commentaire = models.CharField(max_length=255, null=True, blank=True)
#     article = models.ManyToManyField(Article,through='BonLivraisonArticle')
#     # article = models.ManyToManyField(Article, related_name='articlecommander', null=True, blank=True)


# class BonLivraisonArticle(models.Model):
#     article = models.ForeignKey(Article, models.SET_NULL, null = True, blank = True)
#     bonlivraison = models.ForeignKey(BonLivraison, models.SET_NULL, null = True, blank = True)
#     qtelivre = models.IntegerField()
#     puaht = models.DecimalField(max_digits=20, decimal_places=2)
#     # fraisacha = models.DecimalField(max_digits=20, decimal_places=2)


# class BonSorti(TimespantedModel):
#     numsorti = models.CharField(max_length=255,unique=True)
#     datesorti=models.DateField()
#     magasininit = models.ForeignKey(Magasin, on_delete=models.SET_NULL,related_name="sortiinitmagasin", null=True)
#     magasindest = models.ForeignKey(Magasin, on_delete=models.SET_NULL, null=True)
#     commentaire = models.CharField(max_length=255, null=True, blank=True)
#     article = models.ManyToManyField(Article,through='BonSortiArticle')


# class BonSortiArticle(models.Model):
#     article = models.ForeignKey(Article, models.SET_NULL, null = True, blank = True)
#     bonsorti = models.ForeignKey(BonSorti, models.SET_NULL, null = True, blank = True)
#     qtesorti = models.IntegerField()
#     # fraisacha = models.DecimalField(max_digits=20, decimal_places=2)