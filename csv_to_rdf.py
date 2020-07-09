from owlready2 import *
import pandas as pd
from patient_medecin import patient_onto as pat
from patient_medecin import medecin_onto as med
from patient_medecin import consultation_onto as consult
from orientation import orientation_onto as orient
from enrichissement import fiche_onto as fich
import csv
def supprimer_ligne(lignes,fiche="fiche_final.csv"):
    """
    lignes liste ,numero de toutes les lignes qui doivent etre supprimer de 
    -fiche 
    """
    liste=[]
    print("nous sommes dans supprimer ligne")
    with open(fiche,mode='r') as rd:
        i=0#on commence par 1 a cause du header
        for row in csv.reader(rd):
            if i not in lignes:#n'a pas etait consulter par le medecin
                liste.append(row)    
            i+=1
    with open(fiche,mode="w") as out:
        writer=csv.writer(out)
        for i in liste:
            writer.writerow(i)
#lire
def csvToRdf():
    fiche =  pd.read_csv("fiche_final.csv")
    ontolo = pat()
    li=[]
    k=0
    for i,j  in fiche.iterrows():
        ontolo.creer_patient(j["id_patient"],j["sexe"],j["age"],j["poid"],taille=j["taille"],wilaya=j["wilaya_patient"],commune=j["commune_patient"],nb_jrs_depuis_derniere_sortie=j["nb_jrs_depuis_derniere_sortie"],
        nb_jrs_depuis_premiers_sympthomes=j["nb_jrs_depuis_premiers_sympthomes"],symptomes=j["sympthomes"],maladies=j["maladies"],traitements=j["traitement"],gravite_sympthom=j["gravite"],acovid=j["atteint covid"],nom=j["nom"],prenom=j["prenom"])
        ontolo.save_onto()
        co = consult()
        ori = orient()
        medec = med()
        ori.creer_orientation(orient=j["orientation"],patient=ontolo.objet_patient)
        co.creer_consultation(date_cons=j["date"],patient = ontolo.objet_patient,orientation=ori.objet_orientation)
        medec.creer_medecin(id=j["id_medecin"],specialite=j["specialite_medecin"],nom=j["nom_medecin"],prenom=j["prenom_medecin"],consultation=co.objet_consultation)
        li.append(k+1)
        k+=1
    with ontolo.onto:
        sync_reasoner_pellet()  
    ontolo.save_onto()
    supprimer_ligne(li)


#ontolo.request_6(commune="Ouled Zouai",wilaya="Oum El Bouaghi",maladie="coronavirus")
#ontolo.request_3("Oum El Bouaghi","Ouled Zouai")
#ontolo.request_4(age=200,maladie="coronavirus")
#ontolo.request_5("coronavirus")
#la on doit remplir notre entologie$
"""for i in ontolo.onto.individuals():
    print(i.iri)
    if not "commune" in i.name: 
        pass"""