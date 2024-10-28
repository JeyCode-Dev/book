from django.db import models
from gestionstock.models import Farticle
from parametrage.models import Flocation,CustomUser

class TimespantedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True




#
# class Fmvts(TimespantedModel):
#     mvt = models.AutoField(db_column='MVT', primary_key=True)  # Field name made lowercase.
#     location = models.CharField(db_column='LOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
#     periode = models.CharField(db_column='PERIODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
#     datemvt = models.CharField(db_column='DATEMVT', max_length=20, blank=True, null=True)  # Field name made lowercase.
#     ndatemvt = models.FloatField(db_column='NDATEMVT', blank=True, null=True)  # Field name made lowercase.
#     bordereau = models.CharField(db_column='BORDEREAU', max_length=25, blank=True, null=True)  # Field name made lowercase.
#     requisition = models.CharField(db_column='REQUISITION', max_length=25, blank=True, null=True)  # Field name made lowercase.
#     document = models.CharField(db_column='DOCUMENT', max_length=50, blank=True, null=True)  # Field name made lowercase.
#     reference = models.CharField(db_column='REFERENCE', max_length=25, blank=True, null=True)  # Field name made lowercase.
#     ajustement = models.CharField(db_column='AJUSTEMENT', max_length=15, blank=True, null=True)  # Field name made lowercase.
#     imputation = models.CharField(db_column='IMPUTATION', max_length=255, blank=True, null=True)  # Field name made lowercase.
#     tiers = models.CharField(db_column='TIERS', max_length=50, blank=True, null=True)  # Field name made lowercase.
#     facture = models.CharField(db_column='FACTURE', max_length=25, blank=True, null=True)  # Field name made lowercase.
#     article = models.CharField(db_column='ARTICLE', max_length=8, blank=True, null=True)  # Field name made lowercase.
#     famille = models.CharField(db_column='FAMILLE', max_length=50, blank=True, null=True)  # Field name made lowercase.
#     classe = models.CharField(db_column='CLASSE', max_length=50, blank=True, null=True)  # Field name made lowercase.
#     designation = models.CharField(db_column='DESIGNATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
#     emballage = models.CharField(db_column='EMBALLAGE', max_length=50, blank=True, null=True)  # Field name made lowercase.
#     quantite = models.FloatField(db_column='QUANTITE', blank=True, null=True)  # Field name made lowercase.
#     qte_entree = models.FloatField(db_column='QTE_ENTREE', blank=True, null=True)  # Field name made lowercase.
#     qte_sortie = models.FloatField(db_column='QTE_SORTIE', blank=True, null=True)  # Field name made lowercase.
#     qteunitaire = models.FloatField(db_column='QTEUNITAIRE', blank=True, null=True)  # Field name made lowercase.
#     qteunit_entree = models.FloatField(db_column='QTEUNIT_ENTREE', blank=True, null=True)  # Field name made lowercase.
#     qteunit_sortie = models.FloatField(db_column='QTEUNIT_SORTIE', blank=True, null=True)  # Field name made lowercase.
#     prix_achat = models.FloatField(db_column='PRIX_ACHAT', blank=True, null=True)  # Field name made lowercase.
#     pa = models.FloatField(db_column='PA', blank=True, null=True)  # Field name made lowercase.
#     prixachatgros = models.FloatField(db_column='PRIXACHATGROS', blank=True, null=True)  # Field name made lowercase.
#     prix_vente = models.FloatField(db_column='PRIX_VENTE', blank=True, null=True)  # Field name made lowercase.
#     prix_vente_reel = models.FloatField(db_column='PRIX_VENTE_REEL', blank=True, null=True)  # Field name made lowercase.
#     prix_total = models.FloatField(db_column='PRIX_TOTAL', blank=True, null=True)  # Field name made lowercase.
#     prix_base = models.FloatField(db_column='PRIX_BASE', blank=True, null=True)  # Field name made lowercase.
#     pvcdf = models.FloatField(db_column='PVCDF', blank=True, null=True)  # Field name made lowercase.
#     pvusd = models.FloatField(db_column='PVUSD', blank=True, null=True)  # Field name made lowercase.
#     devise = models.CharField(db_column='DEVISE', max_length=20, blank=True, null=True)  # Field name made lowercase.
#     txchange = models.FloatField(db_column='TXCHANGE', blank=True, null=True)  # Field name made lowercase.
#     description = models.CharField(db_column='DESCRIPTION', max_length=100, blank=True, null=True)  # Field name made lowercase.
#     flag = models.CharField(db_column='FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.
#     destination = models.CharField(db_column='DESTINATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
#     txremise = models.FloatField(db_column='TXREMISE', blank=True, null=True)  # Field name made lowercase.
#     remise = models.FloatField(db_column='REMISE', blank=True, null=True)  # Field name made lowercase.
#     remisecdf = models.FloatField(db_column='REMISECDF', blank=True, null=True)  # Field name made lowercase.
#     txtaxe = models.FloatField(db_column='TXTAXE', blank=True, null=True)  # Field name made lowercase.
#     taxe = models.FloatField(db_column='TAXE', blank=True, null=True)  # Field name made lowercase.
#     taxecdf = models.FloatField(db_column='TAXECDF', blank=True, null=True)  # Field name made lowercase.
#     prixnet = models.FloatField(db_column='PrixNet', blank=True, null=True)  # Field name made lowercase.
#     prixnetcdf = models.FloatField(db_column='PrixNetCDF', blank=True, null=True)  # Field name made lowercase.
#     prixnetusd = models.FloatField(db_column='PrixNetUSD', blank=True, null=True)  # Field name made lowercase.
#     indrepare = models.IntegerField(db_column='INDREPARE', blank=True, null=True)  # Field name made lowercase.
#     indvalide = models.IntegerField(db_column='INDVALIDE', blank=True, null=True)  # Field name made lowercase.
#     codesocie = models.CharField(db_column='CODESOCIE', max_length=3, blank=True, null=True)  # Field name made lowercase.
#     prixvteunit = models.FloatField(db_column='PrixVteUnit', blank=True, null=True)  # Field name made lowercase.
#     prixvteunitusd = models.FloatField(db_column='PrixVteUnitUSD', blank=True, null=True)  # Field name made lowercase.
#     prixvteunitcdf = models.FloatField(db_column='PrixVteUnitCDF', blank=True, null=True)  # Field name made lowercase.
#     isused = models.BooleanField(db_column='IsUsed', blank=True, null=True)  # Field name made lowercase.
#     stckused = models.FloatField(db_column='StckUsed', blank=True, null=True)  # Field name made lowercase.
#     codeuser = models.CharField(db_column='CodeUser', max_length=10, blank=True, null=True)  # Field name made lowercase.
#     table = models.CharField(max_length=255, blank=True, null=True)
#     serveur = models.CharField(max_length=255, blank=True, null=True)
#     utilisateur = models.CharField(max_length=255, blank=True, null=True)
#
#     #objects = UserManager()
#
#     def __str__(self):
#         return str(self.created_at) +" "+ str(self.imputation)
#
#     class Meta:
#         unique_together = ('ndatemvt', 'document','article')
#
#
#
#
# class Tattente(TimespantedModel):
#     id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
#     client = models.CharField(db_column='Client', max_length=50, blank=True, null=True)  # Field name made lowercase.
#     monnaie = models.CharField(db_column='Monnaie', max_length=3, blank=True, null=True)  # Field name made lowercase.
#     taux = models.FloatField(db_column='Taux', blank=True, null=True)  # Field name made lowercase.
#     mode = models.CharField(db_column='Mode', max_length=10, blank=True, null=True)  # Field name made lowercase.
#     article = models.CharField(db_column='Article', max_length=12, blank=True, null=True)  # Field name made lowercase.
#     designation = models.CharField(db_column='Designation', max_length=50, blank=True, null=True)  # Field name made lowercase.
#     emb = models.CharField(db_column='Emb', max_length=4, blank=True, null=True)  # Field name made lowercase.
#     qte = models.FloatField(db_column='Qte', blank=True, null=True)  # Field name made lowercase.
#     puht = models.FloatField(db_column='PUHT', blank=True, null=True)  # Field name made lowercase.
#     ptht = models.FloatField(db_column='PTHT', blank=True, null=True)  # Field name made lowercase.
#     pu = models.FloatField(db_column='Pu', blank=True, null=True)  # Field name made lowercase.
#     qteunit = models.FloatField(db_column='QTeUnit', blank=True, null=True)  # Field name made lowercase.
#     tauxremise = models.FloatField(db_column='Tauxremise', blank=True, null=True)  # Field name made lowercase.
#     remise = models.FloatField(db_column='Remise', blank=True, null=True)  # Field name made lowercase.
#     tauxtaxe = models.FloatField(db_column='TauxTaxe', blank=True, null=True)  # Field name made lowercase.
#     taxe = models.FloatField(db_column='Taxe', blank=True, null=True)  # Field name made lowercase.
#     indsuspect = models.IntegerField(db_column='Indsuspect', blank=True, null=True)  # Field name made lowercase.
#     colnet = models.FloatField(db_column='ColNet', blank=True, null=True)  # Field name made lowercase.
#     prixachat = models.FloatField(db_column='PrixAchat', blank=True, null=True)  # Field name made lowercase.
#     qtee = models.FloatField(db_column='Qtee', blank=True, null=True)  # Field name made lowercase.
#     ptttc = models.FloatField(db_column='PTTTC', blank=True, null=True)  # Field name made lowercase.
#     pvreel = models.FloatField(db_column='PVReel', blank=True, null=True)  # Field name made lowercase.
#     location = models.CharField(db_column='Location', max_length=10, blank=True, null=True)  # Field name made lowercase.
#     facture = models.CharField(db_column='Facture', max_length=25, blank=True, null=True)  # Field name made lowercase.
#     famille = models.CharField(db_column='Famille', max_length=50, blank=True, null=True)  # Field name made lowercase.
#     datemvt = models.DateTimeField(db_column='DateMvt', blank=True, null=True)  # Field name made lowercase.
#     classe = models.CharField(db_column='Classe', max_length=50, blank=True, null=True)  # Field name made lowercase.
#     table = models.ForeignKey('TableRestaurent', on_delete=models.SET_NULL, null=True)
#     serveur = models.ForeignKey('Serveur', on_delete=models.SET_NULL, null=True)



#-------------------------------------------------------------------------------------------------------------------
class Recettes(models.Model):
    pu = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    embpu = models.CharField(max_length=50, blank=True, null=True)
    qte = models.IntegerField(default=0,blank=True, null=True)
    pu2 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    embpu2 = models.CharField(max_length=50, blank=True, null=True)
    qte2 = models.IntegerField(default=0, blank=True, null=True)
    pu3 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    embpu3 = models.CharField(max_length=50, blank=True, null=True)
    qte3 = models.IntegerField(default=0, blank=True, null=True)
    article = models.ForeignKey(Farticle, on_delete=models.SET_NULL, null=True)




class SessionNumero(models.Model):
    numero = models.CharField(max_length=200,unique=True)
    txt=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SessionUser(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    dateop = models.DateField()
    etat=models.BooleanField(default=False)

class Droit(models.Model):
    class Meta:
        permissions = (
            ('recettesrapport', 'Rapport Vente Journalieres'),
            ('recettesrapportsys', 'Synthèse Vente'),
            ('validation_facture', 'Validation Facture'),
            ('facturation', 'Facturation'),
            ('reimprimer', 'Reimprimer Facture'),
            ('annulation', 'Annuler Facture'),
            ('createrecette', 'Création Recettes'),
            ('createcatrecette', 'Création Categorie Recettes'),
            ('dashboard', 'Voir Tableau de Bord'),
            ('transferttable', 'Transfert Table'),
            ('transfertserveur', 'Transfert Serveur'),
            ('transfertcompte', 'Transfert Compte'),
            ('transfertproduit', 'Transfert Produit'),
            ('sessionuser', 'Session User'),
            ('liste', 'Brouillard User'),
            ('recettesrapportprofit', 'Rapport Profil'),

        )

