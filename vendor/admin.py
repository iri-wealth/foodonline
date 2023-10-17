from django.contrib import admin
from .models import Vendor
# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'vendor_name', 'created_at', 'updated_at')
    list_display_links = ('user', 'vendor_name')
admin.site.register(Vendor, VendorAdmin)