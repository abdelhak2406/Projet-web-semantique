from owlready2 import *


#On crée une nouvelle ontologie 
onto = get_ontology("https://projetWebsem.org/ontologie.owl")

with onto:
    #les attributs et les relations commence par une minuscule les classes par une majuscule
    
    class Personne(Thing):
        pass
    #attribut d"une personne
    class age (Personne >> int):#une personne n'a qu'un seul age:
        pass
    class sexe (DataProperty, FunctionalProperty):
        range = [str]
        domain = [Personne]
        pass
    
    
    class Patient(Personne):
        pass    
    class Poid (Patient >> float):
        pass
    class Taille (Patient >> float): #une seul Taille
        pass

    class Id(DataProperty,FunctionalProperty):
        domain = [Patient]
        range = [int]
        pass
    
    class Allergies(Thing):
        pass
    
    class Maladies(Thing):
        pass
    
    class Adresse(Thing):
        pass
    
    class Wilaya(Adresse):
        pass
    
    class Daira(Wilaya):
        pass
    class Fiche(Thing):
        pass
    ##----------Relations-----------
    class a_allergies(Patient >> Allergies):
        pass
    class duree_depuis_derniere_sortie(Patient >> int):
        pass
    class duree_depuis_dernier_sympthomes(Patient >> int):
        pass
