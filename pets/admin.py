from django.contrib import admin
from .models import Pet, PetCategory, PetImage, PetReview, AdoptionRequest


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'age', 'adoption_fee', 'available']
    list_filter = ['category', 'available']
    search_fields = ['name', 'description']


@admin.register(PetCategory)
class PetCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name']


@admin.register(PetImage)
class PetImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'pet', 'image']


@admin.register(PetReview)
class PetReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'pet', 'user', 'ratings', 'created_at']
    list_filter = ['ratings', 'created_at']
    search_fields = ['comment', 'user__email', 'pet__name']


@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'pet', 'user', 'approved', 'requested_at']
    list_filter = ['approved', 'requested_at']
    search_fields = ['user__email', 'pet__name']
    readonly_fields = ['requested_at']
