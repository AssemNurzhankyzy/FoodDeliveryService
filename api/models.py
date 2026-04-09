from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, RegexValidator

## c. Address model with FK to User, address type, and validation for phone number and street length.

class Address(models.Model):
    ADDRESS_TYPES =[
        ('home', 'Home'),
        ('work', 'Work'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses') 
    address_type=models.CharField(max_length=10, choices=ADDRESS_TYPES, default='home')
    street = models.CharField(max_length=255, validators=[MinLengthValidator(5)])
    building= models.CharField(max_length=50, blank=True, null=True)
    apartment = models.CharField(max_length=50, blank=True,null=True)
    entrance= models.CharField(max_length=10, blank=True, null=True)
    floor= models.CharField(max_length=5, blank=True, null=True)
    phone_number= models.CharField(max_length=20, validators=[RegexValidator(regex=r'^\+7\(\d{3}\)-\d{3}-\d{2}-\d{2}$', message="Phone number must be in the format +7(XXX)-XXX-XX-XX")])
    special_instructions= models.TextField(blank=True, max_length=200)
    is_default= models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_default', '-created_at']
        unique_together = ('user', 'street', 'building', 'apartment', 'entrance', 'floor')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)   # save first
        if self.is_default:
            Address.objects.filter(
                user=self.user,
                is_default=True
            ).exclude(pk=self.pk).update(is_default=False)

    def __str__(self):
            return f"{self.user.username} - {self.street}, {self.building}, {self.apartment}"
