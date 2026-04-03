from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from orders.models import Order


@api_view(['POST'])
def initiate_payment(request):
    # Placeholder for gateway integration.
    return Response({"detail": "Payment gateway is not configured."}, status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['POST'])
def payment_success(request):
    order_id = request.data.get("tran_id", "").split('_')[-1]
    if order_id:
        Order.objects.filter(id=order_id).update(status="Ready To Ship")
    return HttpResponseRedirect('/api/v1/orders/')


@api_view(['POST'])
def payment_cancel(request):
    return HttpResponseRedirect('/api/v1/orders/')


@api_view(['POST'])
def payment_fail(request):
    return HttpResponseRedirect('/api/v1/orders/')