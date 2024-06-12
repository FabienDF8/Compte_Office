import requests
import os
from dotenv import load_dotenv
from typesMetier import *


# Charegement des données de connexion
load_dotenv()
CLIENT_ID_CF       = os.environ.get("CLIENT_ID_CF")
CLIENT_SECRET_CF   = os.environ.get("CLIENT_SECRET_CF")
TENANT_ID_CF       = os.environ.get("TENANT_ID_CF")
RESOURCE_URL_CF    = os.environ.get("RESOURCE_URL_CF")
AUTHORITY_URL_CF   = os.environ.get("AUTHORITY_URL_CF")

def getGroupOfficeCF():
    # Obtenir le jeton d'accès
    token_endpoint = AUTHORITY_URL_CF + '/oauth2/token'
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID_CF,
        'client_secret': CLIENT_SECRET_CF,
        'resource': RESOURCE_URL_CF
    }
    token_r = requests.post(token_endpoint, data=token_data)
    token = token_r.json().get('access_token')


    url = f"https://graph.microsoft.com/v1.0/groups"
    headers = {'Authorization': 'Bearer ' + token}

############################# Lance la recherche de groupe ######################################
    end = False
    dataOffice=[]
    while not end:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            groups = response.json()["value"]
            if "@odata.nextLink" in response.json():
                url = response.json()["@odata.nextLink"]
            else:
                end = True
############################# Prends les noms et les id des groupes #############################            
            for group in groups: 
                newGroup = GroupOfficeCF(group['displayName'], group['id']) 
                # print(newGroup)
                dataOffice.append(newGroup)                    
        else:
            print('Erreur lors de la requête :', response.status_code, response.text)     
    return dataOffice

# Besoin de print

# for group in getGroupOfficeCF():
#     print(group)
