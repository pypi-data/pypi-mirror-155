"""
AUTEUR : Théo Hurlimann
  LIEU : CFPT Informatique Genève
  DATE : avril 2022
  PROJET: ARCHIVER
  VERSION : 1.0
  FICHIER : Archive.py: 
    - Possède les méthodes pour créer une archive et la gérer.
"""
from typing import Optional
import src.Constants as Constants
from src.FolderImport import FolderImport
from src.FolderName import FolderName
from src.Utilities import Utilities
from src.Resource import Resource
from src.Metadata import Metadata
from src.Type import Type
from src.Bdd import Bdd
from src import myConfig
import src.Archive as Archive
import pickle 
import stat
from os import makedirs, chmod, path, remove
import shutil, os, py7zr, datetime, orjson
from progress.bar import Bar

class Archive :
    def __init__(self, name : str) -> None:
        """Constructeur de la classe Archive
        Parameters:
            name (String): le nom d'archive
        """
        
        
        self.compressFiles = []
        self.name = name
        self.pathArchive = Utilities.getPathOfArchive(name)
        if path.exists(self.pathArchive):           
            self.myDb = Bdd(self.pathArchive)
        else:
            self.createDirectoryArchive(self.pathArchive)
            self.myDb = Bdd(self.pathArchive)
            
        #if not p.endswith("/"):
        #    self.pathArchive = p+"/"
        pass
    
    def __add__(self, archive : Archive) -> Archive:
        return self.mergeTwoArchive(archive)

    def createDirectoryArchive(self, path :str) -> bool:
        """Permet de Créer le dossier de l'archive

        Parameters:
            path (String): chemin de l'archive

        Returns:
            bool: True si le dossier a été créé
            bool: False si le n'a dossier pas été créé
        """
        try :
            makedirs(path)
            return True
        except Exception as e:
            print(e)
            return False

    def archiveFolder(self, FolderImport : FolderImport) -> bool:
        """Permet d'archiver un dossier

        Parameters:
            FolderImport (FolderImport): dossier à archiver

        Returns:
            bool: True si le dossier a été créé
            bool: False si le n'a dossier pas été créé
        """
        try:
            bar = Bar('Processing', max=FolderImport.nbResource, suffix='%(index).0f/%(max).0f fichiers archivés') 
            for Resource in FolderImport.resources:
                self.compressFiles.append(self.archiveResource(Resource))
                bar.next()
                pass
            bar.finish()
            return True
        except Exception as e:
            print(e)
            return False

    def writeMetadataInJson(self, r : Resource, newArchive : Archive= None) -> None:
        """Permet d'écrire les métadonnées dans un fichier json

        Parameters:
            r (Resource): Resource contenant la métadonnées à écrire
            newArchive (Archive): archive où écrire les métadonnées

        Returns:
            
        """
        
        m = r.universalMetadata
        if newArchive is None:
            pathOfJson = self.pathArchive + "/"+ m.sha1[0:2] +"/"+ m.sha1 + ".json"
        else:
            pathOfJson = newArchive.pathArchive + "/"+ m.sha1[0:2] +"/"+ m.sha1 + ".json"
        
        if not path.exists(pathOfJson):
            f= open(pathOfJson,"w+")
            f.write("[")
            f.write(m.toJson(r.type))
            f.write("]")
            f.close()
        else:
            arrayM = []
            with open(pathOfJson, "r") as f:
                data = orjson.loads(f.read())
            for d in data:
                arrayMT = []
                arrayMT.append(Metadata.jsonDecoder(d))
                arrayMT.append(Type(-1, d["typeName"]))
                arrayM.append(arrayMT)
            arrayM.append([m, r.type])
            f = open(pathOfJson,"w+")
            f.write("[")
            for m, t in arrayM:
                f.write(m.toJson(t))
                
                # if it is not the last metadata
                if m != arrayM[-1][0]:
                    f.write(",")
    
            f.write("]")
            f.close()
        
    def rebuildDbWithJson(self) -> None:
        """Permet de reconstruire la base de données à partir des fichiers json

        Parameters:
            

        Returns:
            None
        """
        filesJson = []
        #If exist, delete the old database
        if path.exists(self.pathArchive+"/archiver.db"):
            remove(self.pathArchive+"/archiver.db")
        self.myDb = Bdd(self.pathArchive)
        
        
        for (root, dirs, files) in os.walk(self.pathArchive):
            for file in files:
                if file.endswith(".json"): 
                    filesJson.append(root+"/"+file)

        bar = Bar('Reconstruction de la base de données :', max=len(filesJson), suffix='%(percent)d%%') 
        for file in filesJson:
            with open(file, "r") as f:
                data = orjson.loads(f.read())
                for d in data:
                    r = Resource(d["sha1"], True, Metadata.jsonDecoder(d), Type(-1, d["typeName"]))
                    self.archiveResource(r,True)
            bar.next()
            pass
        bar.finish()
       

    def archiveResource(self, resource : Resource, rebuild : Optional[bool] = False) -> bool:
        """Permet d'archiver une ressource

        Parameters:
            resource (Resource): ressource à archiver

        Returns:
            bool: True si la ressource a été créé
            
        """
        #print("On commence l'archive de "+resource.path)
        #self.verifTemp()
        content = None
        e = self.myDb.addExtension(resource.extension)
        fn = self.myDb.addFileName(resource.fileName)
        t = self.myDb.addType(resource.type)
        pn = self.myDb.addPathName(resource.pathName)

        resource.universalMetadata.extension = e
        resource.universalMetadata.fileName = fn
        resource.universalMetadata.pathName = pn
        resource.type = t

        if not self.myDb.resourceExist(resource): 
            if not rebuild:
                resource.universalMetadata.sizeCompressed = self.compressResource(resource)
                
            self.myDb.addResource(resource,True)
        
        folders = self.myDb.addFoldersWithPathName(resource.universalMetadata.pathName)

        if not self.myDb.metadataExist(resource.universalMetadata):
            resource.universalMetadata = self.myDb.addMetadata(resource.universalMetadata)
            self.myDb.addFullTextMetadatas(resource,folders[-1])
            if not rebuild:
                self.writeMetadataInJson(resource)
        else:
            resource.universalMetadata = self.myDb.getMetadataByAllFields(resource.universalMetadata)
        
        
        self.myDb.addFolderMetadata(folders[-1],resource.universalMetadata)
        for folder in folders:
            self.myDb.addFolderPathName(folder,resource.universalMetadata.pathName)

        
        return True

    def createDirectoryResource(self, resource : Resource) -> str:
        """Créer le dossier pour la ressource dans l'archive

        Parameters:
            resource (Resource): ressource où on a besoin de créer son dossier

        Returns:
            String: chemin du dossier de la ressource
        """
        pathResource = Archive.createPathRessourceInArchive(self.pathArchive, resource) #self.pathArchive+"/"+Resource.sha1[0:2]
        if not path.exists(pathResource):
            makedirs(pathResource)
        return pathResource

    def compressResource(self, Resource : Resource) -> bool:
        """Permet de compresser une ressource directement dans l'archive

        Parameters:
            Resource (Resource): ressource à compresser

        Returns:
            bool: True si la ressource a été créé
            
        """
        self.pathTmp = self.pathArchive+"/temp/"

        # Pour ne pas perdre le fichier
        #shutil.copy(Resource.path,self.pathTmp+Resource.sha1+Resource.extension.value)
        
        dirWork = myConfig.getOption(Constants.NAME_OF_SECTION_ARCHIVE, Constants.NAME_OF_DEFAULT_ARCHIVE_DIR)
        dirResource = self.createDirectoryResource(Resource)
        newPath = dirResource+"/"+Resource.sha1+myConfig.getOption(Constants.NAME_OF_SECTION_ARCHIVE, Constants.NAME_OF_DEFAULT_EXTENSION_COMPRESSION)
        os.chdir(os.path.dirname(Resource.path))
       
        with py7zr.SevenZipFile(newPath, 'w') as archive:
            archive.write(Resource.fileName.value+Resource.extension.value)
        pass
        
        # Get the size of the compressed file
        size = os.path.getsize(newPath)

        os.chdir(dirWork)
        return size

    def extractResources(self, metadatas : list[Metadata], path : str) -> bool:
        """Permet d'extraire une liste de ressources
        
        Parameters:
            ressources (list): liste de métadonné à extraire
            path (str): chemin où extraire les ressources
            
            Returns:
                bool: True si la liste a été extraite
                bool: False si la liste n'a pas été extraite
        """
        fileNames = []
        bar = Bar('Processing', max=len(metadatas), suffix='%(index).0f/%(max).0f fichiers extraits')
        for m in metadatas:
            if m.fileName.value in fileNames:
                m.fileName.value = m.fileName.value+"_"+str(fileNames.count(m.fileName.value) + 1)
            if not self.extractResource(m, path):
                return False
            fileNames.append(m.fileName.value)
            bar.next()
        bar.finish()
        return True

    def extractResource(self, m : Metadata, path : str) -> bool:
        """Permet d'extraire une ressource
        
        Parameters:
            r (Resource): ressource à extraire
            path (str): chemin où extraire la ressource
            
        Returns:
            bool: True si la ressource a été extraite
            bool: False si la ressource n'a pas été extraite
        """
        try:
            pathOfResource = self.pathArchive+"/"+m.sha1[0:2]+"/"+m.sha1+myConfig.getOption(Constants.NAME_OF_SECTION_ARCHIVE, Constants.NAME_OF_DEFAULT_EXTENSION_COMPRESSION)
            pathExtraction = path + "/Extraction"
            with py7zr.SevenZipFile(pathOfResource, 'r') as archive:
                archive.extractall(pathExtraction)

            #change the name of the file
            #os.rename(path+"/"+m.sha1+m.extension.value, path+"/"+m.fileName.value+m.extension.value)

            Metadata.addMetadataInRessource(path+"/"+m.sha1+m.extension.value, m)
            return True
        except Exception as e:
            print(e)
            return False
            
    def duplicateResourceToOtherArchive(self, Resource : Resource, Archive : Archive) -> bool:
        """Duplique le fichier depuis l'archive source vers l'archive destination
        
        Parameters:
            Resource (Resource): ressource à dupliquer
            Archive (Archive): archive destination
            
        Returns:
            bool: True si la ressource a été dupliquée
            bool: False si la ressource n'a pas été dupliquée
        """
        try:
            pathOldFile = self.pathArchive+"/"+Resource.sha1[0:2]+"/"+Resource.sha1+myConfig.getOption(Constants.NAME_OF_SECTION_ARCHIVE, Constants.NAME_OF_DEFAULT_EXTENSION_COMPRESSION)
            pathNewDirectory = Archive.pathArchive+"/"+Resource.sha1[0:2]
            pathNewFile = pathNewDirectory+"/"+Resource.sha1+myConfig.getOption(Constants.NAME_OF_SECTION_ARCHIVE, Constants.NAME_OF_DEFAULT_EXTENSION_COMPRESSION)
            if not path.exists(pathNewDirectory):
                makedirs(pathNewDirectory)
                #chmod(pathNewDirectory, 0o664)
            
            shutil.copy(pathOldFile, pathNewFile)
            return True
        except Exception as e:
            print(e)
            return False
    
    def mergeTwoArchive(self, archive : Archive) -> Archive:
        """Permet de fusionner deux archives
        
        Parameters:
            archive (Archive): archive à fusionner
            
        Returns:
            Archive: archive fusionnée
        """

        LIMIT = 10

        resources = []
        metadatas = []
        offset = 0

        bddA : Bdd = self.myDb
        bddB : Bdd = archive.myDb

        bddA.askToInsertExtensionsWithOtherDb(bddB.pathFile)
        bddA.askToInsertFileNameWithOtherDb(bddB.pathFile)
        bddA.askToInsertFolderNameWithOtherDb(bddB.pathFile)
        bddA.askToInsertPathNameWithOtherDb(bddB.pathFile)
        bddA.askToInsertTypeWithOtherDb(bddB.pathFile)

        # Ajout des ressources        
        resources = bddB.getAllResources(LIMIT, offset)
        while len(resources) > 0:
            
            for r in resources:
                # Récupération du nouveau type_id
                #r.type = self.myDb.getTypeByName(r.type)
                #r.path = archive.pathArchive + "/" + r.sha1[0:2] + "/" + r.sha1
                r, added = bddA.addResource(r)
                if added:
                    archive.duplicateResourceToOtherArchive(r, self)


            offset += LIMIT
            resources = bddB.getAllResources(LIMIT, offset)

        # Ajout des métadonnées
        offset = 0
        metadatas = bddB.getAllMetadatas(LIMIT, offset)
        while len(metadatas) > 0:
            for m in metadatas:
                m = self.getNewIdsMetadata(m)
                m, added = bddA.addMetadata(m,True)
                if added:
                    r = archive.myDb.getResourceBySha1(m.sha1)
                    r.universalMetadata = m
                    bddA.addFullTextMetadatas(r, FolderName(-1,m.pathName.value.rsplit("/",1)[1]))
                    archive.writeMetadataInJson(r, self)
                    
            offset += LIMIT
            metadatas = bddB.getAllMetadatas(LIMIT, offset)
        
        # Ajout des liaisons folderName metadata
        offset = 0
        folderNameMetadata = bddB.getAllFolderNameMetadata(LIMIT, offset)
        while len(folderNameMetadata) > 0:
            for fn, m in folderNameMetadata:
                fn = bddA.getFolderNameByName(fn)
                m = self.getNewIdsMetadata(m)
                m = bddA.getMetadataByAllFields(m)
                bddA.addFolderNameIdMetadataId(fn.id, m.id)
            offset += LIMIT
            folderNameMetadata = bddB.getAllFolderNameMetadata(LIMIT, offset)
                

        # Ajout des liaisons folderName PathName
        offset = 0
        folderNamePathName = bddB.getAllFolderNamePathName(LIMIT, offset)
        while len(folderNamePathName) > 0:
            for fn, pn in folderNamePathName:
                fn = bddA.getFolderNameByName(fn)
                pn = bddA.getPathNameByPath(pn)
                bddA.addFolderNameIdPathNameId(fn.id, pn.id)
            offset += LIMIT
            folderNamePathName = bddB.getAllFolderNamePathName(LIMIT, offset)
    
    def getNewIdsMetadata(self, m : Metadata) -> Metadata:
        """Permet de récupérer les nouvelles ids contenu dans la classe Metadata
        Parameters:
            m (Metadata): La metadata à traiter
        Returns:
            Metadata: La metadata avec les nouvelles ids
        """
        m.extension = self.myDb.getExtensionByName(m.extension)
        m.pathName = self.myDb.getPathNameByPath(m.pathName)
        m.fileName = self.myDb.getFileNameByName(m.fileName)
        return m 

    def search(self, options : dict) -> list:
        """Permet de rechercher des ressources dans l'archive
        
        Parameters:
            options (dict): options de recherche
            
        Returns:
            list: liste des ressources trouvées
        """          
        return self.myDb.search(options)

    def searchFullText(self, options : str) -> list:
        """Permet de rechercher des ressources dans l'archive de façon fulltext
        
        Parameters:
            options (dict): options de recherche
            
        Returns:
            list: liste des ressources trouvées
        """          
        return self.myDb.searchFullText(options)

    def saveToExtract(self, ressources : list) -> bool:
        """Permet de sauvegarder des ressources pour l'extraction
        
        Parameters:
            ressources (list): liste des ressources à sauvegarder pour l'extraction
            
        Returns:
            Bool : True si la sauvegarde a réussi
            Bool : False si la sauvegarde a échoué
        """
        try:
            
            arrayToStore = []
            for r in ressources:
                arrayToStore.append(r.universalMetadata)
            
            file_to_store = open(self.pathArchive+"/ressourcesToExtract.txt", "wb")
            pickle.dump(arrayToStore, file_to_store)
            file_to_store.close()
            
            return True
        except Exception as e:
            print(e)
            return False
    
    def loadFromFileToExtract(self) -> list:
        """Permet de charger les ressources à extraire depuis le fichier ressourcesToExtract.pickle
        
        Returns:
            list: liste des ressources à extraire
            list: liste vide si impossible de charger le fichier
        """
        try:
            file_to_load = open(self.pathArchive+"/ressourcesToExtract.txt", "rb")
            metadatas = pickle.load(file_to_load)
            file_to_load.close()
            # delete the file
            remove(self.pathArchive+"/ressourcesToExtract.txt")
            return metadatas
        except Exception as e:
            print(e)
            return []

    def getResourceBySha1WithMetadataById(self, sha1 : str, id : int) -> Resource:
        """Permet de récupérer une ressource avec ses métadonnées à partir de son sha1 et de son id
        
        Parameters:
            sha1 (str): sha1 de la ressource
            id (int): id de la metadata
            
        Returns:
            Resource: ressource trouvée
        """
    
        return self.myDb.getResourceBySha1WithMetadataById(sha1, id)

    @staticmethod
    def createPathRessourceInArchive(pathOfArchive : str, Resource : Resource) -> str:
        """Crée le chemin d'accès à la ressource dans l'archive
        
        Parameters:
            pathOfArchive (str): chemin d'accès à l'archive
            Resource (Resource): ressource à créer
            
        Returns:
            str: chemin d'accès à la ressource
        """
        return pathOfArchive+"/"+Resource.sha1[0:2]


