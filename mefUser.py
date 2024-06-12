# import pandas as pd
from galia import *
# import os
# import requests
# from dotenv import load_dotenv
from typesMetier import *
from officeCF import *
from officeDF import *

################################# Récupération des Users ##########################################

usersOffice = getUsersOffice()
usersOfficeCF = getUsersOfficeCF()
usersGalia =  getUsersGalia()

#################### Verif des Users qui sont dans Galia et pas dans Office ########################

usersNotInOffice = [user for user in usersGalia if user.emailPro not in [other_user.email for other_user in usersOffice] and user.emailPro not in [other_user.email for other_user in usersOfficeCF]]

############################# Permet de remplacer les "-", "'" et les " " #########################

for user in usersNotInOffice:
    def mise_en_forme_prenom():
        # Recherche si le prénom contient " " ou "'" ou "-"
        prenom = user.prenom
        if ' ' in prenom :
            prenom = prenom.replace(" Marie", "marie").replace(" ", "")
        if '-' in prenom :
            prenom = prenom.replace("-Marie", "marie").replace("-", "")
        if "'" in prenom:    
            prenom = prenom.replace("'Marie", "marie").replace("'", "") 
        # Passe tout en minuscule
        return prenom.lower()


    def mise_en_forme_nom():
        # Recherche si le prénom contient " " ou "'" ou "-"
        nom = user.nom
        if ' ' in nom :
            nom = nom.replace(" Marie", "marie").replace(" ", "")
        if '-' in nom :
            nom = nom.replace("-Marie", "marie").replace("-", "")
        if "'" in nom:    
            nom = nom.replace("'Marie", "marie").replace("'", "") 
        # Passe tout en minuscule
        return nom.lower()
    # nom = mise_en_forme_nom()
    # print(nom)