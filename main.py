from patient_medecin import patient_onto,medecin_onto
from requetes import requests
def menu0():
    print("------------------------------------------Bienvenu dans notre appllication de prise de consultation a distance------------------------------------------")
    print("|\n|---------------------------------------------Que voullez vous faire?----------------------------------------------------------------|\n|")
    print("|\t1-je suis un patient et je desire saisir mes information afin de faire une consultation\t\t\t\t\t\t\t|") 
    print("|\t2-je suis medecin et je desire effectue une ou plusieures consulation\t\t\t\t\t\t\t\t|") 
    print("|\t3-Requetes sparql\t\t\t\t\t\t\t\t\t|")
    choi = input('saisissez votre choix:\n')
    return choi
def menu_requetes():#TODO: dans la 2eme partie penser a precicez la maniere de saisir une date,ect
   
    print("------------------------------------------------------------------Requetes------------------------------------------------------------------")
    print("faite votre choix:\nandeelkhaeraefz",
        "1-trouver patient  et leurs maladies (chroniques) en fonction de l'id\n",
        "2-liste des patient atteint d'une maladie dans une certaine localité(commune,wilaya)\n",
        "3-nombre de patient atteint d'une maladie dans une localite(commune,wilaya)\n",
        "4-nombre de patient de moins d'un age ayant une certaine maladie",
        "5-nombre de patient de moins d'un certain age ayant le covid\n ",
        "6-nombre de patient de moins d'un certain age ayant le covid a une date donne\n",
        "7-liste patient ayant une maladie dans une certaine wilaya\n",
        "8-nombre patient ayant une maladie dans une certaine wilaya\n",
        "9-nombre de patient touché par une maladie dans tout le pays\n",
        "10-nombre de patient touché par le coronavirus dans tout le pays depuis le debut de l'epidemie",
        "11-nombre de patient touche par le coronavirus a une date donne",
        "12-nombre de personne d'un certain sex ayant une maladie dans le pays",
        "13-nombre de personne d'un certain sex ayant une maladie dans une wilaya",
        "14-patient admis dans un certain hopital(nom de l'hopital) avec l'adresse de l'hopital son nom et l'adrese du patient",
        ""
        )
    
if __name__ == "__main__":
    choix=menu0()
    err = False
    while(not err):
        if choix=='1':
            patient_onto().saisie_infos()
            print("merci, vos informations ont bien était enregistrer un medecin vous contactera lors de sa consultation")
            err=True
            
        if choix=='2':
            medecin_onto().creation_fiche_final()
            print("merci de votre visite")
            break
        if choix=='3':
            menu_requetes()
            break
        else:
            print("ERREUR! veuillez refaire votre choix!:\n")
            choix=menu0
    