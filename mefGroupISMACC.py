from typesMetier import *
from officeCF import *

def nomFormateur(email):

    UserinofficeCF = [user for user in userOffice if user.email == email]
    form = UserinofficeCF[0].prenom
    ateur = UserinofficeCF[0].nom
    if "-" in form :
        new = form.split("-")
        pre = new[0]
        nom = new[1]
        newform = (pre[0]+nom[0]+"."+ateur)
        # users.append(newform)
    else:
        newform = (form[0]+"."+ateur)
        # users.append(NewForm)
    return newform

# Lecture du CSV
def csvTeamsISMACC():
    groupes = []
    for line in df[1:] :
        groupe = line.split(";")
        Owner = groupe[0] 
        Section = groupe[1]
        OwnerTeams = mefGroupCF(Owner, Section, nomFormateur(Owner))
        groupes.append(OwnerTeams) # nomFormateur(Owner)+" "+Section)
    return groupes

fileSection = "Equipes Teams DF+5 2023.csv"

userOffice = getUsersOfficeCF()

fichier = open(fileSection,"r")
df = fichier.readlines()
fichier.close

groupesOffice= csvTeamsISMACC()

# for groups in groupesOffice:
#     print(groups.newname + " " + groups.section)
