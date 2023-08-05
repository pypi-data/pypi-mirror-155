'''
AUTEUR : Théo Hurlimann
LIEU : CFPT Informatique Genève
DATE : avril 2022
PROJET: ARCHIVER
VERSION : 1.0
FICHIER : PathName.py
    Classe PathName :
        Classe enfant de ClassIdName, contient la fonction getPathName
'''
from src.ClassIdName import ClassIdName
from os import path

class PathName(ClassIdName): 

    def getFolders(self) -> list:
        '''
        Permet de récupérer les dossiers d'un dossier
        
        Returns:
            - la liste des dossiers
        '''
        return self.value.split("/")


    @staticmethod
    def getPathName(p) -> str:
        """Permet de récupérer le chemin du repertoire du fichier

        Parameters:
            p (str): Le chemin du fichier

        Returns:
            str: Le chemin du dossier
        """
        return path.dirname(p)