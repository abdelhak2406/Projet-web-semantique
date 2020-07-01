import owlready2
import pandas as pd
from enrichissement import patient_onto as pat
#lire
fiche =  pd.read_csv("csv_reference.csv")
ontolo = pat()

for i,j  in fiche.iterrows():
    ontolo.creer_patient(j["id_patient"],j["sexe"],j["age"],j["poid"],j["taille"],j["wilaya_patient"],j["daira_patient"],j["nb_jrs_depuis_derniere_sortie"],
    j["nb_jrs_depuis_premiers_sympthomes"],symptomes=j["sympthomes"],maladies=j["Maladie(diagnostique)"],traitements=j["traitement"])

ontolo.save_onto()
print("something")
#ontolo.request_3("Oum El Bouaghi","Ouled Zouai")
ontolo.request_4(19)
#la on doit remplir notre entologie$
"""for i in ontolo.onto.individuals():
    print(i.iri)
    if not "commune" in i.name: 
        pass"""