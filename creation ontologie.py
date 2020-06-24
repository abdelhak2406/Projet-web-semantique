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
    class poid (Patient >> float):
        pass
    class taille (Patient >> float): #une seul Taille
        pass

    class id(DataProperty,FunctionalProperty):
        domain = [Patient]
        range = [int]
        pass
    
    class Allergies(Thing):
        pass
    
    class Maladies(Thing):
        pass

    class Maladies_chroniques(Maladies):
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
    class nomDaira(Daira >> str ):
        pass
    class idDaira(DataProperty,FunctionalProperty):
        domain = [Daira]
        range = [int]
        pass
    class Sympthomes(Thing):
        pass
    class Sympthomes_covid(Sympthomes):
        pass
    class Sympthomes_autres_maladies(Sympthomes):
        pass
    
    class Fiche(Thing):
        pass
    class Traitement(Thing):
        pass

    ##----------Relations-----------
    class a_allergies(Patient >> Allergies):
        pass
    class duree_depuis_derniere_sortie(Patient >> int):
        pass
    class duree_depuis_dernier_sympthomes(Patient >> int):
        pass
    class a_maladies_chroniques(Patient >> Maladies_chroniques):
        pass
    class a_sympthomes(Patient >> Sympthomes):
        pass
    class na_pas_sympthomes(Patient >> Sympthomes):
        pass
    class est_sympthomes_maladie(Sympthomes >> Maladies):
        pass
    class a_maladie (Patient >> Maladies):
        pass
    class na_pas_maladies( Patient >> Maladies):
        pass
    class prend_traitement ( Patient >> Traitement):
        pass
    class habite_wilaya( Patient >> Wilaya):
        pass
    class habite_daira( Patient >> Daira):
        pass
    
onto.save("ontologie.owl", format="ntriples")
