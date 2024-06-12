import requests
import os
from dotenv import load_dotenv
from typesMetier import *


################################# Charegement des données de connexion ############################
load_dotenv()
CLIENT_ID       = os.environ.get("CLIENT_ID")
CLIENT_SECRET   = os.environ.get("CLIENT_SECRET")
TENANT_ID       = os.environ.get("TENANT_ID")
RESOURCE_URL    = os.environ.get("RESOURCE_URL")
AUTHORITY_URL   = os.environ.get("AUTHORITY_URL")



def getGroupOfficeDF():
    
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
                newGroup = GroupOffice(group['displayName'], group['id'])
                # print(newGroup)
                dataOffice.append(newGroup)                    
        else:
            print('Erreur lors de la requête :', response.status_code, response.text)     
    return dataOffice

# Besoin de print

# for group in getGroupOfficeDF():
#     print(group)
