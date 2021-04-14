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
                msg="Les deux chemins ont bien été enregistré dans la base de données, ci-dessous leur comparaison. Vous pouvez appliquer un filtre avant de valider pour la synchronisation : "
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
        try:
            # Récupération des chemins des dossiers rentrés par l'utilisateur dans la page accueil.html pour permettre leur affichage :
            con=sqlite3.connect("databaseProjet.db")
            con.row_factory=sqlite3.Row
            cur = con.cursor()
            row1 = cur.execute("SELECT * FROM DossiersSource ORDER BY idDossierSource DESC LIMIT 1").fetchall()
            row2 = cur.execute("SELECT * FROM DossiersDestination ORDER BY idDossierDest DESC LIMIT 1").fetchall()
            con.close()
            # Récupération des id des deux dossiers source et destination :
            with sqlite3.connect("databaseProjet.db") as con:
                cur = con.cursor()
                id1 = cur.execute("SELECT * FROM DossiersSource ORDER BY idDossierSource DESC LIMIT 1").fetchall()
                id2 = cur.execute("SELECT * FROM DossiersDestination ORDER BY idDossierDest DESC LIMIT 1").fetchall()
                for row in id1:
                    idSource = str(row[0])
                for row in id2:
                    idDest = str(row[0])
            # Affichage des fichiers provenant des dossiers renseignés :
            con=sqlite3.connect("databaseProjet.db")
            con.row_factory=sqlite3.Row
            cur = con.cursor()
            rowsSource = cur.execute("SELECT * FROM FichiersSource where idDossierSource=?", (idSource,)).fetchall()
            rowsDestination = cur.execute("SELECT * FROM FichiersDestination where idDossierDest=?", (idDest,)).fetchall()
            msg="Voici la comparaison de la dernière sélection de dossiers renseignés"
        except:
            msg="Nous ne pouvons pas afficher les fichiers, veuillez renseigner les dossiers dans l'onglet accueil"
        finally:
            return render_template("comparaison.html", msg=msg, row1=row1, row2=row2, rowsSource=rowsSource, rowsDestination=rowsDestination)

@app.route('/filtre/')
def filtre():
    return render_template("filtre.html")

@app.route('/savefiltre/', methods=["POST", "GET"])
def savefiltre():
    msg="msg"
    if request.method == "POST":
        try:
            global checkactive
            # Récupération des checkbox renseignés par l'utilisateur :
            checkactive = request.form.getlist('mycheckbox')
            # Récupération des chemins des dossiers rentrés par l'utilisateur dans la page accueil.html pour permettre leur affichage :
            con=sqlite3.connect("databaseProjet.db")
            con.row_factory=sqlite3.Row
            cur = con.cursor()
            row1 = cur.execute("SELECT * FROM DossiersSource ORDER BY idDossierSource DESC LIMIT 1").fetchall()
            row2 = cur.execute("SELECT * FROM DossiersDestination ORDER BY idDossierDest DESC LIMIT 1").fetchall()
            con.close()
            # Récupération des id des deux dossiers source et destination :
            with sqlite3.connect("databaseProjet.db") as con:
                cur = con.cursor()
                id1 = cur.execute("SELECT * FROM DossiersSource ORDER BY idDossierSource DESC LIMIT 1").fetchall()
                id2 = cur.execute("SELECT * FROM DossiersDestination ORDER BY idDossierDest DESC LIMIT 1").fetchall()
                for row in id1:
                    idSource = str(row[0])
                    dossierSource = str(row[1])
                for row in id2:
                    idDest = str(row[0])
                    dossierDestination = str(row[1])
                    
                id3 = cur.execute("SELECT idFichier FROM FichiersSource where idDossierSource=?", (idSource,)).fetchall()
                id4 = cur.execute("SELECT idFichier FROM FichiersDestination where idDossierDest=?", (idDest,)).fetchall()
                idFichierSource = []
                idFichierDest = []
                for row in id3:
                    idFichierSource.append(str(row[0]))
                for row in id4:
                    idFichierDest.append(str(row[0]))

                # Suppression de l'ancienne table :
                cur = con.cursor()
                for element in idFichierSource:
                    cur.execute("DELETE FROM FichiersSource where idFichier=?", (int(element),))
                for element in idFichierDest:
                    cur.execute("DELETE FROM FichiersDestination where idFichier=?", (int(element),))
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
                for cle, valeur in FichiersD.items():
                    for ext in checkactive:
                        if valeur[1] == ext:
                            cur.execute("INSERT INTO FichiersDestination (idDossierDest, nomFichier, extensionFichier, sizeFichier, date_create_Fichier, date_modif_Fichier) values (?,?,?,?,?,?)", (int(idDest), valeur[0], valeur[1], valeur[2], valeur[3], valeur[4]))
                con.commit()
                msg="Le filtre a bien été pris en compte, ci-dessous la comparaison des deux dossiers :"
                # Affichage des fichiers provenant des dossiers renseignés avec application du filtre :
                con=sqlite3.connect("databaseProjet.db")
                con.row_factory=sqlite3.Row
                cur = con.cursor()
                fichSource = cur.execute("SELECT * FROM FichiersSource WHERE idDossierSource=?", (idSource,)).fetchall()
                fichDest = cur.execute("SELECT * FROM FichiersDestination WHERE idDossierDest=?", (idDest,)).fetchall()

            return render_template("filtre_comparaison.html", msg=msg, row1=row1, row2=row2, fichSource=fichSource, fichDest=fichDest)

    if request.method == "GET":
        # S'il y a un raffraichissement de la page, retourne sur la méthode GET de la page comparaison :
        return comparaison()

@app.route('/synchronisation/')
def synchronisation():
    if request.method == "GET":
        msg="Attention avant de lancer la synchronisation assurez vous d'avoir appliqué un filtre dans l'onglet comparaison"
        return render_template("synchronisation.html", msg=msg)

@app.route('/save_synchronisation/', methods=["POST", "GET"])
def save_synchronisation():
    if request.method == "POST":
        try:
            # Récupération des chemins des dossiers rentrés par l'utilisateur dans la page accueil.html pour permettre leur affichage :
            con=sqlite3.connect("databaseProjet.db")
            con.row_factory=sqlite3.Row
            cur = con.cursor()
            row1 = cur.execute("SELECT * FROM DossiersSource ORDER BY idDossierSource DESC LIMIT 1").fetchall()
            row2 = cur.execute("SELECT * FROM DossiersDestination ORDER BY idDossierDest DESC LIMIT 1").fetchall()
            con.close()
            # Récupération des id des deux dossiers source et destination :
            with sqlite3.connect("databaseProjet.db") as con:
                cur = con.cursor()
                id1 = cur.execute("SELECT * FROM DossiersSource ORDER BY idDossierSource DESC LIMIT 1").fetchall()
                id2 = cur.execute("SELECT * FROM DossiersDestination ORDER BY idDossierDest DESC LIMIT 1").fetchall()
                for row in id1:
                    idSource = str(row[0])
                    cheminDossierSource = str(row[1])
                for row in id2:
                    idDest = str(row[0])
                    cheminDossierDest = str(row[1])
                # Récupération des données des fichiers :
                id3 = cur.execute("SELECT * FROM FichiersSource where idDossierSource=?", (idSource,)).fetchall()
                id4 = cur.execute("SELECT * FROM FichiersDestination where idDossierDest=?", (idDest,)).fetchall()
                extFichierSource = []
                extFichierDest = []
                nameFichierDest = []
                dateModifFichierDest = []
                for row in id3:
                    extFichierSource.append(str(row[3]))
                for row in id4:
                    extFichierDest.append(str(row[3]))
                    nameFichierDest.append(str(row[2]))
                    dateModifFichierDest.append(str(row[6]))
                #Synchronisation en faisant un INSERT dans la base de données vers le dossier Destination :
                for elementSource in id3:
                    if elementSource[2] not in nameFichierDest:
                        cur.execute("INSERT INTO FichiersDestination (idDossierDest, nomFichier, extensionFichier, sizeFichier, date_create_Fichier, date_modif_Fichier) values (?,?,?,?,?,?)", (elementSource[1], elementSource[2], elementSource[3], elementSource[4], elementSource[5], elementSource[6]))
                        print("insertion réussi")
                    else:
                        print("pas inséré car déjà dans la base")
                con.commit() 
                msg="La synchronisation a bien était effectuée"
        except:
            msg="Impossible d'effectuer la synchronisation"
        finally:
            with sqlite3.connect("databaseProjet.db") as con:
                cur = con.cursor()
                # Copiage des fichiers en local :

                # Sélection des fichiers dans le dossier local :
                FichiersS = selectFichier(cheminDossierSource)
                FichiersD = selectFichier(cheminDossierDest)
                nameFichier1 = []
                nameFichier2 = []
                # Récuération des noms et ajout de leur extension :
                for cle, valeur1 in FichiersS.items():
                    if valeur1[1] in checkactive:
                            nameFichier1.append(valeur1[0] + "." + valeur1[1])
                print("namefichier1 : ", nameFichier1)

                for cle, valeur2 in FichiersD.items():
                    if valeur1[1] in checkactive:
                            nameFichier2.append(valeur2[0] + "." + valeur2[1])
                print("namefichier2 : ", nameFichier2)
                # Copie des fichiers :
                for nameSource in nameFichier1:
                    if nameSource in nameFichier2:
                        print("le fichier existe déjà")
                    else:
                        cheminfinal = (cheminDossierDest + "/" + nameSource)
                        cheminsource = (cheminDossierSource + "/" + nameSource)
                        shutil.copyfile(cheminsource, cheminfinal)
                        print("le fichier n'existe pas, il a donc était copié")

            # for nameDest in nameFichier2:
            #     if nameDest not in nameFichier1:
            #         os.remove(cheminDossierDest + "/" + nameDest)
            #         print("fichier sup")

            # Affichage des fichiers provenant des dossiers renseignés après synchronisation :
            con=sqlite3.connect("databaseProjet.db")
            con.row_factory=sqlite3.Row
            cur = con.cursor()
            fichSource = cur.execute("SELECT * FROM FichiersSource WHERE idDossierSource=?", (idSource,)).fetchall()
            fichDest = cur.execute("SELECT * FROM FichiersDestination WHERE idDossierDest=? ORDER BY nomFichier ASC", (idDest,)).fetchall()
            return render_template("synchronisation_save.html", msg=msg, row1=row1, row2=row2, fichSource=fichSource, fichDest=fichDest)

    if request.method == "GET":
        msg="Une erreure s'est produite, veuillez recommencer"
        return render_template("synchronisation.html", msg=msg)


if __name__ == "__main__":
    app.run(port='5000', debug=True)