# import pyyaml module
import yaml
from yaml.loader import SafeLoader
from consoleutils import ConsoleUtils

class Config:
    def __init__(self, file):
        with open(file) as f:
            self.__data  = yaml.load(f, Loader=SafeLoader)

    def getSecrets(self):
        return self.__data["secrets"]
    
    def getName(self):
        return self.__data["name"]


