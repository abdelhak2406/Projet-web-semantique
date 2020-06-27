"""
script qui permettera d'enrichir l'ontologie en instantiant des elements
"""
from owlready2 import *
import csv
import types
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

class traitemnt_onto:
    onto = get_ontology("/home/goku/Code/Projet-web-semantique/ontologie.owl").load()
    my_iri = "https://projetWebsem.org/ontologie.owl"
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
            with self.onto:
                new_class = types.new_class(nom_classe,(herite_de,))
                #mettre a jour le dictionnaire
                self.dico = self.creation_dictionnaire()

    def is_in_ontology(self,class_name):
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
            nom = mld.split("/")[-1].title() #extraire type maladie
            noms_types.append(nom)
            #creation des classes nécessaire
            self.ajout_classe(nom,self.dico["Maladies"])

        # Parcourir chaque type de maladie
        for maladie in noms_types:
            if maladie != "dermatologie" and maladie != "gynecologie" and maladie != "ophtalmologie": #on s'en fou de ceux la?
                # Création de chaque type de maladie
                self.ajout_classe(maladie,self.dico["Maladies"])            #enrichissement des types? peut etre a supprimer

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
                        liste_maladies.append(nom_maladie)
                        self.ajout_classe(nom_maladie,self.dico[maladie])

    def save_onto(self):
        self.onto.save(self.onto_name, format="ntriples")



if __name__ == "__main__":

    ontolo = traitemnt_onto()
    ontolo.enrichir_maladies()
    ontolo.save_onto()


