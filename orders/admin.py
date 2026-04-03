from django.contrib import admin
from orders.models import Cart, CartItem, CheckoutAddress, Order, OrderItem

# Cart admin
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    search_fields = ['user__email']
    list_filter = ['created_at']  

# Order admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status']
    search_fields = ['user__email']
    list_filter = ['status', 'created_at']  

# Register CartItem and OrderItem without custom admin
admin.site.register(CartItem)
admin.site.register(OrderItem)
admin.site.register(CheckoutAddress)