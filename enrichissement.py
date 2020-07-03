"""
script qui permettera d'enrichir l'ontologie en instantiant des elements
"""
from owlready2 import *
import csv
import types
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pandas as pd
import rdflib
import datetime
class traitemnt_onto:
    
    onto = get_ontology("ontologie.owl").load()
    mon_iri = "https://projetWebsem.org/ontologie.owl#"
    onto_name = "ontologie.owl"

    def __init__(self):
        self.dico = self.creation_dictionnaire()
    
    def creation_dictionnaire(self):
        """ 
        methode qui parcours les classes de l'ontologie et crée un dictionnaire {nomclasse:objet}
        Args : -onto :l'ontologie qu'on veut parcourir
        output : dictionnaire 
        """
        dico = {}
        for i in self.onto.classes():
            dico[i.name] = i
        return dico

    def enrichir_sympthomes_csv(self,nom_sortie):#eventuellement a modifier

        # nom_sortie = "symptomes.csv"    
        with open (nom_sortie, 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(['Symptomes'])
            filewriter.writerow(['fièvre'])
            filewriter.writerow(['toux sèche'])
            filewriter.writerow(['fatigue'])
            filewriter.writerow(['courbatures'])
            filewriter.writerow(['congestion nasale'])
            filewriter.writerow(['écoulement nasal'])
            filewriter.writerow(['maux de gorge'])
            filewriter.writerow(['diarhée'])
            filewriter.writerow(['détresse respiratoire'])

    def ajout_classe(self,nom_classe,herite_de=Thing):#penser a esseyer de voir si le truc avec THing marche
        if not self.is_in_ontology(nom_classe):
            nom_classe = re.sub(r" |-", "_", nom_classe).title()
            with self.onto:
                new_class = types.new_class(nom_classe,(herite_de,))
                #mettre a jour le dictionnaire
                self.dico = self.creation_dictionnaire()

    def ajout_objet(self,nom_classe,nom_objet):
        """
        ajoute une instance d'un certaine objet donc pour cela il faudrait verifier si ce dernier existe ou pas dans la base de donne
        
        """
        rs = self.objet_existe(nom_classe,nom_objet)
        if rs==False :#obj n'existe pas
            nom_classe = re.sub(r" |-", "_", nom_classe).title()
            return self.dico[nom_classe]()
        else:
            return rs
        

    def objet_existe(self,nom_classe,nom_oj):
        """
        verifie si un objet existe ou pas si existe le renvoie sinon renvoie False

        Args:
            -nom_classe :  nom de la classe de l'objet qu'on recherche, la raison est que les iri sont faites ainsi :mon_iri#nom_classe/nomobjet ou id_ibjet
            -nom_oj : nom ou id de l'objet qu'on recherche
        """
        nom_classe = re.sub(r" |-", "_", nom_classe).lower()
        resultat = self.onto.search(iri="*"+nom_classe+"/"+str(nom_oj))
        if resultat == []:
            return False
        else:
            return resultat[0]

    def is_in_ontology(self,class_name):
        class_name = re.sub(r" |-", "_", class_name).title()
        for i in self.onto.classes():
            if (class_name == i.name):
                return True
        return False

    def enrichir_maladies(self):

        quote_page = "https://www.sante-sur-le-net.com/maladies/"
        #ouvrir la page
        page = urlopen(quote_page)
        # parse the html using beautiful soup and store in variable `soup`
        soup = BeautifulSoup(page, 'html.parser')
        
        # Take out the <div> of name and get its value
        name_box = soup.find(
            'div', attrs={'class': 'panel-body'})
        
        # Récuperer les liens (href) des types de maladies
        types_maladies = [i['href'] for i in name_box.find_all('a', href=True)]
        noms_types = []
        liste_maladies = []
        
        # Récupérer les noms des types des maladies et créer les classes
        for mld in types_maladies:
            nom = mld.split("/")[-1] #extraire type maladie
            ##essai de comment marcje relace pour les nom
            noms_types.append(nom)
            nom = re.sub(r" |-", "_", nom).title()
            #creation des classes nécessaire
            self.ajout_classe(nom,self.dico["Maladies"])

        # Parcourir chaque type de maladie
        for maladie in noms_types:
            if maladie != "dermatologie" and maladie != "gynecologie" and maladie != "ophtalmologie": #on s'en fou de ceux la?
                # Création de chaque type de maladie
                mala = re.sub(r" |-", "_", maladie).title()
                self.ajout_classe(mala,self.dico["Maladies"])            #enrichissement des types? peut etre a supprimer

                page_maladie = urlopen(quote_page+maladie)#ouvrir la page d'un type de maladie!
                soup = BeautifulSoup(page_maladie, 'html.parser')
                header_maladies = soup.find_all('h3')#recuperer les maladies de ce type (ils sont dans un <a> dans un h3) 
                print("maladie: ",maladie)
                for x in header_maladies: #parcourir pour les ajouter a notre ontologie
                    lien_maladie = [i['href'] for i in x.find_all('a', href=True)] # a cgaqye iteration sa retourne une liste avec 2 fois la meme url                

                    # Filtrer les pages pour n'avoir que des maladies dans l'ontologie
                    condition = ("myopathies" not in lien_maladie[0] 
                                and "definition" not in lien_maladie[0]
                                and "symptomes" not in lien_maladie[0]
                                and "qu-est-ce" not in lien_maladie[0]
                                and "gastro-enterite" not in lien_maladie[0]
                                and "galactosemie" not in lien_maladie[0]
                                and "maladie-hartnup" not in lien_maladie[0]
                                and "accident-vasculaire-cerebral" not in lien_maladie[0]
                                and "cancer-poumon" not in lien_maladie[0]
                                and "embolie-pulmonaire" not in lien_maladie[0]
                                and "myasthenie" not in lien_maladie[0]
                                and "dysfonction-erectile" not in lien_maladie[0]
                                and "maladies" in lien_maladie[0])
                    if condition:
                        nom_maladie = lien_maladie[0].split('/')[-2].title()
                        nom_maladie = re.sub(r" |-", "_", nom_maladie)
                        liste_maladies.append(nom_maladie)
                        self.ajout_classe(nom_maladie,self.dico[mala])

    def save_onto(self):
        self.onto.save(self.onto_name, format="ntriples")
    
    def replace(self,string, substitutions):
        """remplace un enseble de str en un ensembe de str 
        exemple:
            string = "spam foo bar foo bar spam"
            substitutions = {"foo": "FOO", "bar": "BAR"}
            output = replace(string, substitutions)
        """
        substrings = sorted(substitutions, key=len, reverse=True)
        regex = re.compile('|'.join(map(re.escape, substrings)))
        return regex.sub(lambda match: substitutions[match.group(0)], string)

class adresses_onto(traitemnt_onto):

    path_wilaya = "Localisation_csv/wilayas.csv"
    path_commune = "Localisation_csv/communes.csv"
    encode_wilaya = {}
    encode_commune = {}

    def __init__(self):
        super().__init__()
        self.create_dico_wilaya()
        self.create_dico_commune()
        

    def get_code_wilaya(self,wilaya):
        wilaya = re.sub(r" |-", "_", wilaya).lower()
        return self.encode_wilaya[wilaya]
    

    def get_code_commune(self,commune):
        commune = re.sub(r" |-", "_", commune).lower()
        return self.encode_commune[commune]
    

    def create_dico_wilaya(self):

        wilayas = pd.read_csv(self.path_wilaya)
        for i in range(len(wilayas)):
            nom_w = wilayas.iloc[i]['nom']
            nom_w = re.sub(r" |-", "_", nom_w).lower()
            code_w = str(wilayas.iloc[i]['code'])
            self.encode_wilaya[nom_w]= code_w
    

    def create_dico_commune(self):

        communes = pd.read_csv(self.path_commune)
        for i in range(len(communes)):
            nom_c = communes.iloc[i]['nom']
            nom_c = re.sub(r" |-", "_", nom_c).lower()
            code_c = communes.iloc[i]['code_postal']   
             # code postal se compose de 5 chiffres so ceux qui ont 4 c le 0 qui a été retiré donc on doit l remettre
            if (len(str(code_c)) == 4 ):
                code = self.mon_iri + "commune" + "0" + str(code_c)
            else:
                code = self.mon_iri + "commune" + str(code_c) 
            self.encode_commune[nom_c]= code  


    def creer_Wilaya(self, path):

        wilayas = pd.read_csv(path)
        for i in range(len(wilayas)):
            w = self.dico["Wilaya"]()
            nom_w = wilayas.iloc[i]['nom']
            nom_w = re.sub(r" |-", "_", nom_w)
            code_w = str(wilayas.iloc[i]['code'])
            
            w.nomWilaya = nom_w
            w.idWilaya = int(code_w)
            w.iri =  self.mon_iri + "wilaya" + code_w


    def creer_Commune(self, path):

        communes = pd.read_csv(path)
        for i in range(len(communes)):
            c = self.dico["Commune"]()
            nom_c = communes.iloc[i]['nom']
            nom_c = re.sub(r" |-", "_", nom_c)
            c.nomCommune = nom_c
            code_c = communes.iloc[i]['code_postal']
            wilaya_lie = str(communes.iloc[i]['wilaya_id'])
   
             # code postal se compose de 5 chiffres so ceux qui ont 4 c le 0 qui a été retiré donc on doit l remettre
            if (len(str(code_c)) == 4 ):
                c.iri = self.mon_iri + "commune" + "0" + str(code_c)
            else:
                c.iri = self.mon_iri + "commune" + str(code_c) 

            # lier chaque commune avc sa wilaya
            c.commune_de.append(self.onto.search(iri= self.mon_iri + "wilaya" + wilaya_lie)[0])

class orientation_onto(traitemnt_onto):

    """ a etait tester et marche pour re tester
    on = traitemnt_onto()
    p =  on.dico["Patient"]()
    p.id_patient = 0
    #p.nom = nom    pourquio avoir le nom et le prénom?
    #p.prenom = prenom
    p.taille = 150
    p.sexe = "Homme"
    p.age = 24
    p.poid = 60
    p.nb_jrs_depuis_derniere_sortie = 5
    p.nb_jrs_depuis_premiers_sympthomes = 1

    wil_code = adresses_onto().get_code_wilaya("Bouira")
    wil = on.onto.search(iri='*'+wil_code)[0]#on doit chercher la wilaya sauf aue cette derniere est encode avec son iri donc on va utiliser
    p.habite_wilaya.append(wil) 
   
   
    a = orientation_onto()
    a.creer_orientation(orient="prise_en_charge_hopital",patient=p,hopital="souq ahras")
    a.save_onto()
    """

    objet_orientation = None

    def __init__(self):	    
        super().__init__()	

    def creer_orientation(self, orient,date_rdv=None,patient=None,hopital=None):
        """args
           orient : type d'orientation :prise en charge domicile ou hopital ou bien prise de rdv
           date_rdv: date de rendez vous dans le cas d'une prise de rendez vous jour/mois/annee
           patient : objet patient qui nous sera utile dans le cas ou il y'a prise en charge hopital 
           hopital : on a besoin du nom de l'hopital ou il sait diriger
        on vas créer les objets nécessaire en l'occurence orientation et rdv si nécessaire et ajouter les relations  
        """
        
        #patient = self.onto.search(iri=mon_iri + "patient" + str(id_patient))[0]
        #medecin = self.onto.search(iri=mon_iri + "medecin" + str(id_medecin))[0]
        o = self.dico["Orientation"]()
        print()

        if (orient == "prise_en_charge_domicile"):
            o.type_orientation = orient  

        if (orient == "prise_de_rendez-vous" and date_rdv != None ): 
            o.type_orientation = orient         
            r = self.dico["RDV"]()
            #on va créer un objet de type datetime et l'inputer directement ?           
            tabdate=date_rdv.split("/") #la on devrait obtenir un tableau de 3 elements date mois et anee           
            r.date_rendez_vous= datetime.date(int(tabdate[2]),int(tabdate[1]),int(tabdate[0]))
            #print(r.date_rendez_vous)  donne cette sortie 2026-06-24 pour la date 24/06/2026
            o.prend_RDV.append(r)

            # heu du coup pour la date du rdv et les infos des hopitaux je sais pas trop how to do it 

        if (orient == "prise_en_charge_hopital" and (patient !=None) and hopital !=None):
            o.type_orientation = orient          
            #la faut chercher si l'hopital existe ou pas! on suppose que les iri des opitaux contiendrons le nom des hopitaux (hopitalX/nomhopitale)
            
            #on va vérifier si l'hopital existe sinon on le crée , le probléme c'est qu'il faut savoir ou il se situe, 
            #on pourrait supposer que cela dépend tu patient, donc on vas tout simplement avoir en entrée aussi l'adresse du patient, ou plus simple l'objet patient 
            #lui meme 
            hopital= re.sub(r" |-", "_", hopital).lower()#remplace tout les espaces et - avec _ 
            res = self.onto.search(iri="*"+hopital.lower()+"*")

            if(res ==[]):#objet non instancier
                #creer l'objet
                h = self.dico["Hopital"]()                  
                h.iri = h.iri+"/"+hopital
                wil_code = adresses_onto().get_code_wilaya(patient.habite_wilaya[0].nomWilaya)

                wil = self.onto.search(iri='*'+wil_code)[0]#on doit chercher la wilaya sauf aue cette derniere est encode avec son iri donc on va utilise          
                h.wilaya_hopitale.append(wil)
                o.orienter_vers_hopital.append(h)
            else:
                o.orienter_vers_hopital.append(res[0])

        self.objet_orientation = o

class fiche_onto(traitemnt_onto):

    objet_fiche = None
    def __init__(self):	    
        super().__init__()

    def creer_fiche(self):
        f = self.dico["Fiche"]
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
    
        SELECT ?idpat  ?idmed ?age ?taille ?sexe ?poid ?wilaya_pat ?daira_pat ?sympthomes ?maladies 
        WHERE{
        ?patient rdf:type ns1:Patient . 
        ?patient ns1:id_patient %id.
        ?patient ns1:a_maladie ?maladie .
        }
        """


        self.fich = f


if __name__ == "__main__":
    ontolo = traitemnt_onto()
    ontolo.enrichir_maladies()
    ontolo.save_onto()
    adresse = adresses_onto()
    adresse.creer_Wilaya("Localisation_csv/wilayas.csv")
    adresse.creer_Commune("Localisation_csv/communes.csv")
    adresse.save_onto()
