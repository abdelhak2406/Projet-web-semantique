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
class traitemnt_onto:
    onto = get_ontology("/home/goku/Code/Projet-web-semantique/ontologie.owl").load()
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

    def creer_Wilaya(self, path):
        wilayas = pd.read_csv(path)
        for i in range(len(wilayas)):
            w = self.dico["Wilaya"]()
            nom_w = wilayas.iloc[i]['nom']
            nom_w = re.sub(r" |-", "_", nom_w)
            code_w = str(wilayas.iloc[i]['code'])
            w.nomWilaya = nom_w
            w.idWilaya = code_w
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

    def creer_medecin(self,id,nom,prenom,sexe,spécialité):
        m = self.dico["Medecin"]()
        m.id_medecin = id
        m.nom = nom
        m.prenom = prenom
        m.sexe = sexe
        m.medecin_spcl = spécialité # et si on faisait aussi du scrapping pour les specialités ? nagh smbalec on laisse akka 
        m.iri = self.mon_iri + "medecin" + str(id)
       # je pense qu'on devra mettre ici les relation que le medecin fera genre  rediger fiche et tt 

    def creer_patient(self,id,sexe,age,poid,taille,wilaya,commune,nb_jrs_depuis_derniere_sortie,nb_jrs_depuis_premiers_sympthomes,symptomes,maladies,traitements):
        p =  self.dico["Patient"]()
        p.id_patient = id
        #p.nom = nom    pourquio avoir le nom et le prénom?
        #p.prenom = prenom
        p.taille = taille
        p.sexe = sexe
        p.age = age
        p.poid = poid
        p.duree_depuis_derniere_sortie.append(nb_jrs_depuis_derniere_sortie)
        p.duree_depuis_dernier_sympthomes.append(nb_jrs_depuis_premiers_sympthomes)
        
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

        

#je pense on devrai faire ça aussi pour maladies et symptomes prsq on on a generé un fichier contenant les maladies 
# maiiiiiis on a pas crééer les objets    
        


if __name__ == "__main__":

    ontolo = traitemnt_onto()
    ontolo.enrichir_maladies()
    ontolo.creer_Wilaya("Localisation_csv/wilayas.csv")
    ontolo.creer_Commune("Localisation_csv/communes.csv")
    ontolo.save_onto()