from django.contrib import admin
from .models import Pet, PetCategory, PetImage, PetReview, AdoptionRequest


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'breed', 'age', 'adoption_fee', 'is_available']
    list_filter = ['breed', 'is_available']
    search_fields = ['name', 'breed', 'description']
    ordering = ['name']


@admin.register(PetCategory)
class PetCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name']


@admin.register(PetImage)
class PetImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'pet']


@admin.register(PetReview)
class PetReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'pet', 'user', 'ratings', 'created_at']


@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'pet', 'user', 'approved', 'requested_at']
