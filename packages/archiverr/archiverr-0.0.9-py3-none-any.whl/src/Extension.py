'''
AUTEUR : Théo Hurlimann
LIEU : CFPT Informatique Genève
DATE : avril 2022
PROJET: ARCHIVER
VERSION : 1.0
FICHIER : Extension.py
    Classe Extension :
        Classe enfant de ClassIdName, contient la fonction getExtension
'''

from src.ClassIdName import ClassIdName
from os import path
class Extension(ClassIdName):
    """Classe enfant de ClassIdName, contient la fonction getExtension"""
    @staticmethod
    def getExtension(p) -> str:
        '''
        Permet de récupérer l'extension d'un fichier

        Returns:
            str: L'extension du fichier   
        '''
        return path.splitext(p)[1]

