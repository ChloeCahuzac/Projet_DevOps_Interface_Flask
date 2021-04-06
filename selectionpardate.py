import os
import platform
from datetime import datetime
import datetime
def avoirdate(path_to_file):
    if platform.system() == 'Windows':
        return os.path.getmtime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            return stat.st_mtime

def copiedate(pathsource,pathdest,jour,mois,année,heure,minute,seconde,état):
    import datetime
    dateprov=datetime.datetime(année,mois,jour,heure,minute,seconde)
    from datetime import datetime
    date=datetime.timestamp(dateprov)
    source = os.listdir(pathsource)
    destination = pathdest
    os.chdir(pathsource)
    if état=="après":
        for files in source:
            destination=pathdest
            modedate = avoirdate(pathsource+'/'+files)
            if ( modedate >date):
                destination=destination+'/'+files
                shutil.copyfile(files,destination)
                print("fichier transmis")

            else:
                print("fichier trop vieux")

    elif état=="avant":
        for files in source:
            destination=pathdest
            modedate = avoirdate(pathsource+'/'+files)
            if ( modedate <date):
                destination=destination+'/'+files
                shutil.copyfile(files,destination)
                print("fichier transmis")

            else:
                print("fichier trop jeune")
    elif état=="acettedate  ":
        for files in source:
            destination=pathdest
            modedate = avoirdate(pathsource+'/'+files)
            if ( modedate ==date):
                destination=destination+'/'+files
                shutil.copyfile(files,destination)
                print("fichier transmis")

            else:
                print("pas la bonne date")

    else:
        print("mauvais état")