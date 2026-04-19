from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from pets.validators import validate_file_size
from cloudinary.models import CloudinaryField

class PetCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Pet(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    description = models.TextField()
    adoption_fee = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    
    # FIX: Point this to 'PetCategory' (the actual class name above)
    petCategory = models.ForeignKey(
        'PetCategory', 
        on_delete=models.CASCADE, 
        related_name='pets'
    ) 
    
    image = models.ImageField(upload_to='pets/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class PetImage(models.Model):
    pet = models.ForeignKey(
        Pet, on_delete=models.CASCADE, related_name='images'
    )
    image = CloudinaryField('image')

class PetReview(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ratings = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        # Added a fallback in case user doesn't have a first_name set
        name = self.user.first_name if self.user.first_name else self.user.username
        return f"PetReview by {name} on {self.pet.name}"

class CartRequest(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="cart_requests")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} -> {self.pet.name}"