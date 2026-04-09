from django.test import TestCase
from django.contrib.auth.models import User
from .models import Address

class AddressModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='Test@1234'
        )

    def test_create_address(self):
        address = Address.objects.create(
            user=self.user,
            street='ToleBi',
            building='59',
            phone_number='+7(777)-123-45-67',
            is_default=True
        )
        self.assertEqual(str(address), f"{self.user.username} - {address.street}, {address.building}, {address.apartment}")

    def test_only_one_default_address(self):
        Address.objects.create(
            user=self.user,
            street='Abay',
            building='6',
            phone_number='+7(777)-123-45-67',
            is_default=True
        )
        Address.objects.create(
            user=self.user,
            street='Abylay-khan',
            building='5',
            phone_number='+7(777)-999-88-77',
            is_default=True
        )
        default_count = Address.objects.filter(user=self.user, is_default=True).count()
        self.assertEqual(default_count, 1)