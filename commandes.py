import os.path
import os, sys, stat
import shutil
dst = "C:\\Users\PIERRE\Documents\Formation_Devops\Projet\projet_mi-parcours\projetS1\dossier4"
src="C:\\Users\PIERRE\Documents\Formation_Devops\Projet\projet_mi-parcours\projetS1\dossier2"
#print(os.path.basename(src)) #affiche le nom de fichier
#print(os.path.dirname(src)) #affiche le chemin

#print(os.path.exists(chemin)) #true si le fichier exite
#print(os.path.isfile(chemin)) #true si c'est un fichier
#print(os.path.isdir(chemin)) #true si c'est un dossier


#print(os.listdir(src)) # liste les élements d'un répertoire

#shutil.copytree(src,dst) #copy dans un dossier non existant

 

shutil.move(src,dst) #déplace rep

#shutil.rmtree(dst) #supprime rep