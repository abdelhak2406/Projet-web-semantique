mon_iri = "https://projetWebsem.org/ontologie.owl#"

wilayas = pd.read_csv('wilaya.csv')

for i in range(len(wilayas)):
    w = Wilaya()
    nom_w = wilayas.iloc[i]['nom']
    code_w = wilayas.iloc[i]['code'].tolist()
    w.nomWilaya = nom_w
    w.idWilaya = code_w
    w.iri =  mon_iri + "wilaya" + str(code_w)


communes = pd.read_csv('communes.csv')

for i in range(len(communes)):

    c = Commune()
    nom_c = communes.iloc[i]['nom']
    c.nomCommune = nom_c
    code_c = communes.iloc[i]['code_postal']
    wilaya_liée = communes.iloc[i]['wilaya_id'].tolist()
   
     # code postal se compose de 5 chiffres so ceux qui ont 4 c le 0 qui a été retiré donc on doit l remettre
    if (len(str(code_c)) == 4 ):
        c.iri = mon_iri + "commune" + "0" + str(code_c)
    else:
        c.iri = mon_iri + "commune" + str(code_c) 

     # lier chaque commune avc sa wilaya
    c.commune_de.append(onto.search(iri= mon_iri + "wilaya" + str(wilaya_liée))[0])
