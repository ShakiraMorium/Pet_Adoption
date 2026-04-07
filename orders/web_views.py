from django.conf import settings
from django.contrib import messages
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from pets.models import Pet

from .forms import CheckoutForm
from .models import CheckoutAddress, Order, OrderItem
from .session_cart import SessionCart


class PetCatalogView(ListView):
    model = Pet
    template_name = 'orders/catalog.html'
    context_object_name = 'pets'
    def get_queryset(self):
        return Pet.objects.filter(is_available=True).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = SessionCart(self.request)
        context['cart_count'] = cart.count()
        return context


class PetDetailView(DetailView):
    model = Pet
    template_name = 'orders/pet_detail.html'
    context_object_name = 'pet'

    def get_queryset(self):
        return Pet.objects.select_related('category').prefetch_related('reviews__user', 'images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = SessionCart(self.request)
        context['cart_count'] = cart.count()
        return context

class CartDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/cart_detail.html'
    login_url = '/admin/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = SessionCart(self.request)
        context.update({
            'cart_items': cart.items(),
            'cart_total': cart.total(),
            'cart_count': cart.count(),
        })
        return context
class CartAddView(LoginRequiredMixin, View):
    login_url = '/admin/login/'

    def post(self, request, pet_id):
        cart = SessionCart(request)
        pet = get_object_or_404(Pet, pk=pet_id, is_available=True)
        quantity = int(request.POST.get('quantity', 1))
        cart.add(pet.id, quantity)
        messages.success(request, f'{pet.name} added to cart.')
        return redirect('orders:cart_detail')


class CartUpdateView(LoginRequiredMixin, View):
    login_url = '/admin/login/'

    def post(self, request, pet_id):
        cart = SessionCart(request)
        quantity = int(request.POST.get('quantity', 1))
        cart.update(pet_id, quantity)
        return redirect('orders:cart_detail')


class CartRemoveView(LoginRequiredMixin, View):
    login_url = '/admin/login/'

    def post(self, request, pet_id):
        cart = SessionCart(request)
        cart.remove(pet_id)
        messages.info(request, 'Item removed from your cart.')
        return redirect('orders:cart_detail')
    
class CheckoutView(LoginRequiredMixin, View):
    login_url = '/admin/login/'

    @transaction.atomic
    def post(self, request):
        cart = SessionCart(request)
        if cart.is_empty():
            messages.warning(request, 'Your cart is empty.')
            return redirect('orders:cart_detail')
        
        form = CheckoutForm(request.POST)
        if not form.is_valid():
            return self._render_page(request, cart, form)

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
        messages.success(request, 'Checkout complete. Please complete payment through SSLCommerz.')
        return redirect('orders:payment_redirect', order_id=order.id)

    def get(self, request):
        cart = SessionCart(request)
        if cart.is_empty():
            messages.warning(request, 'Your cart is empty.')
            return redirect('orders:cart_detail')

        user = request.user
        form = CheckoutForm(initial={
            'full_name': f'{user.first_name} {user.last_name}'.strip(),
            'email': user.email,
            'phone': getattr(user, 'phone_number', ''),
            'address_line': getattr(user, 'address', ''),
        })
        return self._render_page(request, cart, form)

    def _render_page(self, request, cart, form):
        return render(request, 'orders/checkout.html', {
            'form': form,
            'cart_items': cart.items(),
            'cart_total': cart.total(),
            'cart_count': cart.count(),
        })


class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/dashboard.html'
    login_url = '/admin/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.filter(user=self.request.user).prefetch_related('items__pet').order_by('-created_at')
        context['orders'] = orders
        context['total_orders'] = orders.count()
        context['pending_orders'] = orders.filter(status=Order.NOT_PAID).count()
        return context


class CheckoutSuccessView(LoginRequiredMixin, DetailView):
    model = Order
    pk_url_kwarg = 'order_id'
    context_object_name = 'order'
    template_name = 'orders/checkout_success.html'
    login_url = '/admin/login/'

    def get_queryset(self):
        return Order.objects.prefetch_related('items__pet').filter(user=self.request.user)


class PaymentRedirectView(LoginRequiredMixin, View):
    login_url = '/admin/login/'

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        from payments.services import initiate_sslcommerz_payment
        checkout_data = {
            'full_name': request.user.get_full_name() or request.user.email,
            'email': request.user.email,
            'phone': request.user.phone_number or '01700000000',
            'address': request.user.address or 'Dhaka',
        }
        payment_url = initiate_sslcommerz_payment(order=order, user_data=checkout_data)
        if payment_url:
            return redirect(payment_url)
        messages.error(request, 'Payment gateway unavailable. Please contact support.')
        return redirect(reverse('orders:checkout_success', kwargs={'order_id': order.id}))