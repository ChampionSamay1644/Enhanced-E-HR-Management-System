import firebase_admin
from firebase_admin import db,credentials

cred=credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred,{'databaseURL':'https://hr-mgntsystem-test.asia-southeast1.firebasedatabase.app/'})

admins = db.reference('Trial')
to_search='Samay'
password1 = admins.child(to_search).child('password').get()
print(password1)
