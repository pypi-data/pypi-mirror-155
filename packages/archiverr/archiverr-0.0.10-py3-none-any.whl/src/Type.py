'''
AUTEUR : Théo Hurlimann
LIEU : CFPT Informatique Genève
DATE : avril 2022
PROJET: ARCHIVER
VERSION : 1.0
FICHIER : Type.py
    Classe Type :
        Classe enfant de ClassIdName, contient la fonction getType
'''
import magic
from src.ClassIdName import ClassIdName
class Type(ClassIdName):
    """"Classe enfant de ClassIdName, contient la fonction getType"""
    
    @staticmethod
    def getType(p : str) -> str:
        """Permet de récupérer le type d'un fichier

        Parameters:
            p (str): Le chemin du fichier

        Returns:
            str: Le type du fichier
        """
        return magic.from_file(p,mime=True).split("/")[0]