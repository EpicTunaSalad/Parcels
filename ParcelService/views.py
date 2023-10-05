from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from .models import Parcel, ParcelLocker
from .serializers import ParcelSerializer, LockerSerializer
DOES_NOT_EXIST_ERROR = {
    "res": "Object with specified ID does not exist."
}
OBJECT_DELETED = {
    "res": "Object has been deleted."
}
ACTION_NOT_SPECIFIED = {
    "res": "Action was not specified."
}

class ParcelListApiView(APIView):
    def get(self, request, *args, **kwargs):
        parcels = Parcel.objects.all()
        serializer = ParcelSerializer(parcels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            "parcel_id": request.data.get("parcel_id"),
            "sender": request.data.get("sender"),
            "sender_email": request.data.get("sender_email"),
            "sender_phone": request.data.get("sender_phone"),
            "receiver": request.data.get("receiver"),
            "receiver_phone": request.data.get("receiver_phone"),
            "parcel_size": request.data.get("parcel_size")
        }
        serializer = ParcelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LockerListApiView(APIView):
    def get(self, request, *args, **kwargs):
        lockers = ParcelLocker.objects.all()
        serializer = LockerSerializer(lockers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = {
            "locker_id": request.data.get("locker_id"),
            "locker_location_address": request.data.get("locker_location_address"),
            "locker_size": request.data.get("locker_size"),
            "status": request.data.get("status")
        }
        serializer = LockerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ParcelActionsApiView(APIView):
    def get_object(self, parcel_id):
        try:
            return Parcel.objects.get(parcel_id=parcel_id)
        except Parcel.DoesNotExist:
            return None
    
    def get(self, request, parcel_id):
        parcel_instance = self.get_object(parcel_id)
        if not parcel_instance:
            return Response(DOES_NOT_EXIST_ERROR, status=status.HTTP_400_BAD_REQUEST)
        serializer = ParcelSerializer(parcel_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def put(self, request, parcel_id, *args, **kwargs):
        parcel_instance = self.get_object(parcel_id)
        if not parcel_instance:
            return Response(DOES_NOT_EXIST_ERROR, status=status.HTTP_400_BAD_REQUEST)
        data = {
            "sender": request.data.get("sender"),
            "sender_email": request.data.get("sender_email"),
            "receiver": request.data.get("receiver"),
            "receiver_phone": request.data.get("receiver_phone"),
            "parcel_size": request.data.get("parcel_size")
        }
        serializer = ParcelSerializer(instance=parcel_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, parcel_id, *args, **kwargs):
        parcel_instance = self.get_object(parcel_id)
        if not parcel_instance:
            return Response(DOES_NOT_EXIST_ERROR, status=status.HTTP_400_BAD_REQUEST)
        parcel_instance.TakeParcelFromLocker()
        parcel_instance.delete()
        return Response(OBJECT_DELETED, status=status.HTTP_200_OK)

class LockerActionsApiView(APIView):
    def get_object(self, locker_id):
        try:
            return ParcelLocker.objects.get(locker_id=locker_id)
        except ParcelLocker.DoesNotExist:
            return None
    
    def get(self, request, locker_id):
        locker_instance = self.get_object(locker_id)
        if not locker_instance:
            return Response(DOES_NOT_EXIST_ERROR, status=status.HTTP_400_BAD_REQUEST)
        serializer = LockerSerializer(locker_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, locker_id, *args, **kwargs):
        locker_instance = self.get_object(locker_id)
        if not locker_instance:
            return Response(DOES_NOT_EXIST_ERROR, status=status.HTTP_400_BAD_REQUEST)
        data = {
            "locker_location_address": request.data.get("locker_location_address"),
            "locker_size": request.data.get("locker_size"),
            "status": request.data.get("status")
        }
        serializer = LockerSerializer(instance=locker_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, locker_id, *args, **kwargs):
        locker_instance = self.get_object(locker_id)
        if not locker_instance:
            return Response(DOES_NOT_EXIST_ERROR, status=status.HTTP_400_BAD_REQUEST)
        if locker_instance.status == "B":
            try:
                parcel_instance = Parcel.objects.get(locker_id=locker_id)
                parcel_instance.TakeParcelFromLocker()
            except:
                pass
        locker_instance.delete()
        return Response(OBJECT_DELETED, status=status.HTTP_200_OK)

class ParcelLockerActionsApiView(APIView):
    def get_parcel_object(self, parcel_id):
        try:
            return Parcel.objects.get(parcel_id=parcel_id)
        except Parcel.DoesNotExist:
            return None
    
    def get_locker_object(self, locker_id):
        try:
            return ParcelLocker.objects.get(locker_id=locker_id)
        except ParcelLocker.DoesNotExist:
            return None
    
    def put(self, request, parcel_id):
        takeFromLocker = request.data.get("takeFromLocker")
        putToLocker = request.data.get("putToLocker")
        moveToLocker = request.data.get("moveToLocker")
        if takeFromLocker == True:
            parcel_instance = self.get_parcel_object(parcel_id)
            if not parcel_instance:
                return Response(DOES_NOT_EXIST_ERROR, status=status.HTTP_400_BAD_REQUEST)
            success = parcel_instance.TakeParcelFromLocker()
            if success[0]:
                serializer = ParcelSerializer(parcel_instance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"res": success[1]}, status=status.HTTP_400_BAD_REQUEST)
        elif putToLocker:
            parcel_instance = self.get_parcel_object(parcel_id)
            locker_instance = self.get_locker_object(putToLocker)
            if not parcel_instance or not locker_instance:
                return Response(DOES_NOT_EXIST_ERROR, status=status.HTTP_400_BAD_REQUEST)
            success = parcel_instance.PutParcelToLocker(locker_instance)
            if success[0]:
                serializer = ParcelSerializer(parcel_instance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"res": success[1]}, status=status.HTTP_400_BAD_REQUEST)
        elif moveToLocker:
            parcel_instance = self.get_parcel_object(parcel_id)
            if not parcel_instance:
                return Response(DOES_NOT_EXIST_ERROR, status=status.HTTP_400_BAD_REQUEST)
            locker_instance = self.get_locker_object(moveToLocker)
            if not locker_instance:
                return Response(DOES_NOT_EXIST_ERROR, status=status.HTTP_400_BAD_REQUEST)
            success = parcel_instance.MoveParcelBetweenLockers(locker_instance)
            if success[0]:
                serializer = ParcelSerializer(parcel_instance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"res": success[1]}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(ACTION_NOT_SPECIFIED, status=status.HTTP_400_BAD_REQUEST)
