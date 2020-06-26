
from owlready2 import *


#On crée une nouvelle ontologie 
onto = get_ontology("https://projetWebsem.org/ontologie.owl")

with onto:
    #les attributs et les relations commence par une minuscule les classes par une majuscule
    
    class Personne(Thing):
        pass

    #attribut d"une personne
    class nom(DataProperty, FunctionalProperty):
        range = [str]
        domain = [Personne]

    class prenom(DataProperty):
        range = [str]
        domain = [Personne]

    class age (DataProperty, FunctionalProperty): #une personne n'a qu'un seul age:
        range = [int]
        domain = [Personne]
        pass

    class sexe (DataProperty, FunctionalProperty):
        range = [str]
        domain = [Personne]
        pass

    class poid (DataProperty, FunctionalProperty):
        range = [float]
        domain = [Personne]
        pass
        
    class taille (DataProperty, FunctionalProperty): #une seul Taille
        range = [float]
        domain = [Personne]
        pass

    class Patient(Personne):
        pass    

    class id_patient(DataProperty,FunctionalProperty):
        domain = [Patient]
        range = [int]
        pass
    
    class Allergies(Thing):
        pass
    
    class Maladies(Thing):
        pass

    class Maladies_chroniques(Maladies): #pourrait éventuellement etre supprimer et faire comme racim !avec du scrapping
        pass
    
    class Adresse(Thing):
        pass
    
    class Wilaya(Adresse):
        pass

    #attributs
    class nomWilaya(DataProperty,FunctionalProperty):
        domain = [Wilaya]
        range = [str]
        pass
    class idWilaya(DataProperty,FunctionalProperty):
        domain = [Wilaya]
        range = [int]
        pass
    
    class Daira(Wilaya):
        pass

    class nomDaira(DataProperty,FunctionalProperty ):
        domain = [Daira]
        range = [int]
        pass

    class idDaira(DataProperty,FunctionalProperty):
        domain = [Daira]
        range = [int]
        pass

    class Sympthomes(Thing):
        pass

    class Sympthomes_covid(Sympthomes):
        pass

    class Sympthomes_autres(Sympthomes):
        pass

    class Traitement(Thing):   # patient --> str ??
        pass

    class Medecin(Personne):
        pass

    class id_medecin(DataProperty, FunctionalProperty):
        domain = [Medecin]
        range = [str]
        pass

    class medecin_spcl(Medecin >> str):#on pourrait utiliser une autre classe pour spécialité
        pass

    class Orientation(Thing):
         pass

    class RDV(Thing):
        pass

    class Hopital(Thing):
        pass

    class prise_charge_domicile(Orientation):
        pass

    class Fiche(Thing):
        pass
      
    class duree_depuis_derniere_sortie(Patient >> int):          # c'est pas une relation mais un attribut de patient 
        pass
    class duree_depuis_dernier_sympthomes(Patient >> int):       # attribut de patient aussi ( c pas une relation entre 2 classes )
        pass

    ##----------Relations-----------
    class a_allergies(Patient >> Allergies):
        pass

    class a_maladies_chroniques(Patient >> Maladies_chroniques):
        pass
    class a_sympthomes(Patient >> Sympthomes):
        pass
    class est_sympthomes_maladie(Sympthomes >> Maladies):
        pass
    class a_maladie (Patient >> Maladies):                     # on le met sois pour maladie nagh maladie chronique pas les 2 
        pass
    class prend_traitement ( Patient >> Traitement):
        pass
    class habite_wilaya( Patient >> Wilaya):        # je pense qu'on doit juste faire la relation habite qui sera entre patient et wilaya
        pass
    class habite_daira( Patient >> Daira):          # prsq daira va heriter de cette relation aussi 
        pass
    class est_daira_de(Daira >> Wilaya):
        pass 
    class prend_RDV( Patient >> RDV):           
        pass
    class rediger( Medecin >> Fiche):           
        pass
    class est_concerne( Patient >> Fiche):           
        pass
    class resultat_or( Fiche >> Orientation):           
        pass
    class consulte( Patient >> Medecin):           
        pass
    class est_oriente( Patient >> Orientation):           
        pass
    class hospitalise_a(Orientation >> Hopital):
        pass
    
    class adresse_hopitale(Hopital >> Adresse):
        pass
   # et si on ne mettait pas la classe orientation mais juste la relation orienté ? mais du coup elle sera entre patient et hopital 
   # et entre patient et domicile c possible ? 


onto.save("ontologie.owl", format="ntriples")
