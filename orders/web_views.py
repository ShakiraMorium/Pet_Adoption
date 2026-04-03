from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from pets.models import Pet

from .forms import CheckoutForm
from .models import CheckoutAddress, Order, OrderItem
from .session_cart import SessionCart


def pet_catalog(request):
    pets = Pet.objects.filter(is_available=True).select_related('category')
    cart = SessionCart(request)
    return render(request, 'orders/catalog.html', {'pets': pets, 'cart_count': cart.count()})


@require_POST
def cart_add(request, pet_id):
    cart = SessionCart(request)
    pet = get_object_or_404(Pet, pk=pet_id, is_available=True)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(pet.id, quantity)
    messages.success(request, f'{pet.name} added to cart.')
    return redirect('orders:cart_detail')


@require_POST
def cart_update(request, pet_id):
    cart = SessionCart(request)
    quantity = int(request.POST.get('quantity', 1))
    cart.update(pet_id, quantity)
    return redirect('orders:cart_detail')


@require_POST
def cart_remove(request, pet_id):
    cart = SessionCart(request)
    cart.remove(pet_id)
    return redirect('orders:cart_detail')


def cart_detail(request):
    cart = SessionCart(request)
    context = {
        'cart_items': cart.items(),
        'cart_total': cart.total(),
        'cart_count': cart.count(),
    }
    return render(request, 'orders/cart_detail.html', context)


@login_required
@transaction.atomic
def checkout(request):
    cart = SessionCart(request)
    if cart.is_empty():
        messages.warning(request, 'Your cart is empty.')
        return redirect('orders:cart_detail')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                total_price=cart.total(),
                status=Order.NOT_PAID,
            )

            for item in cart.items():
                OrderItem.objects.create(
                    order=order,
                    pet=item['pet'],
                    quantity=item['quantity'],
                    price=item['unit_price'],
                    total_price=item['line_total'],
                )

            CheckoutAddress.objects.create(order=order, **form.cleaned_data)
            cart.clear()
            messages.success(request, 'Checkout complete. Your order has been placed.')
            return redirect('orders:checkout_success', order_id=order.id)
    else:
        user = request.user
        form = CheckoutForm(initial={
            'full_name': f'{user.first_name} {user.last_name}'.strip(),
            'email': user.email,
            'phone': getattr(user, 'phone_number', ''),
        })

    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart_items': cart.items(),
        'cart_total': cart.total(),
        'cart_count': cart.count(),
    })


@login_required
def checkout_success(request, order_id):
    order = get_object_or_404(Order.objects.prefetch_related('items__pet'), pk=order_id, user=request.user)
    return render(request, 'orders/checkout_success.html', {'order': order})