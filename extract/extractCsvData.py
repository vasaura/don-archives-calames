import datetime
from datetime import datetime
import re

def extractNormaliseDates (dateNiveau):
    """
    Fonction qui extrait les dates rensignées sous ce format: 27-10-2017
    :param dateNiveau: str colonne dane
    :return: str la date en format normalisée
    """
    date = dateNiveau
    # si la date est sous la forme de AAAA
    if len(date) == 4:
        datenorm = date
    # si la date est sous la forme de AAAA-MM
    elif len(date) == 7 and "/" in date:
        datenorm = str(datetime.strptime(date, "%m%Y"))[:7]
    elif len(date) == 10 and "s.d" not in date and "/" in date :
        datenorm = str(datetime.strptime(date, "%d-%m-%Y"))[:10]
    elif "s.d" in date:
        dateTestObject = re.search( "[0-9]{4}", date)
        datenorm = dateTestObject.group(0)
    else :
        datenorm = date
    return datenorm


def extractPhysfacet (physfacet, typepysfacet, titre, cote):

    # Element PHYSFACET
    listePhysfacet = []

    if physfacet:
        listePhysfacet = physfacet.split(";")

    # attribut PhystfacetType
    listeTypePhysfacet = []

    if typepysfacet:
        listeTypePhysfacet = typepysfacet.split(";")

    if len(listePhysfacet) != len(listeTypePhysfacet):
        print("ATTENTION, @type pour physfacet manque pour cette ressource: ", titre, cote)

    pairPhysfacetType = []
    for pair in zip(listePhysfacet, listeTypePhysfacet):
        pairPhysfacetType.append(pair)

    return pairPhysfacetType



def extractTypeNormalGenreform(typeG, normalG, cote, titre):
    #typeGenreform

    listetypeGenreform = []
    if typeG:
        listetypeGenreform = typeG.split(";")

    listeNormalGenrform =[]
    if normalG:
        listeNormalGenrform = normalG.split(";")

    if len (listetypeGenreform) != len(listeNormalGenrform):
        print("ATTENTION, la balise genreforme ou les @type ou @normal manquent pour cette ressources: ", cote, titre)

    pairTypeNormalGenreform =[]
    for couple in zip(listetypeGenreform, listeNormalGenrform):
        pairTypeNormalGenreform.append(couple)

    return pairTypeNormalGenreform



def extractRoleNormalPersname (persame, role, idref, cote3, codeRoleAuteurs):
    """
    fonction qui extraire le nom, le role et/ou le idref des colonnes du fichier
    csv de métadonnées Calames et Nakala
    :param persame: le nom de la personne sous forme de list
    :param role: le rôle sous forme de list
    :param idref: le idref sous forme de list
    :param cote3: la côte du niveau sous forme de str
    :param codeRoleAuteurs: le couple code:role de Calames sous forme de dictionnaire
    :return: une liste de tuples contenant soit (nom, role) soit (nom, role, idref)
    """

    # séparer les noms des personnes du champ persname sur le  ";" et récupérer les noms dans une liste
    listPersnameNiveau3 = []
    if persame:
        listPersnameNiveau3 = persame.split(";")

    # définnir une liste pour enregistrer les codes Calames des roles.
    listCodeRolepersname3 = []
    #si le champs rolePersname3 existe
    if role :
        # séparer les roles sur le  ";" et les récupérer dans une liste
        listRolepersname3 = role.split(";")
        # itérer sur la liste des roles saisis et vérifier que le rôle est dans le dictionnaire des codes
        for role in listRolepersname3:
            if role in codeRoleAuteurs:
                code = codeRoleAuteurs.get(role)
                # ajouter le code à la liste listCodeRolepersname3
                listCodeRolepersname3.append(code)
    #print(listCodeRolepersname3, cote3)

    # séparer les idref des personnes sur le  ";" et récupérer les identifiants dans une liste
    listIdrefpersname3 = []
    if idref :
        listIdrefpersname3 = idref.split(";")
    #print (listIdrefpersname3, cote3)

    # si la liste des rôle et celle des personnes est différentes
    # il vaut vérifier que chaque auteur a son role (obligatoire pour Calames)
    if len(listPersnameNiveau3) !=  len(listCodeRolepersname3):
        print("ATTENTION, @role obligatoire pour le persname ", cote3)

    # si le champs idref est vide, il faut constituer une liste de tuple : nom; role
    pairRoleIdrefPersname3 = []
    if not listIdrefpersname3 :
        for couple in zip(listPersnameNiveau3, listCodeRolepersname3):
            pairRoleIdrefPersname3.append(couple)

    # si le champs idref a du contenu (y compris contenu vide type "",
    # constituer  une liste avec le tuple : nom, role, idref
    else:
        for tuple in zip(listPersnameNiveau3, listCodeRolepersname3, listIdrefpersname3):
            pairRoleIdrefPersname3.append(tuple)

    return pairRoleIdrefPersname3

