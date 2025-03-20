from rest_framework.response import Response

from booking.apis.serializers import BookingSerializer, CancelBookingSerializer
from booking.models import Booking
from rest_framework import generics, status


class BookingAPIView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class CancelBooking(generics.GenericAPIView):
    queryset = Booking.objects.all()
    serializer_class = CancelBookingSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Booking has been cancelled."}, status=status.HTTP_200_OK)
