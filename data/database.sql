CREATE TABLE IF NOT EXISTS DossiersSource (
    idDossierSource INTEGER PRIMARY KEY AUTOINCREMENT, 
    cheminDossierSource TEXT NOT NULL,
    chemintest1 TEXT
);

CREATE TABLE IF NOT EXISTS DossiersDestination (
    idDossierDest INTEGER PRIMARY KEY AUTOINCREMENT, 
    cheminDossierDest TEXT NOT NULL,
    chemintest2 TEXT
);

CREATE TABLE IF NOT EXISTS FichiersSource (
    idFichier INTEGER PRIMARY KEY AUTOINCREMENT, 
    idDossierSource INTEGER, 
    nomFichier TEXT, 
    extensionFichier TEXT, 
    sizeFichier INTEGER, 
    date_create_Fichier DATE, 
    date_modif_Fichier DATE, 
    CONSTRAINT fk_idDossierSource FOREIGN KEY(idDossierSource) REFERENCES DossiersSource(idDossierSource)
);

CREATE TABLE IF NOT EXISTS FichiersDestination (
    idFichier INTEGER PRIMARY KEY AUTOINCREMENT, 
    idDossierDest INTEGER, 
    nomFichier TEXT, 
    extensionFichier TEXT, 
    sizeFichier INTEGER, 
    date_create_Fichier DATE, 
    date_modif_Fichier DATE, 
    CONSTRAINT fk_idDossierDest FOREIGN KEY(idDossierDest) REFERENCES DossiersDestination(idDossierDest)
);