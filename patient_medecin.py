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
        m = self.obtenir_objet("Medecin",str(id))
        m.id_medecin = str(id)
        m.nom = nom
        m.prenom = prenom
        m.sexe = sexe
        m.medecin_spcl.append(specialite) # et si on faisait aussi du scrapping pour les specialités ? nagh smbalec on laisse akka 
       # je pense qu'on devra mettre ici les relation que le medecin fera genre  rediger fiche et tt 
        if fiche != None:
            m.redige_fiche.append(fiche)

        m.effectue_consultation.append(consultation)

        self.objet_medecin = m


class patient_onto(traitemnt_onto):

    objet_patient = None

    def __init__(self):
        super().__init__()
    
    def ajout_relations(self,liste,typee,pat,relation):
        """
        liste : contient les sympthomes ou les maladies ou les traitement 
        typee : quel est la classe mere : sympthomes maladies , traitements
        pat : l'objet patient
        relation : la relation qu'il faudrait creer
        """
        liste1 = liste.split(",")
        for i in liste1: 
            i = re.sub(r" |-", "_", i)#remplace tout les espaces et - avec _ 
            res = self.onto.search(iri="*"+i.lower()+"*")
            if(res ==[]):#objet non instancier
                if(not self.is_in_ontology(i.lower())):#regarder si classes n'existe pas on la crEe  
                    self.ajout_classe(nom_classe=i.title(),herite_de=self.dico[typee])
                symp = self.dico[i.title()]() #creer objet 
                #creer la relation 
                print("dans le if patient ",pat)
                relation.append(symp)
            else:#objet instancier
                print("else patient: ",pat)
                relation.append(res[0])
    
    def ajout_sympthomes(self,liste_symp,pat):
        liste1 = liste_symp.split(",")
        for i in liste1:
            i = re.sub(r" |-", "_", i).lower()
            res = self.onto.search(iri="*sympthomes/"+i)
            if res== []:
                #créer l'objet sympthome
                symp = self.dico["Sympthomes"]()
                symp.iri = self.mon_iri+"sympthomes/"+i.lower()
                print("le sympthome ",symp.iri)
                pat.a_sympthomes.append(symp)
            elif res[0] not in pat.a_sympthomes: #pour ne pas avoir de repetition dans les sympthomes
                pat.a_sympthomes.append(res[0])        

    def ajout_maladies(self,liste_mala,pat):
        liste1 = liste_mala.split(",")
        for i in liste1:
            i = re.sub(r" |-", "_", i)
            res = self.onto.search(iri="*maladies/"+i)
            if res== []:
                #créer l'objet sympthome
                mala = self.obtenir_objet("Maladies",i.lower())
                pat.a_maladie.append(mala)
            else:#l'objet existe
                pat.a_maladie.append(res[0])
    
    def ajout_traitements(self,liste_trait,pat):
        liste1 = liste_trait.split(",")
        for i in liste1:
            i = re.sub(r" |-", "_", i)
            res = self.onto.search(iri="*traitements/"+i)
            if res== []:
                #créer l'objet sympthome
                trait = self.dico["Traitements"]()
                trait.iri = self.mon_iri+"traitements/"+i.lower()
                pat.prend_traitement.append(trait)
            else:#l'objet existe
                pat.prend_traitement.append(res[0])

    def ajout_wilaya(self,wilaya,pat):
        wil_code = adresses_onto().get_code_wilaya(wilaya)
        wil = self.onto.search(iri='*'+wil_code)[0]#on doit chercher la wilaya sauf aue cette derniere est encode avec son iri donc on va utiliser
        #print("type wil ",type(wil)) 
        pat.habite_wilaya.append(wil)
    
    def ajout_commune(self,commune,pat):
        com_code = adresses_onto().get_code_commune(commune=commune)
        com = self.onto.search(iri='*'+com_code)[0]
        pat.habite_commune.append(com)

    def ajout_hopital(self,hopital):
        pass


    def creer_patient(self,id,sexe,age,poid,taille,wilaya,commune,nb_jrs_depuis_derniere_sortie,nb_jrs_depuis_premiers_sympthomes,symptomes,maladies,traitements,gravite_sympthom, consultation=None):

        ##chercher si l'iri existe
        res0 =self.onto.search(iri="*"+"patient/"+str(id))
        if res0 == []:#il n'existe pas
            print("resultat ",res0)
            p =  self.dico["Patient"]()
            p.iri = self.mon_iri + "patient/" + str(id) #on le cree
        else:#il existe(le patient ayant cet id)
            print("resuultat de la recherche du patient ",res0)
            print("id patient existant dans la base de donne nous supposons que c'est une autre consultation d'un meme patient")
            p = res0[0]
        
        p.id_patient = str(id)
        #p.nom = nom    pourquio avoir le nom et le prénom?
        #p.prenom = prenom
        p.taille = taille
        p.sexe = sexe
        p.age = age
        p.poid = poid
        p.nb_jrs_depuis_derniere_sortie = nb_jrs_depuis_derniere_sortie
        p.nb_jrs_depuis_premiers_sympthomes = nb_jrs_depuis_premiers_sympthomes
        
        p.gravite_sympthome = gravite_sympthom
        
        if(consultation != None):
            p.concerne.append(consultation)

        self.ajout_sympthomes(symptomes,p)

        #-------------------------------------------------------------maladies--------------------------------
        self.ajout_maladies(maladies,p)

        #-------------------------------------------traitement------------------------------
        self.ajout_traitements(traitements,p)

        #-------------------------------------------
        self.ajout_wilaya(wilaya,p)
        
        #print("habite wilaya :\n",p.habite_wilaya[0].nomWilaya)
        
        self.ajout_commune(commune,p)
        
        #print("commune : ",p.habite_commune[0].nomCommune)
               
        self.objet_patient = p

        self.creer_relations_sympthomes(maladies)
                                 
    def creer_relations_sympthomes(self,maladie):
        """
        creer la relation entre maladie et sympthomes est_sympthomes_maladies, le truc c'est que si un malade a plusieurs sympthomes, 
        et bien sa devient vite des données tres fausse! donc on ne l'utilise que si il y'a une seul maladie pour etre sur
        """
        liste1 = maladie.split(",")
        if len(liste1)==1:
            mal= re.sub(r" |-", "_", liste1[0]).lower()
            m = self.obtenir_objet(nom_objet=mal,nom_classe="Maladies")
            print("les sympthomes du patien sont: ",self.objet_patient.a_sympthomes)
            for i in self.objet_patient.a_sympthomes:
                i.est_sympthomes_maladie.append(m)



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