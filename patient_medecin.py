from enrichissement import adresses_onto
from enrichissement import traitemnt_onto
import re
import rdflib
import datetime
class medecin_onto(traitemnt_onto):
    objet_medecin  = None
    def __init__(self):
        super().__init__()
    
    def creer_medecin(self,id,sexe,specialite,nom,prenom,consultation,fiche=None):
        """Args
            id: id du medecin 
            nom
            prenom 
            sexe
            specialite : du medecin
            fiche: objet fiche
            consultation: objet consulatation 
        """
        m = self.dico["Medecin"]()
        m.id_medecin = id
        
        m.nom = nom
        m.prenom = prenom
        m.sexe = sexe
        m.medecin_spcl.append(specialite) # et si on faisait aussi du scrapping pour les specialités ? nagh smbalec on laisse akka 
        #m.iri = self.mon_iri + "medecin" + str(id)
       # je pense qu'on devra mettre ici les relation que le medecin fera genre  rediger fiche et tt 
        if fiche != None:
            m.redige_fiche.append(fiche)

        m.effectue_consultation.append(consultation)

        self.objet_medecin = m


class patient_onto(traitemnt_onto):
    objet_patient = None
    def __init__(self):
        super().__init__()
    def creer_patient(self,id,sexe,age,poid,taille,wilaya,commune,nb_jrs_depuis_derniere_sortie,nb_jrs_depuis_premiers_sympthomes,symptomes,maladies,traitements):
        p =  self.dico["Patient"]()
        p.id_patient = id
        #p.nom = nom    pourquio avoir le nom et le prénom?
        #p.prenom = prenom
        p.taille = taille
        p.sexe = sexe
        p.age = age
        p.poid = poid
        p.nb_jrs_depuis_derniere_sortie = nb_jrs_depuis_derniere_sortie
        p.nb_jrs_depuis_premiers_sympthomes = nb_jrs_depuis_premiers_sympthomes
        #p.iri = self.mon_iri + "patient" + str(id) # faudra mettre str pour l id du patient dans l'ontologie 
        
        liste_sympthomes = symptomes.split(",")
        for i in liste_sympthomes: 
            i = re.sub(r" |-", "_", i)#remplace tout les espaces et - avec _ 
            res = self.onto.search(iri="*"+i.lower()+"*")
            if(res ==[]):#objet non instancier
                if(not self.is_in_ontology(i.lower())):#regarder si classes n'existe pas on la crEe  
                    self.ajout_classe(nom_classe=i.title(),herite_de=self.dico["Sympthomes"])
                symp = self.dico[i.title()]() #creer objet 
                #creer la relation 
                p.a_sympthomes = [symp]
            else:#objet instancier
                p.a_sympthomes.append(res[0])
        #-------------------------------------------------------------maladies--------------------------------
        liste_maladies = maladies.split(",")
        for i in liste_maladies: 
            i = re.sub(r" |-", "_", i)#remplace tout les espaces et - avec _ 
            res = self.onto.search(iri="*"+i.lower()+"*")
            if(res ==[]):#objet non instancier
                if(not self.is_in_ontology(i.lower())):#regarder si classes n'existe pas on la crEe  
                    self.ajout_classe(nom_classe=i.title(),herite_de=self.dico["Maladies"])#nous n`allons pas cherche le type de la maladie
                mala = self.dico[i.title()]() #creer objet 
                #creer la relation 
                p.a_maladie = [mala]
            else:#objet instancier
                p.a_maladie.append(res[0])
        print("les maladies tadadadaaaaaa....\n sont: ")
        for i in p.a_maladie:
            print(i.name)
        #-------------------------------------------traitement------------------------------
        liste_traitements = traitements.split(",")
        for i in liste_traitements: 
            i = re.sub(r" |-", "_", i)#remplace tout les espaces et - avec _ 
            res = self.onto.search(iri="*"+i.lower()+"*")
            if(res ==[]):#objet non instancier
                if(not self.is_in_ontology(i.lower())):#regarder si classes n'existe pas on la crEe  
                    self.ajout_classe(nom_classe=i.title(),herite_de=self.dico["Traitement"])#nous n`allons pas cherche le type de la maladie
                trait = self.dico[i.title()]() #creer objet 
                #creer la relation 
                p.prend_traitement = [trait]
            else:#objet instancier
                p.prend_traitement.append(res[0])
        print("les traitemnt sont ....\n")
        for i in p.prend_traitement:
            print(i.name)
            
        #-------------------------------------------
        wil_code = adresses_onto().get_code_wilaya(wilaya)
        wil = self.onto.search(iri='*'+wil_code)[0]#on doit chercher la wilaya sauf aue cette derniere est encode avec son iri donc on va utiliser
        #print("type wil ",type(wil)) 
        p.habite_wilaya.append(wil) 
        #print("habite wilaya :\n",p.habite_wilaya[0].nomWilaya)
        com_code = adresses_onto().get_code_commune(commune=commune)
        com = self.onto.search(iri='*'+com_code)[0]
        p.habite_commune.append(com)
        #print("commune : ",p.habite_commune[0].nomCommune)
        
        
        self.objet_patient = p

    def request(self,id):

        """
        requete qui permet de trouve les patient et  leurs maladie en fonction de l'id
        """
        graph = rdflib.Graph()
        graph.parse("ontologie.owl",format="turtle")
        open("graph_turtle.rdf","w")    
        graph.serialize("graph_turtle.rdf",format="turtle")


        
        requete = """ 
        prefix ns1: <https://projetWebsem.org/ontologie.owl#> 
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
        prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix xml: <http://www.w3.org/XML/1998/namespace> 
    
        SELECT ?patient  ?maladie
        WHERE{
        ?patient rdf:type ns1:Patient . 
        ?patient ns1:id_patient %id.
        ?patient ns1:a_maladie ?maladie .
        }
        """.replace("%id",id)
        result = graph.query(requete)
        for i in result:
            print("===")
            cpt = 0
            for j in i:
                print(cpt," - ",j)
                cpt = cpt + 1
            print("====")
    
    def request_2(self):

        """
        liste de patient atteint d'une maladie
        """
        graph = rdflib.Graph()
        graph.parse("ontologie.owl",format="turtle")
        open("graph_turtle.rdf","w")    
        graph.serialize("graph_turtle.rdf",format="turtle")

        nom_wilaya = "Béjaïa"
        nom_wilaya = re.sub(r" |-", "_", nom_wilaya).title()#nom de la wilaya
        maladie = "enceinte"
        maladie = re.sub(r" |-", "_",maladie).title()
        
        
        requete = """
        prefix ns1: <https://projetWebsem.org/ontologie.owl#> 
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
        prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix xml: <http://www.w3.org/XML/1998/namespace> 

        SELECT ?patient 
        WHERE{
        ?patient rdf:type ns1:Patient . 
        ?patient ns1:a_maladie ?maladie .
        ?maladie rdf:type ns1:x1 .
        ?patient ns1:habite_wilaya ?wilaya .
        ?wilaya ns1:nomWilaya ?nom_wil  
        FILTER regex(?nom_wil,"x0")
        }
        """
        substitutions = {"x0":nom_wilaya,"x1":maladie}
        requete = self.replace(requete, substitutions)
        result = graph.query(requete)
        for i in result:
            print("===")
            cpt = 0
            for j in i:
                print(cpt," - ",j)
                cpt = cpt + 1
            print("====")

    def request_3(self,wilaya,commune ):
        """ nombre de patient atteint du covid dans une commune d'une certaine wilaya  """
        commune = re.sub(r" |-", "_", commune).title()
        wilaya = re.sub(r" |-", "_", wilaya).title()
        nom_maladie = "Covid19"
        
        
        graph = rdflib.Graph()
        graph.parse("ontologie.owl",format="turtle")
        open("graph_turtle.rdf","w")    
        graph.serialize("graph_turtle.rdf",format="turtle")
        
        requete = """
        prefix ns1: <https://projetWebsem.org/ontologie.owl#> 
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
        prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix xml: <http://www.w3.org/XML/1998/namespace> 

        SELECT  (COUNT(?patient) AS ?triples)
        WHERE{
        ?patient rdf:type ns1:Patient . 
        ?patient ns1:a_maladie ?maladie .
        ?maladie rdf:type ns1:x1 .
        ?patient ns1:habite_wilaya ?wilaya .
        ?wilaya ns1:nomWilaya ?nom_wil  .
        ?patient ns1:habite_commune ?commune .
        ?commune ns1:nomCommune ?nom_com .
        FILTER regex(?nom_wil,"x0")
        FILTER regex(?nom_com,"x2")
        }
        """
        substitutions = {"x0":wilaya,"x1":nom_maladie,"x2":commune}
        requete = self.replace(requete, substitutions)
        result = graph.query(requete)
        for i in result:
            print("===")
            for j in i:
                print(" - ",j)

            print("===")

    def request_4(self,age):
        """ nobre de patient de moins d'un age x ayant le covid """
        graph = rdflib.Graph()
        graph.parse("ontologie.owl",format="turtle")
        open("graph_turtle.rdf","w")    
        graph.serialize("graph_turtle.rdf",format="turtle")
        
        nom_maladie = "Covid19"

        requete = """
        prefix ns1: <https://projetWebsem.org/ontologie.owl#> 
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
        prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix xml: <http://www.w3.org/XML/1998/namespace> 

        SELECT ?patient ?agee
        WHERE{
        ?patient rdf:type ns1:Patient . 
        ?patient ns1:a_maladie ?maladie .
        ?maladie rdf:type ns1:x1 .
        ?patient ns1:age ?agee .
        FILTER (?agee < x0)
        }
        """

        substitutions = {"x0":str(age),"x1":nom_maladie}
        requete = self.replace(requete, substitutions)
        result = graph.query(requete)
        print(requete+"\n")       
        for i in result:
            print("===")
            cpt = 0
            for j in i:
                print(cpt," - ",j)
                cpt = cpt + 1
            print("====")

    def request_5(self):
        """ 
        determiner sympthomes pour une certaine maladie
        """


class consultation_onto(traitemnt_onto):
    objet_consultation = None
    def __init__(self):
        super().__init__()

    def creer_consultation(self, date_cons,patient,orientation):
        """
            patient : l'objet patient qu'on va créer  avant de creer une consultation 
            date_cons : date de la consultation 
            orientation = l'objet orientation qu'on a créer avant 

        """
        

        cons = self.dico["Consultation"]()

        tabdate=date_cons.split("/") #la on devrait obtenir un tableau de 3 elements date mois et anee    
        cons.date_consultation = datetime.date(int(tabdate[2]),int(tabdate[1]),int(tabdate[0]))
        cons.est_oriente.append(orientation)
        cons.consultation_concerne.append(patient)
        #je sais pas ce qu'elle retourne cette fonction prsq j besoin de l iri de l'orientation
        self.objet_consultation = cons