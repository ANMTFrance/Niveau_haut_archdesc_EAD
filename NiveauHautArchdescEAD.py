# permet de parser le fichier XML :
# https://docs.python.org/3/library/xml.etree.elementtree.html
from xml.etree import ElementTree
# permet de créer le fichier CSV :
# https://docs.python.org/fr/3/library/csv.html?highlight=csv
from csv import writer
# permet de communiquer avec le système de fichiers de l'ordinateur :
# https://docs.python.org/fr/3/library/os.html
import os
from pathlib import Path

print("Ce script va transformer un ensemble de fichiers XML EAD "
      "en un tableau CSV avec une ligne par archdesc. "
      "Les fichiers doivent se trouver dans le répertoire 'EAD'.")

# Sélectionner le répertoire (directory)
xml_directory = './EAD'

input("Appuyer sur Entrée pour continuer")

# Créer le fichier CSV (output), dire qu'on veut l'écrire de A à Z ("w"), encodé en UTF-8
# Avec newline="", on indique qu'on ne souhaite pas modifier la gestion des caractères de nouvelle ligne.
# Le comportement par défaut du système d'exploitation sera utilisé.
# le fichier sera dans la variable "f"
with open('output_EAD_multiple.csv', 'w', encoding="utf-8", newline="") as f:
    # séparateur point-virgule
	write_file = writer(f, delimiter=';')

    # Définir les en-têtes de colonnes
    headers = ["nom", "cote", "intitule", "date", "producteur", "statut légal", "conditions d'accès", "conditions d'utilisation"]

    # Ecrire les en-têtes de colonne
    write_file.writerow(headers)

    # Dire que l'on veut travailler sur chaque fichier XML du répertoire
    # Si j'utilise print(xml_files_list) je constate que cette liste fonctionne
    xml_files_list = list(map(str, Path(xml_directory).glob('**/*.xml')))
    print(xml_files_list)

    # Parser chaque fichier XML
    for xml_file in xml_files_list:
        # L'arbre XML est créé et parsé
        tree = ElementTree.parse(xml_file)
        # La première colonne comprendra le nom du fichier
        name = os.path.basename(xml_file)

        # Parser à l'intérieur de chaque fichier XML
        for archdesc in tree.findall("./archdesc"):
            unitid = archdesc.find('./did/unitid').text if archdesc.find('./did/unitid') is not None else ''
			# Ce qui veut dire : le noeud texte présent dans le XPath .did/unitid/text() sera placé dans
			# la variable unitid si (if) il existe (is not None). Sinon, on n'y place rien ('').
			# None = absence de données
			# Le contenu de cette variable unitid sera affiché dans le tableau CSV
            print(unitid) # On affiche ensuite la cote traitée
            unittitle = archdesc.find('./did/unittitle').text if archdesc.find('./did/unittitle') is not None else ''
            unitdate = archdesc.find('./did/unitdate').text if archdesc.find('./did/unitdate') is not None else ''
            corpname = archdesc.find('./did/origination/corpname').text if archdesc.find('./did/origination/corpname') is not None else ''
            # reprendre le contenu de l'attribut ALTRENDER de <legalstatus>
            legalstatus = archdesc.find('./accessrestrict/legalstatus').attrib['altrender'] if archdesc.find('./accessrestrict/legalstatus').attrib['altrender'] is not None else ''
            # itertext() renvoie tout le texte présent à l'intérieur de l'élément, y compris celui contenu dans ses éléments enfants.
			# join() permet de concaténer tout ce texte
            # ne prendre que <accessrestrict> avec l'attribut TYPE "commentaire"
			accessrestrict = ''.join(archdesc.find('./accessrestrict[@type='commentaire']/note').itertext()) if archdesc.find('./accessrestrict[@type='commentaire"]/note') is not None else ''
            userestrict = ''.join(archdesc.find('./userestrict').itertext()) if archdesc.find('./userestrict') is not None else ''   
            # écriture de la ligne dans le CSV
            csv_line = [name, unitid, unittitle, unitdate, corpname, legalstatus, accessrestrict, userestrict]
            # ajouter une nouvelle ligne au fichier CSV avec les données
            write_file.writerow(csv_line)

# Conclusion :
print(f"Un total de {len(xml_files_list)} IR a été parsé."
      f"Le fichier produit se trouve dans {getcwd()}. "
      f"Il comporte {len(headers)} colonnes.")
