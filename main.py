from patient_medecin import patient_onto,medecin_onto
def menu0():
    print("------------------------------------------Bienvenu dans notre appllication de prise de consultation a distance------------------------------------------")
    print("|\n|---------------------------------------------Que voullez vous faire?----------------------------------------------------------------|\n|")
    print("|\t1-je suis un patient et je desire saisir mes information afin de faire une consultation\t\t\t\t\t\t\t|") 
    print("|\t2-je suis medecin et je desire effectue une ou plusieures consulation\t\t\t\t\t\t\t\t|") 
    print("|\t3-Requetes sparql\t\t\t\t\t\t\t\t\t|")
    choi = input('saisissez votre choix:\n')
    return choi
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
            pass
        else:
            print("ERREUR! veuillez refaire votre choix!:\n")
            choix=menu0
      