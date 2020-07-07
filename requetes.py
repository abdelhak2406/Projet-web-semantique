import rdflib,re
from enrichissement import traitemnt_onto
##classes reservé au requetes
class requests(traitemnt_onto):
    def __init__(self):
        self.graph = rdflib.Graph()
        self.graph.parse("ontologie.owl",format="turtle")
        open("graph_turtle.rdf","w")    
        self.graph.serialize("graph_turtle.rdf",format="turtle")
        
    def request_0(self,id):

        """
        requete qui permet de trouve les patient et  leurs maladie en fonction de l'id
        """
        id = str(id)

        requete = """ 
        prefix ns1: <https://projetWebsem.org/ontologie.owl#> 
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
        prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix xml: <http://www.w3.org/XML/1998/namespace> 
    
        SELECT ?patient  ?maladie
        WHERE{
        ?patient rdf:type ns1:Patient . 
        ?patient ns1:a_maladie ?maladie0 .
        ?maladie0 ns1:nom_maladie ?maladie .
        ?patient ns1:id_patient  ?idp.
        FILTER regex(?idp,"x0")

        }
        """.replace("x0",id)
        result = self.graph.query(requete)
        for i in result:
            print("===")
            cpt = 0
            for j in i:
                print(cpt," - ",j)
                cpt = cpt + 1
            print("====")
    
    def request_1 (self,date):
        """ avoir les patient ayant consulter a une certaine date """
        pass
    
    def request_2(self,wilaya,commune,maladie):

        """
        liste des patient atteint d'une maladie dans une certaine localité!(wilaya+commune)
        """

        nom_wilaya = re.sub(r" |-", "_", wilaya).title()
        nom_commune = re.sub(r" |-", "_", commune).title()#nom de la wilaya
        maladie = re.sub(r" |-", "_",maladie).lower()
        
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
        ?maladie ns1:nom_maladie ?nommal .
        ?patient ns1:habite_wilaya ?wilay .
        ?wilay ns1:nomWilaya ?nomw .
        ?patient ns1:habite_commune ?comm .
        ?comm ns1:nomCommune ?nomc .
        FILTER regex(?nomw,"x0")
        FILTER regex(?nomc,"x2")
        FILTER regex(?nommal,"x1")
        }
        """
        substitutions = {"x0":nom_wilaya,"x1":maladie,"x2":nom_commune}
        requete = self.replace(requete, substitutions)
        result = self.graph.query(requete)
        for i in result:
            print("===")
            cpt = 0
            for j in i:
                print(cpt," - ",j)
                cpt = cpt + 1
            print("====")

    def request_3(self,wilaya,commune,maladie):
       
        """nombre de patient atteint d'une certaine maladie dans une localite"""
       
        graph = rdflib.Graph()
        graph.parse("ontologie.owl",format="turtle")
        open("graph_turtle.rdf","w")    
        graph.serialize("graph_turtle.rdf",format="turtle")

        nom_wilaya = re.sub(r" |-", "_", wilaya).title()
        nom_commune = re.sub(r" |-", "_", commune).title()#nom de la wilaya
        maladie = re.sub(r" |-", "_",maladie).lower()
        
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
        ?maladie ns1:nom_maladie ?nommal .
        ?patient ns1:habite_wilaya ?wilay .
        ?wilay ns1:nomWilaya ?nomw .
        ?patient ns1:habite_commune ?comm .
        ?comm ns1:nomCommune ?nomc .
        FILTER regex(?nomw,"x0")
        FILTER regex(?nomc,"x2")
        FILTER regex(?nommal,"x1")
        }
        """
        substitutions = {"x0":nom_wilaya,"x1":maladie,"x2":nom_commune}
        requete = self.replace(requete, substitutions)
        result = self.graph.query(requete)
        for i in result:
            print("===")
            for j in i:
                print(" - ",j)

            print("===")      

    def request_4(self,age,maladie):
        """ nombre de patient de moins d'un age x ayant une maladie X """
        graph = rdflib.Graph()
        graph.parse("ontologie.owl",format="turtle")
        open("graph_turtle.rdf","w")    
        graph.serialize("graph_turtle.rdf",format="turtle")
        
        nom_maladie =  re.sub(r" |-", "_",maladie).lower()

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
        ?maladie ns1:nom_maladie ?nommal .
        ?patient ns1:age ?agee .
        FILTER regex (?nommal,"x1")
        FILTER (?agee < x0)
        }
        """

        substitutions = {"x0":str(age),"x1":nom_maladie}
        requete = self.replace(requete, substitutions)
        result = self.graph.query(requete)   
        for i in result:
            print("===")
            cpt = 0
            for j in i:
                print(cpt," - ",j)
                cpt = cpt + 1
            print("====")

    def request_5(self,maladie): #ne marche pas encore!
        """ 
        determiner sympthomes pour une certaine maladie
        """
        graph = rdflib.Graph()
        graph.parse("ontologie.owl",format="turtle")
        open("graph_turtle.rdf","w")    
        graph.serialize("graph_turtle.rdf",format="turtle")
        
        nom_maladie =  re.sub(r" |-", "_",maladie).lower()

        requete = """
        prefix ns1: <https://projetWebsem.org/ontologie.owl#> 
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
        prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix xml: <http://www.w3.org/XML/1998/namespace> 

        SELECT ?sympthom 
        WHERE{
        ?sympthom0 rdf:type  ns1:Sympthomes .
        ?maladie rdf:type ns1:Maladies . 
        ?maladie ns1:nom_maladie ?nommal .
        ?maladie ns1:a_comme_sympthomes ?sympthom0 .
        ?sympthom0 ns1:nom_sympthome ?sympthom
        FILTER regex (?nommal,"x1")
        }
        """

        substitutions = {"x1":nom_maladie}
        requete = self.replace(requete, substitutions)
        result = self.graph.query(requete)   
        for i in result:
            print("===")
            cpt = 0
            for j in i:
                print(cpt," - ",j)
                cpt = cpt + 1
            print("====")

    def request_6(self,wilaya,maladie):
        """ patient ayant une maladie dans une certaine wilaya """
        nom_wilaya = re.sub(r" |-", "_", wilaya).title()
        maladie = re.sub(r" |-", "_",maladie).lower()
        
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
        ?maladie ns1:nom_maladie ?nommal .
        ?patient ns1:habite_wilaya ?wilay .
        ?wilay ns1:nomWilaya ?nomw .
        FILTER regex(?nomw,"x0")
        FILTER regex(?nommal,"x1")
        }
        """
        substitutions = {"x0":nom_wilaya,"x1":maladie}
        requete = self.replace(requete, substitutions)
        result = self.graph.query(requete)
        for i in result:
            print("===")
            cpt = 0
            for j in i:
                print(cpt," - ",j)
                cpt = cpt + 1
            print("====")
    
    def request_7(self,wilaya,maladie):
        """ nombre patient ayant une maladie dans une certaine wilaya """
        nom_wilaya = re.sub(r" |-", "_", wilaya).title()
        maladie = re.sub(r" |-", "_",maladie).lower()
        
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
        ?maladie ns1:nom_maladie ?nommal .
        ?patient ns1:habite_wilaya ?wilay .
        ?wilay ns1:nomWilaya ?nomw .
        FILTER regex(?nomw,"x0")
        FILTER regex(?nommal,"x1")
        }
        """
        substitutions = {"x0":nom_wilaya,"x1":maladie}
        requete = self.replace(requete, substitutions)
        result = self.graph.query(requete)
        for i in result:
            print("====")
            for j in i:
                print(" - ",j)
            print("====")
    
    def request_8(self,maladie):
        """nombre de patient touché par une maladie dans tout le pays
        """
        maladie = re.sub(r" |-", "_",maladie).lower()
        
        requete = """
        prefix ns1: <https://projetWebsem.org/ontologie.owl#> 
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
        prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix xml: <http://www.w3.org/XML/1998/namespace> 

        SELECT (COUNT(?patient) AS ?triples) 
        WHERE{
        ?patient rdf:type ns1:Patient . 
        ?patient ns1:a_maladie ?maladie .
        ?maladie ns1:nom_maladie ?nommal .
        FILTER regex(?nommal,"x1")
        }
        """
        substitutions = {"x1":maladie}
        requete = self.replace(requete, substitutions)
        result = self.graph.query(requete)
        for i in result:
            print("====")
            for j in i:
                print(" - ",j)
            print("====")
    
    def request_9(self):
        """nombre de patient touché par le coronavirus dans tout le pays"""
        self.request_8(maladie="coronavirus")
   
    def request_10(self,sex,maladie):
        """ nombre de personne d'un certain sex aayant une maladie dans le pays"""
        
        maladie = re.sub(r" |-", "_",maladie).lower()
        sex = sex.lower()

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
        ?maladie ns1:nom_maladie ?nommal .
        ?patient ns1:sexe ?sex .
        FILTER regex(?nommal,"x1")
        FILTER regex(?sex,"x2")
        }
        """
        substitutions = {"x1":maladie,"x2":sex}
        requete = self.replace(requete, substitutions)
        result = self.graph.query(requete)
        for i in result:
            print("====")
            for j in i:
                print(" - ",j)
            print("====")
    
    def request_11(self,maladie,sex,wilaya):
        """nombre de personne d'un certain sex ayant la maladie dans une wilaya"""
        maladie = re.sub(r" |-", "_",maladie).lower()
        sex = sex.lower()
        nom_wilaya = re.sub(r" |-", "_", wilaya).title()

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
        ?maladie ns1:nom_maladie ?nommal .
        ?patient ns1:habite_wilaya ?wilay .
        ?wilay ns1:nomWilaya ?nomw .
        ?patient ns1:sexe ?sex .
        FILTER regex(?nommal,"x1")
        FILTER regex(?sex,"x2")
        FILTER regex(?nomw,"x3")
        }
        """
        substitutions = {"x1":maladie,"x2":sex,"x3":nom_wilaya}
        requete = self.replace(requete, substitutions)
        result = self.graph.query(requete)
        for i in result:
            print("====")
            for j in i:
                print(" - ",j)
            print("====")
    
    def request_12(self,traitement):#a besoin du raisonneur !pour qu'elle marche
        """ les patient prenant un certain traitement"""
        
        traitement = re.sub(r" |-", "_",traitement).lower()

        requete = """
        prefix ns1: <https://projetWebsem.org/ontologie.owl#> 
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
        prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix xml: <http://www.w3.org/XML/1998/namespace> 

        SELECT ?id ?wilaya ?commune   
        WHERE{
        ?trait rdf:type ns1:Traitements .
        ?trait ns1:nom_traitement ?nomtrai .
        ?trait ns1:traitement_pris_par ?patient .
        ?patient ns1:habite_wilaya ?wilaya .
        ?wilay ns1:nomWilaya ?nomw .
        ?patient ns1:habite_commune ?commune .
        ?comm ns1:nomCommune ?nomc .
        FILTER regex(?nomtrai,"x0")
        }
        """
        substitutions = {"x0":traitement}
        requete = self.replace(requete, substitutions)
        result = self.graph.query(requete)

        print("nous sommes dans request12 qui recherche les patient prenant un certain traitement ",traitement)
        for i in result:
            print("===")
            cpt = 0
            for j in i:
                print(cpt," - ",j)
                cpt = cpt + 1
            print("====")

    def request_13(self):
        """ suspecter d'avoir le coronavirus  id wilaya commune"""
        pass

    def request_14(self,hopital):
        """ patient admis dans un certain hopital(nom de l'hopital) avec l'adresse de l'hopital son nom et l'adrese du patient """

        hopital = re.sub(r" |-", "_",hopital).lower()

        requete = """
        prefix ns1: <https://projetWebsem.org/ontologie.owl#> 
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
        prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix xml: <http://www.w3.org/XML/1998/namespace> 

        SELECT  ?id ?commune ?wilaya 
        WHERE{
        ?patient rdf:type ns1:Patient .
        ?patient ns1:est_hospitalilser_a ?hopital.
        ?hopital ns1:nom_hopital ?hop .
        ?patient ns1:habite_wilaya ?wil .
        ?wil ns1:nomWilaya ?wilaya .
        ?patient ns1:habite_commune ?com .
        ?com ns1:nomCommune ?commune .
        ?patient ns1:id_patient ?id .
        FILTER  regex(?hop,"x0")
        }
        """
        substitutions = {"x0":hopital}
        requete = self.replace(requete, substitutions)
        result = self.graph.query(requete)
        for i in result:
            print("====")
            for j in i:
                print(" - ",j)
            print("====")
    

    def request_15(self,nom_medecin,prenom_medecin):
        """ patient selon medecin ayant fait la consultation"""
        nom_medecin = re.sub(r" |-", "_",nom_medecin).lower()
        prenom_medecin= re.sub(r" |-", "_",prenom_medecin).lower()

        requete = """
        prefix ns1: <https://projetWebsem.org/ontologie.owl#> 
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
        prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix xml: <http://www.w3.org/XML/1998/namespace> 

        SELECT  ?id ?commune ?wilaya 
        WHERE{
        ?medecin rdf:type ns1:Medecin .
        ?medecin ns1:nom ?nommed .
        ?medecin ns1:prenom ?prenommed .
        ?medecin ns1:effectue_consultation ?consult.
        ?consult ns1:consultation_concerne ?patient .

        ?patient ns1:habite_wilaya ?wil .
        ?wil ns1:nomWilaya ?wilaya .
        ?patient ns1:habite_commune ?com .
        ?com ns1:nomCommune ?commune .
        ?patient ns1:id_patient ?id .
        FILTER  regex(?nommed,"x0")
        FILTER  regex(?prenommed,"x1")
        }
        """
        substitutions = {"x0":nom_medecin,"x1":prenom_medecin}
        requete = self.replace(requete, substitutions)
        result = self.graph.query(requete)
        for i in result:
            print("====")
            for j in i:
                print(" - ",j)
            print("====")

    def request_16(self):
        """ wilaya la plus touche par le virus? """
        pass

    def request_17(self,gravite):
        """ obtenir id et adresse patient celon gravité """
        gravite = re.sub(r" |-", "_",gravite).lower()


        requete = """
        prefix ns1: <https://projetWebsem.org/ontologie.owl#> 
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
        prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix xml: <http://www.w3.org/XML/1998/namespace> 

        SELECT  ?id ?commune ?wilaya 
        WHERE{
        ?patient rdf:type ns1:Patient .
        ?patient ns1:gravite_sympthome ?grav .

        ?patient ns1:habite_wilaya ?wil .
        ?wil ns1:nomWilaya ?wilaya .
        ?patient ns1:habite_commune ?com .
        ?com ns1:nomCommune ?commune .
        ?patient ns1:id_patient ?id .
        FILTER  regex(?grav,"x0")
        }
        """
        substitutions = {"x0":gravite}
        requete = self.replace(requete, substitutions)
        result = self.graph.query(requete)
        for i in result:
            print("====")
            for j in i:
                print(" - ",j)
            print("====")
    
    def request_18(self,date):
        """ nombre patient atteint du covid a une certaine date!(utiliser dateconsultation)"""
        pass

    def request_19(self):
        """nombre de patient se trouvant dans un hoptal """


        requete = """
        prefix ns1: <https://projetWebsem.org/ontologie.owl#> 
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
        prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix xml: <http://www.w3.org/XML/1998/namespace> 

        SELECT  (COUNT(?patient) AS ?triples) 
        WHERE{
        ?patient rdf:type ns1:Patient .
        ?patient ns1:est_hospitalilser_a ?hopital.
        }
        """
        result = self.graph.query(requete)
        for i in result:
            print("====")
            for j in i:
                print(" - ",j)
            print("====")
    
    def request_21(self):
        """ antécédant patient ayant le covid 19"""
        pass

if __name__ == '__main__':
    req =  requests()
    #req.request_11(maladie="coronavirus",sex="femme",wilaya="Blida")
    #req.request_12("piqure de rat")
    #req.request_14("toghza")
    #req.request_15(nom_medecin="vegapunk",prenom_medecin="noName")
    req.request_19()