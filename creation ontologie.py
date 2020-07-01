
from owlready2 import *


#On cree une nouvelle ontologie 
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
        range = [str]
        pass
        
    class Maladies(Thing):
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
    
    class Commune(Wilaya):
        pass

    class nomCommune(DataProperty,FunctionalProperty ):
        domain = [Commune]
        range = [str]
        pass

    class Sympthomes(Thing):  
        pass
    
    class gravite_sympthome(DataProperty,FunctionalProperty): # severe , grave et moderer 
        domain = [Sympthomes]
        range = [str]
        pass

    class Traitement(Thing):   # les traitement que prend le patient actuellement 
        pass

    class Medecin(Personne):
        pass
    #pour le lieu de residence du medecin et de l'hopital ou il exerce nous estimons que nous navons pas besoin de le preciser
    class id_medecin(DataProperty, FunctionalProperty):
        domain = [Medecin]
        range = [str]
        pass

    class medecin_spcl(Medecin >> str): #on va garder sa comme sa mais ou pourrait faire du scrapping et creer une classe
        pass

    class Consultation(Thing):
        pass
    class date_consultation(DataProperty, FunctionalProperty): # 
        domain = [Consultation]
        range = [datetime.date]
        pass
    
    class Orientation(Thing):# par orientation on parle de soit aller a lhopital ou bien a la maison ou bien
        pass
    class type_orientation(DataProperty, FunctionalProperty): # rdv ou  prise en charge domicile ou prise en charge hopital
        domain = [Orientation]
        range = [str]
        pass
    
    class RDV(Thing): # pour prendre rendez vous chez un medecin 
        pass
    class date_rendez_vous(DataProperty, FunctionalProperty):
        domain = [RDV]
        range = [datetime.date]
        pass
    class Hopital(Thing):
        pass

    class Fiche(Thing):
        pass
      
    class nb_jrs_depuis_derniere_sortie(DataProperty , FunctionalProperty):          # c'est pas une relation mais un attribut de patient 
        domain = [Patient]
        range = [int]
        pass

    class nb_jrs_depuis_premiers_sympthomes(DataProperty , FunctionalProperty):       # attribut de patient aussi ( c pas une relation entre 2 classes )
        domain = [Patient]
        range = [int]
        pass

    ##----------Relations-----------
    class a_sympthomes(Patient >> Sympthomes):
        pass
    class est_sympthomes_maladie(Sympthomes >> Maladies):
        pass
    class a_maladie (Patient >> Maladies):                     # on le met sois pour maladie nagh maladie chronique pas les 2 
        pass
    class prend_traitement ( Patient >> Traitement):
        pass
    class habite_wilaya( Patient >> Wilaya):            # je pense qu'on doit juste faire la relation habite qui sera entre patient et wilaya
        pass
    class habite_commune( Patient >> Commune):          # prsq daira va heriter de cette relation aussi 
        pass
    class commune_de(Commune >> Wilaya):
        pass
    class prend_RDV( Patient >> RDV):           
        pass
    class redige_fiche( Medecin >> Fiche):               #si une fiche est un papier regroupant le nom du medecin et le nom du patient  (un seul) alors je n'en vois pas l"inteet
                                            #si une fiche contient les information des medecin de ces patient ect... alors oui ,l'idee est interessante
        pass

    class consulte( Patient >> Consultation):       #on pourra obtenir la nom du medecim consulter a partir de consultation            
        pass
    class est_oriente( Consultation >> Orientation): # le reesultat de la consultation            
        pass
    class hospitalise_a(Orientation >> Hopital):
        pass   
    class adresse_hopitale(Hopital >> Adresse):
        pass
    class effectue_consultation(Medecin >> Consultation):
        pass 
   # et si on ne mettait pas la classe orientation mais juste la relation orient� ? mais du coup elle sera entre patient et hopital 
   # et entre patient et domicile c possible ? 


onto.save("ontologie.owl", format="ntriples")