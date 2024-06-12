import requests
import os
import json
from dotenv import load_dotenv
from typesMetier import *
import time
from GroupCF import *
from mefGroupISMACC import *



# Charegement des données de connexion
load_dotenv()
CLIENT_ID_CF       = os.environ.get("CLIENT_ID_CF")
CLIENT_SECRET_CF   = os.environ.get("CLIENT_SECRET_CF")
TENANT_ID_CF       = os.environ.get("TENANT_ID_CF")
RESOURCE_URL_CF    = os.environ.get("RESOURCE_URL_CF")
AUTHORITY_URL_CF   = os.environ.get("AUTHORITY_URL_CF")


CSVTeams = csvTeamsISMACC()
groupOff = getGroupOfficeCF()

##################### Cherche les groupes qui ne sont pas dans Office via le CSV ##################

groupNotinOffice = [group for group in CSVTeams if (group.newname + " " + group.section) not in [other_group.nom for other_group in groupOff]]
for group in groupNotinOffice:
    print('Creation du groupe : ' + group.newname + " "+ group.section)

############################ Enlève les espaces des groupes #######################################

    teams = group.newname + " " + group.section
    nickname = group.newname + " " + group.section
    if " " in nickname:
        nickname = nickname.replace(" ", "")

############################# Obtenir le jeton d'accès ############################################

    token_endpoint = AUTHORITY_URL_CF + '/oauth2/token'
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID_CF,
        'client_secret': CLIENT_SECRET_CF,
        'resource': RESOURCE_URL_CF
    }
    token_r = requests.post(token_endpoint, data=token_data)
    token = token_r.json().get('access_token')

    headers = {'Authorization': 'Bearer ' + token}
    create_group_url = 'https://graph.microsoft.com/v1.0/groups'
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

################################# Paramètres pour le groupe #######################################

    group_data = {
        'displayName': teams,
        'mailNickname': nickname,
        'mailEnabled': True,
        'securityEnabled': False,
        'groupTypes': ['Unified'],
    }

################################# Création du groupe ##############################################

    response = requests.post(create_group_url, headers=headers, data=json.dumps(group_data))    
    if response.status_code == 201:
        group_id = response.json().get('id')
        print('Groupe créé avec succès.')
        print('ID du groupe:', group_id)
        time.sleep(20)
        
################################# Ajouter des propriétaires au groupe #############################
        
        owner_email = [group.name, 'c-seignez@chalonformation.com']
        owners_url = f'https://graph.microsoft.com/v1.0/groups/{group_id}/owners/$ref'
        for owner_emails in owner_email:
            owners_data = {
                '@odata.id': f'https://graph.microsoft.com/v1.0/users/{owner_emails}'  
            }
            owners_response = requests.post(owners_url, headers=headers, data=json.dumps(owners_data))

            if owners_response.status_code == 204:
                print ('Propriétaire' +" "+ owner_emails+ " " +'ajouté(e) avec succès.')
            else:
                print("Erreur lors de l'ajout du propriétaire. Code de statut:", owners_response.status_code)
                print('Réponse:', owners_response.text)
        time.sleep(20)

################################# Activer Teams pour le groupe ####################################

        teams_enable_url = f'https://graph.microsoft.com/v1.0/groups/{group_id}/team'
        teams_response = requests.put(teams_enable_url, headers=headers, data=json.dumps({}))

        if teams_response.status_code == 201:
            print('Teams activé avec succès pour le groupe.')
        else:
            print("Erreur lors de l'activation de Teams. Code de statut:", teams_response.status_code)
            print('Réponse:', teams_response.text)
    else:
        print('Erreur lors de la création du groupe. Code de statut:', response.status_code)
        print('Réponse:', response.text)
