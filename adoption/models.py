from django.db import models
from django.core.validators import MinValueValidator
from users.models import PetUser
from pets.models import Pet
from uuid import uuid4

# Create your models here.


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(
        PetUser, on_delete=models.CASCADE, related_name="cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.first_name}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="items"
    )
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = [["cart", "pet"]]

    def __str__(self):
        return f"{self.quantity} x {self.pet.name}"


class Adoption(models.Model):
    NOT_PAID = "Not Paid"
    READY_TO_SHIP = "Ready To Ship"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELED = "Canceled"
    STATUS_CHOICES = [
        (NOT_PAID, "Not Paid"),
        (READY_TO_SHIP, "Ready To Ship"),
        (SHIPPED, "Shipped"),
        (DELIVERED, "Delivered"),
        (CANCELED, "Canceled"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(
        PetUser, on_delete=models.CASCADE, related_name="adoptions"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=NOT_PAID
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Adoption {self.id} by {self.user.first_name} - {self.status}"


class AdoptionItem(models.Model):
    adoption = models.ForeignKey(
        Adoption, on_delete=models.CASCADE, related_name="items"
    )
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.pet.name}"
