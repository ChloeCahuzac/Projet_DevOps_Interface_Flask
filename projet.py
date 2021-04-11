from flask import Flask
import flask
import os
from flask import render_template, make_response, request, url_for, session
import sqlite3
import glob
import shutil
import os.path, time
import math

app = flask.Flask(__name__)
app.config["DEBUG"]=True

# Création de la base de données :
conn = sqlite3.connect('databaseProjet.db')
print("Database bien ouverte")
with open('./data/database.sql') as f:
    conn.executescript(f.read())
conn.close()

def convert_size(size1):
   if size1 == 0:
       return "0 Ko"
   size_name = ("o", "Ko", "Mo", "Go", "To", "Po", "Eo", "Zo", "Yo")
   i = int(math.floor(math.log(size1, 1024)))
   p = math.pow(1024, i)
   s = round(size1 / p, 2)
   return "%s %s" % (s, size_name[i])

def selectFichierSource(chemin1):
    listeFich1 = os.listdir(chemin1)
    dictFichier1 = {}
    select = []
    count = 1
    for fich in listeFich1:
        # nom du fichier
        select.append(fich.split('.')[0])
        # extension du fichier
        select.append(fich.split('.')[-1])
        # taille du fichier
        size = os.path.getsize(chemin1 + "/" + fich)
        select.append(convert_size(size))
        # date de création
        datc = os.path.getctime(chemin1 + "/" + fich)
        select.append(time.strftime("%d/%m/%Y %H:%M",time.gmtime(datc)))
        # date de modification
        datm = os.path.getmtime(chemin1 + "/" + fich)
        select.append(time.strftime("%d/%m/%Y %H:%M",time.gmtime(datm)))
        dictFichier1[count] = select
        count += 1
        select = []
    return dictFichier1

def selectFichierDestination(chemin2):
    listeFich2 = os.listdir(chemin2)
    dictFichier2 = {}
    select = []
    count = 1
    for fich in listeFich2:
        # nom du fichier
        select.append(fich.split('.')[0])
        # extension du fichier
        select.append(fich.split('.')[-1])
        # taille du fichier
        size = os.path.getsize(chemin2 + "/" + fich)
        select.append(convert_size(size))
        # date de création
        datc = os.path.getctime(chemin2 + "/" + fich)
        select.append(time.strftime("%d/%m/%Y %H:%M",time.gmtime(datc)))
        # date de modification
        datm = os.path.getmtime(chemin2 + "/" + fich)
        select.append(time.strftime("%d/%m/%Y %H:%M",time.gmtime(datm)))
        # creation du dictionnaire
        dictFichier2[count] = select
        count += 1
        select = []
    return dictFichier2

@app.route('/accueil')
def accueil():
    return render_template("accueil.html")

@app.route('/savechemin/', methods=["POST", "GET"])
def savechemin():
    msg="msg"
    if request.method == "POST":
        try:
            # on récupère ce qui a été rentré dans la variable dossierSource, dossierDestination dans accueil.html :
            dossierSource = request.form["dossierSource"]
            dossierDestination = request.form["dossierDestination"]
            with sqlite3.connect("databaseProjet.db") as con:
                cur = con.cursor()
                print("Connexion réussi")
                cur.execute("INSERT INTO DossiersSource (cheminDossierSource, chemintest1) VALUES (?, ?)", (dossierSource, "NULL"))
                cur.execute("INSERT INTO DossiersDestination (cheminDossierDest, chemintest2) VALUES (?, ?)", (dossierDestination, "NULL"))
                con.commit()
                msg="Les deux chemins ont bien été enregistré dans la base de données, vueillez cliquer sur 'Appliquer le filtre' pour comparer : "
        except:
            # par sécurité on revient à l'état précédent :
            con.rollback()
            msg="Nous ne pouvons pas enregistrer les deux chemins"
        finally:
            con=sqlite3.connect("databaseProjet.db")
            # Permet de récupérer les rangs d'une table d'une base de données (si on ne l'utilise pas on aura une table vide non exploitable):
            con.row_factory=sqlite3.Row
            cur = con.cursor()
            # Récupération des rangs :
            row1 = cur.execute("SELECT * FROM DossiersSource ORDER BY idDossierSource DESC LIMIT 1").fetchall()
            row2 = cur.execute("SELECT * FROM DossiersDestination ORDER BY idDossierDest DESC LIMIT 1").fetchall()
            # Stockage des rangs (récupération des données de la requête précédente):
            con.close()

            with sqlite3.connect("databaseProjet.db") as con:
                cur = con.cursor()
                print("Connexion réussi")

                id1 = cur.execute("SELECT idDossierSource FROM DossiersSource ORDER BY idDossierSource DESC LIMIT 1").fetchall()
                id2 = cur.execute("SELECT idDossierDest FROM DossiersDestination ORDER BY idDossierDest DESC LIMIT 1").fetchall()
                for row in id1:
                    idSource = str(row[0])
                    print("idSource =", idSource)
                for row in id2:
                    idDest = str(row[0])
                    print("idDest =", idDest)
                
                FichiersS = selectFichierSource(dossierSource)
                FichiersD = selectFichierDestination(dossierDestination)

                for cle, valeur in FichiersS.items():
                    cur.execute("INSERT INTO FichiersSource (idDossierSource, nomFichier, extensionFichier, sizeFichier, date_modif_Fichier, date_create_Fichier) values (?,?,?,?,?,?)", (int(idSource), valeur[0], valeur[1], valeur[2], valeur[3], valeur[4]))
                print("insertion1 réussi")
                for cle, valeur in FichiersD.items():
                    cur.execute("INSERT INTO FichiersDestination (idDossierDest, nomFichier, extensionFichier, sizeFichier, date_modif_Fichier, date_create_Fichier) values (?,?,?,?,?,?)", (int(idDest), valeur[0], valeur[1], valeur[2], valeur[3], valeur[4]))
                print("insertion 2 réussi")
                con.commit()

            con=sqlite3.connect("databaseProjet.db")
            # Permet de récupérer les rangs d'une table d'une base de données (si on ne l'utilise pas on aura une table vide non exploitable):
            con.row_factory=sqlite3.Row
            cur = con.cursor()
            rowsSource = cur.execute("SELECT * FROM FichiersSource where idDossierSource=?", (idSource,)).fetchall()
            print("select 1 réussi")
            rowsDestination = cur.execute("SELECT * FROM FichiersDestination where idDossierDest=?", (idDest,)).fetchall()
            print("select 2 réussi")

            return render_template("comparaison.html", msg=msg, row1=row1, row2=row2, rowsSource=rowsSource, rowsDestination=rowsDestination)

@app.route('/')

@app.route('/comparaison/')
def comparaison():
    return render_template("comparaison.html")

@app.route('/synchronisation/')
def synchronisation():
    return render_template("synchronisation.html")


if __name__ == "__main__":
    app.run(port='5000', debug=True)