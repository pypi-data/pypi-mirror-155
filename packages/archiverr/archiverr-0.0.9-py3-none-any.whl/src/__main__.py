"""
AUTEUR : Théo Hurlimann
LIEU : CFPT Informatique Genève
DATE : avril 2022
PROJET: ARCHIVER
VERSION : 1.0
FICHIER : __main__.py
    Contient le programme principal
"""
from src import myConfig
#from src import commands
from src.Utilities import Utilities
from src.Resource import Resource
from src.FolderImport import FolderImport
from src.Archive import Archive
import src.Constants as Constants

from toml import load
from datetime import datetime, timezone
from time import mktime
import getopt
import sys
from os import system
from os.path import exists, abspath, isdir, isfile

def main():
    """
    Main function of Archiver.
    """

    # Chargement du fichier commands.toml
    commands = load(open(Constants.NAME_OF_COMMANDS_FILE))

    # Récupération des arguments sans l'exécutable
    values = sys.argv[1:]
    
    
    # Options
    lstCommands = commands["commands"]["names"]
 

    # Long options
    #options = commands["commands"]["long_options"]


    try:
        #arguments, values = getopt.getopt(values,lstCommands) #options

        #Vérification des de l'existance de la commande et si elle est valide
        if len(values) == 0 or values[0] not in lstCommands:
            Utilities.displayManPage()
            sys.exit(0)
        
        currentCmd = values[0]

        #region Commande new
        if currentCmd == commands["new"]["name"]:
            # Récupère le nom caché du dossier de l'archive
            nameHidden = Utilities.getHiddenArchiveName(values[1])
            if Utilities.checkIfArchiveExist(nameHidden):
                raise Exception(Constants.MESSAGE_ARCHIVE_ALREADY_EXIST)
            Archive(nameHidden)
        #endregion Commande new
        
        #region Commande import
        elif currentCmd == commands["import"]["name"]:
            Utilities.checkCurrentArchive()
            absPath = abspath(values[1])
            nameOfArchive = myConfig.getOption(
                Constants.NAME_OF_SECTION_ARCHIVE, Constants.NAME_OF_CURRENT_ARCHIVE_NAME)

            Utilities.checkPath(absPath)
            if not exists(absPath):
                raise Exception(Constants.MESSAGE_FOLDER_FILE_DOES_NOT_EXIST)
            if isdir(absPath):
                Archive(nameOfArchive).archiveFolder(FolderImport(absPath))

            elif isfile(absPath):
                Archive(nameOfArchive).archiveResource(
                    Resource(absPath, False))
        #endregion Commande import
        
        #region Commande merge
        elif currentCmd == commands["merge"]["name"]:
            Utilities.checkCurrentArchive()
            nameHidden1 = myConfig.getOption(
                Constants.NAME_OF_SECTION_ARCHIVE, Constants.NAME_OF_CURRENT_ARCHIVE_NAME)
            nameHidden2 = Utilities.getHiddenArchiveName(values[1])

            if not Utilities.checkIfArchiveExist(nameHidden1):
                raise Exception(Constants.MESSAGE_ARCHIVE_FIRST_DOES_NOT_EXIST)

            if not Utilities.checkIfArchiveExist(nameHidden2):
                raise Exception(
                    Constants.MESSAGE_ARCHIVE_SECOND_DOES_NOT_EXIST)

            Archive(nameHidden1).mergeTwoArchive(Archive(nameHidden2))
        #endregion Commande merge

        #region Commande search
        elif currentCmd == commands["search"]["name"]:
            Utilities.checkCurrentArchive()
            extract = False
            resources = []
            # On enlève le premier élément de la liste, car c'est le nom de la commande
            values.pop(0)
            typeSearch = values.pop(0)

            if len(values) > 0 and values[0] == "--extract":
                values.pop(0)
                extract = True
                pathToExtract = abspath(values.pop(0))
                

                                 
            myArchive = Archive(myConfig.getOption(Constants.NAME_OF_SECTION_ARCHIVE, Constants.NAME_OF_CURRENT_ARCHIVE_NAME))

            match typeSearch:
                case "--fullText":
                    filters = ""
                    if len(values) > 0:
                        filters = ''.join(values)
                        resources = myArchive.searchFullText(filters)
                case "--simple":
                    filters = dict()
                    # On vérifie si l'utilisateur a bien renseigné un ou plusieurs filtres et on les récupère
                    if len(values) != 0:
                        filters = dict(x.split(':') for x in values)
                    resources = myArchive.search(filters)
                    
            if extract:
                metadatas = []
                for r in resources:
                    metadatas.append(r.universalMetadata)

                myArchive.extractResources(metadatas,pathToExtract)
            else:
                # On enregistre les ids des métadonnées pour une futur extraction
                myArchive.saveToExtract(resources)
                Utilities.displayResources(resources)

        #endregion Commande search

        #region Commande extract
        elif currentCmd == commands["extract"]["name"]:
            Utilities.checkCurrentArchive()
            metadatas = []
            absPath = abspath(values[0])
            nameOfArchive = myConfig.getOption(
                Constants.NAME_OF_SECTION_ARCHIVE, Constants.NAME_OF_CURRENT_ARCHIVE_NAME)
            myArchive = Archive(nameOfArchive)
            metadatas = myArchive.loadFromFileToExtract()
            #metadatas = myArchive.myDb.getMetadatasByIds(metadataIds)
            myArchive.extractResources(metadatas,absPath)
            pass
        #endregion Commande extract

        #region Commande select
        elif currentCmd == commands["select"]["name"]:
            nameHidden = Utilities.getHiddenArchiveName(values[1])
            if not Utilities.checkIfArchiveExist(nameHidden):
                raise Exception(Constants.MESSAGE_ARCHIVE_DOES_NOT_EXIST)
            myConfig.setOption(Constants.NAME_OF_SECTION_ARCHIVE, Constants.NAME_OF_CURRENT_ARCHIVE_NAME, nameHidden)
            pass
        #endregion Commande select
        
        #region Commande help
        elif currentCmd == commands["help"]["name"]:
            nameOfCmd = ""

            # On vérifie si l'utilisateur veut une commande particulière
            if len(values) != 0:
                nameOfCmd = values[0]
            Utilities.displayManPage(nameOfCmd)
        #endregion Commande help

        #region Commande serve
        elif currentCmd == commands["serve"]["name"]:
            Utilities.checkCurrentArchive()
            Utilities.startServer()
            pass
        #endregion Commande serve

        #region Commande list
        elif currentCmd  == commands["list"]["name"]:
            for archive in Utilities.listArchivesInFolder():
                print(archive)
            pass
        #endregion Commande list

        #region Commande doctor
        elif currentCmd == commands["doctor"]["name"]:
            myArchive = Archive(myConfig.getOption(Constants.NAME_OF_SECTION_ARCHIVE, Constants.NAME_OF_CURRENT_ARCHIVE_NAME))
            myArchive.rebuildDbWithJson()
            pass

    except Exception as err: #Exepction
        # output error, and return with an error code
        Utilities.displayManPage()
        if err != None:
            print(err)
            sys.exit() 
        else:
            
            sys.exit()
        pass






