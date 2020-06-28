import owlready2
import pandas as pd
from enrichissement import patient_onto as pat
#lire
fiche =  pd.read_csv("csv_reference.csv")
print (fiche)
ontolo = pat()

for i,j  in fiche.iterrows():
    ontolo.creer_patient(j["id_patient"],j["sexe"],j["age"],j["poid"],j["taille"],j["wilaya_patient"],j["daira_patient"],j["duree_depuis_derniére_sortie"],
    j["duree_depuis_dernie_sympthomes"],symptomes=j["sympthomes"],maladies=j["Maladie(diagnostique)"],traitements=j["traitement"])

ontolo.save_onto()
#la on doit remplir notre entologie$
for i in ontolo.onto.individuals():
    print(i.iri)
    if not "commune" in i.name: 
        pass

