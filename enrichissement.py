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

    def obtenir_objet(self,nom_classe,nom_objet):
        """
        retourne une instance d'un certaine objet donc pour cela il faudrait verifier si ce dernier existe ou pas dans la base de donne
        
        """
        rs = self.objet_existe(nom_classe,nom_objet)
        if rs==False :#obj n'existe pas
            nom_classe = re.sub(r" |-", "_", nom_classe).title()
            ob = self.dico[nom_classe]()
            nom_classe = nom_classe.lower()
            nom_objet =  re.sub(r" |-", "_", nom_objet).lower() 
            ob.iri = self.mon_iri+nom_classe+"/"+nom_objet
            return ob
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
        #print("--------------------------------------------------------------------------------------\nles maladies dans nomtypes: ")
        for maladie in noms_types:
         #enrichissement des types? peut etre a supprimer
            mala = re.sub(r" |-", "_", maladie).title()
            #print("pour ",maladie)
            page_maladie = urlopen(quote_page+maladie)#ouvrir la page d'un type de maladie!
            soup = BeautifulSoup(page_maladie, 'html.parser')
            header_maladies = soup.find_all('h3')#recuperer les maladies de ce type (ils sont dans un <a> dans un h3) 
            #print("----------------------------------------------------------------------------------:")
            for x in header_maladies: #parcourir pour les ajouter a notre ontologie
                lien_maladie = [i['href'] for i in x.find_all('a', href=True)] # a cgaqye iteration sa retourne une liste avec 2 fois la meme url                
                
                # Filtrer les pages pour n'avoir que des maladies dans l'ontologie
                nom_mala = lien_maladie[0].split('/')[-2]
                condition = ("definition" not in nom_mala
                            and "symptomes" not in nom_mala
                            and "qu-est-ce" not in nom_mala
                            and "allergie" != nom_mala
                            and "www." not in nom_mala)
                            
                if condition:

                    nom_mala = re.sub(r" |-", "_", nom_mala).lower()
                    #print(nom_mala)
                    if not self.objet_existe(nom_classe=mala,nom_oj=nom_mala):
                        m = self.dico[mala]()
                        try:
                            m.iri=self.mon_iri+"maladies/"+nom_mala
                            m.nom_maladie = str(nom_mala)
                        except:
                            print("\n",self.mon_iri+"maladies/"+nom_mala, "existe déja! dans la base de donnee nous ne l'avons donc pas instatier\n")
                    liste_maladies.append(nom_mala)
                    #self.ajout_classe(nom_maladie,self.dico[mala])

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

    def ajout_sympthomes_covid(self):
        symptomes =["fièvre","toux sèche","fatigue","courbatures","congestion nasale","écoulement nasal",
        "maux de gorge","diarrhée","détresse respiratoire","maux de tête","perte de goût",
        "perte de l'odorat","Nausées,vomissements"]
        #coronavirus
        covid = self.onto.search("*maladies/coronavirus*")[0]

        for i in symptomes:
            i = re.sub(r" |-", "_", i).lower()
            res = self.onto.search(iri="*sympthomes/"+i)
            if res== []:
                symp = self.dico["Sympthomes"]()
                symp.iri = self.mon_iri+"sympthomes/"+i.lower()
                symp.nom_sympthome = i.lower()   
                covid.est_sympthomes_maladie.append(symp)
            else: #pour ne pas avoir de repetition dans les sympthome
                covid.est_sympthomes_maladie.append(res[0])
            
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

class fiche_onto(traitemnt_onto):

    objet_fiche = None
    def __init__(self):	    
        super().__init__()
   
    def traitement_orientation(self,obj_orientation,dico,i):
        print("nous sommes dans traitement orientation ",obj_orientation[0].type_orientation)
        if obj_orientation[0].date_rendez_vous=="prise_en_charge_domicile":
            dico[i]["orientation"]=obj_orientation.type_orientation+":"
        if obj_orientation[0].type_orientation=="prise_de_rendez_vous":
            dico[i]["orientation"]=obj_orientation.type_orientation+":"
            #obj_orientation.date_rendez_vous =
            #TODO: voir comment se presnte une date et la transformer ainsi jj/mm/aa
            print("date de rendez-vous: ",obj_orientation.prend_RDV)
        if  obj_orientation[0].type_orientation=="prise_en_charge_hopital":
            pass


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
    
        SELECT ?consult ?patient ?idpat  ?idmed ?age ?taille ?sexe ?poid ?wilaya_pat ?com_pat ?sympthomes ?njds ?njps ?date ?orientation ?gravite 
        WHERE{
        ?consult rdf:type ns1:Consultation .
        ?consult ns1:date_consultation ?date .
        ?consult ns1:consultation_concerne ?patient.
        ?consult ns1:est_oriente ?orientation .
        ?orientation ns1:type_orientation ?typeorient. 
        ?patient ns1:a_covid ?cov .
        ?patient ns1:id_patient ?idpat.
        ?patient ns1:age ?age .
        ?patient ns1:taille ?taille .
        ?patient ns1:sexe ?sexe .
        ?patient ns1:poid ?poid .
        ?patient ns1:habite_wilaya ?wilaya.
        ?wilaya ns1:nomWilaya ?wilaya_pat .
        ?patient ns1:habite_commune ?commune .
        ?commune ns1:nomCommune ?com_pat .
        ?patient ns1:a_sympthomes ?sympt.
        ?sympt ns1:nom_sympthome ?sympthomes .
        ?patient ns1:gravite_sympthome ?gravite .
        ?patient ns1:nb_jrs_depuis_derniere_sortie ?njds.
        ?patient ns1:nb_jrs_depuis_premiers_sympthomes ?njps.

        
        ?medecin rdf:type ns1:Medecin .
        ?medecin ns1:effectue_consultation ?consult .
        ?medecin ns1:id_medecin ?idmed .
        FILTER regex(?cov,"oui")
        }
        """ 
        dico = {}
        consultations =[]
        result = graph.query(requete)

        for i in result:
            print("===")
            cpt = 0
            for j in i:
                if cpt==0 and j in dico:
                    break
                if cpt ==0 and j not in dico :
                    dico[j]=dict()
                    k=j
                if cpt==1:
                    dico[k]["patient"]=j

                if cpt==2:
                    dico[k]["id_patient"]=j
                
                if cpt==3:
                    dico[k]["id_medecin"]=j
               
                if cpt==4:
                    dico[k]["age"]=j

                if cpt==5:
                    dico[k]['taille']=j
               
                if cpt==6:
                    dico[k]["sexe"]=j
                    
                if cpt==7:
                    dico[k]["poid"]=j
                if cpt==8:
                    dico[k]["wilaya_patient"]=j
                if cpt==9:
                    dico[k]["commune_patient"]=j
                if cpt==10:
                    dico[k]["sympthomes"]=j
                if cpt==11:
                    dico[k]["njds"]=j
                if cpt==12:
                    dico[k]["njps"]=j
                
                if cpt==13:
                    dico[k]["date"]=j

                if cpt==14:
                    dico[k]['orientation']=j

                if cpt==15:
                    dico[k]["gravite"]=j

                cpt = cpt + 1
        #ajouter les infos qui reste!
        for i in dico:
            pat = dico[i]["patient"]
            print(pat)
            obj_pat = self.onto.search(iri=pat)    
            print("objpat:", obj_pat)
            dico[i]["sympthomes"]=""
            for j in  obj_pat[0].a_sympthomes:
                dico[i]["sympthomes"] =dico[i]["sympthomes"]+","+j.nom_sympthome
            dico[i]["maladies"]=""
            for j in obj_pat[0].a_maladie:##TODO:gerer le cas ou il n'a aucune maladie ou aucune sympthomes ect
                dico[i]['maladies'] =dico[i]['maladies']+","+j.nom_maladie 
            dico[i]["traitement"]=""
            for j in obj_pat[0].prend_traitement:
                dico[i]['traitement']=dico[i]['traitement']+","+j.nom_traitement
            print("traitement ",dico[i]["traitement"])
        #self.fich = f
            ori = dico[i]["orientation"]#orientation
            obj_orien = self.onto.search(iri=ori) 

            self.traitement_orientation(obj_orien,dico,i)

        #creation de la fiche finale qui est censé etre faite par le ministére

        with open('fiche_sortie.csv', mode='w') as fiche0:
            patient_infos = csv.writer(fiche0, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            patient_infos.writerow(['id_patient',"wilaya_patient","commune_patient", 'age', "poid", "taille", "sexe", "sympthomes", "maladies","traitement","nb_jrs_depuis_derniere_sortie","nb_jrs_depuis_premiers_sympthomes","date","gravite"])
            patient_infos.writerow([dico[i]["id_patient"], dico[i]["wilaya_patient"],dico[i]["commune_patient"],dico[i]["age"],dico[i]["poid"],dico[i]["taille"],dico[i]["sexe"],dico[i]["sympthomes"],dico[i]["maladies"],dico[i]["traitement"],dico[i]["njds"],dico[i]["njps"],dico[i]["date"],dico[i]["gravite"]
            ])
            # wilaya,commune,age, poid,taille, sexe, sympthomes, maladies,traitements,nb_jour_depuis_dernier_sortie,nb_jour_depuis_premier_sympthomes])
            #TODO: ajouter l'orientation


if __name__ == "__main__":
    """ontolo = traitemnt_onto()
    ontolo.enrichir_maladies()
    ontolo.save_onto()
    adresse = adresses_onto()
    adresse.creer_Wilaya("Localisation_csv/wilayas.csv")
    adresse.creer_Commune("Localisation_csv/communes.csv")
    #ontolo.ajout_sympthomes_covid()
    ontolo.save_onto()"""
    fiche_onto().creer_fiche()
