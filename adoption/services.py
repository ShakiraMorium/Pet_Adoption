from adoption.models import Cart, CartItem, AdoptionItem, Adoption
from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError


class AdoptionService:
    @staticmethod
    def create_adoption(user_id, cart_id):
        with transaction.atomic():
            cart = Cart.objects.get(pk=cart_id)
            cart_items = cart.items.select_related('pet').all()

            total_price = sum([item.pet.adoption_fee * item.quantity for item in cart_items])

            adoption = Adoption.objects.create(
                user_id=user_id,
                total_price=total_price
            )

            adoption_items = [
                AdoptionItem(
                    adoption=adoption,
                    pet=item.pet,
                    price=item.pet.adoption_fee,
                    quantity=item.quantity,
                    total_price=item.pet.adoption_fee * item.quantity
                )
                for item in cart_items
            ]

            AdoptionItem.objects.bulk_create(adoption_items)

            # clear the cart after adoption
            cart.delete()

            return adoption

    @staticmethod
    def cancel_adoption(adoption, user):
        if user.is_staff:
            adoption.status = Adoption.CANCELED
            adoption.save()
            return adoption

        if adoption.user != user:
            raise PermissionDenied({"detail": "You can only cancel your own adoption"})

        if adoption.status == Adoption.DELIVERED:
            raise ValidationError({"detail": "You cannot cancel an adoption that is already delivered"})

        adoption.status = Adoption.CANCELED
        adoption.save()
        return adoption
