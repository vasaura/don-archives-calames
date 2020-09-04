import csv
from constantes import INPUTFORARCHDESC, OUTPUTARCHDESC

def eadarchdesc (templateEad=OUTPUTARCHDESC, fichierCSV=INPUTFORARCHDESC):
  with open (templateEad) as fichierxml:
    template=fichierxml.read()

  with open (fichierCSV) as fichier:
    reader=csv.DictReader(fichier, delimiter ="|")

    for ligne in reader:

        dateFonds = ligne["dateFonds"]
        dateNormal = dateFonds[:4]+"/"+dateFonds[5:]
        #print(dateNormal)

        fichierAuteur = template.replace("{coteFonds}", ligne["coteFonds"])\
            .replace("{titreFonds}", ligne["titreFonds"])\
            .replace("{nomAuteurIR}", ligne["nomAuteurIR"])\
            .replace("{financeur}", ligne["financeur"])\
            .replace("{coteFonds}", ligne["coteFonds"])\
            .replace("{dateFonds}", ligne["dateFonds"])\
            .replace("{dateNormalFonds}", dateNormal)\
            .replace("{nomProducteurNormal}", ligne["nomProducteurNormal"])\
            .replace("{identifiantIDREFProducteur}", ligne["identifiantIDREFProducteur"])\
            .replace("{nomProducteur}", ligne["nomProducteur"])\
            .replace("{physfacetFonds}", ligne["physfacetFonds"])\
            .replace("{extentFonds}", ligne["extentFonds"])\
            .replace("{accessrestrictFonds}", ligne["accessrestrictFonds"])\
            .replace("{bioghistProducteur}", ligne["bioghistProducteur"])\
            .replace("{scopecontentFonds}", ligne["scopecontentFonds"])\
            .replace("{custodhistFonds}", ligne["custodhistFonds"])

        with open (OUTPUTARCHDESC, 'w') as eadheadercomplet:
          eadheadercomplet.write(fichierAuteur)
eadarchdesc()