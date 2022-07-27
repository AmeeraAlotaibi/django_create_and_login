from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Booking, Flight
from rest_framework_simplejwt.tokens import RefreshToken


# User Model

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ["destination", "time", "price", "id"]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["flight", "date", "id"]


class BookingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["flight", "date", "passengers", "id"]


class UpdateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["date", "passengers"]

# register
class UserRegistrationSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ["username", "password", "first_name", "last_name"]
    
    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return validated_data


# log in 
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(allow_blank=True, read_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        try: 
            user = User.objects.get(username= username)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exit.")
        
        if not user.check_password(password):
            raise serializers.ValidationError("username or password combo isn't correct")
        
        payload = RefreshToken.for_user(user)
        token = str(payload.access_token)
        data["access"] = token

        return data