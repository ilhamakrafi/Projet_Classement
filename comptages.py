import sys
import os
from datetime import datetime
import re
from PIL import Image
from PIL.ExifTags import TAGS

def get_date_photo(path):
    sort_timestamp = os.path.getmtime(path) # récupere la date de modification
    data = datetime.fromtimestamp(sort_timestamp)
    annee = str(data.year)    # année par défaut stockage
    mois = str(data.month) 
    try:
        image = Image.open(path)
        exif = image._getexif() #lit les données exif
        if exif:
            for tag_id, value in exif.items():  
                if TAGS.get(tag_id) == "DateTimeOriginal":
                    date_str = value #AAAA-MMM-JJ
                    annee, mois = date_str.split()[0].split(":")[:2]  # extrait année et mois
                    return sort_timestamp, annee, mois, "EXIF"
    except:  
        pass

    return sort_timestamp, annee, mois, "Stockage"


# fonction récursive pour parcourir tous les sous dossiers 
def parcours_recursive(dossier): 
    photos = []  # liste vide 
    liste=os.listdir(dossier)
    for nomfichier in liste: 
        chemin = dossier + "/" + nomfichier

        if os.path.isdir(chemin):  # si un fichier est un sous dossier 
            photos += parcours_recursive(chemin)  # ajout a photos les phoots trouvé dans chemin
        else:
            if re.search(".+\.(jpg|jpeg|png|JPG|JPEG|PNG)$", nomfichier): #".+": n'importe quel caractère
                photos.append(chemin)  # ajoute le chemin de la photo à liste  photos 
    return photos

# fonction 
def creer_dossier(chemin): 
    if not os.path.isdir(chemin):
        os.system('mkdir "{}"'.format(chemin))
        
# Fonction pour lancer le script
def lancer(): 
    if len(sys.argv) != 2: # sys.argv doit avoir 2 éléments "comptages.py"+dossierphotos
        print("Erreur: il faut donner 2 éléments en paramètre")

    dossier_base = sys.argv[1] #recupere chemin dossier de base
    if not os.path.isdir(dossier_base):  # test dossier 
        print("Erreur: le dossier n'existe pas")

    photos = parcours_recursive(dossier_base)  # recupere la liste 
    photos_a_classer = [] #liste pour stocker les infos after

    for photo in photos:  # parcours de chaque photo 
        timestamp,annee, mois, source = get_date_photo(photo) 
        dossier_annee = dossier_base + "/" + annee#construction chemin
        creer_dossier(dossier_annee)
        dossier_dest = dossier_annee + "/" + mois
        creer_dossier(dossier_dest)
        
        date=annee+"/"+mois#crée dossiers 
        nom_fichier = photo.split('/')[-1]  # decoupe a chaque /, dernier élément = nom fichier
        chemin_dest = dossier_dest + "/" + nom_fichier
        
       # déplace fihcier avec la commande mv
        os.system('mv "{}" "{}"'.format(photo, chemin_dest))  
      
        photos_a_classer.append((date, nom_fichier, chemin_dest, source)) #ajoute a la liste

    photos_a_classer.sort(key=lambda x: x[0])  # tri sur le premier element des souslistes
    chemin_csv = dossier_base + "/listePhotos.csv" #chemin fichier csv
      
    # Ouverture du fichier en write 
    fd = open(chemin_csv, "w")  # 
    fd.write("NomFichier;Chemin;SourceDate\n")
    
    #pour chaque photo une ligne dans le fichier csv est crée
    for date, nom, chemin, source in photos_a_classer:
        ligne = "{};{};{}\n".format(nom, chemin, source)  
        fd.write(ligne)

    
    fd.close()

    
    print("Classement terminé. CSV:", chemin_csv)

# Appel direct de la fonction lancer
lancer()