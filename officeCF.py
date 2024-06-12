import requests
import os
from dotenv import load_dotenv
from typesMetier import *

load_dotenv()
CLIENT_ID_CF       = os.environ.get("CLIENT_ID_CF")
CLIENT_SECRET_CF   = os.environ.get("CLIENT_SECRET_CF")
TENANT_ID_CF       = os.environ.get("TENANT_ID_CF")
RESOURCE_URL_CF    = os.environ.get("RESOURCE_URL_CF")
AUTHORITY_URL_CF   = os.environ.get("AUTHORITY_URL_CF")

def getUsersOfficeCF():

################################# Obtenir le jeton d'accès ########################################
    
    token_endpoint = AUTHORITY_URL_CF + '/oauth2/token'
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID_CF,
        'client_secret': CLIENT_SECRET_CF,
        'resource': 'https://graph.microsoft.com/'
    }    
    token_r = requests.post(token_endpoint, data=token_data)
    token = token_r.json().get('access_token')

    url = "https://graph.microsoft.com/v1.0/users"
    headers = {'Authorization': 'Bearer ' + token}

################################# Récupère les utilisateurs d'Office ##############################

    end = False
    dataOffice=[]
    while not end:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            users = response.json()["value"]
            if "@odata.nextLink" in response.json():
                url = response.json()["@odata.nextLink"]
            else:
                end = True
            for user in users:
                newUser = UserOfficeCF(user['surname'],user['givenName'],user['mail'])
                dataOffice.append(newUser)                    
        else:
            print('Erreur lors de la requête :', response.status_code, response.text)           
    return dataOffice

# for user in getUsersOfficeCF():
#     print(user)