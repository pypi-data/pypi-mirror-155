'''
AUTEUR : Théo Hurlimann
LIEU : CFPT Informatique Genève
DATE : avril 2022
PROJET: ARCHIVER
VERSION : 1.0
FICHIER : ClassIdName.py
    Classe ClassIdName : 
        Classe mère des classes contenant seulement un id et une valeur
'''
class ClassIdName: 
    """Classe mère des classes contenant seulement un id et une valeur"""
    def __init__(self, id, value):
        """Constructeur de la classe ClassIdName
        
        Parameters:
            id (int): L'id de la classe
            value (str): La valeur de la classe
        """
        self.id = id
        self.value = value
    def __str__(self):
        """Affichage de la classe ClassIdName

        Returns:
            str: Chaine de caractère représentant la classe. (id, value)) 
        """
        return str(self.id) + " " + self.value

    def toJson(self) -> str:
        try : 
            return '{"id": "'+ str(self.id)+'", "name": "'+self.value+'"}'
        except :
            print("Error in Extension.toJson()")