# Prerequisites:
## django (pip install django)
## django_rest_framework (pip install django_rest_framework)

# /api/parcel
## GET: returns list of all parcels
## POST: creates a parcel
### parcel_id - String
### sender - String
### sender_email - String
### sender_phone - String
### receiver - String
### receiver_phone - String
### parcel_size - String - allowed values are XS, S, M, L, XL

# /api/parcel/{ID}
## GET: returns parcel with the specified ID
## POST: updates parcel with the specified ID
### sender - String
### sender_email - String
### sender_phone - String
### receiver - String
### receiver_phone - String
## DELETE: deletes parcel with the specified ID

# /api/locker
## GET: returns list of all parcel lockers
### POST: creates a parcel locker
### locker_id - String
### locker_location_address - String
### locker_size - String - allowed values are XS, S, M, L, XL
### status - String - allowed values are F, B, OOO

# /api/locker/{ID}
## GET: returns parcel locker with the specified ID
## POST: updates parcel locker with the specified ID
### locker_location_address - String
### locker_size - String - allowed values are XS, S, M, L, XL
### status - String - allowed values are F, B, OOO
## DELETE: deletes parcel locker with the specified ID

# /api/parcel/{ID}/actions
## POST: executes provided action
## Possible actions:
### takeFromLocker - boolean
### putToLocker - string - Locker ID
### moveToLocker - string - Locker ID
