from datetime import datetime

from django.contrib import messages
from django.db import transaction
from django.views.generic import FormView
from booking.forms import CSVUploadForm
from booking.models import MemberInfo, Inventory, Booking
from services import CSVService


class UploadCSVView(FormView):
    form_class = CSVUploadForm
    template_name = 'admin/upload_csv.html'

    def form_valid(self, form):
        model_type = form.data["model"]
        file = self.request.FILES["file"]
        if model_type == CSVUploadForm.MEMBER_INFO:
            model = MemberInfo
            process_row_callback = self.process_member_info_row
        else:
            model = Inventory
            process_row_callback = self.process_inventory_row
        csv_service = CSVService()

        with transaction.atomic():
            valid_rows = []
            result = csv_service.write_to_database(file, process_row_callback, valid_rows)

            try:
                if result["success"]:
                    model.objects.bulk_create(valid_rows)
                    message = f"{len(valid_rows)} created successfully!"
                    messages.success(self.request, message)
                else:
                    for error in result["errors"]:
                        message = f"Row :: {error['row']}, error :: {error['error']}"
                        messages.error(self.request, message)
                    messages.error(self.request, result["message"])
            except Exception as e:
                message = f"Error while creating the records :: {str(e)}"
                messages.error(self.request, message)
        return self.render_to_response(self.get_context_data(form=UploadCSVView()))

    def process_member_info_row(self, row, valid_rows):
        name, surname, booking_count, date_joined = row["name"], row["surname"], row["booking_count"], row["date_joined"]
        err_msg = ""
        if not name:
            err_msg += "name"
        if not surname:
            err_msg += ", surname"
        if booking_count is None:
            err_msg += ", booking_count"
        if not date_joined:
            err_msg += ", date_joined"

        if err_msg:
            err_msg += " are required."

        if type(booking_count) is not int:
            err_msg += " booking_count should be a number"

        if err_msg:
            raise ValueError(err_msg)
        valid_rows.append(
            MemberInfo(
                name=name, surname=surname, booking_count=booking_count, date_joined=date_joined
            )
        )

    def process_inventory_row(self, row, valid_rows):
        title, description, remaining_count, expiration_date = row["title"], row["description"], \
            row["remaining_count"], row["expiration_date"]

        err_msg = ""
        if not title:
            err_msg += "title"
        if not description:
            err_msg += ", description"
        if remaining_count is None:
            err_msg += ", remaining_count"
        if not expiration_date:
            err_msg += ", expiration_date"
        if err_msg:
            err_msg += " are required."

        try:
            expiration_date = datetime.strptime(expiration_date, "%d/%m/%Y").date()
        except ValueError:
            err_msg += "expiration_date should be in this format i.e., 01/12/2030"

        if err_msg:
            raise ValueError(err_msg)

        valid_rows.append(
            Inventory(
                title=title, description=description, remaining_count=remaining_count,
                expiration_date=expiration_date
            )
        )

