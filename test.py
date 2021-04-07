from sys import *
from os import *
from filecmp import *
import shutil
import os, shutil
 
def verif():
    if len(argv)<=3:
        exit("Utilisation : ce programme necessite au moins 3\
        arguments : le repertoire source, le repertoire cible et le\
        mode de synchronisation (detail,deplacer,copier ou sup)" )
 
#comparer le contennu des fichier
def detail(source, cible):
 
    list=dircmp(source,cible)
    list.report()
    for i in list.left_list:
            print(i)

#déplacer les fichiers de source vers cible    
def move (source,cible):
    shutil.move(source,cible)
    print("le repertoir: " +source+ " à bien été déplacer dans le répertoir: "+cible)

#copier les fichiers de source vers cible      
def copy (source,cible):
    for src_dir, dirs, files in os.walk(source):
        dst_dir = src_dir.replace(source,cible, 1)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    for file_ in files:
        src_file = os.path.join(src_dir, file_)
        dst_file = os.path.join(dst_dir, file_)
        if os.path.exists(dst_file):
            os.remove(dst_file)
        shutil.copy(src_file, dst_dir)
    print("le repertoir: " +source+ " à bien été copier dans le répertoir: "+cible)

def delete(source, cible):
 
    list=dir(source)
    list.report()

#suprimer les fichiers qui ont le même nom dans source et destination





# Debut prog principal
 
verif()  #verif nbre parametres
 
#verification de l'existence des repertoires
 
if access(argv[1],F_OK)==0:
         ("Le dossier source n'existe pas, verifier et recommencer")
 
if access(argv[2],F_OK)==0:
    while 1:
        rep=input("Le dossier cible n'existe pas, voulez vous le creer o/n ?" )
        if rep=="n":
            exit("Abandon utilisateur" )
        if rep=="o":
            mkdir(argv[2])
            break
     
if argv[3]=="detail":
    detail(argv[1],argv[2])

if argv[3]=="deplacer":
    move(argv[1],argv[2])

if argv[3]=="copier":
    copy(argv[1],argv[2])

if argv[3]=="sup":
    delete(argv[1],argv[2])
