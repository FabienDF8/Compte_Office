import requests
import os
from dotenv import load_dotenv
from typesMetier import *


# Charegement des données de connexion
load_dotenv()
CLIENT_ID       = os.environ.get("CLIENT_ID")
CLIENT_SECRET   = os.environ.get("CLIENT_SECRET")
TENANT_ID       = os.environ.get("TENANT_ID")
RESOURCE_URL    = os.environ.get("RESOURCE_URL")
AUTHORITY_URL   = os.environ.get("AUTHORITY_URL")

def getUsersOffice():

################################# Obtenir le jeton d'accès ########################################

    token_endpoint = AUTHORITY_URL + '/oauth2/token'
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'resource': RESOURCE_URL
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
                newUser = UserOffice(user['surname'],user['givenName'],user['mail'])
                dataOffice.append(newUser)                    
        else:
            print('Erreur lors de la requête :', response.status_code, response.text)           
    return dataOffice

# for user in getUsersOffice():
#     print(user)