from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase

from pets.models import Pet, PetCategory

from .session_cart import SessionCart


class SessionCartTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            email='cart@example.com',
            password='password123',
            first_name='Cart',
            last_name='Tester',
            phone_number='123456789',
            address='Test Address',
        )
        self.category = PetCategory.objects.create(name='Dog')
        self.pet = Pet.objects.create(
            name='Buddy',
            breed='Labrador',
            age=2,
            adoption_fee=150,
            category=self.category,
            is_available=True,
        )

    def _request(self):
        request = self.factory.get('/')
        request.user = self.user
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()
        return request

    def test_add_and_total(self):
        request = self._request()
        cart = SessionCart(request)
        cart.add(self.pet.id, 2)

        self.assertEqual(cart.count(), 2)
        self.assertEqual(float(cart.total()), 300.0)