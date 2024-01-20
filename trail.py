import firebase_admin
from firebase_admin import db,credentials

cred=credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred,{'databaseURL':'https://hr-management-system-f7c9f-default-rtdb.asia-southeast1.firebasedatabase.app/'})

admins = db.reference('admins')
to_search='Samay'
password1 = admins.child(to_search).child('password').get()
print(password1)
