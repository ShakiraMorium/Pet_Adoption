from decimal import Decimal

from pets.models import Pet


class SessionCart:
    SESSION_KEY = 'cart'

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(self.SESSION_KEY)
        if cart is None:
            cart = self.session[self.SESSION_KEY] = {}
        self.cart = cart

    def add(self, pet_id: int, quantity: int = 1):
        pet_key = str(pet_id)
        if pet_key not in self.cart:
            self.cart[pet_key] = {'quantity': 0}
        self.cart[pet_key]['quantity'] += max(1, int(quantity))
        self.save()

    def update(self, pet_id: int, quantity: int):
        pet_key = str(pet_id)
        if pet_key not in self.cart:
            return
        if quantity <= 0:
            self.remove(pet_id)
            return
        self.cart[pet_key]['quantity'] = int(quantity)
        self.save()

    def remove(self, pet_id: int):
        pet_key = str(pet_id)
        if pet_key in self.cart:
            del self.cart[pet_key]
            self.save()

    def clear(self):
        self.session[self.SESSION_KEY] = {}
        self.session.modified = True
        self.cart = {}

    def save(self):
        self.session[self.SESSION_KEY] = self.cart
        self.session.modified = True

    def items(self):
        pet_ids = self.cart.keys()
        pets = Pet.objects.filter(id__in=pet_ids)
        pet_map = {str(p.id): p for p in pets}
        line_items = []
        for pet_id, entry in self.cart.items():
            pet = pet_map.get(pet_id)
            if not pet:
                continue
            quantity = int(entry['quantity'])
            unit_price = Decimal(pet.adoption_fee)
            line_total = unit_price * quantity
            line_items.append({
                'pet': pet,
                'quantity': quantity,
                'unit_price': unit_price,
                'line_total': line_total,
            })
        return line_items

    def total(self):
        return sum((item['line_total'] for item in self.items()), Decimal('0.00'))

    def count(self):
        return sum(int(item['quantity']) for item in self.cart.values())

    def is_empty(self):
        return len(self.cart) == 0