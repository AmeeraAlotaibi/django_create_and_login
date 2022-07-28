import datetime
from rest_framework import generics
from flights import serializers
import flights
from flights.models import Booking, Flight
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


class FlightsList(generics.ListAPIView):
    queryset = Flight.objects.all()
    serializer_class = serializers.FlightSerializer


class BookingsList(generics.ListAPIView):
    serializer_class = serializers.BookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(date__gte=datetime.date.today())


class BookingDetails(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = serializers.BookingDetailsSerializer
    lookup_url_kwarg = "booking_id"


class UpdateBooking(generics.RetrieveUpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = serializers.UpdateBookingSerializer
    lookup_url_kwarg = "booking_id"


class CancelBooking(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    lookup_url_kwarg = "booking_id"


class UserRegisterationView(generics.CreateAPIView):
    serializer_class= serializers.UserRegistrationSerializer


# log in view
class UserLoginView(APIView):
    serializer_class = serializers.UserLoginSerializer
    
    def post(self, request):
        data = request.data
        serializer = serializers.UserLoginSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            valid_data = serializer.data
            return Response(valid_data, status=HTTP_200_OK)
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)


class CreateBookingView(generics.CreateAPIView):
    serializer_class = serializers.UpdateBookingSerializer
    lookup_field = 'id'
    lookup_url_kwarg = "flight_id"
    
    def perform_create(self, serializer):
        flight = self.kwargs["flight_id"]
        serializer.save(user=self.request.user, flight_id = flight)
        
        