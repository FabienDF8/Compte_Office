import requests
import os
from dotenv import load_dotenv
import datetime
from typesMetier import *

# Donne les idendifiants et le lien pour l'API Galia (besoin du fichier .env)
load_dotenv()
SCFORM_LOGIN    = os.environ.get("SCFORM_LOGIN")
SCFORM_PASSWORD = os.environ.get("SCFORM_PASSWORD")
SCFORM_URL      = os.environ.get("SCFORM_URL")

def getUsersGalia():
    
################################# Donne la requète à l'API ########################################
    url = SCFORM_URL+'/Entite/GetEntite?ACTION=INSCRIT&IDSociete=2'

    response = requests.get(url, auth=(SCFORM_LOGIN, SCFORM_PASSWORD))
    users = response.json()
    usersOk = []

################################## On applique les filtres ########################################
    
    if response.status_code == 200:
        for user in users:
            # Cherche les Stagiaires de Galia
            stagiaire = user["Stagiaire"]
            # Cherche le nom, prénom, Email pro, Email perso, la Date de Sortie et sa Classe
            newUser = UserGalia(stagiaire['Nom'], stagiaire['Prenom'], stagiaire["Email_Pro"], stagiaire["Email_Perso"], user["Date_Sortie"], user["Libelle_Parcours"])
            date = user["Date_Sortie"]
            datet= datetime.date.today().strftime('%Y-%m-%d"T"%H:%M:%S')
            # Regarde si la date de sortie est supérieur à la date du jour, si oui le stagiaire est bon.
            if date > datet:
               usersOk.append(newUser) 
                      
    else:
        # Renvoie une erreur si l'API ne repond pas 
        print('Erreur lors de la requête :', response.status_code, response.text)
    return usersOk



# for user in getUsersGalia():
#     print(user)