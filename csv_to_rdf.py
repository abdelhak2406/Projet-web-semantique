from owlready2 import *
import pandas as pd
from patient_medecin import patient_onto as pat
from patient_medecin import medecin_onto as med
from patient_medecin import consultation_onto as consult
from orientation import orientation_onto as orient
from enrichissement import fiche_onto as fich

#lire
fiche =  pd.read_csv("fiche_final.csv")
ontolo = pat()
for i,j  in fiche.iterrows():
    ontolo.creer_patient(j["id_patient"],j["sexe"],j["age"],j["poid"],j["taille"],j["wilaya_patient"],j["commune_patient"],j["nb_jrs_depuis_derniere_sortie"],
    j["nb_jrs_depuis_premiers_sympthomes"],symptomes=j["sympthomes"],maladies=j["maladies"],traitements=j["traitement"],gravite_sympthom=j["gravite"],acovid=j["atteint covid"],nom=j["nom"],prenom=j["prenom"])
    ontolo.save_onto()
    co = consult()
    ori = orient()
    medec = med()
    ori.creer_orientation(orient=j["orientation"],patient=ontolo.objet_patient)
    co.creer_consultation(date_cons=j["date"],patient = ontolo.objet_patient,orientation=ori.objet_orientation)
    medec.creer_medecin(id=j["id_medecin"],specialite=j["specialite_medecin"],nom=j["nom_medecin"],prenom=j["prenom_medecin"],consultation=co.objet_consultation)


with ontolo.onto:
    sync_reasoner_pellet()  
ontolo.save_onto()


print("apres le raisonneur")
#ontolo.request_6(commune="Ouled Zouai",wilaya="Oum El Bouaghi",maladie="coronavirus")
#ontolo.request_3("Oum El Bouaghi","Ouled Zouai")
#ontolo.request_4(age=200,maladie="coronavirus")
#ontolo.request_5("coronavirus")
#la on doit remplir notre entologie$
"""for i in ontolo.onto.individuals():
    print(i.iri)
    if not "commune" in i.name: 
        pass"""