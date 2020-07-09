from enrichissement import adresses_onto
from enrichissement import traitemnt_onto
import re
import rdflib
import datetime
import csv
import pandas as pd
from datetime import date
class medecin_onto(traitemnt_onto):

    objet_medecin  = None

    def __init__(self):
        super().__init__()
    
    def creer_medecin(self,id,specialite,nom,prenom,consultation,fiche=None):
        """Args
            id: id du medecin 
            nom
            prenom  

            specialite : du medecin
            fiche: objet fiche
            consultation: objet consulatation 
        """
        m = self.obtenir_objet("Medecin",str(id))
        m.id_medecin = str(id)
        m.nom = re.sub(r" |-", "_",nom).lower()
        m.prenom = re.sub(r" |-", "_",prenom).lower()
        m.medecin_spcl.append(specialite) # et si on faisait aussi du scrapping pour les specialités ? nagh smbalec on laisse akka 
       # je pense qu'on devra mettre ici les relation que le medecin fera genre  rediger fiche et tt 
        if fiche != None:
            m.redige_fiche.append(fiche)

        m.effectue_consultation.append(consultation)

        self.objet_medecin = m
    def crreation_header_fiche_final(self):
        with open('fiche_final.csv', mode='w') as fiche0:
            patient_infos = csv.writer(fiche0, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            patient_infos.writerow(['nom', 'prenom', 'id_patient',"wilaya_patient","commune_patient", 'age', "poid", "taille", "sexe",
                            "sympthomes", "maladies","traitement","nb_jrs_depuis_derniere_sortie","nb_jrs_depuis_premiers_sympthomes",
                            "date","nom_medecin","prenom_medecin","id_medecin","atteint covid","orientation","gravite","specialite_medecin"])
    
    def supprimer_ligne(self,lignes,fiche="fiche_preliminaire.csv"):
        """
        lignes liste ,numero de toutes les lignes qui doivent etre supprimer de 
        -fiche 
        """
        liste=[]
        print("nous sommes dans supprimer ligne")
        with open(fiche,mode='r') as rd:
            i=0#on commence par 1 a cause du header
            for row in csv.reader(rd):
                if i not in lignes:#n'a pas etait consulter par le medecin
                    liste.append(row)    
                i+=1
        with open(fiche,mode="w") as out:
            writer=csv.writer(out)
            for i in liste:
                writer.writerow(i)
                
    def creation_fiche_final(self,fiche_preliminaire="fiche_preliminaire.csv"):
        """
        fiche_preliminaire: contient les infos que le patient a saisie! on la parcours donc et pour chaque colonne qu'il reste on remplie! 
        donc il faut affiché le contenu de 
        """
        #parcourir la fiche préliminaire
        df = pd.read_csv(fiche_preliminaire)
        listes_consultation=[]
        for i in range(len(df)):
            print("-----------------------------------------------------------------------------------------------------------------------------\n")
            print("------------------------------------------voici les infos saisie par le patient---------------------------------------------\n")
            print("-----------------------------------------------------------------------------------------------------------------------------\n")
            print("age: ",df.iloc[i]["age"],"\npoid: ",df.iloc[i]["poid"],"\ntaille: ",df.iloc[i]["taille"],"\nsexe: ", 
                df.iloc[i]["sexe"]," \nsympthomes:",df.iloc[i]["sympthomes"] ,"\nmaladies: ",df.iloc[i]["maladies"],
                '\nnb_jrs_depuis_derniere_sortie: '
                ,df.iloc[i]["nb_jrs_depuis_derniere_sortie"],
                "\nnb_jrs_depuis_premiers_sympthomes: ",df.iloc[i]["nb_jrs_depuis_premiers_sympthomes"])

            try:
                print("traitements: ",df.iloc[i]["traitement"])
            except:
                pass

            print("-----------------------------------------------------------------------------------------------------------------------------\n")

            print("------------------------------------------veuille remplir le reste des information-------------------------------------------\n")
            
            #infos medecin
            nom = input("saisir votre nom: ")
            prenom = input("saisir votre prenom: ")
            id = input("donner votre id: ")
            specialite = input("precisez votre specialite: ")
            cov=input("ce patient est_il atteint du covid celon vous!\n\ty:oui\n\tn:non\n")
            if cov=="y":
                cov="oui"
            else:
                cov="non"
            grav = input("gravite sympthomes:\n1-faible\n2-moyen\n3-grave")
            if grav=='1':
                gravite="faible"
            elif grav=="2":
                gravite="moyen"
            else:
                gravite="grave"
                
            ori = input("quel est l'orientation a suivre?\n1-prise en charge domicile\n2-prise_rendez-vous\n3-prise en charge hopital\n")
            if ori=='1':
                orientation='prise_en_charge_domicile:'
            elif ori=='2':
                rdv = input("saisir la date de rendez vous jj/mm/aa: ")
                orientation ="prise_de_rendez_vous:"+rdv
            else:
                hop =input("saisir l'hopital de prise en charge: ")
                orientation = "prise_en_charge_hopital:"+hop
            date0 = date.today()
            dat=str(date0.day)+"/"+str(date0.month)+"/"+str(date0.year)
            #remplissage nouvelle fiche
            with open('fiche_final.csv', mode='a+') as fiche0:
                patient_infos = csv.writer(fiche0, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                """patient_infos.writerow(['nom', 'prenom', 'id_patient',"wilaya_patient","commune_patient", 'age', "poid", "taille", "sexe",
                "sympthomes", "maladies","traitement",nb_jrs_depuis_derniere_sortie","nb_jrs_depuis_premiers_sympthomes",
                "date","nom_medecin","prenom_medecin","id_medecin","atteint covid","orientation","gravite","specialite_medecin"])
                """
                try:
                    patient_infos.writerow([df.iloc[i]["nom"], df.iloc[i]["prenom"], df.iloc[i]["id_patient"], df.iloc[i]["wilaya_patient"], df.iloc[i]["commune_patient"], df.iloc[i] ["age"],  df.iloc[i]['poid'], df.iloc[i]["taille"],  df.iloc[i]["sexe"],  df.iloc[i]["sympthomes"], 
                    df.iloc[i]["maladies"],df.iloc[i]["traitement"],df.iloc[i]["nb_jrs_depuis_derniere_sortie"],df.iloc[i]["nb_jrs_depuis_premiers_sympthomes"],
                    dat,nom,prenom,id,cov,orientation,gravite,specialite])
                except:
                    print("valleur de traitement:")
                    print(df.iloc[i]["traitement"])
            listes_consultation.append(i+1)
            reponse=input("voullez vous effectuez une autre consultation?\n1-oui\n2-non\n\t")
            #TODO:cas ou il n'y a plus de consultation
            print("le i : ",i)
            if reponse=="2":
                break
            print("-----------------------------------------------------------------------------------------------------------------------------")
            #supression infos de la fiche 
        self.supprimer_ligne(lignes=listes_consultation)
            #poser la question pour continuer ou pas



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
        liste1 =[]
        try:
            liste1 = liste_symp.split(",")
        except :
            if not isinstance(liste_symp, float):
                liste1.append(liste_symp) #cas ou il n'ya q'un seul sympthome

        for i in liste1:
            i = re.sub(r" |-", "_", i).lower()
            res = self.onto.search(iri="*sympthomes/"+i)
            if res== []:
                #créer l'objet sympthome
                symp = self.dico["Sympthomes"]()
                symp.iri = self.mon_iri+"sympthomes/"+i.lower()
                symp.nom_sympthome = i.lower()
                print("le sympthome ",symp.iri)
                pat.a_sympthomes.append(symp)
            elif res[0] not in pat.a_sympthomes: #pour ne pas avoir de repetition dans les sympthomes
                pat.a_sympthomes.append(res[0])        

    def ajout_maladies(self,liste_mala,pat):
        liste1 =[]
        try:
            liste1 = liste_mala.split(",")
        except :

            if not isinstance(liste_mala, float):
                liste1.append(liste_mala) #cas ou il n'ya q'un seul sympthome

        for i in liste1:
            i = re.sub(r" |-", "_", i)
            res = self.onto.search(iri="*maladies/"+i)
            if res== []:
                #créer l'objet sympthome
                mala = self.obtenir_objet("Maladies",i.lower())
                mala.nom_maladie = str(i)
                pat.a_maladie.append(mala)
            else:#l'objet existe
                pat.a_maladie.append(res[0])
    
    def ajout_traitements(self,liste_trait,pat):
        liste1 =[]
        try:
            liste1 = liste_trait.split(",")
        except:
            if not isinstance(liste_trait, float):
                liste1.append(liste_trait) #cas ou il n'ya q'un seul sympthome
        
        for i in liste1:
            i = re.sub(r" |-", "_", i)
            res = self.onto.search(iri="*traitements/"+i)
            if res== []:
                #créer l'objet sympthome
                trait = self.dico["Traitements"]()
                trait.iri = self.mon_iri+"traitements/"+i.lower()
                trait.nom_traitement = i.lower()
                pat.prend_traitement.append(trait)
            else:#l'objet existe
                pat.prend_traitement.append(res[0])

    def ajout_wilaya(self,wilaya,pat):
        wilaya=re.sub(r" |-", "_", wilaya).lower()
        wil_code = adresses_onto().get_code_wilaya(wilaya)
        print("wilaya: ",wilaya," son code:",wil_code)
        print("aaaaaaa:\n\n\n",self.onto.search(iri='*wilaya'+wil_code),"\n\n",type(wil_code))
        print("wil  ",self.onto.search(iri=self.mon_iri+"wilaya*"))
        wil = self.onto.search(iri="*wilaya"+wil_code+"*")[0]#on doit chercher la wilaya sauf aue cette derniere est encode avec son iri donc on va utiliser
        #print("type wil ",type(wil)) 
        pat.habite_wilaya= [wil]
    
    def ajout_commune(self,commune,pat):
        commune = re.sub(r" |-", "_", commune).lower()
        com_code = adresses_onto().get_code_commune(commune=commune)
        com = self.onto.search(iri='*'+com_code)[0]
        pat.habite_commune.append(com)

    def creer_patient(self,id,sexe,age,poid,taille,wilaya,commune,nb_jrs_depuis_derniere_sortie,nb_jrs_depuis_premiers_sympthomes,symptomes,maladies,traitements,gravite_sympthom,acovid,nom,prenom, consultation=None):

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
        p.sexe = sexe.lower()
        p.age = age
        p.poid = poid
        p.nb_jrs_depuis_derniere_sortie = nb_jrs_depuis_derniere_sortie
        p.nb_jrs_depuis_premiers_sympthomes = nb_jrs_depuis_premiers_sympthomes
        p.a_covid = acovid.lower()
        p.gravite_sympthome = re.sub(r" |-", "_",gravite_sympthom).lower() 
        p.nom =re.sub(r" |-", "_",nom).lower()
        p.prenom  =re.sub(r" |-", "_",prenom).lower() 

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
        liste1 =[]
        try:
            liste1 = maladie.split(",")
        except:
            if not isinstance(maladie, float):
                liste1.append(maladie) #cas ou il n'ya q'un seul sympthome

        
        if len(liste1)==1:
            mal= re.sub(r" |-", "_", liste1[0]).lower()
            m = self.obtenir_objet(nom_objet=mal,nom_classe="Maladies")
            m.nom_maladie = mal
            print("les sympthomes du patien sont: ",self.objet_patient.a_sympthomes)
            for i in self.objet_patient.a_sympthomes:
                i.est_sympthomes_maladie.append(m)

    def saisie_infos(self,ajouter=True):
        """
        ajouter : si vrai alors on ajoute a la fiche actuelle
        si faux alors on créer depuis le debut
        """
        print("------------------------------------------veiller donner vos informations------------------------------------------")
        nom = input("Nom: ")
        prenom = input("Prenom: ")
        id =  input("id: ")
        age =  input("age: ")
        poid = input("poid: ")
        taille =  input("taille: ")
        sexe = input("sexe: ")

        sympthomes = input("veillez saisir vos sympthomes avec une virgule entre chaque sympthomes:\n") 
        question = input("avez vous des maladies chroniques ou autres ?\n\ty: oui\n\tn:non\n ")
        if(question =="y"):  
            maladies = input("veillez saisir vos maladies avec une virgule entre chaque maladies si vous en avez plusieurs:\n")
        else :
            maladies=""
        question = input("prenez vous des traitements?\n\ty: oui\n\tn:non\n ")
        if question =="y":
            traitements= input("donner la liste des traitement que vous suivez actuellement:\n ")
        else:
            traitements=""
        nb_jour_depuis_dernier_sortie =  input("nombre de jour depuis derniére sortie: ")
        nb_jour_depuis_premier_sympthomes = input ("nombre de jour depuis premier sympthomes: ")
        commune = input("Commune: ")
        wilaya =  input('Wilaya: ')

        #creation de la fiche préliminaire a partir de sa!
        if not ajouter: 
            with open('fiche_preliminaire.csv', mode='w') as fiche0:
                patient_infos = csv.writer(fiche0, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                patient_infos.writerow(['nom', 'prenom', 'id_patient',"wilaya_patient","commune_patient", 'age', "poid", "taille", "sexe", "sympthomes", "maladies","traitement","nb_jrs_depuis_derniere_sortie","nb_jrs_depuis_premiers_sympthomes"])
                patient_infos.writerow([nom, prenom, id,wilaya,commune,age, poid,taille, sexe, sympthomes, maladies,traitements,nb_jour_depuis_dernier_sortie,nb_jour_depuis_premier_sympthomes])
        else:
             with open('fiche_preliminaire.csv', mode='a+') as fiche00:
                patient_infos1 = csv.writer(fiche00, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                patient_infos1.writerow([nom, prenom, id,wilaya,commune,age, poid,taille, sexe, sympthomes, maladies,traitements,nb_jour_depuis_dernier_sortie,nb_jour_depuis_premier_sympthomes])

        print("-----------------------------------------------------------------------------------------------------------------------------")



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

if __name__ == '__main__':
    #patient_onto().saisie_infos(False)
    #for i in range(2):
    #    patient_onto().saisie_infos(True)
    
    medecin_onto().crreation_header_fiche_final()
    medecin_onto().creation_fiche_final(fiche_preliminaire="fiche_preliminaire.csv")
