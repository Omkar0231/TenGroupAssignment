from django.db import models


class MemberInfo(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    booking_count = models.IntegerField()
    date_joined = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Inventory(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    remaining_count = models.IntegerField()
    expiration_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Booking(models.Model):
    STATUS_ACTIVE, STATUS_CANCELLED = "active", "cancelled"
    STATUS_CHOICES = (
        (STATUS_ACTIVE, "Active"),
        (STATUS_CANCELLED, "Cancelled"),
    )

    member = models.ForeignKey(MemberInfo, on_delete=models.CASCADE)
    item = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    booking_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)

