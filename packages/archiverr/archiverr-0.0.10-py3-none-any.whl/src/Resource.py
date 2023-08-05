'''
AUTEUR : Théo Hurlimann
LIEU : CFPT Informatique Genève
DATE : avril 2022
PROJET: ARCHIVER
VERSION : 1.0
FICHIER : Resource.py
    Classe Resource :
        Classe contenant un sha1 et une ou des métadonnées
'''
from src.Metadata import Metadata
from src.Extension import Extension
from src.PathName import PathName
from src.FileName import FileName
from src.Type import Type
from datetime import datetime
import hashlib
import json

'''
import shutil
import time
import py7zr
'''


class Resource():

    def __init__(self, p, isCompressed, m: Metadata = None, type : Type = None) -> None:
        """Constructeur de la classe Resource

        Parameters:
            p (_type_): Chemin du fichier
            isCompressed (bool): Indique si le fichier est compressé
            m (Metadata, optional): Metadata appartenant à la resource. Defaults to None.
            type (Type, optional): Type de la resource. Defaults to None.
        """
        self.path = p
        #self.allMetadatas = []
        
        #self.mime = None
        self.universalMetadata = None

        # Ce champs sert à la fusion pour stocker toutes les métadonnées appartenant à la même ressource
        self.allMetadatas = []
        if not isCompressed:
            self.sha1 = self.__getSha1(self.path)
            self.type = Type(-1, Type.getType(self.path))
            self.universalMetadata = Metadata(
                FileName(-1, FileName.getFileName(self.path)), 
                Extension(-1, Extension.getExtension(self.path)), 
                Metadata.getCreationDate(self.path), 
                Metadata.getModificationDate(self.path), 
                0,#Metadata.getSizeCompressed(self.path), 
                Metadata.getSizeUncompressed(self.path),
                PathName(-1, PathName.getPathName(self.path)),
                self.sha1) 
            #self.allMetadatas.append(m)
            Metadata.deleteMetadataInResource(p)
            self.content = self.__getContent()
        else:
            self.sha1 = p
            self.type = type
            #self.allMetadatas.append(m)
            self.universalMetadata = m
        pass

    def __getContent(self) -> str:
        """Permet de récupérer le contenu d'un fichier de type text

        Returns:
            str: Retourne le contenu du fichier
        """
        if self.typeName == "text":
            #with open(self.path, 'r') as f:
            #    return f.read()
            data = ""
            f = open(self.path, 'r')
            while True: # from   w  w w  .j av a  2  s  .c o  m
                chunk = f.read(1000)       # Read byte chunks: up to 10 bytes 
                if not chunk: break 
                data += chunk
            f.close()
            return data

        else:
            return ""

    def __getSha1(self, fileName) -> str:
        """Permet de récupérer le sha1 d'un fichier

        Parameters:
            fileName (_type_): _description_

        Returns:
            str: _description_
        """
        sha1 = hashlib.sha1()
        with open(fileName, 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                sha1.update(data)
        return sha1.hexdigest()


    def __getattr__(self, attr : str):
        """Permet de récupérer les attributs d'un objet Resource

        Parameters:
            attr (str): Nom de l'attribut

        Returns:
            object: Retourne l'attribut
        """
        match attr:
            case "typeName":
                return self.type.value
            case "fileName":
                return self.universalMetadata.fileName
            case "pathName":
                return self.universalMetadata.pathName
            case "sizeUncompressed":
                return self.universalMetadata.sizeUncompressed
            case "extension":
                return self.universalMetadata.extension
            case "creationDate":
                return self.universalMetadata.creationDate
            case "modificationDate":
                return self.universalMetadata.modificationDate
            case "createdAt":
                return self.universalMetadata.createdAt

    def __eq__(self, other) -> bool:
        """Permet de comparer deux objets Resource

        Parameters:
            other (Resource): L'objet à comparer

        Returns:
            bool: Retourne True si les objets sont égaux
        """
        return self.sha1 == other.sha1

    def __str__(self) -> str:
        """Permet de récupérer la représentation d'un objet Resource
            
        Returns:
            str: Retourne la représentation d'un objet Resource
        """
        return self.path + " : " + self.sha1
