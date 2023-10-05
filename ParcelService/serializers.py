from rest_framework import serializers
from .models import Parcel, ParcelLocker

class ParcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = ["parcel_id", "sender", "sender_email", "receiver", "receiver_phone", "parcel_size", "lockerID"]

class LockerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParcelLocker
        fields = ["locker_id", "locker_location_address", "locker_size", "status"]
