from cart.models import Cart, CartItem, CartItem, Cart
from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError


class CartService:
    @staticmethod
    def create_cart(user_id, cart_id):
        with transaction.atomic():
            cart = Cart.objects.get(pk=cart_id)
            cart_items = cart.items.select_related('pet').all()

            total_price = sum([item.pet.cart_fee * item.quantity for item in cart_items])

            cart = Cart.objects.create(
                user_id=user_id,
                total_price=total_price
            )

            cart_items = [
                CartItem(
                    cart=cart,
                    pet=item.pet,
                    price=item.pet.cart_fee,
                    quantity=item.quantity,
                    total_price=item.pet.cart_fee * item.quantity
                )
                for item in cart_items
            ]

            CartItem.objects.bulk_create(cart_items)

            # clear the cart after adoption
            cart.delete()

            return cart

    @staticmethod
    def cancel_cart(cart, user):
        if user.is_staff:
            cart.status = Cart.CANCELED
            cart.save()
            return cart

        if cart.user != user:
            raise PermissionDenied({"detail": "You can only cancel your own adoption"})

        if cart.status == Cart.DELIVERED:
            raise ValidationError({"detail": "You cannot cancel an adoption that is already delivered"})

        cart.status = Cart.CANCELED
        cart.save()
        return cart
