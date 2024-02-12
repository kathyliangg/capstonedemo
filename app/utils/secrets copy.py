import os

def getSecrets():
    secrets = {
        'MONGO_HOST':"mongodb+srv://lattekat:343305@lattekat.azra2tt.mongodb.net/kathypractice?retryWrites=true&w=majority",
        'MONGO_DB_NAME':"kathypractice",
        'GOOGLE_CLIENT_ID': "",
        'GOOGLE_CLIENT_SECRET':"",
        'GOOGLE_DISCOVERY_URL':"https://accounts.google.com/.well-known/openid-configuration",
        'MY_EMAIL_ADDRESS':""
        }
    return secrets