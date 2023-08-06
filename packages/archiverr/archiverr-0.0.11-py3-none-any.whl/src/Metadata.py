'''
AUTEUR : Théo Hurlimann
LIEU : CFPT Informatique Genève
DATE : avril 2022
PROJET: ARCHIVER
VERSION : 1.0
FICHIER : Metadata.py
    Classe FolderName :
        Permet de stocker les métadonnées d'un fichier, contient diverse fonctions les concernant
'''
from src.Extension import Extension
from src.FileName import FileName
from src.PathName import PathName
from src.Type import Type
import src.Metadata as Metadata

from src import Constants

from os import stat, path
from datetime import datetime
from time import mktime


from numpy import double


class Metadata():
    """Classe contenant les métadonnées d'un fichier, ainsi que certaines fonctions permettant de les manipuler"""
    
    def __init__(self, fileName : FileName, extension : Extension, creationDate : int, modificationDate : int, sizeCompressed : int, sizeUncompressed : int, pathName : PathName,sha1 : str, id : int = None, createdAt : int = None) -> None:
        """Constructeur de la classe Metadata

        Parameters:
            fileName (FileName): Le nom du fichier
            extension (Extension): L'extension du fichier
            creationDate (int): La date de création du fichier
            modificationDate (int): La date de modification du fichier
            sizeCompressed (int): La taille du fichier compressé
            sizeUncompressed (int): La taille du fichier non compressé
            pathName (PathName): Le chemin du fichier
            sha1 (str): Le sha1 du fichier
            id (int, optional): L'id de la métadonnée. Par défaut : None.
            createdAt (int, optional): La data d'ajout dans l'archive. Par défaut : None.
        """
        self.id : int = id
        self.fileName : FileName = fileName 
        self.extension : Extension = extension
        self.creationDate : int = creationDate
        self.modificationDate : int = modificationDate 
        self.sizeCompressed : int = sizeCompressed
        self.sizeUncompressed : int = sizeUncompressed
        self.pathName : PathName = pathName
        if createdAt is None:
            self.createdAt : datetime = datetime.now().timestamp()
        else:
            self.createdAt : datetime =  createdAt 
        self.sha1 : str = sha1
        pass
    
    @property
    def getSizeUnCompressedInKo(self) -> int:
        """
        Permet de récupérer la taille du fichier non compressé en Ko.
        Returns:
            int: La taille du fichier non compressé en Ko
        """
        return ("%.2f" % (self.sizeUncompressed / 1024))
    
    @property
    def getCreationDateInString(self) -> str:
        """
        Permet de récupérer la date de création du fichier en string.
        Returns:
            str: La date de création du fichier en string
        """
        return datetime.fromtimestamp(self.creationDate).strftime('%d/%m/%Y')
    @property
    def getModificationDateInString(self) -> str:
        """
        Permet de récupérer la date de modification du fichier en string.
        Returns:
            str: La date de modification du fichier en string
        """
        return datetime.fromtimestamp(self.modificationDate).strftime('%d/%m/%Y')

    @property
    def getCreatedAtInString(self) -> str:
        """
        Permet de récupérer la date de création du fichier en string.
        Returns:
            str: La date de création du fichier en string
        """
        return datetime.fromtimestamp(self.createdAt).strftime('%d/%m/%Y')
    @staticmethod
    def convertDateInTimeStamp(date : str) -> int:
        '''
        Permet de convertir une date en timestamp
        
        Parameters:
            - date: la date à convertir (YY/MM/DD)
        
        Returns:
            - le timestamp correspondant à la date
        '''
        return int(mktime(datetime.strptime(date, "%Y/%m/%d").timetuple()))

    @staticmethod
    def convertTimeStampInDate(timestamp : int) -> str:
        '''
        Permet de convertir un timestamp en date
        
        Parameters:
            - timestamp: le timestamp à convertir
        
        Returns:
            - la date correspondant au timestamp
        '''
        return datetime.fromtimestamp(timestamp).strftime('%Y/%m/%d')

    @staticmethod
    def convertOctetToKiloOctet(size : int) -> float:
        '''
        Permet de convertir une taille en kilo-octet
        
        Parameters:
            - size: la taille à convertir
        
        Returns:
            - la taille en kilo-octet
        '''
        return size/1024

        

    @staticmethod
    def convertSizeToOctet(sizeToConvert, unit):
        '''
        Permet de convertir une taille en octet
        
        Parameters:
            - sizeToConvert: la taille à convertir
            - unit: l'unité de la taille à convertir
        
        Returns:
            - la taille convertie en octet
        '''

        match unit:
            case "O":
                size  =  double(sizeToConvert)
            case "KO":
                size  = double(sizeToConvert) * 1000
            case "MO":
                size  = double(sizeToConvert) * 1000 * 1000
            case "GO":
                size  = double(sizeToConvert) * 1000 * 1000 * 1000
            case "TO":
                size  = double(sizeToConvert) * 1000 * 1000 * 1000 * 1000

        return size
    
    
    @staticmethod
    def getCreationDate(p) -> int:
        '''
        Permet de récupérer la date de création d'un fichier
    
        Returns:
            - la date de création du fichier en format timestamp
        '''
        file = stat(p)
        try:
            return file.st_ctime
        except AttributeError:
            # Nous sommes probablement sous Linux. Pas de moyen pour obtenir la date de création, que la dernière date de modification.
            return file.st_mtime
        #return path.getctime(self.path)
    
    @staticmethod
    def getModificationDate(p) -> int:
        '''
        Permet de récupérer la date de modification d'un fichier
    
        Returns:
            - la date de modification du fichier
        '''
        return stat(p).st_mtime
    
    @staticmethod
    def getSizeUncompressed(p) -> int:
        '''
        Permet de récupérer la taille d'un fichier
    
        Returns:
            - la taille du fichier
        '''
        return path.getsize(p)
    

    @staticmethod
    def deleteMetadataInResource(p) -> None:
        '''
        Permet de supprimer les métadonnées d'un fichier

        Parameters:
            - p: le chemin du fichier
        '''
        try:
            stat(p).st_mtime = 0
            stat(p).st_ctime = 0
        except:
            pass

    @staticmethod
    def addMetadataInRessource( p, m : Metadata) -> None:
        '''
        Permet d'ajouter les métadonnées d'un fichier

        Parameters:
            - p: le chemin du fichier
        '''
        try:
            stat(p).st_mtime = m.modificationDate
            stat(p).st_ctime = m.creationDate
        except:
            pass

    @staticmethod
    def jsonDecoder(metadataDict : dict) -> Metadata:
        '''
        Permet de décoder un dictionnaire en objet Metadata

        Parameters:
            - dict: le dictionnaire à décoder
        
        Returns:
            Metadata: l'objet Metadata correspondant au dictionnaire
        '''
        return Metadata(FileName(-1,metadataDict["fileName"]), Extension(-1,metadataDict["extension"]), metadataDict["creationDate"], metadataDict["modificationDate"], metadataDict["sizeCompressed"], metadataDict["sizeUncompressed"], PathName(-1,metadataDict["pathName"]), metadataDict["sha1"], metadataDict["id"], metadataDict["createdAt"])



    def toJson(self, t : Type) -> str:
        """Permet de convertir un objet Metadata en json

        Parameters:
            - r: l'objet Resource associé au fichier pour enregistrer son type

        Returns:
            str: La metadata convertie en format json
        """
        return '{"typeName": "' + str(t.value) + '", "id": "' + str(self.id) + '", "fileName": "'+ str(self.fileName if type(self.fileName) is str else self.fileName.value)+'", "extension": "'+str(self.extension if type(self.extension) is str else self.extension.value) +'", "creationDate": "'+ str(self.creationDate)+'", "modificationDate": "'+ str(self.modificationDate)+'", "sizeCompressed": "'+str(self.sizeCompressed)+'", "sizeUncompressed": "'+ str(self.sizeUncompressed)+'", "createdAt": "'+ str(self.createdAt)+'", "pathName": "'+ str(self.pathName if type(self.pathName) is str else self.pathName.value)+'", "sha1": "'+self.sha1+'"}'

    def __str__(self) -> str:
        return "Metadata : "+self.fileName+" "+str(self.size)+" "+self.extension+" "+str(self.creationDate)+" "+str(self.modificationDate) + " " + str(self.sha1)

    def __eq__(self, other : Metadata) -> bool:
        return self.id == other.id
        #return self.fileName == other.fileName and self.extension == other.size and self.extension == other.extension and self.creationDate == other.creationDate and self.modificationDate == other.modificationDate and self.sha1 == other.sha1

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)