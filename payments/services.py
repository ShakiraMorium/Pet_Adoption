import uuid

import requests
from django.conf import settings


def initiate_sslcommerz_payment(order, user_data):
    """Initiate SSLCommerz payment and return redirect URL."""
    store_id = getattr(settings, 'SSLCOMMERZ_STORE_ID', None)
    store_pass = getattr(settings, 'SSLCOMMERZ_STORE_PASSWORD', None)
    sandbox = getattr(settings, 'SSLCOMMERZ_IS_SANDBOX', True)

    if not store_id or not store_pass:
        return None

    endpoint = 'https://sandbox.sslcommerz.com/gwprocess/v4/api.php' if sandbox else 'https://securepay.sslcommerz.com/gwprocess/v4/api.php'
    transaction_id = f"order_{order.id}_{uuid.uuid4().hex[:8]}"

    payload = {
        'store_id': store_id,
        'store_passwd': store_pass,
        'total_amount': f'{order.total_price:.2f}',
        'currency': 'BDT',
        'tran_id': transaction_id,
        'success_url': f"{settings.BACKEND_URL}/api/v1/payment/success/",
        'fail_url': f"{settings.BACKEND_URL}/api/v1/payment/fail/",
        'cancel_url': f"{settings.BACKEND_URL}/api/v1/payment/cancel/",
        'shipping_method': 'NO',
        'product_name': 'Pet Adoption Checkout',
        'product_category': 'Adoption',
        'product_profile': 'general',
        'cus_name': user_data['full_name'],
        'cus_email': user_data['email'],
        'cus_add1': user_data['address'],
        'cus_city': 'Dhaka',
        'cus_country': 'Bangladesh',
        'cus_phone': user_data['phone'],
        'value_a': str(order.id),
    }

    try:
        response = requests.post(endpoint, data=payload, timeout=15)
        data = response.json()
        return data.get('GatewayPageURL') if data.get('status') == 'SUCCESS' else None
    except (requests.RequestException, ValueError):
        return None