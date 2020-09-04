import xml.etree.ElementTree as ET
import csv
from constantes import ATTRIBIDENTIFIANTCALAMES, NIVEAUDEUX, NIVEAUTROIX, INPUTFILE, OUTPUTCALAMES, CODEROLEAUTEUR
from extract.extractCsvData import extractNormaliseDates, extractPhysfacet, extractRoleNormalPersname, extractTypeNormalGenreform



#-----------------------Creation du XML-EAD niveau C --------------------_#


racine = ET.Element("dsc")
def createLevel2():
    global cNiveau2, unitdateNiveau3, tuple, physfacetNiveau2
    cNiveau2 = ET.SubElement(racine, "c", level=NIVEAUDEUX, id=ATTRIBIDENTIFIANTCALAMES + ligne["coteNiveau2"])
    didNiveau2 = ET.SubElement(cNiveau2, "did")
    unitidNiveau2 = ET.SubElement(didNiveau2, "unitid", type="cote")
    unitidNiveau2.text = ligne["coteNiveau2"]
    unittitleNiveau2 = ET.SubElement(didNiveau2, "unittitle")
    unittitleNiveau2.text = ligne["TitreNiveau2"]

    # Dates
    if date2Debut and date2Fin:
        unitdate2Extreme = ET.SubElement(didNiveau2, "unitdate", calendar="gregorian", era="ce",
                                         normal=date2Debut + "/" + date2Fin)
        unitdate2Extreme.text = "du " + ligne["DateNiveau2Debut"] + " au " + ligne["DateNiveau2Fin"]

    elif date2Debut:
        unitdateNiveau2 = ET.SubElement(didNiveau2, "unitdate", calendar="gregorian", era="ce",
                                        normal=date2Debut)
        unitdateNiveau2.text = ligne["DateNiveau2Debut"]

    # Physfacet
    if pairPhysfacetType2 or ligne["extentNiveau2"] or ligne["dimensionNiveau2"]:
        physdescNiveau2 = ET.SubElement(didNiveau2, "physdesc")

        if pairPhysfacetType2:
            for tuple in pairPhysfacetType2:
                physfacetNiveau2 = ET.SubElement(physdescNiveau2, "physfacet", type=tuple[1].strip())
                physfacetNiveau2.text = tuple[0]

        # ajouter la condition d'existance, autrement, une balise vide est crée ce qui est rejeté par Calames
        if ligne["extentNiveau2"]:
            extentNiveau2 = ET.SubElement(physdescNiveau2, "extent")
            extentNiveau2.text = ligne["extentNiveau2"]

        if ligne["dimensionNiveau2"]:
            dimensionNiveau2 = ET.SubElement(physdescNiveau2, "dimensions")
            dimensionNiveau2.text = ligne["dimensionNiveau2"]

    # Scopecontent: descripion du contenu
    if ligne["scopecontentNiveau2"]:
        scopecontentNiveau2 = ET.SubElement(cNiveau2, "scopecontent")
        paragrapheNiv2 = ET.SubElement(scopecontentNiveau2, "p")
        paragrapheNiv2.text = ligne["scopecontentNiveau2"]

    # ---------CONTROLACCESS -----------
    if ligne["corpnameNiveau2"]:
        controlaccesNiveau2 = ET.SubElement(cNiveau2, "controlaccess")

        # corpname
        corpnameNiveau2 = ET.SubElement(controlaccesNiveau2, "corpname", normal=ligne["corpnameNiveau2"])

        if ligne["roleCorpname2"] in CODEROLEAUTEUR:
            roleC2 = CODEROLEAUTEUR.get(ligne["roleCorpname2"])
            corpnameNiveau2.set("role", roleC2)
        else:
            corpnameNiveau2.set("role", ligne["roleCorpname2"])
            print("Attention, le rôle pour cette Organisation n'a pas de code ", ligne["CoteNiveau2"])

        if idrefcorpname2:
            corpnameNiveau2.set("id", idrefcorpname2)
            corpnameNiveau2.text = ligne["idrefcorpname2"]
        else:
            corpnameNiveau2.text = ligne["corpnameNiveau2"]

        corpnameNiveau2.text = ligne["corpnameNiveau2"]

    #genreform
    if pairTypeNormalGenreform2:

        for tuple in pairTypeNormalGenreform2:
            controlaccesNiveau2 = ET.SubElement(cNiveau2, "controlaccess")
            genreformNiveau2 = ET.SubElement(controlaccesNiveau2, "genreform", type=tuple[0].strip(),
                                             normal=tuple[1].strip())
            # par défaut imposé par Calames : la valeur de l'attribut normal
            genreformNiveau2.text = tuple[1].strip()



def createLevel3():
    global cNiveau3, didNiveau3, unitidNiveau3, unittitleNiveau3, unitdateExtreme, unitdateNiveau3, physdescNiveau3, tuple, physfacetNiveau2, extentNiveau3, dimensionNiveau3, scopecontentNiveau3, paragrapheNiv3, person, controlaccesNiveau3, persnameNiveau3, role, corpnameNiveau3, roleC3, geognameNiveau3, subjectNiveau3, genreformNiveau3

    cNiveau3 = ET.SubElement(cNiveau2, "c", level=NIVEAUTROIX, id=ATTRIBIDENTIFIANTCALAMES + ligne["CoteNiveau3"])
    didNiveau3 = ET.SubElement(cNiveau3, "did")
    unitidNiveau3 = ET.SubElement(didNiveau3, "unitid", type="cote")
    unitidNiveau3.text = ligne["CoteNiveau3"].strip()
    unittitleNiveau3 = ET.SubElement(didNiveau3, "unittitle")
    unittitleNiveau3.text = ligne["TitreNiveau3"].strip()

    ###-------DATES ---------------###

    # si les dates de debut et de fin niveau2 et 3 sont identiques et que les champs dates ne sont pas vides, alerte répétition. utilisation des dates normalisées dans les conditions. utilisation des dates saisies pour l'affichage dans calames
    if date2Debut != "" and date3Debut != "" and date2Debut == date3Debut and date2Fin==date3Fin:
        print("ATTENTION LES DATES DU NIVEAU 2 ET 3 se répetent: ", ligne["CoteNiveau3"])

    # si la date niveau 2 est vide et celle de niveau 3 existe, prendre celle du niveau3
    elif date2Debut == "" and date3Debut:

        # s'il y a une date3 de debut et une de fin mettre les dates3 extremes
        if date3Debut and date3Fin:
            unitdateExtreme = ET.SubElement(didNiveau3, "unitdate", calendar="gregorian", era="ce",
                                            normal=date3Debut + "/" + date3Fin)
            unitdateExtreme.text = "du " + ligne["DateNiveau3Debut"] + " au " + ligne["DateNiveau3Fin"]
        # sinon, prendre que la date3 du début
        else:
            unitdateNiveau3 = ET.SubElement(didNiveau3, "unitdate", calendar="gregorian", era="ce", normal=date3Debut)
            unitdateNiveau3.text = ligne["DateNiveau3Debut"]

    # si la date de niveau 3 existe (peu importe si celle de niveau 2 exite)
    elif date3Debut :
        unitdateNiveau3 = ET.SubElement(didNiveau3, "unitdate", calendar="gregorian", era="ce", normal=date3Debut)
        unitdateNiveau3.text = ligne["DateNiveau3Debut"]

    # si les dates 2 et 3 sont vides, lancer une alerte
    elif date2Debut == "" and date3Debut == "":
        print ("ATTENTION, la date manque ou elle est décrite au niveau Archdesc pour cette ressource : ", ligne["CoteNiveau3"].strip())

    ###-------PHYSFACET, EXTENT, DIMENSION ---------------###

    if pairPhysfacetType2 is None and pairPhysfacetType3 or ligne["extentNiveau3"]:
        physdescNiveau3 = ET.SubElement(didNiveau3, "physdesc")

        for tuple in pairPhysfacetType3:
            physfacetNiveau2 = ET.SubElement(physdescNiveau3, "physfacet", type=tuple[1].strip())
            physfacetNiveau2.text = tuple[0]

        if ligne["extentNiveau3"]:
            extentNiveau3 = ET.SubElement(physdescNiveau3, "extent")
            extentNiveau3.text = ligne["extentNiveau3"]

        if ligne["dimensionNiveau3"]:
            dimensionNiveau3 = ET.SubElement(physdescNiveau3, "dimensions")
            dimensionNiveau3.text = ligne["dimensionNiveau3"]

    ###-------SCOPCONTENT ---------------###

    if ligne["scopecontentNiveau2"] is None and ligne["scopecontentNiveau3"]:
        scopecontentNiveau3 = ET.SubElement(cNiveau3, "scopecontent")
        paragrapheNiv3 = ET.SubElement(scopecontentNiveau3, "p")
        paragrapheNiv3.text = ligne["scopecontentNiveau3"]


    # ---------CONTROLACCESS Niveau 3 ---------

    # PERSNAME

    for tuple in pairRoleIdrefPersname3:
        if tuple [0] != "anonyme":

            controlaccesNiveau3 = ET.SubElement(cNiveau3, "controlaccess")
            # si le tuple est composé de deux éléments (persname et role), créer uniquement @role. @normal existe par défaut
            if len (tuple) == 2:
                persnameNiveau3 = ET.SubElement(controlaccesNiveau3, "persname", role = tuple[1].strip(), normal = tuple[0].strip())
                persnameNiveau3.text = tuple[0].strip()

            # si le tuple est composé de trois éléments (persname, role, idref), créer @role, @id. @normal existe par défaut
            elif len(tuple) == 3:

                persnameNiveau3 = ET.SubElement(controlaccesNiveau3, "persname", role=tuple[1].strip(), normal= tuple[0].strip())
                # @ idref peut être vide, pas rensignée, donc, ne pas afficher @id.

                if tuple [2].strip() != "":
                    persnameNiveau3.set("id", "https://www.idref.fr/"+tuple[2].strip())
                    persnameNiveau3.text = tuple[0].strip()
                else:
                    persnameNiveau3.text = tuple[0].strip()

    #CORPNAME

    if ligne["corpnameNiveau3"]:
        if ligne["corpnameNiveau3"] != "collectif":

            controlaccesNiveau3 = ET.SubElement(cNiveau3, "controlaccess")
            corpnameNiveau3 = ET.SubElement(controlaccesNiveau3, "corpname", normal=ligne["corpnameNiveau3"])

            if ligne["roleCorpname3"] in CODEROLEAUTEUR:
                roleC3 = CODEROLEAUTEUR.get(ligne["roleCorpname3"])
                corpnameNiveau3.set("role", roleC3)
            else:
                corpnameNiveau3.set("role", ligne["roleCorpname3"])
                print("Attention, le rôle pour cette Organisation n'a pas de code ", ligne["CoteNiveau3"])

            if idrefcorpname3:
                corpnameNiveau3.set("id", idrefcorpname3)
                corpnameNiveau3.text = ligne["idrefcorpname3"]
            else:
                corpnameNiveau3.text = ligne["corpnameNiveau3"]

            corpnameNiveau3.text = ligne["corpnameNiveau3"]

    if ligne["geognameNiveau3"]:
        controlaccesNiveau3 = ET.SubElement(cNiveau3, "controlaccess")
        geognameNiveau3 = ET.SubElement(controlaccesNiveau3, "geogname")
        geognameNiveau3.text = ligne["geognameNiveau3"]

    if ligne["subjectNiveau3"]:
        controlaccesNiveau3 = ET.SubElement(cNiveau3, "controlaccess")
        subjectNiveau3 = ET.SubElement(controlaccesNiveau3, "subject")
        subjectNiveau3.text = ligne["subjectNiveau3"]


    # GENREFORM
    if pairTypeNormalGenreform3:
        for tuple in pairTypeNormalGenreform3:
            controlaccesNiveau3 = ET.SubElement(cNiveau3, "controlaccess")
            genreformNiveau3 = ET.SubElement(controlaccesNiveau3, "genreform", type=tuple[0].strip(),
                                             normal=tuple[1].strip())
            # par défaut imposé par Calames : la valeur de l'attribut normal
            genreformNiveau3.text = tuple[1].strip()

    # --------DAO depuis NAKALA--------#
    #if ligne["accessEmail"] == "":
       # dao = ET.SubElement(cNiveau3, "dao")
       # dao.set("href", "https://www.nakala.fr/nakala/data/"+ ligne["handle"])



# le lancement du parsing du fichier csv et l'application des méthodes pour générer les niveaux c
with open(INPUTFILE, "r") as fichiercsv:
    reader = csv.DictReader(fichiercsv, delimiter =",")

    # initialisation de la variable niveau2 à vide
    niveau2 = ""

    for ligne in reader:


        # -------Normaliser les dates avec la méthode extractNormaliseDates--------#

        date2Debut = extractNormaliseDates(ligne["DateNiveau2Debut"])
        date2Fin = extractNormaliseDates(ligne["DateNiveau2Fin"])

        date3Debut = extractNormaliseDates(ligne["DateNiveau3Debut"])
        date3Fin = extractNormaliseDates(ligne["DateNiveau3Fin"])


        # -------------PERSNAME : Récupérer les roles, idref, pêrsname niveaux 3 avec la metdode extractRoleNormalPersname -----

        pairRoleIdrefPersname3 = extractRoleNormalPersname(ligne["persnameNiveau3"], ligne["rolePersname3"], ligne["idrefpersname3"], ligne["CoteNiveau3"], CODEROLEAUTEUR)
        #print(pairRoleIdrefPersname3)


        #--------CORPNAME: Normaliser les noms d'organisations -------#


        idrefcorpname2 = ""
        if ligne["idrefcorpname2"] != "":
            idrefcorpname2 = "https://www.idref.fr/" + ligne["idrefcorpname2"]

        idrefcorpname3 =""
        if ligne["idrefcorpname3"] != "":
            idrefcorpname3 = "https://www.idref.fr/" + ligne["idrefcorpname3"]


        #-------------Extraire le PHYSFACET et le PhystfacetType avec la méthode extractPhysfacet--------------#

        pairPhysfacetType2 = extractPhysfacet(ligne["physfacetNiveau2"], ligne["typePhysfacet2"], ligne["coteNiveau2"], ligne["TitreNiveau2"])
        pairPhysfacetType3 = extractPhysfacet(ligne["physfacetNiveau3"], ligne["typePhysfacet3"], ligne["CoteNiveau3"], ligne["TitreNiveau3"])

        # -------------Extraire le GENREFORM: typeGenreform et le normalGenreform avec la methode extractTypeNormalGenreform --------------#

        pairTypeNormalGenreform2 = extractTypeNormalGenreform (ligne["typeGenreform2"],ligne["normalGenreform2"], ligne["coteNiveau2"], ligne["TitreNiveau2"])
        pairTypeNormalGenreform3 = extractTypeNormalGenreform (ligne["typeGenreform3"],ligne["normalGenreform3"], ligne["CoteNiveau3"], ligne["TitreNiveau3"])





            # ======== Générer les NIVEAU 2 + Niveau 3 ==========#

        if ligne["coteNiveau2"] != niveau2:

            createLevel2()

            # ======== NIVEAU 3 ==========#

            # appel de la méthode extractLevel3
            createLevel3()

            niveau2 = ligne["coteNiveau2"]


#---------------------------Niveau 3 intégré dans le même niveau 2 ------------
        else:
            # appel de la méthode extractLevel3
            createLevel3()

        tree = ET.ElementTree(racine)
        tree.write(OUTPUTCALAMES, encoding="UTF-8")