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

# Fonction qui permet de convertir la taille d'un fichier :
def convert_size(size):
   if size == 0:
       return "0 B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size, 1024)))
   p = math.pow(1024, i)
   s = round(size / p, 2)
   return "%s %s" % (s, size_name[i])

# Fonction qui permet de récupérer toutes les données d'un fichier :
def selectFichier(chemin):
    # récupération des fichiers provenant du dossier renseigné dans une liste :
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

# Création des différents route :
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
                msg="Les deux chemins ont été enregistré dans la base de données, vous pouvez appliquer un filtre avant de valider la comparaison : "
        except:
            # Par sécurité, revient à l'état précédent :
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
            checkactive = request.form.getlist('mycheckbox')
            print(checkactive)

            con=sqlite3.connect("databaseProjet.db")
            con.row_factory=sqlite3.Row
            cur = con.cursor()
            row1 = cur.execute("SELECT * FROM DossiersSource ORDER BY idDossierSource DESC LIMIT 1").fetchall()
            print("select 1 effectué")
            row2 = cur.execute("SELECT * FROM DossiersDestination ORDER BY idDossierDest DESC LIMIT 1").fetchall()
            print("select 2 effectué")
            con.close()

            with sqlite3.connect("databaseProjet.db") as con:
                # Récupération des id des deux dossiers source et destination :
                cur = con.cursor()
                print("connexion réussi")
                id1 = cur.execute("SELECT * FROM DossiersSource ORDER BY idDossierSource DESC LIMIT 1").fetchall()
                print("select 3 effectué")
                id2 = cur.execute("SELECT * FROM DossiersDestination ORDER BY idDossierDest DESC LIMIT 1").fetchall()
                print("select 4 effectué")
                for row in id1:
                    idSource = str(row[0])
                    dossierSource = str(row[1])
                    print(idSource)
                    print(dossierSource)
                for row in id2:
                    idDest = str(row[0])
                    dossierDestination = str(row[1])
                    print(idDest)
                    print(dossierDestination)
                    
                id3 = cur.execute("SELECT idFichier FROM FichiersSource where idDossierSource=?", (idSource,)).fetchall()
                print("select 3 effectué")
                id4 = cur.execute("SELECT idFichier FROM FichiersDestination where idDossierDest=?", (idDest,)).fetchall()
                print("select 4 effectué")
                idFichierSource = []
                idFichierDest = []
                for row in id3:
                    idFichierSource.append(str(row[0]))
                print("id fichier source :", idFichierSource)
                for row in id4:
                    idFichierDest.append(str(row[0]))
                print(idFichierDest)

                # Suppression de l'ancienne table :
                cur = con.cursor()
                print("connexion 2 réussi avant suppresion")
                for element in idFichierSource:
                    cur.execute("DELETE FROM FichiersSource where idFichier=?", (int(element),))
                print("la table DossiersSource a bien était supprimée")
                for element in idFichierDest:
                    cur.execute("DELETE FROM FichiersDestination where idFichier=?", (int(element),))
                print("la table DossiersDestination a bien était supprimée")
        except:
            con.rollback()
            msg="Nous ne pouvons pas appliquer le filtre"
        finally:
            with sqlite3.connect("databaseProjet.db") as con:
                cur = con.cursor()

                FichiersS = selectFichier(dossierSource)
                FichiersD = selectFichier(dossierDestination)

                for cle, valeur in FichiersS.items():
                    for ext in checkactive:
                        if valeur[1] == ext:
                            cur.execute("INSERT INTO FichiersSource (idDossierSource, nomFichier, extensionFichier, sizeFichier, date_create_Fichier, date_modif_Fichier) values (?,?,?,?,?,?)", (int(idSource), valeur[0], valeur[1], valeur[2], valeur[3], valeur[4]))
                print("insert 1 effectué")
                for cle, valeur in FichiersD.items():
                    for ext in checkactive:
                        if valeur[1] == ext:
                            cur.execute("INSERT INTO FichiersDestination (idDossierDest, nomFichier, extensionFichier, sizeFichier, date_create_Fichier, date_modif_Fichier) values (?,?,?,?,?,?)", (int(idDest), valeur[0], valeur[1], valeur[2], valeur[3], valeur[4]))
                print("insert 2 effectué")
                
                con.commit()
                msg="Le filtre a bien été pris en compte, ci-dessous la comparaison des deux dossiers :"
                con=sqlite3.connect("databaseProjet.db")
                print("connexion finale réussi")
                con.row_factory=sqlite3.Row
                cur = con.cursor()
                fichSource = cur.execute("SELECT * FROM FichiersSource WHERE idDossierSource=?", (idSource,)).fetchall()
                print("select 1 réussi")
                fichDest = cur.execute("SELECT * FROM FichiersDestination WHERE idDossierDest=?", (idDest,)).fetchall()
                print("select 2 réussi")
            return render_template("filtre_comparaison.html", msg=msg, row1=row1, row2=row2, fichSource=fichSource, fichDest=fichDest)

@app.route('/synchronisation/')
def synchronisation():
    return render_template("synchronisation.html")


if __name__ == "__main__":
    app.run(port='5000', debug=True)