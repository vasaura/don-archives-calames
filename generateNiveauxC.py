import xml.etree.ElementTree as ET
import csv
from constantes import ATTRIBIDENTIFIANTCALAMES, INPUTFILE, OUTPUTCALAMES, CODEROLEAUTEUR
from extract.extractCsvData import extractNormaliseDates, extractPhysfacet, extractRoleNormalPersname, extractTypeNormalGenreform



#-----------------------Creation du XML-EAD niveau C --------------------_#


racine = ET.Element("dsc")
def createLevel2():
    global cNiveau2, unitdateNiveau3, tuple, physfacetNiveau2
    cNiveau2 = ET.SubElement(racine, "c", level=ligne["levelNiveau2"], id=ATTRIBIDENTIFIANTCALAMES + ligne["coteNiveau2"])
    didNiveau2 = ET.SubElement(cNiveau2, "did")
    unitidNiveau2 = ET.SubElement(didNiveau2, "unitid", type="cote")
    unitidNiveau2.text = ligne["coteNiveau2"]
    unittitleNiveau2 = ET.SubElement(didNiveau2, "unittitle")
    unittitleNiveau2.text = ligne["titreNiveau2"]

    # Dates
    if date2Debut and date2Fin:
        unitdate2Extreme = ET.SubElement(didNiveau2, "unitdate", calendar="gregorian", era="ce",
                                         normal=date2Debut + "/" + date2Fin)
        unitdate2Extreme.text = "du " + ligne["dateNiveau2Debut"] + " au " + ligne["dateNiveau2Fin"]

    elif date2Debut:
        unitdateNiveau2 = ET.SubElement(didNiveau2, "unitdate", calendar="gregorian", era="ce",
                                        normal=date2Debut)
        unitdateNiveau2.text = ligne["dateNiveau2Debut"]

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
            print("Attention, le rôle pour cette Organisation n'a pas de code ", ligne["coteNiveau2"])

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

    cNiveau3 = ET.SubElement(cNiveau2, "c", level=ligne["levelNiveau3"], id=ATTRIBIDENTIFIANTCALAMES + ligne["coteNiveau3"])
    didNiveau3 = ET.SubElement(cNiveau3, "did")
    unitidNiveau3 = ET.SubElement(didNiveau3, "unitid", type="cote")
    unitidNiveau3.text = ligne["coteNiveau3"].strip()
    unittitleNiveau3 = ET.SubElement(didNiveau3, "unittitle")
    unittitleNiveau3.text = ligne["titreNiveau3"].strip()

    ###-------DATES ---------------###

    # si les dates de debut et de fin niveau2 et 3 sont identiques et que les champs dates ne sont pas vides, alerte répétition. utilisation des dates normalisées dans les conditions. utilisation des dates saisies pour l'affichage dans calames
    if date2Debut != "" and date3Debut != "" and date2Debut == date3Debut and date2Fin==date3Fin:
        print("ATTENTION LES DATES DU NIVEAU 2 ET 3 se répetent: ", ligne["coteNiveau3"])

    # si la date niveau 2 est vide et celle de niveau 3 existe, prendre celle du niveau3
    elif date2Debut == "" and date3Debut:

        # s'il y a une date3 de debut et une de fin mettre les dates3 extremes
        if date3Debut and date3Fin:
            unitdateExtreme = ET.SubElement(didNiveau3, "unitdate", calendar="gregorian", era="ce",
                                            normal=date3Debut + "/" + date3Fin)
            unitdateExtreme.text = "du " + ligne["dateNiveau3Debut"] + " au " + ligne["dateNiveau3Fin"]
        # sinon, prendre que la date3 du début
        else:
            unitdateNiveau3 = ET.SubElement(didNiveau3, "unitdate", calendar="gregorian", era="ce", normal=date3Debut)
            unitdateNiveau3.text = ligne["dateNiveau3Debut"]

    # si la date de niveau 3 existe (peu importe si celle de niveau 2 exite)
    elif date3Debut :
        unitdateNiveau3 = ET.SubElement(didNiveau3, "unitdate", calendar="gregorian", era="ce", normal=date3Debut)
        unitdateNiveau3.text = ligne["dateNiveau3Debut"]

    # si les dates 2 et 3 sont vides, lancer une alerte
    elif date2Debut == "" and date3Debut == "":
        print ("ATTENTION, la date manque ou elle est décrite au niveau supérieur pour cette ressource : ", ligne["coteNiveau3"].strip())

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

def createLevel4():
    global cNiveau4, didNiveau4, unitidNiveau4, unittitleNiveau4, unitdateExtreme4, unitdateNiveau4, physdescNiveau4, tuple, physfacetNiveau3, extentNiveau4, dimensionNiveau4, scopecontentNiveau4, paragrapheNiv4, person, controlaccesNiveau4, persnameNiveau4, role, corpnameNiveau4, roleC4, geognameNiveau4, subjectNiveau4, genreformNiveau4

    cNiveau4 = ET.SubElement(cNiveau3, "c", level=ligne["levelNiveau3"], id=ATTRIBIDENTIFIANTCALAMES + ligne["coteNiveau4"])
    didNiveau4 = ET.SubElement(cNiveau4, "did")
    unitidNiveau4 = ET.SubElement(didNiveau4, "unitid", type="cote")
    unitidNiveau4.text = ligne["coteNiveau4"].strip()
    unittitleNiveau4 = ET.SubElement(didNiveau4, "unittitle")
    unittitleNiveau4.text = ligne["titreNiveau4"].strip()

    ###-------DATES ---------------###

    # si les dates de debut et de fin niveau2 et 3 sont identiques et que les champs dates ne sont pas vides, alerte répétition. utilisation des dates normalisées dans les conditions. utilisation des dates saisies pour l'affichage dans calames
    if date3Debut != "" and date4Debut != "" and date3Debut == date4Debut and date3Fin==date4Fin:
        print("ATTENTION LES DATES DU NIVEAU 3 ET 4 se répetent: ", ligne["coteNiveau4"])

    # si la date niveau 3 est vide et celle de niveau 4 existe, prendre celle du niveau4
    elif date3Debut == "" and date4Debut:

        # s'il y a une date3 de debut et une de fin mettre les dates3 extremes
        if date4Debut and date4Fin:
            unitdateExtreme4 = ET.SubElement(didNiveau4, "unitdate", calendar="gregorian", era="ce",
                                            normal=date4Debut + "/" + date3Fin)
            unitdateExtreme4.text = "du " + ligne["dateNiveau4Debut"] + " au " + ligne["dateNiveau4Fin"]
        # sinon, prendre que la date3 du début
        else:
            unitdateNiveau4 = ET.SubElement(didNiveau4, "unitdate", calendar="gregorian", era="ce", normal=date4Debut)
            unitdateNiveau4.text = ligne["dateNiveau4Debut"]

    # si la date de niveau 3 existe (peu importe si celle de niveau 2 exite)
    elif date4Debut :
        unitdateNiveau4 = ET.SubElement(didNiveau4, "unitdate", calendar="gregorian", era="ce", normal=date4Debut)
        unitdateNiveau4.text = ligne["dateNiveau4Debut"]

    # si les dates 3 et 4 sont vides, lancer une alerte
    elif date3Debut == "" and date4Debut == "":
        print ("ATTENTION, la date manque ou elle est décrite au niveau supérieur pour cette ressource : ", ligne["coteNiveau4"].strip())

    ###-------PHYSFACET, EXTENT, DIMENSION ---------------###

    if pairPhysfacetType3 is None and pairPhysfacetType4 or ligne["extentNiveau4"]:
        physdescNiveau4 = ET.SubElement(didNiveau4, "physdesc")

        for tuple in pairPhysfacetType4:
            physfacetNiveau3 = ET.SubElement(physdescNiveau4, "physfacet", type=tuple[1].strip())
            physfacetNiveau3.text = tuple[0]

        if ligne["extentNiveau4"]:
            extentNiveau4 = ET.SubElement(physdescNiveau4, "extent")
            extentNiveau4.text = ligne["extentNiveau4"]

        if ligne["dimensionNiveau4"]:
            dimensionNiveau4 = ET.SubElement(physdescNiveau4, "dimensions")
            dimensionNiveau4.text = ligne["dimensionNiveau4"]

    ###-------SCOPCONTENT ---------------###

    if ligne["scopecontentNiveau3"] is None and ligne["scopecontentNiveau4"]:
        scopecontentNiveau4 = ET.SubElement(cNiveau4, "scopecontent")
        paragrapheNiv4 = ET.SubElement(scopecontentNiveau4, "p")
        paragrapheNiv4.text = ligne["scopecontentNiveau4"]


    # ---------CONTROLACCESS Niveau 3 ---------

    # PERSNAME

    for tuple in pairRoleIdrefPersname4:
        if tuple [0] != "anonyme":

            controlaccesNiveau4 = ET.SubElement(cNiveau4, "controlaccess")
            # si le tuple est composé de deux éléments (persname et role), créer uniquement @role. @normal existe par défaut
            if len (tuple) == 2:
                persnameNiveau4 = ET.SubElement(controlaccesNiveau4, "persname", role = tuple[1].strip(), normal = tuple[0].strip())
                persnameNiveau4.text = tuple[0].strip()

            # si le tuple est composé de trois éléments (persname, role, idref), créer @role, @id. @normal existe par défaut
            elif len(tuple) == 3:

                persnameNiveau4 = ET.SubElement(controlaccesNiveau4, "persname", role=tuple[1].strip(), normal= tuple[0].strip())
                # @ idref peut être vide, pas rensignée, donc, ne pas afficher @id.

                if tuple [2].strip() != "":
                    persnameNiveau4.set("id", tuple[2].strip())
                    persnameNiveau4.text = tuple[0].strip()
                else:
                    persnameNiveau4.text = tuple[0].strip()

    #CORPNAME

    if ligne["corpnameNiveau4"]:
        if ligne["corpnameNiveau4"] != "collectif":

            controlaccesNiveau4 = ET.SubElement(cNiveau4, "controlaccess")
            corpnameNiveau4 = ET.SubElement(controlaccesNiveau4, "corpname", normal=ligne["corpnameNiveau4"])

            if ligne["roleCorpname4"] in CODEROLEAUTEUR:
                roleC4 = CODEROLEAUTEUR.get(ligne["roleCorpname4"])
                corpnameNiveau4.set("role", roleC4)
            else:
                corpnameNiveau4.set("role", ligne["roleCorpname4"])
                print("Attention, le rôle pour cette Organisation n'a pas de code ", ligne["coteNiveau4"])

            if idrefcorpname4:
                corpnameNiveau4.set("id", idrefcorpname4)
                corpnameNiveau4.text = ligne["idrefcorpname4"]
            else:
                corpnameNiveau4.text = ligne["corpnameNiveau4"]

            corpnameNiveau4.text = ligne["corpnameNiveau4"]

    if ligne["geognameNiveau4"]:
        controlaccesNiveau4 = ET.SubElement(cNiveau4, "controlaccess")
        geognameNiveau4 = ET.SubElement(controlaccesNiveau4, "geogname")
        geognameNiveau4.text = ligne["geognameNiveau4"]

    if ligne["subjectNiveau4"]:
        controlaccesNiveau4 = ET.SubElement(cNiveau4, "controlaccess")
        subjectNiveau4 = ET.SubElement(controlaccesNiveau4, "subject")
        subjectNiveau4.text = ligne["subjectNiveau4"]


    # GENREFORM
    if pairTypeNormalGenreform4:
        for tuple in pairTypeNormalGenreform4:
            controlaccesNiveau4 = ET.SubElement(cNiveau4, "controlaccess")
            genreformNiveau4 = ET.SubElement(controlaccesNiveau4, "genreform", type=tuple[0].strip(),
                                             normal=tuple[1].strip())
            # par défaut imposé par Calames : la valeur de l'attribut normal
            genreformNiveau4.text = tuple[1].strip()

# le lancement du parsing du fichier csv et l'application des méthodes pour générer les niveaux c
with open(INPUTFILE, "r") as fichiercsv:
    reader = csv.DictReader(fichiercsv, delimiter =",")

    # initialisation de la variable niveau2 à vide
    niveau2 = ""
    # initialisation de la variable niveau3 à vide
    niveau3 = ""

    for ligne in reader:


        # -------Normaliser les dates avec la méthode extractNormaliseDates--------#

        date2Debut = extractNormaliseDates(ligne["dateNiveau2Debut"])
        date2Fin = extractNormaliseDates(ligne["dateNiveau2Fin"])

        date3Debut = extractNormaliseDates(ligne["dateNiveau3Debut"])
        date3Fin = extractNormaliseDates(ligne["dateNiveau3Fin"])

        date4Debut = extractNormaliseDates(ligne["dateNiveau4Debut"])
        date4Fin = extractNormaliseDates(ligne["dateNiveau4Fin"])


        # -------------PERSNAME : Récupérer les roles, idref, pêrsname niveaux 4 avec la metdode extractRoleNormalPersname -----
        if ligne["persnameNiveau4"]:
            pairRoleIdrefPersname4 = extractRoleNormalPersname(ligne["persnameNiveau4"], ligne["rolePersname4"],
                                                               ligne["idrefpersname4"], ligne["coteNiveau4"],
                                                               CODEROLEAUTEUR)

        #--------CORPNAME: Normaliser les noms d'organisations -------#

        idrefcorpname2 = ""
        if ligne["idrefcorpname2"] != "":
            idrefcorpname2 = ligne["idrefcorpname2"]

        idrefcorpname3 =""
        if ligne["idrefcorpname3"] != "":
            idrefcorpname3 = ligne["idrefcorpname3"]

        idrefcorpname4 = ""
        if ligne["idrefcorpname4"] != "":
            idrefcorpname3 = ligne["idrefcorpname4"]

        #-------------Extraire le PHYSFACET et le PhystfacetType avec la méthode extractPhysfacet--------------#

        pairPhysfacetType2 = extractPhysfacet(ligne["physfacetNiveau2"], ligne["typePhysfacet2"], ligne["coteNiveau2"], ligne["titreNiveau2"])
        pairPhysfacetType3 = extractPhysfacet(ligne["physfacetNiveau3"], ligne["typePhysfacet3"], ligne["coteNiveau3"], ligne["titreNiveau3"])
        pairPhysfacetType4 = extractPhysfacet(ligne["physfacetNiveau4"], ligne["typePhysfacet4"], ligne["coteNiveau4"],
                                              ligne["titreNiveau4"])

        # -------------Extraire le GENREFORM: typeGenreform et le normalGenreform avec la methode extractTypeNormalGenreform --------------#

        pairTypeNormalGenreform2 = extractTypeNormalGenreform (ligne["typeGenreform2"],ligne["normalGenreform2"], ligne["coteNiveau2"], ligne["titreNiveau2"])
        pairTypeNormalGenreform3 = extractTypeNormalGenreform (ligne["typeGenreform3"],ligne["normalGenreform3"], ligne["coteNiveau3"], ligne["titreNiveau3"])
        pairTypeNormalGenreform4 = extractTypeNormalGenreform(ligne["typeGenreform4"], ligne["normalGenreform4"],ligne["coteNiveau4"], ligne["titreNiveau4"])



            # ======== Générer les NIVEAU 2 + Niveau 3 ==========#

        # si le contenu de la cote du niveau 2 est différent du contenu de la ligne précédente
        if ligne["coteNiveau2"] != niveau2:
            #on crée le niveau 2 "serie"
            createLevel2()
            # si le contenu de la cote du niveau 3 est différent du contenu de la ligne précédente
            if ligne["coteNiveau3"] != niveau3:
                #on crée le niveau 3, "file" et le premier niveau4 "item"
                createLevel3()
                if ligne["coteNiveau4"] != "":
                    createLevel4()
            # si le contenu de la cote du niveau 3 est identique au contenu de la ligne précédente
            elif ligne["coteNiveau3"] == niveau3 and ligne["coteNiveau4"] != "":
                #on rajoute dans le niveau 3 les balises du niveau 4 "item"
                createLevel4()
        # si le contenu de la cote du niveau 2 est identique au contenu de la ligne précédente
        else :
            # si le contenu de la cote du niveau 3 est identique au contenu de la ligne précédente
            if ligne["coteNiveau3"] == niveau3:
                # on crée uniquement le niveau 4 qui arrive à la suite des autres items dans le dernier "file"
                createLevel4()
            else:
                # autrement, on crée un niveau3 avec le niveau 4 associé
                createLevel3()
                createLevel4()
        #on fini par mettre à jour l'affection des deux variable de teste pour la deuxième boucle.
        niveau2 = ligne["coteNiveau2"]
        niveau3 = ligne["coteNiveau3"]


        tree = ET.ElementTree(racine)
        tree.write(OUTPUTCALAMES, encoding="UTF-8")