from flask import Flask
import flask
import os
from flask import render_template, make_response, request, url_for, session
import sqlite3
import glob
import shutil
import os.path

app = flask.Flask(__name__)
app.config["DEBUG"]=True

# Mise en place de la base de données :

## Création de la base :
con = sqlite3.connect("projetDevops.db")
print("Database bien ouverte")

## Rédaction des requêtes SQL :
con.execute("CREATE TABLE IF NOT EXISTS Dossiers (idDossier INTEGER PRIMARY KEY AUTOINCREMENT, cheminDossierSource TEXT NOT NULL, cheminDossierDestination TEXT NOT NULL)")
con.execute("CREATE TABLE IF NOT EXISTS Fichiers (idFichier INTEGER PRIMARY KEY AUTOINCREMENT, idDossier INTEGER, nomFichier TEXT, extensionFichier TEXT, sizeFichier INTEGER, date_modif_Fichier DATE, date_create_Fichier DATE, CONSTRAINT fk_idDossier FOREIGN KEY(idDossier) REFERENCES Dossiers(idDossier))")

## Fermer la base après toutes commandes :
con.close()

def selectFichierSource(chemin1):
    listeFich1 = os.listdir(chemin1)
    # if listeFich1 == []:
    #     print("Le dossier est vide ou le chemin n'a pas correctement était renseigné --> exemple : /Users/utilisateur/Documents/DossierA")
    # else:
    return listeFich1

def selectFichierDestination(chemin2):
    listeFich2 = os.listdir(chemin2)
    return listeFich2

@app.route('/accueil')
def accueil():
    return render_template("accueil.html")

@app.route('/savechemin/', methods=["POST", "GET"])
def savechemin():
    msg="msg"
    if request.method == "POST":
        try:
            # on récupère ce qui a été rentré dans la variable dossierSource, dossierDestination :
            dossierSource = request.form["dossierSource"]
            dossierDestination = request.form["dossierDestination"]
            # on effectue la requete dans la base :
            with sqlite3.connect("projetDevops.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Dossiers (cheminDossierSource, cheminDossierDestination) values (?,?)", (dossierSource, dossierDestination))
                con.commit()
                msg="Les deux chemins ont bien été enregistré dans la base de données"
        except:
            # par sécurité on revient à l'état précédent :
            con.rollback()
            msg="Nous ne pouvons pas enregistrer les deux chemins"
        finally:
            con=sqlite3.connect("projetDevops.db")
            # Permet de récupérer les rangs d'une table d'une base de données (si on ne l'utilise pas on aura une table vide non exploitable):
            con.row_factory=sqlite3.Row
            cur = con.cursor()
            # Récupération des rangs :
            cur.execute("SELECT idDossier, cheminDossierSource, cheminDossierDestination FROM Dossiers ORDER BY idDossier DESC LIMIT 1")
            # Stockage des rangs (récupération des données de la requête précédente):
            rows = cur.fetchall()
            listeFich1 = selectFichierSource(dossierSource)
            listeFich2 = selectFichierDestination(dossierDestination)
            return render_template("comparaison.html", msg=msg, rows=rows, listeFich1=listeFich1, listeFich2=listeFich2)

@app.route('/')

@app.route('/comparaison/')
def comparaison():
    return render_template("comparaison.html")

@app.route('/synchronisation/')
def synchronisation():
    return render_template("synchronisation.html")


if __name__ == "__main__":
    app.run(port='5000', debug=True)