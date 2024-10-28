from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import GroupAdmin, UserAdmin
# Register your models here.

from .models import *


# admin.site.register(Monnaie)
# admin.site.register(LocationUser)
# admin.site.register(SommeInventaire)
# admin.site.register(Paramet)




@admin.register(Femballage)
class EmballageAdmin(admin.ModelAdmin):
    ordering = ('designation',)
    exclude = ("flag", "codesocie")
    list_display = ("emballage","designation")
    search_fields = ['emballage', 'designation']


@admin.register(Ffamilles)
class FamillesAdmin(admin.ModelAdmin):
    ordering = ('designation',)
    exclude = ("flag","codesocie")
    list_display = ("famille","designation")
    search_fields = ['famille', 'designation']
#
# @admin.register(Fclasse)
# class ClassesAdmin(admin.ModelAdmin):
#     ordering = ('designation',)
#     exclude = ("flag", "codesocie")
#     list_display = ("classe","designation")
#     search_fields = ['classe', 'designation']


@admin.register(Flocation)
class LocationAdmin(admin.ModelAdmin):
    ordering = ('designation',)
    list_display_links = ("location","designation","adresse","txchange",'cptetaxe','cptetaxev','cptechf','dernierecloture','periode')
    list_display = ("location","designation","adresse","txchange",'cptetaxe','cptetaxev','cptechf','dernierecloture','periode')
    search_fields = ['location', 'designation']
    exclude=('dateinventaire','datejour','majstock','dateinvetactuel','cloture','inactivite','imputation1','imputation2','ctrfac',
    'codesocie','indinventaire','dernierecloturav','ctrach','ctrtransf','ctrajust','ctrrecu','strpapier','cpteclient','estcpte','articauto','ctrart','prixunik','flag')


# @admin.register(Ftiers)
# class TiersAdmin(admin.ModelAdmin):
#     ordering = ('nompostnom',)
#     list_display = ("tiers","nompostnom","nature","adresse","raisonsoc")
#     search_fields = ['nompostnom', 'nature']
    # readonly_fields=['dateinventaire','periode','dernierecloture','datejour','majstock','dateinvetactuel','cloture','inactivite','typelocation',
    # 'codesocie','indinventaire','dernierecloturav','ctrach','ctrtransf','ctrajust','ctrrecu','strpapier','cpteclient','cptetaxe','cptetaxev',
    # 'cptechf','estcpte','articauto','ctrart','prixunik']

#
# @admin.register(Ftaxes)
# class TaxesAdmin(admin.ModelAdmin):
#     ordering = ('designation',)
#     exclude = ("codesocie","application")
#     list_display = ("taxe","designation","taux")
#     search_fields = ['designation']


# @admin.register(Fajustement)
# class AjustementAdmin(admin.ModelAdmin):
#     ordering = ('designation',)
#     list_display = ("ajustement","designation","mvt")
#     search_fields = ['designation']



# @admin.register(Farticle)
# class ArticleAdmin(admin.ModelAdmin):
#     ordering = ('designation',)
#     list_display = ("article","designation","famille","classe","emballagee","emballageu","quantitee")
#     search_fields = ['article', 'designation']
#     # readonly_fields=['dateinventaire','periode','dernierecloture','datejour','majstock','dateinvetactuel','cloture','inactivite','typelocation',
#     # 'codesocie','indinventaire','dernierecloturav','ctrach','ctrtransf','ctrajust','ctrrecu','strpapier','cpteclient','cptetaxe','cptetaxev',
#     # 'cptechf','estcpte','articauto','ctrart','prixunik']


# class MyGroupAdminForm(forms.ModelForm):
#
#     class Meta:
#         model = Group
#         fields = (
#             'name',
#             'permissions',
#         )
#
#     permissions = forms.ModelMultipleChoiceField(
#         # Permission.objects.exclude(content_type__app_label='auth'),
#         Permission.objects.exclude(name__startswith='Can'),
#         # Permission.objects.exclude(content_type__app_label__in=['auth', 'admin', 'sessions', 'users', 'contenttypes']),
#         widget=admin.widgets.FilteredSelectMultiple(('permissions'), False))
#
# class MyGroupAdmin(GroupAdmin):
#     form = MyGroupAdminForm
#     search_fields = ('name',)
#     ordering = ('name',)
#
# class MyUserAdmin(UserAdmin):
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
#         (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
#                                       'groups',)}),
#         (('Important dates'), {'fields': ('last_login', 'date_joined')}),
#     )
#
# admin.site.unregister(Group)
# admin.site.register(Group, MyGroupAdmin)
# admin.site.unregister(User)
# admin.site.register(User, MyUserAdmin)
