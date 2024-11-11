from consoleutils import ConsoleUtils
from config import Config
from secrets import Secrets
import os



class Controller:
    def __init__(self, file, logOptions):   
        self.__config = Config(file)
        self_cons = ConsoleUtils(logOptions)
        self.__folder = "./podjumper_" + self.__config.getName() + "/"
        self.__secrets = Secrets(self.__config, self.__folder)
        
    def init(self):
        self.initPodjumperFolder()
        self.__secrets.assembleSecretGPGFiles()

    def initPodjumperFolder(self):
        print("Initializing Podjumper directory")
        if not os.path.exists(self.__folder):
            os.mkdir(self.__folder)
            print("Created directory " + self.__folder) 
        else:
            print("Directory already exists")

    def setup(self):
        print("asd")

    def deploy(self):
        print("asd")
    

c = Controller("test.yaml", True)
c.init()

