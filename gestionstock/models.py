# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


#relation article,classe,famille
#relation commdande( ajout champs userr),location,tiers
#relation detailcommande (ajout champs id),commande,article
from django.db import models

from parametrage.models import CustomUser,Flocation,CategorieArticle,TimespantedModel


class Femballage(models.Model):
    emballage = models.CharField("Code",db_column='EMBALLAGE', primary_key=True, max_length=4)  # Field name made lowercase.
    designation = models.CharField("Désignation",db_column='DESIGNATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    codesocie = models.CharField(db_column='CODESOCIE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    flag = models.CharField(db_column='FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):

        return self.designation
    class Meta:
        managed = False
        verbose_name="Unité"
        verbose_name_plural="Unités"
        db_table = 'FEMBALLAGE'
class Ftiers(models.Model):
    tiers = models.CharField(db_column='TIERS', primary_key=True, max_length=8)  # Field name made lowercase.
    nature = models.CharField(db_column='NATURE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    nompostnom = models.CharField(db_column='NOMPOSTNOM', max_length=50, blank=True, null=True)  # Field name made lowercase.
    raisonsoc = models.CharField(db_column='RAISONSOC', max_length=20, blank=True, null=True)  # Field name made lowercase.
    idnational = models.CharField(db_column='IDNATIONAL', max_length=20, blank=True, null=True)  # Field name made lowercase.
    adresse = models.CharField(db_column='ADRESSE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    typetiers = models.CharField(db_column='TYPETIERS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    origine = models.CharField(db_column='ORIGINE', max_length=25, blank=True, null=True)  # Field name made lowercase.
    compte = models.CharField(db_column='COMPTE', max_length=16, blank=True, null=True)  # Field name made lowercase.
    indinature = models.IntegerField(db_column='IndiNature', blank=True, null=True)  # Field name made lowercase.
    codesocie = models.CharField(db_column='CODESOCIE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ischeck = models.BooleanField(db_column='IsCheck', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FTIERS'


class Facces(models.Model):
    users = models.CharField(max_length=50, blank=True, null=True)
    codope = models.IntegerField(blank=True, null=True)
    droit = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'FACCES'


class Ffamilles(models.Model):
    famille = models.CharField("Code",db_column='FAMILLE',  primary_key=True ,max_length=4)  # Field name made lowercase.
    designation = models.CharField("Désignation",db_column='DESIGNATION', max_length=50)  # Field name made lowercase.
    flag = models.CharField(db_column='FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    codesocie = models.CharField(db_column='CODESOCIE', max_length=3, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):

        return self.designation

    class Meta:
        managed = False
        verbose_name="Famille Produit"
        verbose_name_plural="Familles Produits"
        db_table = 'FFAMILLES'



class Fajustement(models.Model):
    ajustement = models.CharField(db_column='AJUSTEMENT', max_length=4, primary_key=True)  # Field name made lowercase.
    designation = models.CharField(db_column='DESIGNATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mvt = models.CharField(db_column='MVT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag = models.CharField(db_column='FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pardefaut = models.CharField(db_column='PARDEFAUT', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FAJUSTEMENT'



class Fclasse(models.Model):
    classe = models.CharField(db_column='CLASSE',  primary_key=True,max_length=2)  # Field name made lowercase.
    designation = models.CharField("Désignation",db_column='DESIGNATION', max_length=50)  # Field name made lowercase.
    flag = models.CharField(db_column='FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    codesocie = models.CharField(db_column='CODESOCIE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    

    class Meta:
        managed = False
        verbose_name="Classe Produit"
        verbose_name_plural="Classes Produits"
        db_table = 'FCLASSE'






#EMBALLAGEE_ID=emb1
#EMBALLAGEU_ID=emb2
#EMBALLAGEA=emb3

#PRIX_ACHAT=prixachat1
#PA=prixachat2
#OLD_PRIX_ACHAT=prixachat3

#QUANTITEE=qte1
#QUANTITEU=qte2
#QUANTITEA=qte3

#PRIX_VENTE=prixvente1
#PRIX_VENTE_CDF=prixvente2
#OLD_PRIX_VENTE=prixvente3

#LIBEMBALLAGEE=Date Modification Prix


class Farticle(models.Model):
    article = models.CharField(db_column='ARTICLE', primary_key=True, max_length=8)  # Field name made lowercase.
    famille = models.ForeignKey(Ffamilles, on_delete=models.SET_NULL, null=True)
    classe = models.ForeignKey(Fclasse, on_delete=models.SET_NULL, null=True)
    # famille = models.CharField(db_column='FAMILLE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # classe = models.CharField(db_column='CLASSE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    numcompte = models.CharField(db_column='NUMCOMPTE', max_length=16, blank=True, null=True)  # Field name made lowercase.
    partnumber = models.CharField(db_column='PARTNUMBER', max_length=100, blank=True, null=True)  # Field name made lowercase.
    designation = models.CharField(db_column='DESIGNATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    emballagea = models.CharField(db_column='EMBALLAGEA', max_length=14, blank=True, null=True)  # Field name made lowercase.
    emballagee = models.ForeignKey(Femballage, on_delete=models.SET_NULL, null=True)
    emballageu = models.ForeignKey(Femballage,related_name="embalagearticle", on_delete=models.SET_NULL, null=True)
    # emballagee = models.CharField(db_column='EMBALLAGEE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # emballageu = models.CharField(db_column='EMBALLAGEU', max_length=50, blank=True, null=True)  # Field name made lowercase.
    libemballagea = models.CharField(db_column='LIBEMBALLAGEA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    libemballagee = models.CharField(db_column='LIBEMBALLAGEE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    libemballageu = models.CharField(db_column='LIBEMBALLAGEU', max_length=50, blank=True, null=True)  # Field name made lowercase.
    quantitea = models.FloatField(db_column='QUANTITEA', blank=True, null=True)  # Field name made lowercase.
    quantitee = models.FloatField(db_column='QUANTITEE', blank=True, null=True)  # Field name made lowercase.
    quantiteu = models.FloatField(db_column='QUANTITEU', blank=True, null=True)  # Field name made lowercase.
    specialite = models.BooleanField(db_column='SPECIALITE', blank=True, null=True)  # Field name made lowercase.
    fournisseur = models.CharField(db_column='FOURNISSEUR', max_length=8, blank=True, null=True)  # Field name made lowercase.
    nomfournisseur = models.CharField(db_column='NOMFOURNISSEUR', max_length=50, blank=True, null=True)  # Field name made lowercase.
    coefficient = models.FloatField(db_column='COEFFICIENT', blank=True, null=True)  # Field name made lowercase.
    old_prix_achat = models.FloatField(db_column='OLD_PRIX_ACHAT', blank=True, null=True)  # Field name made lowercase.
    old_prix_vente = models.FloatField(db_column='OLD_PRIX_VENTE', blank=True, null=True)  # Field name made lowercase.
    old_d_usd = models.FloatField(db_column='OLD_D_USD', blank=True, null=True)  # Field name made lowercase.
    old_prix_ventecdf = models.FloatField(db_column='OLD_PRIX_VENTECDF', blank=True, null=True)  # Field name made lowercase.
    old_d_cdf = models.FloatField(db_column='OLD_D_CDF', blank=True, null=True)  # Field name made lowercase.
    prix_achat = models.FloatField(db_column='PRIX_ACHAT', blank=True, null=True)  # Field name made lowercase.
    pa = models.FloatField(db_column='PA', blank=True, null=True)  # Field name made lowercase.
    prix_vente = models.FloatField(db_column='PRIX_VENTE', blank=True, null=True)  # Field name made lowercase.
    prix_vente_cdf = models.FloatField(db_column='PRIX_VENTE_CDF', blank=True, null=True)  # Field name made lowercase.
    prix_moyen = models.FloatField(db_column='PRIX_MOYEN', blank=True, null=True)  # Field name made lowercase.
    prixtot = models.FloatField(db_column='PRIXTOT', blank=True, null=True)  # Field name made lowercase.
    flag = models.CharField(db_column='FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prixrevientgro = models.FloatField(db_column='PRIXREVIENTGRO', blank=True, null=True)  # Field name made lowercase.
    prixachgro = models.FloatField(db_column='PRIXACHGRO', blank=True, null=True)  # Field name made lowercase.
    codesocie = models.CharField(db_column='CODESOCIE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    qte_stock_minimal = models.FloatField(db_column='QTE_STOCK_MINIMAL', blank=True, null=True)  # Field name made lowercase.
    prixvtegroscdf = models.FloatField(db_column='PRIXVTEGROSCDF', blank=True, null=True)  # Field name made lowercase.
    prixvtedetcdf = models.FloatField(db_column='PRIXVTEDETCDF', blank=True, null=True)  # Field name made lowercase.
    prixvtegrosusd = models.FloatField(db_column='PRIXVTEGROSUSD', blank=True, null=True)  # Field name made lowercase.
    prixvtedetusd = models.FloatField(db_column='PRIXVTEDETUSD', blank=True, null=True)  # Field name made lowercase.
    cpteach = models.CharField(db_column='CpteAch', max_length=15, blank=True, null=True)  # Field name made lowercase.
    cptestock = models.CharField(db_column='CpteStock', max_length=15, blank=True, null=True)  # Field name made lowercase.
    categorie = models.IntegerField(db_column='Categorie', blank=True, null=True)  # Field name made lowercase.
    TYPEARTICLE = models.CharField(db_column='TYPEARTICLE', max_length=15, blank=True, null=True)
    LOCATION = models.ForeignKey(Flocation, on_delete=models.SET_NULL, null=True)

    class Meta:
        managed = False
        db_table = 'FARTICLE'






class Fcours(models.Model):
    idcours = models.AutoField(db_column='IDCOURS', primary_key=True)  # Field name made lowercase.
    datej = models.CharField(db_column='DATEJ', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cddevise = models.CharField(db_column='CDDEVISE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    txvente = models.DecimalField(db_column='TXVENTE', max_digits=12, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    txachat = models.DecimalField(db_column='TXACHAT', max_digits=12, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    codesocie = models.CharField(db_column='CODESOCIE', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FCOURS'


class Fcreance(models.Model):
    location = models.CharField(db_column='LOCATION', max_length=4, blank=True, null=True)  # Field name made lowercase.
    facture = models.CharField(db_column='FACTURE', max_length=12, blank=True, null=True)  # Field name made lowercase.
    client = models.CharField(db_column='CLIENT', max_length=8, blank=True, null=True)  # Field name made lowercase.
    jour = models.CharField(db_column='JOUR', max_length=8, blank=True, null=True)  # Field name made lowercase.
    devise = models.CharField(db_column='DEVISE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    totcreance = models.FloatField(db_column='TOTCREANCE', blank=True, null=True)  # Field name made lowercase.
    totrecouvre = models.FloatField(db_column='TOTRECOUVRE', blank=True, null=True)  # Field name made lowercase.
    solde = models.FloatField(db_column='SOLDE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FCREANCE'


class Fctrmvt(models.Model):
    codesocie = models.CharField(db_column='CODESOCIE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    mvt = models.SmallIntegerField(db_column='MVT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FCTRMVT'





class Fdetfacture(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    location = models.CharField(db_column='LOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    facture = models.CharField(db_column='FACTURE', max_length=25, blank=True, null=True)  # Field name made lowercase.
    ligne = models.SmallIntegerField(db_column='LIGNE', blank=True, null=True)  # Field name made lowercase.
    article = models.CharField(db_column='ARTICLE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    famille = models.CharField(db_column='FAMILLE', max_length=40, blank=True, null=True)  # Field name made lowercase.
    classe = models.CharField(db_column='CLASSE', max_length=30, blank=True, null=True)  # Field name made lowercase.
    designation = models.CharField(db_column='DESIGNATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    emballage = models.CharField(db_column='EMBALLAGE', max_length=40, blank=True, null=True)  # Field name made lowercase.
    prix_achat = models.FloatField(db_column='PRIX_ACHAT', blank=True, null=True)  # Field name made lowercase.
    prixvente = models.FloatField(db_column='PRIXVENTE', blank=True, null=True)  # Field name made lowercase.
    prixtotal = models.FloatField(db_column='PRIXTOTAL', blank=True, null=True)  # Field name made lowercase.
    quantite = models.FloatField(db_column='QUANTITE', blank=True, null=True)  # Field name made lowercase.
    quantiteunit = models.FloatField(db_column='QUANTITEUNIT', blank=True, null=True)  # Field name made lowercase.
    txremise = models.FloatField(db_column='TXREMISE', blank=True, null=True)  # Field name made lowercase.
    remise = models.FloatField(db_column='REMISE', blank=True, null=True)  # Field name made lowercase.
    txtaxe = models.FloatField(db_column='TXTAXE', blank=True, null=True)  # Field name made lowercase.
    taxe = models.FloatField(db_column='TAXE', blank=True, null=True)  # Field name made lowercase.
    indprixsuspect = models.IntegerField(db_column='INDPRIXSUSPECT', blank=True, null=True)  # Field name made lowercase.
    idfact = models.IntegerField(db_column='IDFACT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FDETFACTURE'




class Fdevis(models.Model):
    cddevise = models.CharField(db_column='CDDEVISE', primary_key=True, max_length=3)  # Field name made lowercase.
    libelle = models.CharField(db_column='LIBELLE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    swlocal = models.CharField(db_column='SWLOCAL', max_length=3, blank=True, null=True)  # Field name made lowercase.
    swetalon = models.CharField(db_column='SWETALON', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FDEVIS'


class Fdetproforma(models.Model):
    numfacture = models.CharField(db_column='NumFacture', max_length=25, blank=True, null=True)  # Field name made lowercase.
    codeart = models.CharField(db_column='CodeArt', max_length=8, blank=True, null=True)  # Field name made lowercase.
    emb = models.CharField(db_column='Emb', max_length=3, blank=True, null=True)  # Field name made lowercase.
    qte = models.FloatField(db_column='Qte', blank=True, null=True)  # Field name made lowercase.
    pu = models.FloatField(db_column='Pu', blank=True, null=True)  # Field name made lowercase.
    prixtot = models.FloatField(db_column='PrixTot', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FDetProforma'





class Ffacture(models.Model):
    idfact = models.AutoField(db_column='IDFACT', primary_key=True)  # Field name made lowercase.
    societe = models.CharField(db_column='SOCIETE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='LOCATION', max_length=50)  # Field name made lowercase.
    facture = models.CharField(db_column='FACTURE', max_length=25)  # Field name made lowercase.
    datejour = models.CharField(db_column='DATEJOUR', max_length=15)  # Field name made lowercase.
    ndatejour = models.FloatField(db_column='NDATEJOUR')  # Field name made lowercase.
    commande = models.CharField(db_column='COMMANDE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tiers = models.CharField(db_column='TIERS', max_length=8, blank=True, null=True)  # Field name made lowercase.
    devise = models.CharField(db_column='DEVISE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    totalusd = models.FloatField(db_column='TOTALUSD', blank=True, null=True)  # Field name made lowercase.
    totalcdf = models.FloatField(db_column='TOTALCDF', blank=True, null=True)  # Field name made lowercase.
    txremise = models.FloatField(db_column='TXREMISE', blank=True, null=True)  # Field name made lowercase.
    remiseusd = models.FloatField(db_column='REMISEUSD', blank=True, null=True)  # Field name made lowercase.
    remisecdf = models.FloatField(db_column='REMISECDF', blank=True, null=True)  # Field name made lowercase.
    taxe = models.FloatField(db_column='TAXE', blank=True, null=True)  # Field name made lowercase.
    taxeusd = models.FloatField(db_column='TAXEUSD', blank=True, null=True)  # Field name made lowercase.
    taxecdf = models.FloatField(db_column='TAXECDF', blank=True, null=True)  # Field name made lowercase.
    netcdf = models.FloatField(db_column='NETCDF', blank=True, null=True)  # Field name made lowercase.
    netusd = models.FloatField(db_column='NETUSD', blank=True, null=True)  # Field name made lowercase.
    modepaiement = models.CharField(db_column='MODEPAIEMENT', max_length=15, blank=True, null=True)  # Field name made lowercase.
    nomtiers = models.CharField(db_column='NOMTIERS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    imputation = models.CharField(db_column='IMPUTATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    echeance = models.CharField(db_column='ECHEANCE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    necheance = models.FloatField(db_column='NECHEANCE', blank=True, null=True)  # Field name made lowercase.
    valide = models.CharField(db_column='VALIDE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    txchange = models.FloatField(db_column='TXCHANGE', blank=True, null=True)  # Field name made lowercase.
    montlettre = models.TextField(db_column='MONTLETTRE', blank=True, null=True)  # Field name made lowercase.
    recouvrement = models.FloatField(db_column='RECOUVREMENT', blank=True, null=True)  # Field name made lowercase.
    soldrecouvrement = models.FloatField(db_column='SOLDRECOUVREMENT', blank=True, null=True)  # Field name made lowercase.
    apuresolde = models.CharField(db_column='APURESOLDE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    indicecloture = models.CharField(db_column='INDICECLOTURE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    indicemodif = models.BooleanField(db_column='INDICEMODIF', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FFACTURE'
        unique_together = (('idfact', 'location', 'facture'),)




class Fimputation(models.Model):
    location = models.CharField(db_column='LOCATION', max_length=4, blank=True, null=True)  # Field name made lowercase.
    imputation = models.CharField(db_column='IMPUTATION', max_length=4, blank=True, null=True)  # Field name made lowercase.
    designation = models.CharField(db_column='DESIGNATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cptedebit = models.CharField(db_column='CPTEDEBIT', max_length=14, blank=True, null=True)  # Field name made lowercase.
    cptecredit = models.CharField(db_column='CPTECREDIT', max_length=14, blank=True, null=True)  # Field name made lowercase.
    journal = models.CharField(db_column='JOURNAL', max_length=4, blank=True, null=True)  # Field name made lowercase.
    vtedebit = models.CharField(db_column='VTEDEBIT', max_length=14, blank=True, null=True)  # Field name made lowercase.
    vtecredit = models.CharField(db_column='VTECREDIT', max_length=14, blank=True, null=True)  # Field name made lowercase.
    vtejournal = models.CharField(db_column='VTEJOURNAL', max_length=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FIMPUTATION'




class Fjournal(models.Model):
    mvt = models.AutoField(db_column='MVT', primary_key=True)  # Field name made lowercase.
    codesocie = models.CharField(db_column='CODESOCIE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    journal = models.CharField(db_column='JOURNAL', max_length=4, blank=True, null=True)  # Field name made lowercase.
    datemvt = models.DateTimeField(db_column='DATEMVT', blank=True, null=True)  # Field name made lowercase.
    ndatemvt = models.FloatField(db_column='NDATEMVT', blank=True, null=True)  # Field name made lowercase.
    compte = models.CharField(db_column='COMPTE', max_length=16, blank=True, null=True)  # Field name made lowercase.
    periode = models.IntegerField(db_column='PERIODE', blank=True, null=True)  # Field name made lowercase.
    numpiece = models.CharField(db_column='NUMPIECE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    libmvt = models.CharField(db_column='LIBMVT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sens = models.CharField(db_column='SENS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    montantdb = models.FloatField(db_column='MONTANTDB', blank=True, null=True)  # Field name made lowercase.
    montantcr = models.FloatField(db_column='MONTANTCR', blank=True, null=True)  # Field name made lowercase.
    devise = models.CharField(db_column='DEVISE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    taux = models.FloatField(db_column='TAUX', blank=True, null=True)  # Field name made lowercase.
    mlmontantdb = models.FloatField(db_column='MLMONTANTDB', blank=True, null=True)  # Field name made lowercase.
    mlmontantcr = models.FloatField(db_column='MLMONTANTCR', blank=True, null=True)  # Field name made lowercase.
    memontantdb = models.FloatField(db_column='MEMONTANTDB', blank=True, null=True)  # Field name made lowercase.
    memontantcr = models.FloatField(db_column='MEMONTANTCR', blank=True, null=True)  # Field name made lowercase.
    isexport = models.BooleanField(db_column='IsExport', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FJOURNAL'


class Fkardex(models.Model):
    location = models.CharField(db_column='LOCATION', max_length=4, blank=True, null=True)  # Field name made lowercase.
    kardex = models.CharField(db_column='KARDEX', primary_key=True, max_length=6)  # Field name made lowercase.
    designation = models.CharField(db_column='DESIGNATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    flag = models.CharField(db_column='FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FKARDEX'







class Finventaire(models.Model):
    compteur = models.AutoField(db_column='COMPTEUR', primary_key=True)  # Field name made lowercase.
    location = models.ForeignKey(Flocation, on_delete=models.SET_NULL, null=True)
    #location = models.CharField(db_column='LOCATION', max_length=9, blank=True, null=True)  # Field name made lowercase.
    liblocation = models.CharField(db_column='LIBLOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    periode = models.CharField(db_column='PERIODE', max_length=25, blank=True, null=True)  # Field name made lowercase.
    # article = models.CharField(db_column='ARTICLE', max_length=8, blank=True, null=True)  # Field name made lowercase.
    article = models.ForeignKey(Farticle, on_delete=models.SET_NULL, null=True)
    famille = models.CharField(db_column='FAMILLE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    classe = models.CharField(db_column='CLASSE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    designation = models.CharField(db_column='DESIGNATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    emballage_e = models.CharField(db_column='EMBALLAGE_E', max_length=10, blank=True, null=True)  # Field name made lowercase.
    emballage_u = models.CharField(db_column='EMBALLAGE_U', max_length=10, blank=True, null=True)  # Field name made lowercase.
    quantitee = models.FloatField(db_column='QUANTITEE', blank=True, null=True)  # Field name made lowercase.
    quantiteu = models.FloatField(db_column='QUANTITEU', blank=True, null=True)  # Field name made lowercase.
    qte_u_log = models.FloatField(db_column='QTE_U_LOG', blank=True, null=True)  # Field name made lowercase.
    qte_u_phys = models.FloatField(db_column='QTE_U_PHYS', blank=True, null=True)  # Field name made lowercase.
    qte_u_ecart = models.FloatField(db_column='QTE_U_ECART', blank=True, null=True)  # Field name made lowercase.
    prix_achat_u = models.FloatField(db_column='PRIX_ACHAT_U', blank=True, null=True)  # Field name made lowercase.
    prix_vente_u = models.FloatField(db_column='PRIX_VENTE_U', blank=True, null=True)  # Field name made lowercase.
    dateinventaire = models.CharField(db_column='DATEINVENTAIRE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    ndateinvent = models.DecimalField(db_column='NDATEINVENT', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    ind = models.IntegerField(db_column='IND', blank=True, null=True)  # Field name made lowercase.
    codesocie = models.CharField(db_column='CODESOCIE', max_length=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FINVENTAIRE'



class Flogbook(models.Model):
    numero = models.AutoField(db_column='NUMERO', primary_key=True)  # Field name made lowercase.
    codelocation = models.CharField(db_column='Codelocation', max_length=3, blank=True, null=True)  # Field name made lowercase.
    codeuser = models.CharField(db_column='CODEUser', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dateop = models.DateTimeField(db_column='DateOp', blank=True, null=True)  # Field name made lowercase.
    ndateop = models.DecimalField(db_column='Ndateop', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    heure = models.CharField(db_column='Heure', max_length=15, blank=True, null=True)  # Field name made lowercase.
    operation = models.CharField(db_column='Operation', max_length=50, blank=True, null=True)  # Field name made lowercase.
    typemvt = models.CharField(db_column='TypeMvt', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FLOGBOOK'



class Fmvts(models.Model):
    mvt = models.AutoField(db_column='MVT', primary_key=True)  # Field name made lowercase.
    # location = models.CharField(db_column='LOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    periode = models.CharField(db_column='PERIODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    datemvt = models.CharField(db_column='DATEMVT', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ndatemvt = models.FloatField(db_column='NDATEMVT', blank=True, null=True)  # Field name made lowercase.
    bordereau = models.CharField(db_column='BORDEREAU', max_length=25, blank=True, null=True)  # Field name made lowercase.
    requisition = models.CharField(db_column='REQUISITION', max_length=25, blank=True, null=True)  # Field name made lowercase.
    document = models.CharField(db_column='DOCUMENT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    reference = models.CharField(db_column='REFERENCE', max_length=25, blank=True, null=True)  # Field name made lowercase.
    ajustement = models.ForeignKey(Fajustement, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(Flocation, on_delete=models.SET_NULL, null=True)
    # ajustement = models.CharField(db_column='AJUSTEMENT', max_length=15, blank=True, null=True)  # Field name made lowercase.
    imputation = models.CharField(db_column='IMPUTATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tiers = models.ForeignKey(Ftiers, on_delete=models.SET_NULL, null=True)
    # tiers = models.CharField(db_column='TIERS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    facture = models.CharField(db_column='FACTURE', max_length=25, blank=True, null=True)  # Field name made lowercase.
    # article = models.CharField(db_column='ARTICLE', max_length=8, blank=True, null=True)  # Field name made lowercase.
    article = models.ForeignKey(Farticle, on_delete=models.SET_NULL, null=True)
    # recette = models.ForeignKey(Recettes, on_delete=models.SET_NULL, null=True)
    famille = models.CharField(db_column='FAMILLE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    classe = models.CharField(db_column='CLASSE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    designation = models.CharField(db_column='DESIGNATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # emballage = models.CharField(db_column='EMBALLAGE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    emballage = models.ForeignKey(Femballage, on_delete=models.SET_NULL, null=True)
    quantite = models.FloatField(db_column='QUANTITE', blank=True, null=True)  # Field name made lowercase.
    qte_entree = models.FloatField(db_column='QTE_ENTREE', blank=True, null=True)  # Field name made lowercase.
    qte_sortie = models.FloatField(db_column='QTE_SORTIE', blank=True, null=True)  # Field name made lowercase.
    qteunitaire = models.FloatField(db_column='QTEUNITAIRE', blank=True, null=True)  # Field name made lowercase.
    qteunit_entree = models.FloatField(db_column='QTEUNIT_ENTREE', blank=True, null=True)  # Field name made lowercase.
    qteunit_sortie = models.FloatField(db_column='QTEUNIT_SORTIE', blank=True, null=True)  # Field name made lowercase.
    prix_achat = models.FloatField(db_column='PRIX_ACHAT', blank=True, null=True)  # Field name made lowercase.
    pa = models.FloatField(db_column='PA', blank=True, null=True)  # Field name made lowercase.
    prixachatgros = models.FloatField(db_column='PRIXACHATGROS', blank=True, null=True)  # Field name made lowercase.
    prix_vente = models.FloatField(db_column='PRIX_VENTE', blank=True, null=True)  # Field name made lowercase.
    prix_vente_reel = models.FloatField(db_column='PRIX_VENTE_REEL', blank=True, null=True)  # Field name made lowercase.
    prix_total = models.FloatField(db_column='PRIX_TOTAL', blank=True, null=True)  # Field name made lowercase.
    prix_base = models.FloatField(db_column='PRIX_BASE', blank=True, null=True)  # Field name made lowercase.
    pvcdf = models.FloatField(db_column='PVCDF', blank=True, null=True)  # Field name made lowercase.
    pvusd = models.FloatField(db_column='PVUSD', blank=True, null=True)  # Field name made lowercase.
    devise = models.CharField(db_column='DEVISE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    txchange = models.FloatField(db_column='TXCHANGE', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=100, blank=True, null=True)  # Field name made lowercase.
    flag = models.CharField(db_column='FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    destination = models.CharField(db_column='DESTINATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    txremise = models.FloatField(db_column='TXREMISE', blank=True, null=True)  # Field name made lowercase.
    remise = models.FloatField(db_column='REMISE', blank=True, null=True)  # Field name made lowercase.
    remisecdf = models.FloatField(db_column='REMISECDF', blank=True, null=True)  # Field name made lowercase.
    txtaxe = models.FloatField(db_column='TXTAXE', blank=True, null=True)  # Field name made lowercase.
    taxe = models.FloatField(db_column='TAXE', blank=True, null=True)  # Field name made lowercase.
    taxecdf = models.FloatField(db_column='TAXECDF', blank=True, null=True)  # Field name made lowercase.
    prixnet = models.FloatField(db_column='PrixNet', blank=True, null=True)  # Field name made lowercase.
    prixnetcdf = models.FloatField(db_column='PrixNetCDF', blank=True, null=True)  # Field name made lowercase.
    prixnetusd = models.FloatField(db_column='PrixNetUSD', blank=True, null=True)  # Field name made lowercase.
    indrepare = models.IntegerField(db_column='INDREPARE', blank=True, null=True)  # Field name made lowercase.
    indvalide = models.IntegerField(db_column='INDVALIDE', blank=True, null=True)  # Field name made lowercase.
    codesocie = models.CharField(db_column='CODESOCIE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    prixvteunit = models.FloatField(db_column='PrixVteUnit', blank=True, null=True)  # Field name made lowercase.
    prixvteunitusd = models.FloatField(db_column='PrixVteUnitUSD', blank=True, null=True)  # Field name made lowercase.
    prixvteunitcdf = models.FloatField(db_column='PrixVteUnitCDF', blank=True, null=True)  # Field name made lowercase.
    isused = models.BooleanField(db_column='IsUsed', blank=True, null=True)  # Field name made lowercase.
    stckused = models.FloatField(db_column='StckUsed', blank=True, null=True)  # Field name made lowercase.
    # codeuser = models.CharField(db_column='CodeUser', max_length=10, blank=True, null=True)  # Field name made lowercase.
    codeuser = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    destinat = models.ForeignKey(Flocation,related_name="destinationlocation", on_delete=models.SET_NULL, null=True)
    class Meta:
        managed = False
        db_table = 'FMVTS'


class Fproforma(models.Model):
    idfact = models.AutoField(db_column='IDFACT', primary_key=True)  # Field name made lowercase.
    location = models.CharField(db_column='LOCATION', max_length=50)  # Field name made lowercase.
    facture = models.CharField(db_column='FACTURE', max_length=25)  # Field name made lowercase.
    datejour = models.CharField(db_column='DATEJOUR', max_length=15)  # Field name made lowercase.
    ndatejour = models.FloatField(db_column='NDATEJOUR')  # Field name made lowercase.
    adrescli = models.CharField(db_column='ADRESCLI', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tiers = models.CharField(db_column='TIERS', max_length=8, blank=True, null=True)  # Field name made lowercase.
    devise = models.CharField(db_column='DEVISE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    totalusd = models.FloatField(db_column='TOTALUSD', blank=True, null=True)  # Field name made lowercase.
    totalcdf = models.FloatField(db_column='TOTALCDF', blank=True, null=True)  # Field name made lowercase.
    taxe = models.FloatField(db_column='TAXE', blank=True, null=True)  # Field name made lowercase.
    taxeusd = models.FloatField(db_column='TAXEUSD', blank=True, null=True)  # Field name made lowercase.
    taxecdf = models.FloatField(db_column='TAXECDF', blank=True, null=True)  # Field name made lowercase.
    netcdf = models.FloatField(db_column='NETCDF', blank=True, null=True)  # Field name made lowercase.
    netusd = models.FloatField(db_column='NETUSD', blank=True, null=True)  # Field name made lowercase.
    nomtiers = models.CharField(db_column='NOMTIERS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    txchange = models.FloatField(db_column='TXCHANGE', blank=True, null=True)  # Field name made lowercase.
    montlettre = models.TextField(db_column='MONTLETTRE', blank=True, null=True)  # Field name made lowercase.
    note1 = models.TextField(db_column='NOTE1', blank=True, null=True)  # Field name made lowercase.
    note2 = models.TextField(db_column='NOTE2', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FPROFORMA'
        unique_together = (('idfact', 'location', 'facture'),)


class Frecap(models.Model):
    numenreg = models.AutoField(db_column='NUMENREG',primary_key=True)  # Field name made lowercase.
    location = models.CharField(db_column='LOCATION', max_length=4, blank=True, null=True)  # Field name made lowercase.
    article = models.CharField(db_column='ARTICLE', max_length=8, blank=True, null=True)  # Field name made lowercase.
    famille = models.CharField(db_column='FAMILLE', max_length=4, blank=True, null=True)  # Field name made lowercase.
    classe = models.CharField(db_column='CLASSE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    designation = models.CharField(db_column='DESIGNATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    prix_moyen = models.FloatField(db_column='PRIX_MOYEN', blank=True, null=True)  # Field name made lowercase.
    prix_achat = models.FloatField(db_column='PRIX_ACHAT', blank=True, null=True)  # Field name made lowercase.
    prix_vente = models.FloatField(db_column='PRIX_VENTE', blank=True, null=True)  # Field name made lowercase.
    qte_stock_a = models.FloatField(db_column='QTE_STOCK_A', blank=True, null=True)  # Field name made lowercase.
    qte_stock_e = models.FloatField(db_column='QTE_STOCK_E', blank=True, null=True)  # Field name made lowercase.
    qte_stock_u = models.FloatField(db_column='QTE_STOCK_U', blank=True, null=True)  # Field name made lowercase.
    emballagea = models.CharField(db_column='EMBALLAGEA', max_length=4, blank=True, null=True)  # Field name made lowercase.
    emballagee = models.CharField(db_column='EMBALLAGEE', max_length=4, blank=True, null=True)  # Field name made lowercase.
    emballageu = models.CharField(db_column='EMBALLAGEU', max_length=4, blank=True, null=True)  # Field name made lowercase.
    datejour = models.CharField(db_column='DATEJOUR', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qte_entree_a = models.FloatField(db_column='QTE_ENTREE_A', blank=True, null=True)  # Field name made lowercase.
    qte_entree_e = models.FloatField(db_column='QTE_ENTREE_E', blank=True, null=True)  # Field name made lowercase.
    qte_entree_u = models.FloatField(db_column='QTE_ENTREE_U', blank=True, null=True)  # Field name made lowercase.
    qte_sortie_a = models.FloatField(db_column='QTE_SORTIE_A', blank=True, null=True)  # Field name made lowercase.
    qte_sortie_e = models.FloatField(db_column='QTE_SORTIE_E', blank=True, null=True)  # Field name made lowercase.
    qte_sortie_u = models.FloatField(db_column='QTE_SORTIE_U', blank=True, null=True)  # Field name made lowercase.
    qte_fin_a = models.FloatField(db_column='QTE_FIN_A', blank=True, null=True)  # Field name made lowercase.
    qte_fin_e = models.FloatField(db_column='QTE_FIN_E', blank=True, null=True)  # Field name made lowercase.
    qte_fin_u = models.FloatField(db_column='QTE_FIN_U', blank=True, null=True)  # Field name made lowercase.
    reference = models.CharField(db_column='REFERENCE', max_length=12, blank=True, null=True)  # Field name made lowercase.
    operation = models.CharField(db_column='OPERATION', max_length=14, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FRECAP'


class Frecouvrement(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    location = models.CharField(db_column='LOCATION', max_length=40, blank=True, null=True)  # Field name made lowercase.
    desiloca = models.CharField(db_column='DESILOCA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    facture = models.CharField(db_column='FACTURE', max_length=40, blank=True, null=True)  # Field name made lowercase.
    client = models.CharField(db_column='CLIENT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    daterecouv = models.DateTimeField(db_column='DATERECOUV', blank=True, null=True)  # Field name made lowercase.
    recu = models.CharField(db_column='RECU', max_length=12, blank=True, null=True)  # Field name made lowercase.
    devise = models.CharField(db_column='DEVISE', max_length=7, blank=True, null=True)  # Field name made lowercase.
    txchange = models.FloatField(db_column='TXCHANGE', blank=True, null=True)  # Field name made lowercase.
    montant = models.FloatField(db_column='MONTANT', blank=True, null=True)  # Field name made lowercase.
    eqcreance = models.FloatField(db_column='EQCREANCE', blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(db_column='COMMENT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    codesocie = models.CharField(db_column='CODESOCIE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    montlettre = models.TextField(db_column='MONTLETTRE', blank=True, null=True)  # Field name made lowercase.
    dtmvt = models.FloatField(db_column='Dtmvt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FRECOUVREMENT'


class Fstock(models.Model):
    location = models.CharField(db_column='LOCATION', primary_key=True, max_length=50)  # Field name made lowercase.
    article = models.CharField(db_column='ARTICLE', max_length=15)  # Field name made lowercase.
    famille = models.CharField(db_column='FAMILLE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    classe = models.CharField(db_column='CLASSE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    kardex = models.CharField(db_column='KARDEX', max_length=6, blank=True, null=True)  # Field name made lowercase.
    designation = models.CharField(db_column='DESIGNATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dateachat = models.CharField(db_column='DATEACHAT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    prix_achat = models.FloatField(db_column='PRIX_ACHAT', blank=True, null=True)  # Field name made lowercase.
    dernier_prix_achat = models.FloatField(db_column='DERNIER_PRIX_ACHAT', blank=True, null=True)  # Field name made lowercase.
    date_achat = models.CharField(db_column='DATE_ACHAT', max_length=15, blank=True, null=True)  # Field name made lowercase.
    derniere_date_achat = models.CharField(db_column='DERNIERE_DATE_ACHAT', max_length=15, blank=True, null=True)  # Field name made lowercase.
    date_majpvente = models.CharField(db_column='DATE_MAJPVENTE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    derniere_date_majpvente = models.CharField(db_column='DERNIERE_DATE_MAJPVENTE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    qte_stock_a = models.FloatField(db_column='QTE_STOCK_A', blank=True, null=True)  # Field name made lowercase.
    qte_stock_e = models.FloatField(db_column='QTE_STOCK_E', blank=True, null=True)  # Field name made lowercase.
    qte_stock_u = models.FloatField(db_column='QTE_STOCK_U', blank=True, null=True)  # Field name made lowercase.
    prix_vente = models.FloatField(db_column='PRIX_VENTE', blank=True, null=True)  # Field name made lowercase.
    dernier_prix_vente = models.DecimalField(db_column='DERNIER_PRIX_VENTE', max_digits=15, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    expiration = models.DateTimeField(db_column='EXPIRATION', blank=True, null=True)  # Field name made lowercase.
    derniere_date_vente = models.CharField(db_column='DERNIERE_DATE_VENTE', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qte_stock_minimal = models.FloatField(db_column='QTE_STOCK_MINIMAL', blank=True, null=True)  # Field name made lowercase.
    emballagea = models.CharField(db_column='EMBALLAGEA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    emballagee = models.CharField(db_column='EMBALLAGEE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    emballageu = models.CharField(db_column='EMBALLAGEU', max_length=50, blank=True, null=True)  # Field name made lowercase.
    quantitea = models.FloatField(db_column='QUANTITEA', blank=True, null=True)  # Field name made lowercase.
    quantitee = models.FloatField(db_column='QUANTITEE', blank=True, null=True)  # Field name made lowercase.
    quantiteu = models.FloatField(db_column='QUANTITEU', blank=True, null=True)  # Field name made lowercase.
    stock_init_a = models.FloatField(db_column='STOCK_INIT_A', blank=True, null=True)  # Field name made lowercase.
    stock_init_e = models.FloatField(db_column='STOCK_INIT_E', blank=True, null=True)  # Field name made lowercase.
    stock_init_u = models.FloatField(db_column='STOCK_INIT_U', blank=True, null=True)  # Field name made lowercase.
    prix_moyen = models.FloatField(db_column='PRIX_MOYEN', blank=True, null=True)  # Field name made lowercase.
    codesocie = models.CharField(db_column='CODESOCIE', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FSTOCK'
        unique_together = (('location', 'article'),)


class Ftarif(models.Model):
    datejour = models.CharField(db_column='DATEJOUR', max_length=8, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='LOCATION', max_length=4, blank=True, null=True)  # Field name made lowercase.
    article = models.CharField(db_column='ARTICLE', max_length=8, blank=True, null=True)  # Field name made lowercase.
    famille = models.CharField(db_column='FAMILLE', max_length=4, blank=True, null=True)  # Field name made lowercase.
    classe = models.CharField(db_column='CLASSE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    pucdf = models.DecimalField(db_column='PUCDF', max_digits=15, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    puref = models.DecimalField(db_column='PUREF', max_digits=15, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FTARIF'


class Ftaxes(models.Model):
    taxe = models.AutoField(db_column='TAXE',primary_key=True)  # Field name made lowercase.
    designation = models.CharField(db_column='DESIGNATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    taux = models.FloatField(db_column='TAUX', blank=True, null=True)  # Field name made lowercase.
    application = models.CharField(db_column='APPLICATION', max_length=9, blank=True, null=True)  # Field name made lowercase.
    codesocie = models.CharField(db_column='CODESOCIE', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        verbose_name="Taxe"
        verbose_name_plural="Taxes"
        db_table = 'FTAXES'


class Fcommande(models.Model):
    commande = models.CharField(db_column='COMMANDE', max_length=12, primary_key=True)  # Field name made lowercase.
    datejour = models.TextField(db_column='DATEJOUR', blank=True, null=True)  # Field name made lowercase.
    location = models.ForeignKey(Flocation, on_delete=models.SET_NULL, null=True)
    # location = models.CharField(db_column='LOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    reference = models.CharField(db_column='REFERENCE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    requisition = models.CharField(db_column='REQUISITION', max_length=20, blank=True, null=True)  # Field name made lowercase.
    # tiers = models.CharField(db_column='TIERS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tiers = models.ForeignKey(Ftiers, on_delete=models.SET_NULL, null=True)
    nomtiers = models.CharField(db_column='NOMTIERS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    devise = models.CharField(db_column='DEVISE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    total = models.FloatField(db_column='TOTAL', blank=True, null=True)  # Field name made lowercase.
    remise = models.FloatField(db_column='REMISE', blank=True, null=True)  # Field name made lowercase.
    etatcde = models.CharField(db_column='ETATCDE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    echeance = models.CharField(db_column='ECHEANCE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    datelivraison = models.CharField(db_column='DATELIVRAISON', max_length=50, blank=True, null=True)  # Field name made lowercase.
    imputation = models.CharField(db_column='IMPUTATION', max_length=15, blank=True, null=True)  # Field name made lowercase.
    typecommande = models.CharField(db_column='TYPECOMMANDE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    observation = models.CharField(db_column='OBSERVATION', max_length=100, blank=True, null=True)  # Field name made lowercase.
    serielivraison = models.CharField(db_column='SERIELIVRAISON',max_length=50, blank=True, null=True)  # Field name made lowercase.
    flaganul = models.SmallIntegerField(db_column='FlagAnul', blank=True, null=True)  # Field name made lowercase.
    userr = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    validation = models.BooleanField(default=False)
    cloture = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'FCOMMANDE'

class Flivraison(models.Model):
    location = models.CharField(db_column='LOCATION', max_length=4, blank=True, null=True)  # Field name made lowercase.
    commande = models.ForeignKey(Fcommande,related_name="livraisoncmd", on_delete=models.SET_NULL, null=True)
    # commande = models.CharField(db_column='COMMANDE', max_length=12, blank=True, null=True)  # Field name made lowercase.
    serielivraison = models.CharField(db_column='SERIELIVRAISON',max_length=50, primary_key=True)  # Field name made lowercase.
    datejour = models.CharField(db_column='DATEJOUR', max_length=8, blank=True, null=True)  # Field name made lowercase.
    document = models.CharField(db_column='DOCUMENT', max_length=12, blank=True, null=True)  # Field name made lowercase.
    tiers = models.CharField(db_column='TIERS', max_length=8, blank=True, null=True)  # Field name made lowercase.
    nomtiers = models.CharField(db_column='NOMTIERS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    adresselivraison = models.CharField(db_column='ADRESSELIVRAISON', max_length=50, blank=True, null=True)  # Field name made lowercase.
    imputation = models.CharField(db_column='IMPUTATION', max_length=4, blank=True, null=True)  # Field name made lowercase.
    observation = models.CharField(db_column='OBSERVATION', max_length=100, blank=True, null=True)  # Field name made lowercase.
    etatliv = models.CharField(db_column='ETATLIV', max_length=1, blank=True, null=True)
    validation = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'FLIVRAISON'



class Fdetlivraison(models.Model):
    location = models.CharField(db_column='LOCATION', max_length=4, blank=True, null=True)  # Field name made lowercase.
    commande = models.CharField(db_column='COMMANDE', max_length=12, blank=True, null=True)  # Field name made lowercase.
    serielivraison = models.ForeignKey(Flivraison, on_delete=models.SET_NULL, null=True)
    # serielivraison = models.SmallIntegerField(db_column='SERIELIVRAISON', blank=True, null=True)  # Field name made lowercase.
    ligne = models.SmallIntegerField(db_column='LIGNE', blank=True, null=True)  # Field name made lowercase.
    # article = models.CharField(db_column='ARTICLE', max_length=8, blank=True, null=True)  # Field name made lowercase.
    article = models.ForeignKey(Farticle, on_delete=models.SET_NULL, null=True)
    famille = models.CharField(db_column='FAMILLE', max_length=4, blank=True, null=True)  # Field name made lowercase.
    classe = models.CharField(db_column='CLASSE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    # emballage = models.CharField(db_column='EMBALLAGE', max_length=4, blank=True, null=True)  # Field name made lowercase.
    emballage = models.ForeignKey(Femballage, on_delete=models.SET_NULL, null=True)
    quantite = models.FloatField(db_column='QUANTITE', blank=True, null=True)  # Field name made lowercase.
    qtelivree = models.FloatField(db_column='QTELIVREE', blank=True, null=True)  # Field name made lowercase.
    prixunitaire = models.FloatField(db_column='PRIXUNITAIRE', blank=True, null=True)  # Field name made lowercase.
    pucdf = models.FloatField(db_column='PUCDF', blank=True, null=True)  # Field name made lowercase.
    puusd = models.FloatField(db_column='PUUSD', blank=True, null=True)  # Field name made lowercase.
    prixtotal = models.FloatField(db_column='PRIXTOTAL', blank=True, null=True)  # Field name made lowercase.
    ptcdf = models.FloatField(db_column='PTCDF', blank=True, null=True)  # Field name made lowercase.
    ptusd = models.FloatField(db_column='PTUSD', blank=True, null=True)  # Field name made lowercase.
    qteunitaire = models.FloatField(db_column='QTEUNITAIRE', blank=True, null=True)  # Field name made lowercase.
    qteunitairelivree = models.FloatField(db_column='QTEUNITAIRELIVREE', blank=True, null=True)  # Field name made lowercase.
    id = models.AutoField(db_column='Id', primary_key=True)

    class Meta:
        managed = False
        db_table = 'FDETLIVRAISON'


class Fdetcde(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True) 
    location = models.CharField(db_column='LOCATION', max_length=20, blank=True, null=True)  # Field name made lowercase.
    # commande = models.CharField(db_column='COMMANDE', max_length=30, blank=True, null=True)  # Field name made lowercase.
    commande = models.ForeignKey(Fcommande, on_delete=models.SET_NULL, null=True)
    ligne = models.SmallIntegerField(db_column='LIGNE', blank=True, null=True)  # Field name made lowercase.
    # article = models.CharField(db_column='ARTICLE', max_length=30, blank=True, null=True)  # Field name made lowercase.
    article = models.ForeignKey(Farticle, on_delete=models.SET_NULL, null=True)
    famille = models.CharField(db_column='FAMILLE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    classe = models.CharField(db_column='CLASSE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    designation = models.CharField(db_column='DESIGNATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # emballage = models.CharField(db_column='EMBALLAGE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    emballage = models.ForeignKey(Femballage, on_delete=models.SET_NULL, null=True)
    emballage2 = models.ForeignKey(Femballage,related_name="emballlagev", on_delete=models.SET_NULL, null=True)
    quantite = models.FloatField(db_column='QUANTITE', blank=True, null=True)  # Field name made lowercase.
    qteunitaire = models.FloatField(db_column='QTEUNITAIRE', blank=True, null=True)  # Field name made lowercase.
    prix_unitaire = models.FloatField(db_column='PRIX_UNITAIRE', blank=True, null=True)  # Field name made lowercase.
    prix_unitaire_livree = models.FloatField(db_column='PRIX_UNITAIRE_LIVREE', blank=True, null=True)  # Field name made lowercase.
    pucdf = models.FloatField(db_column='PUCDF', blank=True, null=True)  # Field name made lowercase.
    puusd = models.FloatField(db_column='PUUSD', blank=True, null=True)  # Field name made lowercase.
    prix_total = models.FloatField(db_column='PRIX_TOTAL', blank=True, null=True)  # Field name made lowercase.
    ptcdf = models.FloatField(db_column='PTCDF', blank=True, null=True)  # Field name made lowercase.
    ptusd = models.FloatField(db_column='PTUSD', blank=True, null=True)  # Field name made lowercase.
    qte_livree = models.FloatField(db_column='QTE_LIVREE', blank=True, null=True)  # Field name made lowercase.
    qteunitaire_livree = models.FloatField(db_column='QTEUNITAIRE_LIVREE', blank=True, null=True)  # Field name made lowercase.
    flaganul = models.SmallIntegerField(db_column='FlagAnul', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FDETCDE'


class Ftransfert(models.Model):
    idtrans = models.AutoField(db_column='IdTrans', primary_key=True)  # Field name made lowercase.
    numdoc = models.CharField(db_column='NumDoc', max_length=25, blank=True, null=True)  # Field name made lowercase.
    datemvt = models.DateTimeField(db_column='Datemvt', blank=True, null=True)  # Field name made lowercase.
    ndate = models.IntegerField(db_column='Ndate', blank=True, null=True)  # Field name made lowercase.
    locatdepar = models.CharField(db_column='LocatDepar', max_length=4, blank=True, null=True)  # Field name made lowercase.
    locatarriver = models.CharField(db_column='LocatArriver', max_length=4, blank=True, null=True)  # Field name made lowercase.
    devise = models.CharField(db_column='Devise', max_length=3, blank=True, null=True)  # Field name made lowercase.
    montant = models.FloatField(db_column='Montant', blank=True, null=True)  # Field name made lowercase.
    totpv = models.FloatField(db_column='TotPv', blank=True, null=True)  # Field name made lowercase.
    isrecup = models.BooleanField(db_column='IsRecup', blank=True, null=True)  # Field name made lowercase.
    cuser = models.CharField(db_column='Cuser', max_length=8, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FTRANSFERT'


class Fusers(models.Model):
    code = models.CharField(db_column='CODE', max_length=8)  # Field name made lowercase.
    nom = models.CharField(db_column='NOM', max_length=25, blank=True, null=True)  # Field name made lowercase.
    secret = models.CharField(db_column='SECRET', max_length=12, blank=True, null=True)  # Field name made lowercase.
    dsaisie = models.CharField(db_column='DSAISIE', max_length=6, blank=True, null=True)  # Field name made lowercase.
    fsaisie = models.CharField(db_column='FSAISIE', max_length=6, blank=True, null=True)  # Field name made lowercase.
    societe = models.CharField(db_column='SOCIETE', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FUSERS'


class Fwliste(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    location = models.CharField(db_column='LOCATION', max_length=3, blank=True, null=True)  # Field name made lowercase.
    totale = models.FloatField(db_column='TOTALE', blank=True, null=True)  # Field name made lowercase.
    codeart = models.CharField(db_column='CodeArt', max_length=8, blank=True, null=True)  # Field name made lowercase.
    designation = models.CharField(db_column='Designation', max_length=50, blank=True, null=True)  # Field name made lowercase.
    totals = models.FloatField(db_column='TOTALS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FWLISTE'


class Operation(models.Model):
    idopera = models.CharField(db_column='IDopera', max_length=15)  # Field name made lowercase.
    operation = models.CharField(db_column='Operation', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OPERATION'





class Retourstock(models.Model):
    article = models.CharField(db_column='ARTICLE', max_length=8, blank=True, null=True)  # Field name made lowercase.
    famille = models.CharField(db_column='FAMILLE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    classe = models.CharField(db_column='CLASSE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    designation = models.CharField(db_column='DESIGNATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    emballage = models.CharField(db_column='EMBALLAGE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    qte_sortie = models.FloatField(db_column='QTE_SORTIE', blank=True, null=True)  # Field name made lowercase.
    prix_achat = models.FloatField(db_column='PRIX_ACHAT', blank=True, null=True)  # Field name made lowercase.
    emballageu = models.CharField(db_column='EMBALLAGEU', max_length=50, blank=True, null=True)  # Field name made lowercase.
    quantitee = models.FloatField(db_column='QUANTITEE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RETOURSTOCK'


class Societe(models.Model):
    codesocie = models.CharField(db_column='CODESOCIE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    libelle = models.CharField(db_column='LIBELLE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    telephone = models.CharField(db_column='TELEPHONE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    adresse = models.CharField(db_column='ADRESSE', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SOCIETE'


class Tattente(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    client = models.CharField(db_column='Client', max_length=50, blank=True, null=True)  # Field name made lowercase.
    monnaie = models.CharField(db_column='Monnaie', max_length=3, blank=True, null=True)  # Field name made lowercase.
    taux = models.FloatField(db_column='Taux', blank=True, null=True)  # Field name made lowercase.
    mode = models.CharField(db_column='Mode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    article = models.CharField(db_column='Article', max_length=12, blank=True, null=True)  # Field name made lowercase.
    designation = models.CharField(db_column='Designation', max_length=50, blank=True, null=True)  # Field name made lowercase.
    emb = models.CharField(db_column='Emb', max_length=4, blank=True, null=True)  # Field name made lowercase.
    qte = models.FloatField(db_column='Qte', blank=True, null=True)  # Field name made lowercase.
    puht = models.FloatField(db_column='PUHT', blank=True, null=True)  # Field name made lowercase.
    ptht = models.FloatField(db_column='PTHT', blank=True, null=True)  # Field name made lowercase.
    pu = models.FloatField(db_column='Pu', blank=True, null=True)  # Field name made lowercase.
    qteunit = models.FloatField(db_column='QTeUnit', blank=True, null=True)  # Field name made lowercase.
    tauxremise = models.FloatField(db_column='Tauxremise', blank=True, null=True)  # Field name made lowercase.
    remise = models.FloatField(db_column='Remise', blank=True, null=True)  # Field name made lowercase.
    tauxtaxe = models.FloatField(db_column='TauxTaxe', blank=True, null=True)  # Field name made lowercase.
    taxe = models.FloatField(db_column='Taxe', blank=True, null=True)  # Field name made lowercase.
    indsuspect = models.IntegerField(db_column='Indsuspect', blank=True, null=True)  # Field name made lowercase.
    colnet = models.FloatField(db_column='ColNet', blank=True, null=True)  # Field name made lowercase.
    prixachat = models.FloatField(db_column='PrixAchat', blank=True, null=True)  # Field name made lowercase.
    qtee = models.FloatField(db_column='Qtee', blank=True, null=True)  # Field name made lowercase.
    ptttc = models.FloatField(db_column='PTTTC', blank=True, null=True)  # Field name made lowercase.
    pvreel = models.FloatField(db_column='PVReel', blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=10, blank=True, null=True)  # Field name made lowercase.
    facture = models.CharField(db_column='Facture', max_length=25, blank=True, null=True)  # Field name made lowercase.
    famille = models.CharField(db_column='Famille', max_length=50, blank=True, null=True)  # Field name made lowercase.
    datemvt = models.DateTimeField(db_column='DateMvt', blank=True, null=True)  # Field name made lowercase.
    classe = models.CharField(db_column='Classe', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TATTENTE'


class Tcaisse(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    compte = models.CharField(db_column='Compte', max_length=14, blank=True, null=True)  # Field name made lowercase.
    datemvt = models.DateTimeField(db_column='DateMvt', blank=True, null=True)  # Field name made lowercase.
    ndatemvt = models.IntegerField(db_column='NdateMvt', blank=True, null=True)  # Field name made lowercase.
    numpiece = models.CharField(db_column='NumPiece', max_length=20, blank=True, null=True)  # Field name made lowercase.
    noteinterne = models.CharField(db_column='NoteInterne', max_length=30, blank=True, null=True)  # Field name made lowercase.
    codecat = models.IntegerField(db_column='CodeCat', blank=True, null=True)  # Field name made lowercase.
    typemvt = models.CharField(db_column='TypeMvt', max_length=1, blank=True, null=True)  # Field name made lowercase.
    montant = models.FloatField(db_column='Montant', blank=True, null=True)  # Field name made lowercase.
    mtenlettre = models.TextField(db_column='MtenLettre', blank=True, null=True)  # Field name made lowercase.
    cuser = models.CharField(db_column='Cuser', max_length=8, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TCAISSE'


class Tcatemenu(models.Model):
    codec = models.CharField(db_column='CodeC', primary_key=True, max_length=10)  # Field name made lowercase.
    desicate = models.CharField(db_column='DesiCate', max_length=50, blank=True, null=True)  # Field name made lowercase.
    debit = models.FloatField(db_column='Debit', blank=True, null=True)  # Field name made lowercase.
    credit = models.FloatField(db_column='Credit', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TCateMenu'


class Tdetnote(models.Model):
    iddet = models.AutoField(db_column='IdDet', primary_key=True)  # Field name made lowercase.
    codeloc = models.CharField(db_column='codeLoc', max_length=4, blank=True, null=True)  # Field name made lowercase.
    no = models.CharField(db_column='No', max_length=25, blank=True, null=True)  # Field name made lowercase.
    code = models.IntegerField(db_column='Code', blank=True, null=True)  # Field name made lowercase.
    libproduit = models.CharField(db_column='LibProduit', max_length=50, blank=True, null=True)  # Field name made lowercase.
    emb = models.CharField(db_column='Emb', max_length=10, blank=True, null=True)  # Field name made lowercase.
    qte = models.FloatField(db_column='Qte', blank=True, null=True)  # Field name made lowercase.
    pu = models.FloatField(db_column='Pu', blank=True, null=True)  # Field name made lowercase.
    mttaxe = models.FloatField(db_column='MtTaxe', blank=True, null=True)  # Field name made lowercase.
    montht = models.FloatField(db_column='MontHT', blank=True, null=True)  # Field name made lowercase.
    montttc = models.FloatField(db_column='MontTTC', blank=True, null=True)  # Field name made lowercase.
    fam = models.CharField(db_column='Fam', max_length=10, blank=True, null=True)  # Field name made lowercase.
    indsusp = models.BooleanField(db_column='Indsusp', blank=True, null=True)  # Field name made lowercase.
    indchek = models.BooleanField(db_column='IndChek', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TDetNote'


class Tfacpointv(models.Model):
    idmvt = models.AutoField(primary_key=True)
    idloc = models.CharField(db_column='IdLoc', max_length=4, blank=True, null=True)  # Field name made lowercase.
    refdoc = models.CharField(db_column='RefDoc', max_length=25, blank=True, null=True)  # Field name made lowercase.
    codeuser = models.CharField(db_column='CodeUser', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nomserveur = models.CharField(db_column='NomServeur', max_length=50, blank=True, null=True)  # Field name made lowercase.
    datemvt = models.DateTimeField(db_column='DateMvt', blank=True, null=True)  # Field name made lowercase.
    dtmvt = models.IntegerField(db_column='DtMvt', blank=True, null=True)  # Field name made lowercase.
    heuremvt = models.CharField(db_column='HeureMvt', max_length=15, blank=True, null=True)  # Field name made lowercase.
    idclient = models.CharField(db_column='IdClient', max_length=10, blank=True, null=True)  # Field name made lowercase.
    libclient = models.CharField(db_column='LibClient', max_length=50, blank=True, null=True)  # Field name made lowercase.
    chbre = models.CharField(db_column='Chbre', max_length=20, blank=True, null=True)  # Field name made lowercase.
    notable = models.CharField(db_column='NoTable', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tiers = models.CharField(db_column='Tiers', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dev = models.CharField(db_column='Dev', max_length=3, blank=True, null=True)  # Field name made lowercase.
    montantfc = models.FloatField(db_column='Montantfc', blank=True, null=True)  # Field name made lowercase.
    montus = models.FloatField(db_column='Montus', blank=True, null=True)  # Field name made lowercase.
    monteur = models.FloatField(db_column='Monteur', blank=True, null=True)  # Field name made lowercase.
    taux = models.FloatField(db_column='Taux', blank=True, null=True)  # Field name made lowercase.
    percu = models.FloatField(db_column='Percu', blank=True, null=True)  # Field name made lowercase.
    recouvrema = models.FloatField(db_column='Recouvrema', blank=True, null=True)  # Field name made lowercase.
    rendu = models.FloatField(db_column='Rendu', blank=True, null=True)  # Field name made lowercase.
    modep = models.CharField(db_column='ModeP', max_length=20, blank=True, null=True)  # Field name made lowercase.
    txremise = models.FloatField(db_column='Txremise', blank=True, null=True)  # Field name made lowercase.
    montantremis = models.FloatField(db_column='MontantRemis', blank=True, null=True)  # Field name made lowercase.
    monttaxe = models.FloatField(db_column='MontTaxe', blank=True, null=True)  # Field name made lowercase.
    etatf = models.IntegerField(db_column='EtatF', blank=True, null=True)  # Field name made lowercase.
    indclo = models.BooleanField(db_column='IndClo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TFacPointV'


class Tfichtech(models.Model):
    idf = models.AutoField(db_column='IdF', primary_key=True)  # Field name made lowercase.
    idm = models.IntegerField(db_column='IdM', blank=True, null=True)  # Field name made lowercase.
    codearticle = models.CharField(db_column='CodeArticle', max_length=10, blank=True, null=True)  # Field name made lowercase.
    qte = models.FloatField(db_column='Qte', blank=True, null=True)  # Field name made lowercase.
    emb = models.CharField(db_column='Emb', max_length=10, blank=True, null=True)  # Field name made lowercase.
    unite = models.CharField(db_column='Unite', max_length=10, blank=True, null=True)  # Field name made lowercase.
    flag = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TFichTech'


class Tloctrans(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    cuser = models.CharField(db_column='Cuser', max_length=8, blank=True, null=True)  # Field name made lowercase.
    locationtran = models.CharField(db_column='LocationTran', max_length=4, blank=True, null=True)  # Field name made lowercase.
    libuser = models.CharField(db_column='LibUser', max_length=50, blank=True, null=True)  # Field name made lowercase.
    libloca = models.CharField(db_column='LibLoca', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TLocTrans'


class Tlogerr(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    datemvt = models.DateTimeField(db_column='DateMvt', blank=True, null=True)  # Field name made lowercase.
    localiser = models.CharField(db_column='Localiser', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TLogErr'


class Tmenu(models.Model):
    idmenu = models.AutoField(db_column='IdMenu', primary_key=True)  # Field name made lowercase.
    cateplan = models.CharField(db_column='CatePlan', max_length=10, blank=True, null=True)  # Field name made lowercase.
    libproduit = models.CharField(db_column='LibProduit', max_length=100, blank=True, null=True)  # Field name made lowercase.
    montant1 = models.FloatField(db_column='Montant1', blank=True, null=True)  # Field name made lowercase.
    montant2 = models.FloatField(db_column='Montant2', blank=True, null=True)  # Field name made lowercase.
    montant3 = models.FloatField(db_column='Montant3', blank=True, null=True)  # Field name made lowercase.
    dispo = models.BooleanField(db_column='Dispo', blank=True, null=True)  # Field name made lowercase.
    unitemesure = models.CharField(db_column='UniteMesure', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fichtec = models.BooleanField(db_column='FichTec', blank=True, null=True)  # Field name made lowercase.
    dev = models.BooleanField(db_column='dEV', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TMenu'


class Tparampv(models.Model):
    idp = models.AutoField(db_column='IdP', primary_key=True)  # Field name made lowercase.
    idloc = models.CharField(db_column='IdLoc', max_length=4, blank=True, null=True)  # Field name made lowercase.
    stkcontrol = models.BooleanField(db_column='StkControl', blank=True, null=True)  # Field name made lowercase.
    printticket = models.TextField(db_column='PrintTicket', blank=True, null=True)  # Field name made lowercase.
    printraport = models.TextField(db_column='PrintRaport', blank=True, null=True)  # Field name made lowercase.
    norec = models.IntegerField(db_column='NoRec', blank=True, null=True)  # Field name made lowercase.
    indilo = models.IntegerField(db_column='IndiLo', blank=True, null=True)  # Field name made lowercase.
    passw = models.CharField(db_column='Passw', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TParamPV'


class Tplancpte(models.Model):
    compte = models.CharField(db_column='Compte', primary_key=True, max_length=25)  # Field name made lowercase.
    libcompte = models.CharField(db_column='LibCompte', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TPlanCpte'


class Travfstock(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    location = models.CharField(db_column='LOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    article = models.CharField(db_column='ARTICLE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    famille = models.CharField(db_column='FAMILLE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    classe = models.CharField(db_column='CLASSE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    kardex = models.CharField(db_column='KARDEX', max_length=50, blank=True, null=True)  # Field name made lowercase.
    designation = models.CharField(db_column='DESIGNATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    qteenter = models.FloatField(db_column='QTEENTER', blank=True, null=True)  # Field name made lowercase.
    qtesortie = models.FloatField(db_column='QTESORTIE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRAVFSTOCK'


class Travlistfact(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    location = models.CharField(db_column='LOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    facture = models.CharField(db_column='FACTURE', max_length=50)  # Field name made lowercase.
    datejour = models.DateTimeField(db_column='DATEJOUR', blank=True, null=True)  # Field name made lowercase.
    ndate = models.IntegerField(db_column='NDATE', blank=True, null=True)  # Field name made lowercase.
    nomtiers = models.CharField(db_column='NOMTIERS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    devise = models.CharField(db_column='DEVISE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    txremise = models.FloatField(db_column='TXREMISE', blank=True, null=True)  # Field name made lowercase.
    remise = models.FloatField(db_column='REMISE', blank=True, null=True)  # Field name made lowercase.
    taxe = models.FloatField(db_column='TAXE', blank=True, null=True)  # Field name made lowercase.
    ajustement = models.CharField(db_column='AJUSTEMENT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modepaiement = models.CharField(db_column='MODEPAIEMENT', max_length=15, blank=True, null=True)  # Field name made lowercase.
    net = models.FloatField(db_column='NET', blank=True, null=True)  # Field name made lowercase.
    netusd = models.FloatField(db_column='NETUSD', blank=True, null=True)  # Field name made lowercase.
    codesocie = models.CharField(db_column='CODESOCIE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    valide = models.CharField(db_column='VALIDE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    indicemodif = models.CharField(db_column='INDICEMODIF', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRAVLISTFACT'


class Travprintfichstock(models.Model):
    id = models.AutoField(db_column='ID',primary_key=True)  # Field name made lowercase.
    datejour = models.DateTimeField(db_column='DATEJOUR', blank=True, null=True)  # Field name made lowercase.
    article = models.CharField(db_column='ARTICLE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    designation = models.CharField(db_column='DESIGNATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mouvement = models.CharField(db_column='MOUVEMENT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    stini = models.FloatField(db_column='STINI', blank=True, null=True)  # Field name made lowercase.
    qteenter = models.FloatField(db_column='QTEENTER', blank=True, null=True)  # Field name made lowercase.
    qtesortie = models.FloatField(db_column='QTESORTIE', blank=True, null=True)  # Field name made lowercase.
    stfinal = models.FloatField(db_column='STFINAL', blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='LOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    emballagee = models.CharField(db_column='EMBALLAGEE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    emballageu = models.CharField(db_column='EMBALLAGEU', max_length=50, blank=True, null=True)  # Field name made lowercase.
    qteembach = models.IntegerField(db_column='QTEEMBACH', blank=True, null=True)  # Field name made lowercase.
    codesocie = models.CharField(db_column='CODESOCIE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    dtedebut = models.CharField(db_column='DTEDEBUT', max_length=15, blank=True, null=True)  # Field name made lowercase.
    dtefin = models.CharField(db_column='DTEFIN', max_length=15, blank=True, null=True)  # Field name made lowercase.
    famille = models.CharField(db_column='FAMILLE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    prixachat = models.FloatField(db_column='PRIXACHAT', blank=True, null=True)  # Field name made lowercase.
    prixvte = models.FloatField(db_column='PRIXVTE', blank=True, null=True)  # Field name made lowercase.
    prixamoyen = models.FloatField(db_column='PRIXAMOYEN', blank=True, null=True)  # Field name made lowercase.
    quantitee = models.FloatField(db_column='QUANTITEE', blank=True, null=True)  # Field name made lowercase.
    vente = models.FloatField(db_column='VENTE', blank=True, null=True)  # Field name made lowercase.
    transfert = models.FloatField(db_column='TRANSFERT', blank=True, null=True)  # Field name made lowercase.
    autresortie = models.FloatField(db_column='AUTRESORTIE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRAVPRINTFICHSTOCK'


class Travprofit(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    article = models.CharField(db_column='ARTICLE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    designation = models.CharField(db_column='DESIGNATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    emb = models.CharField(db_column='EMB', max_length=30, blank=True, null=True)  # Field name made lowercase.
    qtevendu = models.FloatField(db_column='QTEVENDU', blank=True, null=True)  # Field name made lowercase.
    pachatmoyen = models.FloatField(db_column='PACHATMOYEN', blank=True, null=True)  # Field name made lowercase.
    pvtemoyen = models.FloatField(db_column='PVTEMOYEN', blank=True, null=True)  # Field name made lowercase.
    benef = models.FloatField(db_column='BENEF', blank=True, null=True)  # Field name made lowercase.
    totvte = models.FloatField(db_column='TOTVTE', blank=True, null=True)  # Field name made lowercase.
    totach = models.FloatField(db_column='TOTACH', blank=True, null=True)  # Field name made lowercase.
    codesocie = models.CharField(db_column='CODESOCIE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='LOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    famille = models.CharField(db_column='FAMILLE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    datedebut = models.CharField(db_column='DATEDEBUT', max_length=15, blank=True, null=True)  # Field name made lowercase.
    datefin = models.CharField(db_column='DATEFIN', max_length=15, blank=True, null=True)  # Field name made lowercase.
    frs = models.CharField(db_column='FRS', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRAVPROFIT'


class Travstatvtevalorise(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    location = models.CharField(db_column='LOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    famille = models.CharField(db_column='FAMILLE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    article = models.CharField(db_column='ARTICLE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    designation = models.CharField(db_column='DESIGNATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    qte = models.FloatField(db_column='QTE', blank=True, null=True)  # Field name made lowercase.
    emballage = models.CharField(db_column='EMBALLAGE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    emballageu = models.CharField(db_column='EMBALLAGEU', max_length=50, blank=True, null=True)  # Field name made lowercase.
    pvusd = models.FloatField(db_column='PVUSD', blank=True, null=True)  # Field name made lowercase.
    pvcdf = models.FloatField(db_column='PVCDF', blank=True, null=True)  # Field name made lowercase.
    codesocie = models.CharField(db_column='CODESOCIE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    qtenter = models.FloatField(db_column='QTENTER', blank=True, null=True)  # Field name made lowercase.
    qtsortie = models.FloatField(db_column='QTSORTIE', blank=True, null=True)  # Field name made lowercase.
    ajustement = models.CharField(db_column='AJUSTEMENT', max_length=15, blank=True, null=True)  # Field name made lowercase.
    datedebu = models.CharField(db_column='DATEDEBU', max_length=20, blank=True, null=True)  # Field name made lowercase.
    datefin = models.CharField(db_column='DATEFIN', max_length=20, blank=True, null=True)  # Field name made lowercase.
    devise = models.CharField(db_column='DEVISE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    pvmoyen = models.FloatField(db_column='PVMOYEN', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRAVSTATVTEVALORISE'


class Trequisition(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    daterec = models.DateTimeField(db_column='DateRec', blank=True, null=True)  # Field name made lowercase.
    ndate = models.IntegerField(db_column='Ndate', blank=True, null=True)  # Field name made lowercase.
    refarticle = models.CharField(db_column='RefArticle', max_length=8, blank=True, null=True)  # Field name made lowercase.
    libelleart = models.CharField(db_column='LibelleArt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    qte = models.FloatField(db_column='Qte', blank=True, null=True)  # Field name made lowercase.
    numref = models.CharField(db_column='NumRef', max_length=15, blank=True, null=True)  # Field name made lowercase.
    cde = models.BooleanField(db_column='Cde', blank=True, null=True)  # Field name made lowercase.
    clo = models.BooleanField(db_column='Clo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRequisition'


class Tstatiq1(models.Model):
    location = models.CharField(db_column='LOCATION', primary_key=True, max_length=4)  # Field name made lowercase.
    article = models.CharField(db_column='ARTICLE', max_length=10)  # Field name made lowercase.
    designation = models.CharField(db_column='DESIGNATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    col1 = models.FloatField(db_column='COL1', blank=True, null=True)  # Field name made lowercase.
    col2 = models.FloatField(db_column='COL2', blank=True, null=True)  # Field name made lowercase.
    col3 = models.FloatField(db_column='COL3', blank=True, null=True)  # Field name made lowercase.
    col4 = models.FloatField(db_column='COL4', blank=True, null=True)  # Field name made lowercase.
    col5 = models.FloatField(db_column='COL5', blank=True, null=True)  # Field name made lowercase.
    col6 = models.FloatField(db_column='COL6', blank=True, null=True)  # Field name made lowercase.
    col7 = models.FloatField(db_column='COL7', blank=True, null=True)  # Field name made lowercase.
    col8 = models.FloatField(db_column='COL8', blank=True, null=True)  # Field name made lowercase.
    col9 = models.FloatField(db_column='COL9', blank=True, null=True)  # Field name made lowercase.
    col10 = models.FloatField(db_column='COL10', blank=True, null=True)  # Field name made lowercase.
    col11 = models.FloatField(db_column='COL11', blank=True, null=True)  # Field name made lowercase.
    col12 = models.FloatField(db_column='COL12', blank=True, null=True)  # Field name made lowercase.
    col13 = models.FloatField(db_column='COL13', blank=True, null=True)  # Field name made lowercase.
    col14 = models.FloatField(db_column='COL14', blank=True, null=True)  # Field name made lowercase.
    col15 = models.FloatField(db_column='COL15', blank=True, null=True)  # Field name made lowercase.
    col16 = models.FloatField(db_column='COL16', blank=True, null=True)  # Field name made lowercase.
    col17 = models.FloatField(db_column='COL17', blank=True, null=True)  # Field name made lowercase.
    col18 = models.FloatField(db_column='COL18', blank=True, null=True)  # Field name made lowercase.
    col19 = models.FloatField(db_column='COL19', blank=True, null=True)  # Field name made lowercase.
    col20 = models.FloatField(db_column='COL20', blank=True, null=True)  # Field name made lowercase.
    col21 = models.FloatField(db_column='COL21', blank=True, null=True)  # Field name made lowercase.
    col22 = models.FloatField(db_column='COL22', blank=True, null=True)  # Field name made lowercase.
    col23 = models.FloatField(db_column='COL23', blank=True, null=True)  # Field name made lowercase.
    col24 = models.FloatField(db_column='COL24', blank=True, null=True)  # Field name made lowercase.
    col25 = models.FloatField(db_column='COL25', blank=True, null=True)  # Field name made lowercase.
    col26 = models.FloatField(db_column='COL26', blank=True, null=True)  # Field name made lowercase.
    col27 = models.FloatField(db_column='COL27', blank=True, null=True)  # Field name made lowercase.
    col28 = models.FloatField(db_column='COL28', blank=True, null=True)  # Field name made lowercase.
    col29 = models.FloatField(db_column='COL29', blank=True, null=True)  # Field name made lowercase.
    col30 = models.FloatField(db_column='COL30', blank=True, null=True)  # Field name made lowercase.
    col31 = models.FloatField(db_column='COL31', blank=True, null=True)  # Field name made lowercase.
    devise = models.CharField(db_column='DEVISE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    documa = models.CharField(db_column='DOCUMA', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TSTATIQ1'
        unique_together = (('location', 'article'),)


class Tsynthese(models.Model):
    societe = models.CharField(db_column='SOCIETE', primary_key=True, max_length=3)  # Field name made lowercase.
    location = models.CharField(db_column='LOCATION', max_length=4)  # Field name made lowercase.
    datemvt = models.DateTimeField(db_column='DATEMVT')  # Field name made lowercase.
    cashusd = models.FloatField(db_column='CASHUSD', blank=True, null=True)  # Field name made lowercase.
    cashcdf = models.FloatField(db_column='CASHCDF', blank=True, null=True)  # Field name made lowercase.
    creditusd = models.FloatField(db_column='CREDITUSD', blank=True, null=True)  # Field name made lowercase.
    creditcdf = models.FloatField(db_column='CREDITCDF', blank=True, null=True)  # Field name made lowercase.
    recusd = models.FloatField(db_column='RECUSD', blank=True, null=True)  # Field name made lowercase.
    reccdf = models.FloatField(db_column='RECCDF', blank=True, null=True)  # Field name made lowercase.
    qte1 = models.FloatField(db_column='QTE1', blank=True, null=True)  # Field name made lowercase.
    qte2 = models.FloatField(db_column='QTE2', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TSYNTHESE'
        unique_together = (('societe', 'location', 'datemvt'),)


class Tsyscaisse(models.Model):
    compte = models.CharField(db_column='Compte', primary_key=True, max_length=14)  # Field name made lowercase.
    monnaie = models.CharField(db_column='Monnaie', max_length=3, blank=True, null=True)  # Field name made lowercase.
    libellecaisse = models.CharField(db_column='LibelleCaisse', max_length=50, blank=True, null=True)  # Field name made lowercase.
    jnl = models.CharField(db_column='Jnl', max_length=3, blank=True, null=True)  # Field name made lowercase.
    solde = models.FloatField(db_column='Solde', blank=True, null=True)  # Field name made lowercase.
    lastjour = models.DateTimeField(db_column='LastJour', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TSYSCAISSE'


class Tserveur(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    nomserveur = models.CharField(db_column='NomServeur', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sexe = models.IntegerField(db_column='Sexe', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TServeur'


class Ttva(models.Model):
    location = models.CharField(db_column='Location', max_length=10, blank=True, null=True)  # Field name made lowercase.
    datemvt = models.DateTimeField(db_column='DateMvt', blank=True, null=True)  # Field name made lowercase.
    article = models.CharField(db_column='Article', max_length=8, blank=True, null=True)  # Field name made lowercase.
    designation = models.CharField(db_column='Designation', max_length=50, blank=True, null=True)  # Field name made lowercase.
    qte = models.FloatField(db_column='Qte', blank=True, null=True)  # Field name made lowercase.
    tvapayee = models.FloatField(db_column='TvaPayee', blank=True, null=True)  # Field name made lowercase.
    tvarecolte = models.FloatField(db_column='TvaRecolte', blank=True, null=True)  # Field name made lowercase.
    monnaie = models.CharField(db_column='Monnaie', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nomfrs = models.CharField(db_column='NomFrs', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TTVA'


class Ttable(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    nomtable = models.CharField(db_column='Nomtable', max_length=50, blank=True, null=True)  # Field name made lowercase.
    localiser = models.CharField(db_column='Localiser', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TTable'


class Tventefrs(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    codelocation = models.CharField(db_column='CodeLocation', max_length=4, blank=True, null=True)  # Field name made lowercase.
    facture = models.CharField(db_column='Facture', max_length=25, blank=True, null=True)  # Field name made lowercase.
    tiers = models.CharField(db_column='Tiers', max_length=50, blank=True, null=True)  # Field name made lowercase.
    codeart = models.CharField(db_column='CodeArt', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qtevendue = models.FloatField(db_column='QteVendue', blank=True, null=True)  # Field name made lowercase.
    pa = models.FloatField(db_column='Pa', blank=True, null=True)  # Field name made lowercase.
    pv = models.FloatField(db_column='Pv', blank=True, null=True)  # Field name made lowercase.
    prixusd = models.FloatField(db_column='PrixUsd', blank=True, null=True)  # Field name made lowercase.
    dtjour = models.FloatField(db_column='Dtjour')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TVENTEFRS'


class Twrkcpta(models.Model):
    idw = models.AutoField(db_column='IdW', primary_key=True)  # Field name made lowercase.
    compte = models.CharField(db_column='Compte', max_length=16, blank=True, null=True)  # Field name made lowercase.
    libcpte = models.TextField(db_column='Libcpte', blank=True, null=True)  # Field name made lowercase.
    datemvt = models.DateTimeField(db_column='Datemvt', blank=True, null=True)  # Field name made lowercase.
    ndate = models.FloatField(db_column='Ndate', blank=True, null=True)  # Field name made lowercase.
    jnl = models.CharField(db_column='Jnl', max_length=4, blank=True, null=True)  # Field name made lowercase.
    refdoc = models.CharField(db_column='Refdoc', max_length=30, blank=True, null=True)  # Field name made lowercase.
    libmvt = models.TextField(db_column='LibMvt', blank=True, null=True)  # Field name made lowercase.
    dev = models.CharField(db_column='Dev', max_length=3, blank=True, null=True)  # Field name made lowercase.
    txjour = models.FloatField(db_column='Txjour', blank=True, null=True)  # Field name made lowercase.
    mtdebit = models.FloatField(db_column='MtDebit', blank=True, null=True)  # Field name made lowercase.
    mtcredit = models.FloatField(db_column='MtCredit', blank=True, null=True)  # Field name made lowercase.
    soldedeb = models.FloatField(db_column='SoldeDeb', blank=True, null=True)  # Field name made lowercase.
    soldecre = models.FloatField(db_column='SoldeCre', blank=True, null=True)  # Field name made lowercase.
    initdeb = models.FloatField(db_column='InitDeb', blank=True, null=True)  # Field name made lowercase.
    initcre = models.FloatField(db_column='InitCre', blank=True, null=True)  # Field name made lowercase.
    anteriee = models.CharField(db_column='Anteriee', max_length=50, blank=True, null=True)  # Field name made lowercase.
    monnaiedem = models.CharField(db_column='MonnaieDem', max_length=3, blank=True, null=True)  # Field name made lowercase.
    col10 = models.FloatField(db_column='Col10', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TWRKCPTA'


class Ddddd(models.Model):
    numprod = models.BigIntegerField(blank=True, null=True)
    libelle = models.CharField(max_length=34, blank=True, null=True)
    emb_entree = models.CharField(max_length=5, blank=True, null=True)
    typrod = models.CharField(max_length=5, blank=True, null=True)
    prix_achat = models.BigIntegerField(blank=True, null=True)
    prix_vente = models.BigIntegerField(blank=True, null=True)
    qte_stock = models.BigIntegerField(blank=True, null=True)
    num = models.BigIntegerField(blank=True, null=True)
    emb_sortie = models.CharField(max_length=5, blank=True, null=True)
    taux_emb = models.BigIntegerField(blank=True, null=True)
    devise = models.CharField(max_length=3, blank=True, null=True)
    type_produit = models.CharField(max_length=5, blank=True, null=True)
    code_barre = models.CharField(max_length=13, blank=True, null=True)
    id_type = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ddddd'


class Teste(models.Model):
    f1 = models.CharField(db_column='F1', max_length=255, blank=True, null=True)  # Field name made lowercase.
    f2 = models.CharField(db_column='F2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    f3 = models.CharField(db_column='F3', max_length=255, blank=True, null=True)  # Field name made lowercase.
    f4 = models.CharField(db_column='F4', max_length=255, blank=True, null=True)  # Field name made lowercase.
    f5 = models.CharField(db_column='F5', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fam1 = models.CharField(db_column='Fam1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fam2 = models.CharField(db_column='Fam2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    emb1 = models.CharField(db_column='Emb1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    emb2 = models.CharField(db_column='Emb2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    qte = models.IntegerField(db_column='Qte', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'teste'

#-------------------------------------------------------------------------------------------------------------------

class LocationUser(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(Flocation, on_delete=models.SET_NULL, null=True)
    dateop = models.DateField()

    def __str__(self):
        return self.user.username +" - "+ self.location.designation

class DelaiInventaire(models.Model):
    location = models.ForeignKey(Flocation, on_delete=models.SET_NULL, null=True)
    # datedebutop = models.DateField()
    datefinop = models.DateField()
    periode = models.CharField(max_length=8)

class IncremaClient(models.Model):
    libelle = models.CharField(max_length=8,null=True)



class SommeInventaire(models.Model):
    location = models.ForeignKey(Flocation, on_delete=models.SET_NULL, null=True)
    famille = models.ForeignKey(Ffamilles, on_delete=models.SET_NULL, null=True,blank=True)
    periode = models.CharField(max_length=8, null=True,blank=True)
    somme=models.FloatField()

    def __str__(self):
        return self.location.location +" - "+ self.famille.designation +" "+str(self.somme)

class TempoPrix(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    article = models.ForeignKey(Farticle, on_delete=models.SET_NULL, null=True)
    emb1 = models.ForeignKey(Femballage, on_delete=models.SET_NULL, null=True)
    emb2 = models.ForeignKey(Femballage,related_name="emballaprix", on_delete=models.SET_NULL, null=True)
    prix1 = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    prix2 = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    etat = models.BooleanField(default=False)
    devise = models.CharField(max_length=10)
    dateop = models.DateField()

    def __str__(self):
        return self.user.username +" - "+ self.article.designation


class etatbesoin(models.Model):
    location = models.ForeignKey(Flocation, on_delete=models.SET_NULL, null=True)
    article = models.ForeignKey(Farticle, on_delete=models.SET_NULL, null=True)
    emb1 = models.ForeignKey(Femballage, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    qte=models.FloatField(default=1)
    qteliv=models.FloatField(default=1)
    code = models.CharField(max_length=20)
    etat = models.BooleanField(default=False)
    dateop=models.DateField(auto_created=True)
    locationfour = models.ForeignKey(Flocation, on_delete=models.SET_NULL,related_name='location_fournisseur', null=True)


class Recettes(models.Model):
    libelle = models.CharField(max_length=50,null=True)
    categorie=models.BooleanField(default=False)

class DetailRecettes(models.Model):
    recettes = models.ForeignKey(Recettes, on_delete=models.SET_NULL, null=True)
    produit = models.ForeignKey(Farticle, on_delete=models.SET_NULL, null=True)
    emballage = models.ForeignKey(Femballage, on_delete=models.SET_NULL, null=True)
    # client = models.ForeignKey(Ftiers, on_delete=models.SET_NULL, null=True)
    qte=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pu=models.DecimalField(max_digits=4, decimal_places=2, default=0)

class PlatRecette(models.Model):
    plat = models.ForeignKey(Recettes,related_name='platrecetteproduit', on_delete=models.PROTECT)
    recettes = models.ForeignKey(Recettes, on_delete=models.PROTECT,blank=True, null=True)
    produit = models.ForeignKey(Farticle, on_delete=models.PROTECT,blank=True, null=True)
    emballage = models.ForeignKey(Femballage, on_delete=models.PROTECT, null=True)
    # client = models.ForeignKey(Ftiers, on_delete=models.SET_NULL, null=True)
    qte=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pu=models.DecimalField(max_digits=4, decimal_places=2, default=0)
    obs = models.CharField(max_length=20,blank=True, null=True)

class Droit(models.Model):
    class Meta:
        permissions = (
            ('Produit', 'Onglet Produit'),
            # ('Modifi_Produit_Prix', 'Onglet Modification Produit'),
            # ('Modifi_Produit_Prix_valide', 'Onglet Valider Prix Produit'),
            # ('Bon_Commande_Interne', 'Onglet Bon de Commande Interne'),
            ('Bon_Commande_Externe', 'Onglet Bon de Commande'),
            # ('Bon_Commande_Modi', 'Onglet Bon de Commande Modifier'),
            # ('Bon_Commande_valide', 'Onglet Validation Bon de Commande'),
            # ('ajustement_valide', 'Onglet Validation Ajustement'),
            # ('ajustementpro', 'Onglet Validation Ajustement Produit'),
            # ('supprimer_valide', 'Onglet Validation Visualisation'),
            # ('Delai_Inventaire', 'Onglet Validation Délai Inventaire'),
            # ('Saisie_Stock', 'Onglet Saisie Stock Physique'),

            ('recettesfiche', 'Onglet Recettes création rec./Fiche Tech.'),
            ('recettesrapport', 'Rapport Vente Journalieres'),
            ('recettesrapportentree', 'Rapport Entrée Stock Article'),
            ('recettesrapportsys', 'Synthèse Vente'),
            # ('recettestock', 'Onglet Recettes Entrée Stock'),
            ('view_recettestocksortie', 'Voir Article Facturation'),
            ('change_recettestocksortie', 'Modifier Article Facturation'),
            ('delete_recettestocksortie', 'Supprimer Article Facturation'),
            ('add_recettestocksortie', 'Ajouter Article Facturation'),
            #
            # ('Entrer_Stock', 'Onglet Entrer Stock'),
            # ('Sortie_Stock', 'Onglet Sortie Stock'),
            # ('Retour_Stock', 'Onglet Retour Stock'),
            # ('Rap_Prise_Inventaire', 'Onglet Rap. Prise Inv.Physique'),
            # ('Entrer_Stock_valid', 'Onglet Validation Entrer Stock'),
            # ('Bon_Commande_rapport', 'Onglet Rapport Bon Commande'),
            # ('Bon_Livraison_rapport', 'Onglet Rapport Bon Livraison'),
            # ('Rap_Logique_Physique', 'Onglet Rapport Physique/Logique'),
            # ('Rap_Stock', 'Onglet Rapport Stock'),
            # ('Rap_varia', 'Onglet Rapport Variation Stock'),
            # ('Rap_Client', 'Onglet Facturation Client'),
            # ('Rap_Sortie', 'Onglet Rapport Sortie'),
            # ('Rap_Sortie_full', 'Onglet Rapport Sortie Full'),
            # ('Rap_achat', 'Onglet Rapport Achat Full'),
            ('stockmenu', 'Onglet Stock'),
            ('auditmenu', 'Onglet Audit'),
            ('rapportmenu', 'Onglet Rapport'),

            # ('Rap_Client_Co', 'Onglet Rapport Consommations Client'),
            # ('Rap_Fourni', 'Onglet Facturation Fournisseur'),
            # ('Mise_Stock_Inventaire', 'Onglet Mise à Jour Stock Inventaire'),
            # ('Rap_Inventaire', 'Onglet Inventaire'),
            # ('Rap_Mvt_Produit', 'Onglet Rapport Mouvement Produit'),
            # ('Rap_Inve_Theori', 'Onglet Rapport Inventaire Théorique'),
            # ('Rap_Inve_Theori_Val', 'Onglet Rapport Inventaire Théorique Valorisé'),

            ('changelocation', 'Onglet Produit Change Location'),

        )


