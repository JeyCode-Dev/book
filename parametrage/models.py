from django.contrib.auth.models import User, AbstractUser
from django.db import models

# Create your models here.
class TimespantedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

class CategorieArticle(TimespantedModel):
    libelle = models.CharField(max_length=200,null=True)

class Paramet(models.Model):
    codesocie = models.CharField("Code",db_column='CODESOCIE', primary_key=True, max_length=3)  # Field name made lowercase.
    libelle = models.CharField(db_column='LIBELLE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    adresse = models.CharField(db_column='ADRESSE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cdpostal = models.CharField("RCCM",db_column='CDPOSTAL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    telephone = models.CharField("Id Nat",db_column='TELEPHONE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fax = models.CharField("Téléphone",db_column='FAX', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ville = models.CharField(db_column='VILLE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    pays = models.CharField(db_column='PAYS', max_length=12, blank=True, null=True)  # Field name made lowercase.
    cddevise = models.CharField(db_column='CDDEVISE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    lastperiode = models.CharField(db_column='LASTPERIODE', max_length=6, blank=True, null=True)  # Field name made lowercase.
    debutperiode = models.TextField(db_column='DEBUTPERIODE', blank=True, null=True)  # Field name made lowercase.
    finperiode = models.TextField(db_column='FINPERIODE', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.libelle
    class Meta:
        managed = False
        verbose_name="Socièté"
        verbose_name_plural="Sociètés"
        db_table = 'PARAMET'



Sexe = (
    ("F","Feminin"),
    ("M","Masculin")
    )
categorie=(
    ('D', 'Depôt'),
    ('M', 'Magasin'),
    ('A', 'Agent'),
    ('E', 'Externe')


)


#CPTETAXE=txemb1
#CPTETAXEV=txemb2
#CPTECHF=txemb3

class Flocation(models.Model):
    location = models.CharField(db_column='LOCATION', primary_key=True, max_length=50)  # Field name made lowercase.
    designation = models.CharField(db_column='DESIGNATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    adresse = models.CharField(db_column='ADRESSE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dateinventaire = models.CharField(db_column='DATEINVENTAIRE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    periode = models.CharField('RCCM',db_column='PERIODE', max_length=25, blank=True, null=True)  # Field name made lowercase.
    imputation1 = models.CharField("Caisse CDF",db_column='IMPUTATION1', max_length=16, blank=True, null=True)  # Field name made lowercase.
    imputation2 = models.CharField("Caisse USD",db_column='IMPUTATION2', max_length=16, blank=True, null=True)  # Field name made lowercase.
    dernierecloture = models.CharField('numero',db_column='DERNIERECLOTURE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    datejour = models.CharField(db_column='DATEJOUR', max_length=15, blank=True, null=True)  # Field name made lowercase.
    inactivite = models.SmallIntegerField(db_column='INACTIVITE', blank=True, null=True)  # Field name made lowercase.
    majstock = models.BooleanField(db_column='MAJSTOCK', blank=True, null=True)  # Field name made lowercase.
    txchange = models.FloatField(db_column='TXCHANGE', blank=True, null=True)  # Field name made lowercase.
    ctrfac = models.FloatField("N° Facture",db_column='CTRFAC', blank=True, null=True)  # Field name made lowercase.
    dateinvetactuel = models.CharField(db_column='DATEINVETACTUEL', max_length=15, blank=True, null=True)  # Field name made lowercase.
    cloture = models.BooleanField(db_column='CLOTURE', blank=True, null=True)  # Field name made lowercase.
    typelocation = models.CharField("Catégorie",db_column='TYPELOCATION',choices=categorie ,max_length=1, default='M')  # Field name made lowercase.
    codesocie = models.CharField(db_column='CODESOCIE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    flag = models.BooleanField("Dépôt central ?",db_column='FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    indinventaire = models.CharField(db_column='INDINVENTAIRE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    dernierecloturav = models.CharField(db_column='DERNIERECLOTURAV', max_length=15, blank=True, null=True)  # Field name made lowercase.
    ctrach = models.IntegerField(db_column='CTRACH', blank=True, null=True)  # Field name made lowercase.
    ctrtransf = models.IntegerField(db_column='CTRTRANSF', blank=True, null=True)  # Field name made lowercase.
    ctrajust = models.IntegerField(db_column='CTRAJUST', blank=True, null=True)  # Field name made lowercase.
    ctrrecu = models.IntegerField(db_column='CTRRECU', blank=True, null=True)  # Field name made lowercase.
    strpapier = models.CharField(db_column='STRPAPIER', max_length=2, blank=True, null=True)  # Field name made lowercase.
    cpteclient = models.CharField(db_column='CPTECLIENT', max_length=16, blank=True, null=True)  # Field name made lowercase.
    cptetaxe = models.CharField('Pourc.Emb1',db_column='CPTETAXE', max_length=16, blank=True, null=True)  # Field name made lowercase.
    cptetaxev = models.CharField('Pourc.Emb2',db_column='CPTETAXEV', max_length=16, blank=True, null=True)  # Field name made lowercase.
    cptechf = models.CharField('Pourc.Emb3',db_column='CPTECHF', max_length=16, blank=True, null=True)  # Field name made lowercase.
    estcpte = models.BooleanField(db_column='ESTCPTE', blank=True, null=True)  # Field name made lowercase.
    articauto = models.BooleanField(db_column='ARTICAUTO', blank=True, null=True)  # Field name made lowercase.
    ctrart = models.IntegerField(db_column='CTRART', blank=True, null=True)  # Field name made lowercase.
    prixunik = models.BooleanField(db_column='PRIXUNIK', blank=True, null=True)  # Field name made lowercase.


    def __str__(self):

        return self.designation

    class Meta:
        managed = False
        verbose_name="Magasin"
        verbose_name_plural="Magasins"
        db_table = 'FLOCATION'


class CustomUser(AbstractUser):

    sexe = models.CharField(choices=Sexe, max_length=255)
    matricule = models.CharField(max_length=255, null=True, blank=True)
    telephone = models.CharField(max_length=16, null=True, blank=True)
    adresse = models.CharField(max_length=255, null=True, blank=True)

    affectation = models.ManyToManyField(Flocation,null=True, blank=True)


# class CategorieProduit(TimespantedModel):
#     libelle = models.CharField(max_length=255)
#     created_by = models.ForeignKey(CustomUser, editable=False,on_delete=models.SET_NULL, null=True, blank=True)
#
#     def __str__(self):
#         return self.libelle
#
#
#
# class Produit(TimespantedModel):
#     libelle = models.CharField(max_length=255)
#     prix = models.DecimalField(max_digits=8, decimal_places=2)
#     image=models.ImageField(upload_to='uploads/%Y/%m/%d/')
#     categorie= models.ForeignKey(CategorieProduit, on_delete=models.SET_NULL, null=True)
#     created_by = models.ForeignKey(CustomUser, editable=False,on_delete=models.SET_NULL, null=True, blank=True)
#
# class Client(TimespantedModel):
#     nom = models.CharField(max_length=50)
#     telephone = models.CharField(max_length=50)
#     adresse = models.CharField(max_length=50)
#     created_by = models.ForeignKey(CustomUser, editable=False, on_delete=models.SET_NULL,null=True, blank=True)
#
#
# class Societe(TimespantedModel):
#     nom = models.CharField(max_length=100)
#     sigle = models.CharField(max_length=15)
#     adresse = models.CharField(max_length=100)
#     telephone = models.CharField(max_length=100)
#     idetat = models.CharField(max_length=255)
#     email = models.EmailField(max_length=100)


class Droit(models.Model):
    class Meta:
        permissions = (
            # ('cuisine', 'Acceuil Cuisine'),
            # ('serveur', 'Operation Sur le serveur'),

        )