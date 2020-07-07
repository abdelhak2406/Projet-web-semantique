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
        m.nom = re.sub(r" |-", "_",nom).lower()
        m.prenom = re.sub(r" |-", "_",prenom).lower()
        m.sexe = sexe.lower()
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
        liste1 = liste_trait.split(",")
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
        wil_code = adresses_onto().get_code_wilaya(wilaya)
        wil = self.onto.search(iri='*wilaya'+wil_code)[0]#on doit chercher la wilaya sauf aue cette derniere est encode avec son iri donc on va utiliser
        print("wil  ",wil)
        #print("type wil ",type(wil)) 
        pat.habite_wilaya= [wil]
    
    def ajout_commune(self,commune,pat):
        com_code = adresses_onto().get_code_commune(commune=commune)
        com = self.onto.search(iri='*'+com_code)[0]
        pat.habite_commune.append(com)

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
        p.sexe = sexe.lower()
        p.age = age
        p.poid = poid
        p.nb_jrs_depuis_derniere_sortie = nb_jrs_depuis_derniere_sortie
        p.nb_jrs_depuis_premiers_sympthomes = nb_jrs_depuis_premiers_sympthomes
        
        p.gravite_sympthome = re.sub(r" |-", "_",gravite_sympthom).lower() 
        
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
            m.nom_maladie = mal
            print("les sympthomes du patien sont: ",self.objet_patient.a_sympthomes)
            for i in self.objet_patient.a_sympthomes:
                i.est_sympthomes_maladie.append(m)



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