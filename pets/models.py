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
    adoption_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    description = models.TextField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(
        PetCategory, on_delete=models.CASCADE, related_name="pets")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(PetCategory,on_delete=models.CASCADE,related_name="pets")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id',]
    
    def __str__(self):
        return self.name
    



class PetImage(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="images")
    image = CloudinaryField('image')
    # image = models.ImageField(upload_to="images", validators=[validate_file_size])


    # def __str__(self):
    #     return f"Image of {self.pet.name}"


class PetReview(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ratings = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.first_name} - {self.ratings}"


class CartRequest(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="price")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} -> {self.pet.name}"
