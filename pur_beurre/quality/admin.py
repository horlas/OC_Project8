from django.contrib import admin
from .models import *

@admin.register(CustonUserModel)
class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ['username', "email", "password"]
    readonly_fields = ['created_at']



@admin.register(Backup)
class BackupAdmin(admin.ModelAdmin):
   model = Backup
   verbose_name = 'Sauvegarde'


@admin.register(SelectedProduct)
class SelectedProductAdmin(admin.ModelAdmin):
    model = SelectedProduct
    verbose_name = 'Produit selectionné'



@admin.register(SubstitutProduct)
class SubstitutProductAdmin(admin.ModelAdmin):
    model = SubstitutProduct
    verbose_name = 'Produit substitué'



