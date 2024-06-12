class UserOffice:
    nom = ""
    prenom = ""
    email = ""
    def __init__(self, nom,prenom,email):
        if nom:
            self.nom = nom
        if prenom:
            self.prenom = prenom
        if email:
            self.email = email
    def __str__(self):
        return self.nom + ' ' + self.prenom + ' ' + self.email

    
class UserOfficeCF:
    nom = ""
    prenom = ""
    email = ""
    def __init__(self, nom,prenom,email):
        if nom:
            self.nom = nom
        if prenom:
            self.prenom = prenom
        if email:
            self.email = email
    def __str__(self):
        return self.nom + ' ' + self.prenom + ' ' + self.email


class UserGalia:
    nom = ""
    prenom = ""
    emailPro = ""
    emailPerso = ""
    dateFin = ""
    section = ""
    def __init__(self, nom, prenom, emailPro, emailPerso, dateFin, section):
        if nom:
            self.nom = nom.title()
        if prenom:
            self.prenom = prenom.title()
        if emailPro:
            self.emailPro = emailPro.lower()
        if emailPerso:
            self.emailPerso = emailPerso.lower()
        if dateFin:
            self.dateFin = dateFin
        if section:
            self.section = section
    def __str__(self):
        return self.nom + ' ' + self.prenom + ' ' + self.section + ' ' + self.emailPro
    def __eq__(self, other):
        if isinstance(other, UserOffice):
            return self.emailPro == other.email
        return False

class GroupOffice:
    nom= ""
    id= ""
    def __init__(self, nom, id):
        if nom:
            self.nom = nom
        if id:
            self.id = id
    def __str__(self):
        return self.nom + ' ' + self.id
    
class GroupOfficeCF:
    nom= ""
    id= ""
    def __init__(self, nom, id):
        if nom:
            self.nom = nom
        if id:
            self.id = id
    def __str__(self):
        return self.nom + ' ' + self.id
    
class mefGroupDF :
    name= ""
    section= ""
    newname= ""
    def __init__(self, name, section, newname):
        if name:
            self.name = name
        if section:
            self.section = section
        if newname:
            self.newname = newname
    def __str__(self):
        return self.name + ' ' + self.section + ' ' + self.newname
    
class mefGroupCF :
    name= ""
    section= ""
    newname= ""
    def __init__(self, name, section, newname):
        if name:
            self.name = name
        if section:
            self.section = section
        if newname:
            self.newname = newname
    def __str__(self):
        return self.name + ' ' + self.section + ' ' + self.newname