from rest_framework import serializers

from booking.models import Booking, MemberInfo


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ("id", "item", "member", "booking_time")

    def validate_member(self, value):
        member = value
        MAX_BOOKINGS_ALLOWED = 2
        member_booking_count = Booking.objects.filter(member_id=member.id).count()
        if member_booking_count >= MAX_BOOKINGS_ALLOWED - 1:
            raise serializers.ValidationError(f"Maximum bookings allowed are {MAX_BOOKINGS_ALLOWED - 1}.")
        return value

    def validate_item(self, value):
        item = value
        if item.remaining_count <= 0:
            raise serializers.ValidationError(f"Inventory is not available for the selected item.")
        return value


class CancelBookingSerializer(serializers.Serializer):
    member = serializers.PrimaryKeyRelatedField(
        queryset=MemberInfo.objects.all()
    )
    booking = serializers.PrimaryKeyRelatedField(
        queryset=Booking.objects.all()
    )

    def validate(self, attrs):
        booking = attrs["booking"]
        member = attrs["member"]

        if booking.member_id != member.id:
            raise serializers.ValidationError("This Booking does not belong to the given member id.")

        if booking.status == Booking.STATUS_CANCELLED:
            raise serializers.ValidationError("This Booking has already been cancelled.")
        return attrs

    def save(self, **kwargs):
        booking = self.validated_data["booking"]
        booking.status = Booking.STATUS_CANCELLED
        booking.save()

