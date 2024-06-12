from typesMetier import *
from officeDF import *

def nomFormateur(email):

################################# Crée les noms pour les groupes #################################

    Userinoffice = [user for user in userOffice if user.email == email]
    form = Userinoffice[0].prenom
    ateur = Userinoffice[0].nom
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

################################# Met en forme les noms de groupes ################################

def csvTeams():
    groupes = []
    for line in df[1:] :
        groupe = line.split(";")
        Owner = groupe[0] 
        Section = groupe[1]
        OwnerTeams = mefGroupDF(Owner, Section, nomFormateur(Owner))
        groupes.append(OwnerTeams) # nomFormateur(Owner)+" "+Section)
    return groupes

######################################### Ouvre le CSV ############################################

fileSection = "Equipes Teams DF 2023.csv"
userOffice = getUsersOffice()
fichier = open(fileSection,"r")
df = fichier.readlines()
fichier.close
groupesOffice= csvTeams()



# for groups in groupesOffice:
#     print(groups.newname + " "+ groups.section)