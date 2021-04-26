# Projet_DevOps_Interface_Flask 

### Projet mi-parcours : Interface Web Python Flask

## Environnement :
Windows

## Démarrage de l'application :
1. Ouvrir un invité de commande
2. Créer un environnement virtuel dans le dossier Projet_DevOps_Interface_Flask contenant tous les fichiers du projet :
    ```bash
    > cd Projet_DevOps_Interface_Flask | py -m venv venv
    ```
3. Activer cet envrionnement :
    ```bash
    > venv\Scripts\activate
    ```
4. Installer Flask :
    ```bash
    (venv) > pip install Flask
    ```
5. Lancer le code projet.py :
    ```bash
    (venv) > py projet.py
    ```

Aide pour l'installation : https://flask.palletsprojects.com/en/1.1.x/installation/

## Groupe projet :

Chloé Cahuzac
Morgane Froment
Pierre Maudet

## Application Python :

Choix de fonctionnement : 
- Synchronisation uni-directionnelle
- Synchronisation en local

Fonctionnement global :
- Cette application utilise une base de données sqlite3 qui permet d'enregistrer les résultats en fonction de la requêtes données

Fonctionnement par onglet :
1. **Interface (console avec input et menu)** :
    - Interface Web et serveur python Flask
    - L'interface est composée de trois parties :
        1. Accueil : qui permet de renseigner les chemins des deux dossiers que l'on veut synchroniser --> format des chemins à renseigner : C:\Users\utilisateur\Documents\NomDossier
        3. Comparaison : qui permet de voir le contenu de nos deux fichiers ainsi que de pouvoir sélectionner un filtre si besoin --> bien penser à valider notre filtre pour passer à la synchronisation !
        4. Synchronisation : qui permet de synchronisaer les deux dossiers (en uni-directionnelle)

2. **Comparaison de dossiers et de fichiers (taille, date de modification, date de création)** :
    - Mise en place de filtres (sur les extensions des fichiers) qui permet de mettre à jour la comparaison en fonction de l'extension choisie
    - Pouvoir mettre en pause l’application et reprise de la synchro de fichiers --> non effectué

3. **Si arrêt du programme** :
    - Pouvoir faire une reprise avec la liste des fichiers à synchroniser grâce à une base de données SQLite qui a enregistrer la liste des fichiers à synchroniser
      avec bien sûr le type de synchro (local)
     
## Informations consernant les erreurs :
1. Ne pas avoir de nom de fichier comportant de "." avant l'extension
2. Toujours valider l'application du filtre
