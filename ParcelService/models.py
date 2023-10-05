from django.db import models

PARCEL_SIZES = [
    ("XS", "Extra Small"),
    ("S", "Small"),
    ("M", "Medium"),
    ("L", "Large"),
    ("XL", "Extra Large")
]

LOCKER_STATUSES = [
    ("F", "Free"),
    ("B", "Busy"),
    ("OOO", "Out Of Order")
]

class ParcelLocker(models.Model):
    locker_id = models.CharField(max_length=50, primary_key=True)
    locker_location_address = models.CharField(max_length=50)
    locker_size = models.CharField(max_length=2, choices=PARCEL_SIZES)
    status = models.CharField(max_length=3, choices=LOCKER_STATUSES)

class Parcel(models.Model):
    parcel_id = models.CharField(max_length=50, primary_key=True)
    sender = models.CharField(max_length=50)
    sender_email = models.CharField(max_length=50)
    sender_phone = models.CharField(max_length=50)
    receiver = models.CharField(max_length=50)
    receiver_phone = models.CharField(max_length=50)
    parcel_size = models.CharField(max_length=2, choices=PARCEL_SIZES)
    lockerID = models.ForeignKey(ParcelLocker, on_delete=models.SET_NULL, null=True)

    def PutParcelToLocker(self, locker):
        if locker.status == "F":
            parcel_sizes_indexes = [x[0] for x in PARCEL_SIZES]
            if parcel_sizes_indexes.index(locker.locker_size) < parcel_sizes_indexes.index(self.parcel_size):
                return (False, "Locker is too small for the parcel.")
            self.lockerID = locker
            locker.status = "B"
            locker.save()
            self.save()
            return (True, "Success")
        return (False, "Locker is busy or out of order.")

    def MoveParcelBetweenLockers(self, new_locker):
        if self.lockerID and new_locker.status == "F":
            parcel_sizes_indexes = [x[0] for x in PARCEL_SIZES]
            if parcel_sizes_indexes.index(new_locker.locker_size) < parcel_sizes_indexes.index(self.parcel_size):
                return (False, "New locker is too small for the parcel.")
            self.lockerID.status = "F"
            self.lockerID.save()
            new_locker.status = "B"
            new_locker.save()
            self.lockerID = new_locker
            self.save()
            return (True, "Success")
        elif not self.lockerID:
            return (False, "Parcel is not in locker.")
        elif new_locker.status != "F":
            return (False, "New locker is busy.")

    def TakeParcelFromLocker(self):
        if self.lockerID:
            self.lockerID.status = "F"
            self.lockerID.save()
            self.lockerID = None
            self.save()
            return (True, "Success")
        return (False, "Parcel is not in locker.")
