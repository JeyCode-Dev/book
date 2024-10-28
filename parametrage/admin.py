from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

# @admin.register(Produit)
# class ProduitAdmin(admin.ModelAdmin):
#     ordering = ('libelle',)
#     list_display = ("id","libelle","prix","categorie")
#     search_fields = ['libelle']
#     def save_model(self, request, obj, form, change):
#         if not obj.created_by:
#             obj.created_by = request.user
#         obj.save()
#
#
#
# @admin.register(Societe)
# class SocieteAdmin(admin.ModelAdmin):
#     ordering = ('-created_at',)
#     list_display = ("id","nom","sigle","created_at")
#     search_fields = ['nom', ]
@admin.register(Paramet)
class ParametAdmin(admin.ModelAdmin):
    ordering = ('libelle',)
    exclude = ("lastperiode","debutperiode","finperiode")
    list_display = ("codesocie","libelle","adresse","fax")
    search_fields = ['codesocie', 'libelle']


# @admin.register(CategorieArticle)
# class CategorieArticleAdmin(admin.ModelAdmin):
#     ordering = ('libelle',)
#     list_display = ("id","libelle")
#     search_fields = ['libelle']

class CustomUserAdmin(UserAdmin):
    list_display = (
        'username','matricule', 'first_name', 'last_name', 'is_staff',
        'email','sexe','telephone','adresse'
    )

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('matricule','first_name', 'last_name', 'email','sexe','telephone','adresse')
        }),
        ('Affecations', {
            'fields': (
                'affectation',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        # ('Additional info', {
        #     'fields': ('add1', 'add1', 'add1')
        # })
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('matricule','first_name', 'last_name', 'email','sexe','telephone','adresse')
        }),
        ('Affecations', {
            'fields': (
                'affectation',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        # ('Additional info', {
        #     'fields': ('add1', 'add1', 'add1')
        # })
    )

admin.site.register(CustomUser, CustomUserAdmin)

#
# @admin.register(CategorieProduit)
# class CategorieProduitAdmin(admin.ModelAdmin):
#     ordering = ('libelle',)
#     list_display = ("id","libelle")
#     search_fields = ['libelle']
#     def save_model(self, request, obj, form, change):
#         if not obj.created_by:
#             obj.created_by = request.user
#         obj.save()
#
#
# @admin.register(Client)
# class ClientAdmin(admin.ModelAdmin):
#     ordering = ('nom',)
#     list_display = ("id","nom","telephone","adresse")
#     search_fields = ['nom']
#     def save_model(self, request, obj, form, change):
#         if not obj.created_by:
#             obj.created_by = request.user
#         obj.save()


