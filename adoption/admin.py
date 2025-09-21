from django.contrib import admin
from adoption.models import Cart, CartItem, Adoption, AdoptionItem

# Register your models here.


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']


@admin.register(Adoption)
class AdoptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status']


admin.site.register(CartItem)
admin.site.register(AdoptionItem)
