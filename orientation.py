from enrichissement import traitemnt_onto,adresses_onto
import datetime
import re

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

    def ajouter_hopital(self,hopital,patient):
        """
        hopital : nom de l'hopital 
        patient : objet patient pour extraire la wilaya ect
        """
        hopital= re.sub(r" |-", "_", hopital).lower()#remplace tout les espaces et - avec _ 
        res =  self.objet_existe("Hopital",hopital.lower())

        if not res :#objet n'existe pas on le crée
            h = self.dico['Hopital']()
            h.nom_hopital =  hopital.lower()
            h.iri = self.mon_iri+"hopital/"+hopital.lower()
            wil_code = adresses_onto().get_code_wilaya(patient.habite_wilaya[0].nomWilaya)
            wil = self.onto.search(iri='*wilaya'+wil_code)[0]#on doit chercher la wilaya sauf aue cette derniere est encode avec son iri donc on va utilise          
            h.wilaya_hopitale.append(wil)
        else:
            h = res    
        self.objet_orientation.orienter_vers_hopital  = [h]
        patient.est_hospitalilser_a = [h]
        print("\n\n patient hospitallise: ", patient.est_hospitalilser_a[0].nom_hopital )
        pass

    def creer_orientation(self, orient,patient=None):
        """args
           orient : type d'orientation :prise en charge domicile ou hopital ou bien prise de rdv
           date_rdv: date de rendez vous dans le cas d'une prise de rendez vous jour/mois/annee
           patient : objet patient qui nous sera utile dans le cas ou il y'a prise en charge hopital 
           hopital : on a besoin du nom de l'hopital ou il sait diriger
        on vas créer les objets nécessaire en l'occurence orientation et rdv si nécessaire et ajouter les relations  
        """
        
        #patient = self.onto.search(iri=mon_iri + "patient" + str(id_patient))[0]
        #medecin = self.onto.search(iri=mon_iri + "medecin" + str(id_medecin))[0]
        orient = orient.split(":")
        orient[0]=  re.sub(r" |-", "_",orient[0]).lower()
        o = self.dico["Orientation"]()
        self.objet_orientation = o
        print()

        if (orient[0] == "prise_en_charge_domicile"):
            o.type_orientation = orient[0]  

        if (orient[0] == "prise_de_rendez_vous" and len(orient)>1 ): 
            o.type_orientation = orient[0]         
            date_rdv = orient[1]
            r = self.dico["RDV"]()
            #on va créer un objet de type datetime et l'inputer directement ?           
            tabdate=date_rdv.split("/") #la on devrait obtenir un tableau de 3 elements date mois et anee           
            r.date_rendez_vous= datetime.date(int(tabdate[2]),int(tabdate[1]),int(tabdate[0]))
            #print(r.date_rendez_vous)  donne cette sortie 2026-06-24 pour la date 24/06/2026
            o.prend_RDV.append(r)

            # heu du coup pour la date du rdv et les infos des hopitaux je sais pas trop how to do it 

        if (orient[0] == "prise_en_charge_hopital" and (patient !=None) and len(orient)>1):
            o.type_orientation = orient[0]          
            #la faut chercher si l'hopital existe ou pas! on suppose que les iri des opitaux contiendrons le nom des hopitaux (hopitalX/nomhopitale)
            
            #on va vérifier si l'hopital existe sinon on le crée , le probléme c'est qu'il faut savoir ou il se situe, 
            #on pourrait supposer que cela dépend tu patient, donc on vas tout simplement avoir en entrée aussi l'adresse du patient, ou plus simple l'objet patient 
            #lui meme 
            self.ajouter_hopital(hopital=orient[1],patient=patient)

        self.objet_orientation = o
