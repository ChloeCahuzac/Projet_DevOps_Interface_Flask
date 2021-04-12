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

def convert_size(size):
   if size == 0:
       return "0 B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size, 1024)))
   p = math.pow(1024, i)
   s = round(size / p, 2)
   return "%s %s" % (s, size_name[i])

def selectFichier(chemin):
    listeFich = os.listdir(chemin)
    dictFichier = {}
    select = []
    count = 1
    for fichier in listeFich:
        # nom du fichier
        select.append(fichier.split('.')[0])
        # extension du fichier
        select.append(fichier.split('.')[-1])
        # taille du fichier
        size = os.path.getsize(chemin + "/" + fichier)
        select.append(convert_size(size))
        # date de création
        datc = os.path.getctime(chemin + "/" + fichier)
        select.append(time.strftime("%d/%m/%Y %H:%M",time.gmtime(datc)))
        # date de modification
        datm = os.path.getmtime(chemin + "/" + fichier)
        select.append(time.strftime("%d/%m/%Y %H:%M",time.gmtime(datm)))
        dictFichier[count] = select
        count += 1
        select = []
    return dictFichier

@app.route('/accueil')
def accueil():
    return render_template("accueil.html")

@app.route('/comparaison/', methods=["POST", "GET"])
def comparaison():
    msg="msg"
    if request.method == "POST":
        try:
            # Variables récupées par la saisie de l'utilisateur sur la page accueil.html :
            dossierSource = request.form["dossierSource"]
            dossierDestination = request.form["dossierDestination"]
            # Insertion de ses variables dans la BDD :
            with sqlite3.connect("databaseProjet.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO DossiersSource (cheminDossierSource, chemintest1) VALUES (?, ?)", (dossierSource, "NULL"))
                cur.execute("INSERT INTO DossiersDestination (cheminDossierDest, chemintest2) VALUES (?, ?)", (dossierDestination, "NULL"))
                con.commit()
                msg="Les deux chemins ont bien été enregistré dans la base de données, vueillez cliquer sur 'Appliquer le filtre' pour comparer : "
        except:
            # par sécurité on revient à l'état précédent :
            con.rollback()
            msg="Nous ne pouvons pas enregistrer les deux chemins"
        finally:
            # Récupération des chemins des dossiers rentrés par l'utilisateur dans la page accueil.html pour permettre leur affichage :
            con=sqlite3.connect("databaseProjet.db")
            con.row_factory=sqlite3.Row
            cur = con.cursor()
            row1 = cur.execute("SELECT * FROM DossiersSource ORDER BY idDossierSource DESC LIMIT 1").fetchall()
            row2 = cur.execute("SELECT * FROM DossiersDestination ORDER BY idDossierDest DESC LIMIT 1").fetchall()
            con.close()

            with sqlite3.connect("databaseProjet.db") as con:
                # Récupération des id des deux dossiers source et destination :
                cur = con.cursor()
                id1 = cur.execute("SELECT idDossierSource FROM DossiersSource ORDER BY idDossierSource DESC LIMIT 1").fetchall()
                id2 = cur.execute("SELECT idDossierDest FROM DossiersDestination ORDER BY idDossierDest DESC LIMIT 1").fetchall()
                for row in id1:
                    idSource = str(row[0])
                for row in id2:
                    idDest = str(row[0])
                # Récupération des valeurs de chaques fichiers du dossier correspondant, puis insertion de ces valeurs dans la BDD :
                FichiersS = selectFichier(dossierSource)
                FichiersD = selectFichier(dossierDestination)
                for cle, valeur in FichiersS.items():
                    cur.execute("INSERT INTO FichiersSource (idDossierSource, nomFichier, extensionFichier, sizeFichier, date_create_Fichier, date_modif_Fichier) values (?,?,?,?,?,?)", (int(idSource), valeur[0], valeur[1], valeur[2], valeur[3], valeur[4]))
                for cle, valeur in FichiersD.items():
                    cur.execute("INSERT INTO FichiersDestination (idDossierDest, nomFichier, extensionFichier, sizeFichier, date_create_Fichier, date_modif_Fichier) values (?,?,?,?,?,?)", (int(idDest), valeur[0], valeur[1], valeur[2], valeur[3], valeur[4]))
                con.commit()

            # Récupération des données des fichiers contenu dans les dossiers pour permettre leur affichage dans la page comparaison.html :
            con=sqlite3.connect("databaseProjet.db")
            con.row_factory=sqlite3.Row
            cur = con.cursor()
            rowsSource = cur.execute("SELECT * FROM FichiersSource where idDossierSource=?", (idSource,)).fetchall()
            rowsDestination = cur.execute("SELECT * FROM FichiersDestination where idDossierDest=?", (idDest,)).fetchall()

            return render_template("comparaison.html", msg=msg, row1=row1, row2=row2, rowsSource=rowsSource, rowsDestination=rowsDestination)

    if request.method == "GET":
        return render_template("comparaison.html")

@app.route('/filtre/')
def filtre():
    return render_template("filtre.html")

@app.route('/savefiltre/', methods=["POST", "GET"])
def savefiltre():
    msg="msg"
    if request.method == "POST":
        try:
            newext = "jpg"
            print(newext)
            if request.form.get('jpg'):
                con=sqlite3.connect("databaseProjet.db")
                con.row_factory=sqlite3.Row
                cur = con.cursor()
                id1 = cur.execute("SELECT * FROM DossiersSource ORDER BY idDossierSource DESC LIMIT 1").fetchall()
                id2 = cur.execute("SELECT * FROM DossiersDestination ORDER BY idDossierDest DESC LIMIT 1").fetchall()
                con.close()
                with sqlite3.connect("databaseProjet.db") as con:
                    # Récupération des id des deux dossiers source et destination :
                    cur = con.cursor()
                    print("connexion réussi")
                    for row in id1:
                        idSource = str(row[0])
                        print(idSource)
                    for row in id2:
                        idDest = str(row[0])
                        print(idDest)
                    fich1 = cur.execute("SELECT * FROM FichiersSource WHERE extensionFichier='jpg' AND idDossierSource=?", (idSource,)).fetchall()
                    fich2 = cur.execute("SELECT * FROM FichiersDestination WHERE extensionFichier='jpg' AND idDossierDest=?", (idDest,)).fetchall()
                    print("fich1 =", fich1)
                    print("fich2 =", fich2)
                    for row in fich1:
                        print(row)
                        print(row[0])
                        cur.execute("UPDATE FichiersSource SET idFichier=?, idDossierSource=?, nomFichier=?, extensionFichier=?, sizeFichier=?, date_create_Fichier=?, date_modif_Fichier=? WHERE idDossierSource=?", ((str(row[0]),), (str(row[1]),), (str(row[2]),), (str(row[3]),), (str(row[4]),), (str(row[5]),), (str(row[6]),), (str(row[1]),)))
                        print("update effectué")                    
                    for row in fich2:
                        row2 = str(row[0])
                        cur.execute("UPDATE FichiersDestination SET idFichier=?, idDossierDest=?, nomFichier=?, extensionFichier=?, sizeFichier=?, date_create_Fichier=?, date_modif_Fichier=? WHERE idDossierDest=?", ((str(row[0]),), (str(row[1]),), (str(row[2]),), (str(row[3]),), (str(row[4]),), (str(row[5]),), (str(row[6]),), (str(row[1]),)))
                        print(row2)
                    con.commit()
                    msg="Filtre a bien été pris en compte"
            else:
                con.rollback()
                msg="Filtre n'a pas pu être pris en compte"
        except:
            msg="Nous ne pouvons pas appliquer le filtre"
        finally:
            con=sqlite3.connect("databaseProjet.db")
            con.row_factory=sqlite3.Row
            cur = con.cursor()
            fichSource = cur.execute("SELECT * FROM FichiersSource WHERE idDossierSource=?", (idSource,)).fetchall()
            fichDest = cur.execute("SELECT * FROM FichiersDestination WHERE idDossierDest=?", (idDest,)).fetchall()
            return render_template("filtre_comparaison.html", msg=msg, id1=id1, id2=id2, fichSource=fichSource, fichDest=fichDest)

@app.route('/synchronisation/')
def synchronisation():
    return render_template("synchronisation.html")


if __name__ == "__main__":
    app.run(port='5000', debug=True)