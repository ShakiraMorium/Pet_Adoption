from django.contrib import admin
from pets.models import Pet, PetCategory, PetReview, PetImage, CartRequest

# Simple registrations
# admin.site.register(PetReview)
# admin.site.register(CartRequest)

# @admin.register(PetCategory)
# class PetCategoryAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'description']
#     search_fields = ['name']

# @admin.register(PetImage)
# class PetImageAdmin(admin.ModelAdmin):
#     list_display = ['id', 'pet']

# @admin.register(Pet)
# class PetAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'breed', 'age', 'cart_items_count']

    # def cart_items_count(self, obj):
    #     return obj.cart_items.count()  # Make sure CartItem has related_name="cart_items"
    # cart_items_count.short_description = 'Cart Items'
admin.site.register(Pet)
admin.site.register(PetImage)
admin.site.register(PetCategory)
admin.site.register(PetReview)