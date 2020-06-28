import owlready2
import pandas as pd
import enrichissement as enr
#lire
fiche =  pd.read_csv("csv_reference.csv")
print (fiche)
ontolo = enr.traitemnt_onto()

for i,j  in fiche.iterrows():
    ontolo.creer_patient(j["id_patient"],j["sexe"],j["age"],j["poid"],j["taille"],j["wilaya_patient"],j["daira_patient"],j["duree_depuis_derniére_sortie"],
    j["duree_depuis_dernie_sympthomes"],symptomes=j["sympthomes"],maladies=j["Maladie(diagnostique)"],traitements=j["traitement"])

#la on doit remplir notre entologie$
for i in ontolo.onto.individuals():
    if not "commune" in i.name: 
        print(i.iri)

