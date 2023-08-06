'''
AUTEUR : Théo Hurlimann
LIEU : CFPT Informatique Genève
DATE : avril 2022
PROJET: ARCHIVER
VERSION : 1.0
FICHIER : Config.py
    Classe Config : 
        Classe qui permet de gérer le fichier de configuration
'''
from configparser import ConfigParser

import src.Constants as Constants
from os import path, getcwd
class Config:
    """Classe config qui permet de gérer le fichier de configuration"""
    def __init__(self):
        """Constructeur de la classe Config"""
        self.config = ConfigParser()
        self.configFile = Constants.NAME_OF_CONFIG_FILE
        # if the getcwd end with "flask_app"
        # then we are in the flask_app folder
        # and we need to go up one level
        if getcwd().endswith("flask_app"):
            # remove the last two folders
            self.configPath =  self.configFile
        else:
            self.configPath = self.configFile
        
        if not path.isfile(self.configPath):
            self.__initSectionsAndOptions()

        self.config.read(self.configPath)
        pass

    def getOption(self, section, option):
        """Permet de récupérer une option dans la section spécifiée

        Parameters:
            section (Str): La section dans laquelle on cherche l'option
            option (Str): L'option à récupérer

        Returns:
            Str: La valeur de l'option
        """
        return self.config.get(section, option)
    
    def setOption(self, section, option, value):
        """Permet de modifier une option dans la section spécifiée

        Parameters:
            section (str): La section dans laquelle on cherche l'option
            option (str): L'option à modifier
            value (str): La nouvelle valeur de l'option
        """
        self.config.set(section, option, value)
        self.__updateConfig()
        pass

    def __initSectionsAndOptions(self):
        """Permet d'initialiser les sections et les options du fichier de configuration"""
        for section in Constants.DICT_OF_CONFIG_SECTIONS:
            if not self.config.has_section(section):
                self.__addSection(section)
            for option in Constants.DICT_OF_CONFIG_SECTIONS[section]:
                if not self.config.has_option(section, option):
                    self.setOption(section, option, Constants.DICT_OF_CONFIG_SECTIONS[section][option])
        self.__updateConfig()
        
        pass

    def __addSection(self, section):
        """Permet d'ajouter une section au fichier de configuration"""
        self.config.add_section(section)
        pass

    def __updateConfig(self):
        """Permet de mettre à jour le fichier de configuration"""
        with open(self.configPath, 'w') as configfile:
            self.config.write(configfile)
        self.config.read(Constants.NAME_OF_CONFIG_FILE)
        pass