from django.contrib import admin
from .models import Cart, CartItem, Adoption, AdoptionItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'pet', 'quantity']

@admin.register(Adoption)
class AdoptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'total_price', 'created_at']

@admin.register(AdoptionItem)
class AdoptionItemAdmin(admin.ModelAdmin):
    list_display = ['adoption', 'pet', 'quantity', 'price', 'total_price']
