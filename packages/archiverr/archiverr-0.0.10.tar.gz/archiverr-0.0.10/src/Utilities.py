'''
AUTEUR : Théo Hurlimann
LIEU : CFPT Informatique Genève
DATE : avril 2022
PROJET: ARCHIVER
VERSION : 1.0
FICHIER : Utilities.py
    Fichier contenant des fontions utiles
'''
from email import utils
import os
from os import chmod, listdir, walk, system, getcwd
from os.path import exists, isdir, isfile, join
from typing import Optional
import src.Constants as Constants
from src import myConfig

class Utilities:
    """Classe contenant des fonctions utiles"""
    @staticmethod
    def startServer():
        """Start the server."""
        path = getcwd()
        os.chdir(Constants.PATH_TO_SERVER)
        print(getcwd())
        system("flask run")
        os.chdir(path)

    @staticmethod
    def displayResources(ressources : list):
        """Display the resources in array.
        
        Parameters
            ressources (list): La liste de ressources à afficher)
        """
        array2d = []
        arrayFirstLine = ["Nom du fichier", "Emplacement", "Taille"]
        array2d.append(arrayFirstLine)
        for r in ressources:
            array = []
            array.append(r.fileName.value)
            array.append(r.pathName.value)
            array.append(str(r.sizeUncompressed))
            array2d.append(array)
        
        print("\nListe des ressources trouvées:")
        for i in array2d:
            for j in i:
                print("|", end=" ")
                print(j, end=" ")
            print()
    @staticmethod
    def displayManPage(nameOfCmd : str=None):
        """Afficher la page d'aide du programme.

        Parameters:
            nameOfCmd (str): Le nom de la commande pour afficher la page d'aide.
        """
        if nameOfCmd is None:
            msg = """ Usage : archiver [COMMAND] [ARGS]

                    Archiver - System for archiving, searching and extraction files and folders

                    Commands:
                        new [ARCHIVE]   Create a new archive
                        import [ARCHIVE] [FOLDER]  Import a folder into an archive
                        merge [ARCHIVE1] [ARCHIVE2]  Merge two archives
                        extract [FOLDER]  Extract an archive into a folder
                        search [KEYWORD]  Search an archive for a keyword
                        update Update an archive
                        choose [ARCHIVE]  Choose an archive to work with
                        man [COMMAND] Displays the man page of a command
                    """
        else:
            match nameOfCmd:
                case "New":
                    msg = "Usage: Archiver -n [ARCHIVE]\n"
                case "Import":
                    msg = "Usage: Archiver -i [ARCHIVE] [FOLDER]\n"
                case "Merge":
                    msg = "Usage: Archiver -m [ARCHIVE1] [ARCHIVE2]\n"
                case "Extract":
                    msg = "Usage: Archiver -e \n"  # @TODO
                case "Search":
                    msg = "Usage: Archiver -s [ARCHIVE] [KEYWORD]\n"  # @TODO
                case "Update":
                    msg = "Usage: Archiver -u [ARCHIVE]\n"  # @TODO
                case "Choose":
                    msg = "Usage: Archiver -c [ARCHIVE]\n"

        print(msg)
        pass

    @staticmethod
    def getPathOfArchive(archiveName):
        """Retourne le dossier de l'archive cachée.
        
        Parameters:
            archiveName (str): Le nom de l'archive.
            
        Returns:
            str: Le chemin de l'archive."""
        return myConfig.getOption(Constants.NAME_OF_SECTION_ARCHIVE, Constants.NAME_OF_DEFAULT_ARCHIVE_DIR) + "/" + archiveName

    @staticmethod
    def checkIfArchiveExist(archiveName):
        """Vérifie si une archive existe.

        Parameters:
            archiveName (_type_): _description_

        Returns:
            _type_: _description_
        """
        pathOfArchive = myConfig.getOption(
            Constants.NAME_OF_SECTION_ARCHIVE, Constants.NAME_OF_DEFAULT_ARCHIVE_DIR) + "/" + archiveName
        if exists(pathOfArchive):
            return True
        else:
            return False

    @staticmethod
    def getHiddenArchiveName(name : str) -> str:
        """Retourne le nom de l'archive cachée.

        Parameters:
            name (str): Le nom de l'archive.

        Returns:
            str: Retourne le nom de l'archive cachée.
        """
        return Constants.HIDDEN_ARCHIVE_PREFIX + name

    @staticmethod
    def getArchiveName(name : str) -> str:
        """Retourne le nom de l'archive.

        Parameters:
            name (str): Le nom de l'archive caché.

        Returns:
            str: Retourne le nom de l'archive.
        """
        return name[len(Constants.HIDDEN_ARCHIVE_PREFIX):]
        return name[1:]

    @staticmethod
    def listArchivesInFolder():
        """Liste les archives dans le dossier d'archive.

        Returns:
            list: Retourne la liste des archives.
        """
        folder = myConfig.getOption(
            Constants.NAME_OF_SECTION_ARCHIVE, Constants.NAME_OF_DEFAULT_ARCHIVE_DIR)
        if not exists(folder):
            raise Exception("Archive folder does not exist")

        if not isdir(folder):
            raise Exception("Folder is not a directory.")
        archives = []
        for folder in listdir(folder):
            archives.append(Utilities.getArchiveName(folder))
        return archives

    @staticmethod
    def checkCurrentArchive():
        """Vérifie si une archive est sélectionnée.

        Raises:
            Exception: Si aucune archive n'est sélectionnée.
            Exception: Si l'archive sélectionnée n'existe pas.
        """
        name = myConfig.getOption(
            Constants.NAME_OF_SECTION_ARCHIVE, Constants.NAME_OF_CURRENT_ARCHIVE_NAME)
        if name == "":
            raise Exception(Constants.MESSAGE_NO_CURRENT_ARCHIVE)
        elif not Utilities.checkIfArchiveExist(name):
            raise Exception(Constants.MESSAGE_ARCHIVE_DOES_NOT_EXIST)
            
    @staticmethod
    def checkPath(path):
        """Vérifie si le chemin existe.

        Parameters:
            path (str): Le chemin à vérifier.

        Raises:
            Exception: Si le chemin n'existe pas.
        """
        if exists(path):
            return True
        return False
