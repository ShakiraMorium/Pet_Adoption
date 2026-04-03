from django import forms


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone = forms.CharField(max_length=32)
    address_line = forms.CharField(max_length=255)
    city = forms.CharField(max_length=120)
    postal_code = forms.CharField(max_length=20, required=False)
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))