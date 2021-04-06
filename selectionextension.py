
def copieext(pathsource,pathdest,extensionchoisi,état):


    source = os.listdir(pathsource)
    destination = pathdest
    os.chdir(pathsource)
    if état=="contient":
        for files in source:
            extension=files.split('.')[-1]
            destination=pathdest

            if ( extension ==extensionchoisi):
                destination=destination+'/'+files
                shutil.copyfile(files,destination)
                print("fichier transmis")

            else:
                print("pas la bonne extension")
    elif état=="sauf":
        for files in source:
            extension=files.split('.')[-1]
            destination=pathdest

            if ( extension !=extensionchoisi):
                destination=destination+'/'+files
                shutil.copyfile(files,destination)
                print("fichier transmis")

            else:
                print("extension sélectionné")
    else:
        print("mauvais état")

