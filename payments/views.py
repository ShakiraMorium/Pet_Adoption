from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


from orders.models import Order
from .services import initiate_sslcommerz_payment


@api_view(['POST'])
def initiate_payment(request):
    order_id = request.data.get('order_id')
    if not order_id:
        return Response({'detail': 'order_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    user_data = {
        'full_name': request.data.get('full_name') or request.user.get_full_name() or request.user.email,
        'email': request.data.get('email') or request.user.email,
        'phone': request.data.get('phone') or request.user.phone_number or '01700000000',
        'address': request.data.get('address') or request.user.address or 'Dhaka',
    }
    payment_url = initiate_sslcommerz_payment(order=order, user_data=user_data)
    if payment_url:
        return Response({'payment_url': payment_url})

    return Response({'detail': 'Payment gateway is not configured.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)



@api_view(['POST'])
def payment_success(request):
    order_id = request.data.get('value_a') or request.POST.get('value_a')
    if order_id:
        Order.objects.filter(id=order_id).update(status=Order.READY_TO_SHIP)
    return HttpResponseRedirect('/shop/dashboard/')


@api_view(['POST'])
def payment_cancel(request):
    return HttpResponseRedirect('/shop/dashboard/')


@api_view(['POST'])
def payment_fail(request):
    return HttpResponseRedirect('/shop/dashboard/')