from patient_medecin import patient_onto,medecin_onto
from requetes import requests
from enrichissement import fiche_onto
from csv_to_rdf import supprimer_ligne,csvToRdf
def menu0():
    print("------------------------------------------Bienvenu dans notre appllication de prise de consultation a distance------------------------------------------")
    print("|\n|---------------------------------------------Que voullez vous faire?----------------------------------------------------------------|\n|")
    print("|\t1-je suis un patient et je desire saisir mes information afin de faire une consultation|") 
    print("|\t2-je suis medecin et je desire effectue une ou plusieures consulation\|") 
    print("|\t3-Requetes sparql\t\t\t\t\t\t\t\t\t|")
    print("|\t4-creation de la fichesortie")
    print("|\t5-quittez")
    choi = input('saisissez votre choix:\n')
    if (int(choi)>5) or (int(choi)<1) :
        print('erreur resaisir votre choic')
        menu0()
        
    return choi
def menu_requetes():#TODO: dans la 2eme partie penser a precicez la maniere de saisir une date,ect
   
    print("------------------------------------------------------------------Menu Requetes------------------------------------------------------------------")
    print("---------------------faite votre choix:----------------------------------\nz",
        "1-liste patient  et leurs maladies (chroniques) en fonction de l'id\n",
        "2-liste des patient atteint d'une maladie dans une certaine localité!(wilaya+commune)\n",
        "3-nombre de patient atteint d'une maladie dans une localite(commune,wilaya)\n",
        "4-nombre de patient de moins d'un age ayant une certaine maladie\n",
        "5-nombre de patient de moins d'un certain age ayant le covid\n",
        "6-nombre de patient de moins d'un certain age ayant le covid a une date donne\n",
        "7-liste patient ayant une maladie dans une certaine wilaya\n",
        "8-nombre patient ayant une maladie dans une certaine wilaya\n",
        "9-nombre de patient touché par une maladie dans tout le pays\n",
        "10-nombre de patient touché par le coronavirus dans tout le pays depuis le debut de l'epidemie\n",
        "11-nombre de patient touche par le coronavirus a une date donne\n",
        "12-nombre de personne d'un certain sex ayant une maladie dans le pays\n",
        "13-nombre de personne d'un certain sex ayant une maladie dans une wilaya\n",
        "14-nombre patient admis dans un certain hopital(nom de l'hopital) \n",
        "15-liste patient selon medecin ayant fait la consultation(nom et prenom du medecin)\n",
        "16-liste patient celon gravite_sympthomes (faible moyen grand)\n",
        "17-nombre de patient se trouvant dans un hoptal\n"
        )
    choi = input()
    if int(choi)>17:
        print("---------------------------------------------------------------------------------------------------------------------")
        print('Commande non comprise veuillez refaire votre choix\n\n')
        menu_requetes()
    return choi
   
    
if __name__ == "__main__":
    
    err = False
    while(not err):
        choix=menu0()
        if choix=='1':
            patient_onto().saisie_infos()
            print("merci, vos informations ont bien était enregistrer un medecin vous contactera lors de sa consultation")
            err=True
            
        if choix=='2':
            medecin_onto().creation_fiche_final()
            print("merci de votre visite")
            csvToRdf()
            continue
        if choix=='3':
            choix2= menu_requetes()
            req= requests()
            
            if choix2=='1':
                a = input("donnez l'id du patient: ")
                req.request_0(a)#TODO:faire marcher cette requetes sinon l'enlever
                continue
            if choix2=='2':
                wil =input("donner la wilaya") 
                com=input("donner la commune")
                mala=input("donner la maladie")
                req.request_2(wilaya=wil,commune=com,maladie=mala)
                continue
            if choix2=='3':
                wil =input("donner la wilaya") 
                com=input("donner la commune")
                mala=input("donner la maladie")                
                req.request_3(wilaya=wil,commune=com,maladie=mala)
                continue
            if choix2=='4':
                mala=input("donner la maladie") 
                ag= input("donner age")
                req.request_4(age=ag,maladie=mala)
                continue
            if choix2=='5':
                ag= input("donner age")
                req.request_22(age=ag)
                continue
            
            if choix2=='6':
                ag= input("donner age")
                datee= input('donner date jj/mm/aaaa')
                req.request_23(age=ag,dat=datee)
                continue
            if choix2=='7':
                wil =input("donner la wilaya") 
                mala=input("donner la maladie")                
                req.request_6(wilaya=wil,maladie=mala)
                continue
            if choix2=='8':
                wil =input("donner la wilaya") 
                mala=input("donner la maladie") 
                req.request_7(wilaya=wil,maladie=mala)
                continue
            if choix2=='9':
                mala=input("donner la maladie") 
                req.request_8(maladie=mala)
                continue
            if choix2=='10':
                req.request_9()
                continue
            if choix2=='11':
                datee= input('donner date jj/mm/aaaa')
                req.request_24(dat=datee)
                continue
            if choix2=='12':
                s = input("donner sex homme ou femme")
                mala=input("donner la maladie") 
                req.request_10(sex=s,maladie=mala)
                continue
            if choix2=='13':
                s = input("donner sex homme ou femme")
                mala=input("donner la maladie") 
                wil =input("donner la wilaya") 
                req.request_11(maladie=mala,sex=s,wilaya=wil)
                continue
            if choix2=='14':
                hop= input("donner nom de l'hopital")
                req.request_14(hopital=hop)
                continue
            
            if choix2=='15':
                nm=input("donnez nom medecin ")
                pm=input("donner prenom medecin ")
                req.request_15(nom_medecin=nm,prenom_medecin=pm)
                
            if choix2=='16':
                gr = input("donner gravite sympthomes:\n1-faible\n2-moyen\n3-grave")
                if gr=='1':
                    grav="faible"
                elif grav=="2":
                    grav="moyen"
                else:
                    grav="grave"
                req.request_17(gravite=grav)
                continue
            if choix2=='17':
                req.request_19()
                continue
        
        if choix=="4":#TODO:tester
            fiche_onto().creer_fiche()
            print('vous trouverez la fiche créer dans le repertoire courant sous le nom: fiche_sortie.csv')
        if choix=="5":
            err=True
        else:
            print("ERREUR! veuillez refaire votre choix!:\n")
            choix=menu0

    
