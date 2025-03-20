from django.contrib import admin
from django.urls import path

from django_nonmodel_admin import NonModelAdmin, register as non_model_admin_register
from booking.views import UploadCSVView
from booking.models import MemberInfo, Inventory, Booking


@admin.register(MemberInfo)
class MemberInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "surname", "booking_count", "date_joined", "created_at")


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "remaining_count", "expiration_date", "created_at")


@admin.register(Booking)
class MemberInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "member", "booking_time", "status")


@non_model_admin_register()
class UploadCSVAdmin(NonModelAdmin):
    name = 'upload-csv-admin'
    verbose_name = 'Write CSV to Database'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_site.admin_view(self.upload_csv_admin_view), name='upload_csv_admin_view'),
        ]
        return custom_urls + urls

    def upload_csv_admin_view(self, request, extra_context=None):
        request.current_app = self.name
        return UploadCSVView.as_view()(request)

