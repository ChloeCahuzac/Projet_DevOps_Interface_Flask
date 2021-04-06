import shutil
import os

def copietaille(pathsource,pathdest,taille,état):


    source = os.listdir(pathsource)
    destination = pathdest
    os.chdir(pathsource)
    if état=="plusgrandque":
        for files in source:
            destination=pathdest
            e = os.path.getsize(files)
            if ( e >taille):
                destination=destination+'/'+files
                shutil.copyfile(files,destination)
                print("fichier transmis")

            else:
                print("fichier trop petit")

    elif état=="pluspetitque":
        for files in source:
            e = os.path.getsize(files)
            if ( e <taille):
                destination=destination+'/'+files
                shutil.copyfile(files,destination)
                print("fichier transmis")

            else:
                print("fichier trop grand")
    elif état=="egal":
        for files in source:
            e = os.path.getsize(files)
            if ( e ==taille):
                destination=destination+'/'+files
                shutil.copyfile(files,destination)
                print("fichier transmis")

            else:
                print("fichier pas de la bonne taille")

    else:
        print("mauvais état")
