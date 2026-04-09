from django.contrib import admin
from .models import Address

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_type', 'street', 'building', 'apartment', 'is_default', 'created_at')
    list_filter = ('address_type', 'is_default')
    search_fields = ('user__username', 'street', 'building', 'apartment')
    ordering = ('-created_at',)

# Register your models here.
