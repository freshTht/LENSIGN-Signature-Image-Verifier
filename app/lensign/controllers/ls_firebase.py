import pyrebase

# init
config = {
  "apiKey": "AIzaSyDQQnuPM2VpAiTWttzIC75HjLBMb_u55M0",
  "authDomain": "lensign-wanda.firebaseapp.com",
  "databaseURL": 'https://lensign-wanda.firebaseio.com',
  "storageBucket": "lensign-wanda.appspot.com"
}

firebase = pyrebase.initialize_app(config)

class LSFirebase:
    def list_all(self):
        ref = storage.child("images/example.jpg")

        return results
    
#
# create an object for each Controller class (similar to export in JS)
#
ls_firebase = LSFirebase()