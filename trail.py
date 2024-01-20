import firebase_admin
from firebase_admin import db,credentials

cred=credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred,{'databaseURL':'https://hr-management-system-f7c9f-default-rtdb.asia-southeast1.firebasedatabase.app/'})

ref = db.reference('/')
ref.update({'name':'Samay'})
