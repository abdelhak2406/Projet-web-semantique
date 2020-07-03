import owlready2
import pandas as pd
from patient_medecin import patient_onto as pat
from patient_medecin import medecin_onto as med
from patient_medecin import consultation_onto as consult
from enrichissement import orientation_onto as orient
from enrichissement import fiche_onto as fich

#lire
fiche =  pd.read_csv("csv_reference.csv")
ontolo = pat()

for i,j  in fiche.iterrows():
    ontolo.creer_patient(j["id_patient"],j["sexe"],j["age"],j["poid"],j["taille"],j["wilaya_patient"],j["daira_patient"],j["nb_jrs_depuis_derniere_sortie"],
    j["nb_jrs_depuis_premiers_sympthomes"],symptomes=j["sympthomes"],maladies=j["Maladie"],traitements=j["traitement"])
    
    co = consult()
    ori = orient()
    medec = med()
    ori.creer_orientation(orient="prise_en_charge_hopital",date_rdv=j["date"],hopital="Toghza",patient=ontolo.objet_patient)
    co.creer_consultation(date_cons=j["date"],patient = ontolo.objet_patient,orientation=ori.objet_orientation)
    medec.creer_medecin(id=j["id_medecin"],sexe="Homme",specialite=j["specialite_medecin"],nom=j["nom medecin"],prenom=j["prenom medecin"],consultation=co.objet_consultation)


ontolo.save_onto()
print("something")
#ontolo.request_3("Oum El Bouaghi","Ouled Zouai")
#ontolo.request_4(19)
#la on doit remplir notre entologie$
"""for i in ontolo.onto.individuals():
    print(i.iri)
    if not "commune" in i.name: 
        pass"""