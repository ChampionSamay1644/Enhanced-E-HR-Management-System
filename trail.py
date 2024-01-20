import firebase_admin
from firebase_admin import db,credentials

cred=credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred,{'databaseURL':'https://console.firebase.google.com/project/hr-management-system-f7c9f/database/hr-management-system-f7c9f-default-rtdb/data/~2F'})

ref = db.reference('/name')
print(ref.get())