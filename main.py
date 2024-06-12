from officeDF import *
from galia import *
from typesMetier import *
from officeCF import *
from GroupDF import *
from GroupCF import *
import requests
import os
from dotenv import load_dotenv
import json
import pandas as pd
from mefUser import *
from CréaGroupDF import *
import time

# Création des groupes 
print("Création des groupes")

CréationGroupOfficeDF= CreationGroupOfficeDF()

# On récupère les utilisateurs dans Office
print("Récupération des utilisateurs de Galia et d'Office")

usersOffice = getUsersOffice()
usersOfficeCF = getUsersOfficeCF()

# Ceux de Galia

usersGalia =  getUsersGalia()

# Récupère les groupes 
print("Récupération des groupes Office")
groupOfficeDF = getGroupOfficeDF()

groupOfficeCF = getGroupOfficeCF()


# Met en forme les prénoms et noms de utilisateurs 

# prenomMef = mise_en_forme_prenom(prenom)

# nomMef = mise_en_forme_nom(nom)

# Recherche des alternants non présents dans Office

# La fonction récupère les emailPro qui se trouve dans les utilisateurs de Galia et ensuite vient la comparer aux utilisateurs d'Office de DF et CF
usersNotInOffice = [user for user in usersGalia if user.emailPro not in [other_user.email for other_user in usersOffice] and user.emailPro not in [other_user.email for other_user in usersOfficeCF]]

####### On appelle les données qui nous sont utilses (Password, Identifiant, ...)############

load_dotenv()
CLIENT_ID       = os.environ.get("CLIENT_ID")
CLIENT_SECRET   = os.environ.get("CLIENT_SECRET")
TENANT_ID       = os.environ.get("TENANT_ID")
RESOURCE_URL    = os.environ.get("RESOURCE_URL")
AUTHORITY_URL   = os.environ.get("AUTHORITY_URL")
CLIENT_ID_CF       = os.environ.get("CLIENT_ID_CF")
CLIENT_SECRET_CF   = os.environ.get("CLIENT_SECRET_CF")
TENANT_ID_CF       = os.environ.get("TENANT_ID_CF")
RESOURCE_URL_CF    = os.environ.get("RESOURCE_URL_CF")
AUTHORITY_URL_CF   = os.environ.get("AUTHORITY_URL_CF")
#############################################################################################

################################# Pour DF +2 +3 #############################################

########################### Demande d'un jeton pour Office ##################################
for user in usersNotInOffice:
    if '@dijonformation.com' in user.emailPro :
        print("C'est un compte Dijon Formation :")
        token_endpoint = AUTHORITY_URL + '/oauth2/token'
        token_data = {
            'grant_type': 'client_credentials',
            
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'resource': RESOURCE_URL
        }
        token_r = requests.post(token_endpoint, data=token_data)
        token = token_r.json().get('access_token')

        #############################################################################################

        ################################ Changement de la section ###################################

        # Ce sont tous les utilisateurs qui ne sont pas dans Galia
        fileSection = "Correspondances sections Galia Office.csv"

        # Cherche dans un csv toutes les colonnes séparés par des " ; "
        df = pd.read_csv(fileSection, sep=';')

        # Les sections sont placés dans une variables afin de pouvoir récupérer les données placées sur la même ligne d'une colonne spécifique
        nom = user.section
        
        # Les noms des colonnes
        colonneGalia = 'Galia'
        colonneDepartement ='Département Office 365'
        colonneOffice = 'Groupe Office 365'
        colonneSharepoint = 'SharePoint Alternant'
        
        ### Cherche les colonnes demandé ci-dessus et retient le resultat dans un variables ###
        
        #Celle-ci transforme pour le département
        departement = df.loc[df[colonneGalia] == nom, colonneDepartement].values
        
        #Celle-ci transforme pour la recherche de groupe
        gOffice = df.loc[df[colonneGalia] == nom, colonneOffice].values


    ########################## Mise en forme des prénoms et noms #################################

        prenom = mise_en_forme_prenom()
        nom = mise_en_forme_nom()
        print("Mise en forme du prénom et du nom pour le nickname : ",prenom, nom)

    #############################################################################################

    ###################### Paramètres pour la création du compte ################################

        print("Création du compte en cours de "+ user.nom + " " + user.prenom)
        # Rentre les paramètres pour la création
        userOffice = {
            "accountEnabled": True,
            "displayName": user.prenom + " " + user.nom, # Demande le prénom et le nom
            "givenName": user.prenom, # Que le prénom
            "userPrincipalName": user.emailPro, #  Demande l'email pro
            "JobTitle": "Alternant(e)", # Demande le poste
            "department": departement[0], # Demande le département 
            "passwordPolicies": "DisablePasswordExpiration", # Demande si on veux mettre des options et dans ce cas on désactive l'expiration de mot de passe
            "passwordProfile": {
                "password": "Azerty123!", # On rentre le mot de passe
                "forceChangePasswordNextSignIn": True, # On demande de changer le mot de passe lors de la première connexion
            },
            "surname": user.nom, # On demande le nom 
            "mailNickname": prenom+"."+nom # C'est le début de l'adresse mail 
        }
    ############################################################################################

    ##################################### Création du compte ###################################

        create_user_url = "https://graph.microsoft.com/v1.0/users"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.post(create_user_url, json=userOffice, headers=headers)
        user_data = response.json()
        user_id = user_data.get('id')
        

        if response.status_code == 201:
            print("Compte créé avec succès.")
        else:
            print(f"Échec de la création du compte. Code de réponse : {response.status_code, response.text}")
    #############################################################################################

    ############################ Ajout au groupe gsAlternant ####################################
        print("Ajout de l'alternant dans le groupe gsAltenant")

        group_id = '6b7487e8-c740-4b1a-8563-5b8eabbe6888'
        add_to_group_endpoint = f'https://graph.microsoft.com/v1.0/groups/{group_id}/members/$ref'
        add_to_group_data = {
            '@odata.id': f'https://graph.microsoft.com/v1.0/users/{user_id}'
        }

        add_to_group_response = requests.post(add_to_group_endpoint, headers=headers, data=json.dumps(add_to_group_data))

        if add_to_group_response.status_code == 204:
            print('Utilisateur ajouté au groupe avec succès!')
        else:
            print(f'Erreur {add_to_group_response.status_code}: {add_to_group_response.text}')


############################### Ajout aux groupes de sa section ###############################
        print("Ajout de l'alternant dans ses groupes de classe")

        # Ajouter l'utilisateur à chaque groupe dont le nom contient un certain mot
        search_word = gOffice[0] # récupère les sections dans le CSV "Correspondances Galia"
        for group in groupOfficeDF: # dans tous les groupes présents dans l'office de dijon
            if search_word in group.nom: # on recherche les noms de groupes qui correspondent à la section de l'étudiant
                add_user_to_group_url = f'https://graph.microsoft.com/v1.0/groups/{group.id}/members/$ref'
                headers = {
                    'Authorization': 'Bearer ' + token,
                    'Content-Type': 'application/json'
                }
                data = {
                    '@odata.id': f"https://graph.microsoft.com/v1.0/users/{user_id}"
                }
                response = requests.post(add_user_to_group_url, headers=headers, data=json.dumps(data))

                if response.status_code == 204:
                    print(f'Utilisateur ajouté au groupe {group.nom}')
                else:
                    print(f"Erreur lors de l'ajout de l'utilisateur au groupe {group.nom}. Code d'état : {response.status_code}: {response.text}")


################################################ Pour DF +5 ##########################################

    else:
        print("C'est un compte ISMACC :")
        token_endpoint = AUTHORITY_URL_CF + '/oauth2/token'
        token_data = {
            'grant_type': 'client_credentials',
            
            'client_id': CLIENT_ID_CF,
            'client_secret': CLIENT_SECRET_CF,
            'resource': RESOURCE_URL_CF
        }
        token_r = requests.post(token_endpoint, data=token_data)
        token = token_r.json().get('access_token')

        #############################################################################################

        ################################ Changement de la section ###################################

        # Ce sont tous les utilisateurs qui ne sont pas dans Galia
        fileSection = "Correspondances sections Galia Office.csv"

        # Cherche dans un csv toutes les colonnes séparés par des " ; "
        df = pd.read_csv(fileSection, sep=';')

        # Les sections sont placés dans une variables afin de pouvoir récupérer les données placées sur la même ligne d'une colonne spécifique
        nom = user.section
        
        # Les noms des colonnes
        colonneGalia = 'Galia'
        colonneDepartement ='Département Office 365'
        colonneOffice = 'Groupe Office 365'
        colonneSharepoint = 'SharePoint Alternant'
        
        ### Cherche les colonnes demandé ci-dessus et retient le resultat dans un variables ###
        
        #Celle-ci transforme pour le département
        departement = df.loc[df[colonneGalia] == nom, colonneDepartement].values
        
        #Celle-ci transforme pour la recherche de groupe
        gOffice = df.loc[df[colonneGalia] == nom, colonneOffice].values


    ########################## Mise en forme des prénoms et noms #################################

        prenom = mise_en_forme_prenom()
        nom = mise_en_forme_nom()
        print("Mise en forme du prénom et du nom pour le nickname : ",prenom, nom)

    #############################################################################################

    ###################### Paramètres pour la création du compte ################################

        print("Création du compte en cours de "+ user.nom + " " + user.prenom)
        # Rentre les paramètres pour la création
        userOfficeCF = {
            "accountEnabled": True,
            "displayName": user.prenom + " " + user.nom, # Demande le prénom et le nom
            "givenName": user.prenom, # Que le prénom
            "userPrincipalName": user.emailPro, #  Demande l'email pro
            "JobTitle": "Alternant(e)", # Demande le poste
            "department": departement[0], # Demande le département 
            "passwordPolicies": "DisablePasswordExpiration", # Demande si on veux mettre des options et dans ce cas on désactive l'expiration de mot de passe
            "passwordProfile": {
                "password": "Azerty123!", # On rentre le mot de passe
                "forceChangePasswordNextSignIn": True, # On demande de changer le mot de passe lors de la première connexion
            },
            "surname": user.nom, # On demande le nom 
            "mailNickname": prenom+"."+nom # C'est le début de l'adresse mail 
        }
    ############################################################################################

    ##################################### Création du compte ###################################

        create_user_url = "https://graph.microsoft.com/v1.0/users"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.post(create_user_url, json=userOfficeCF, headers=headers)
        user_data = response.json()
        user_id = user_data.get('id')
        

        if response.status_code == 201:
            print("Compte créé avec succès.")
        else:
            print(f"Échec de la création du compte. Code de réponse : {response.status_code, response.text}")
    #############################################################################################

    ############################ Ajout au groupe gsAlternant ####################################
        print("Ajout de l'alternant dans le groupe gsAltenant")

        group_id = 'd82517f7-4ead-4bec-ba7f-a863891bbceb'
        add_to_group_endpoint = f'https://graph.microsoft.com/v1.0/groups/{group_id}/members/$ref'
        add_to_group_data = {
            '@odata.id': f'https://graph.microsoft.com/v1.0/users/{user_id}'
        }

        add_to_group_response = requests.post(add_to_group_endpoint, headers=headers, data=json.dumps(add_to_group_data))

        if add_to_group_response.status_code == 204:
            print('Utilisateur ajouté au groupe avec succès!')
        else:
            print(f'Erreur {add_to_group_response.status_code}: {add_to_group_response.text}')


############################### Ajout aux groupes de sa section ###############################
        print("Ajout de l'alternant dans ses groupes de classe")

        # Ajouter l'utilisateur à chaque groupe dont le nom contient un certain mot
        search_word = gOffice[0] # récupère les sections dans le CSV "Correspondances Galia"
        for group in groupOfficeCF: # dans tous les groupes présents dans l'office de dijon
            if search_word in group.nom: # on recherche les noms de groupes qui correspondent à la section de l'étudiant
                add_user_to_group_url = f'https://graph.microsoft.com/v1.0/groups/{group.id}/members/$ref'
                headers = {
                    'Authorization': 'Bearer ' + token,
                    'Content-Type': 'application/json'
                }
                data = {
                    '@odata.id': f'https://graph.microsoft.com/v1.0/users/{user_id}'
                }
                response = requests.post(add_user_to_group_url, headers=headers, data=json.dumps(data))

                if response.status_code == 204:
                    print(f'Utilisateur ajouté au groupe {group.nom}')
                else:
                    print(f"Erreur lors de l'ajout de l'utilisateur au groupe {group.nom}. Code d'état : {response.status_code}: {response.text}")