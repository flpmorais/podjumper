from consoleutils import ConsoleUtils, LogOptions
import glob



class Secrets:
    def __init__(self, config, folder, cons):
        self.__secretDefenitions = config.getSecrets()
        self.__folder = folder
        self.__cons = cons

    def assembleSecretGPGFiles(self):
        self.__cons.log("Assembling secret encrypted source files", LogOptions.Normal)
        missingSecrets = self.__findMissingSecretGPGFiles(self.__folder)
        if missingSecrets:
            self.__createSecretGPGFiles(self.__requestMissingSecrets(missingSecrets))

    
    def __findMissingSecrets(self):
        missingSecrets = {}
        for key in self.__secretDefenitions :
            if not self.secretExists(key):
                missingSecrets[key] = self.__secretDefenitions[key]
        return missingSecrets

    def __secretExists(self, key):
        cmd = ConsoleUtils.run("podman secret inspect " + self.__secretDefenitions[key])
        return cmd.returncode == 0
    
    def __findMissingSecretGPGFiles(self, folder):
        self.__cons.log("Checking which GPG files are missing", LogOptions.Normal)
        missingSecrets = {}
        files = self.__findGPGFilesInFolder()
        for key in self.__secretDefenitions:
            if self.__secretDefenitions[key] not in files:
                self.__cons.log("File " + self.__secretDefenitions[key] + " is missing", LogOptions.Verbose)
                missingSecrets[key] = self.__secretDefenitions[key]
            else: 
                self.__cons.log("File " + self.__secretDefenitions[key] + " found", LogOptions.Verbose)
        return missingSecrets
    
    def __findGPGFilesInFolder(self):
        self.__cons.log("Polling " + self.__folder + " directory for .gpg files", LogOptions.Verbose)
        returnList = []
        files = glob.glob(self.__folder + "*.gpg")
        for f in files:
            returnList.append(f.replace(self.__folder,"").replace(".gpg",""))
        self.__cons.log("found " + len(files) + ".gpg files in directory")
        return returnList



    def __requestMissingSecrets(self, missingSecrets):
        self.__cons.log("Requesting missing secrets.")
        secretsToCreate = {}
        for key in missingSecrets:
            secretsToCreate[self.__secretDefenitions[key]]  = ConsoleUtils.requestUserPass(key)
        return secretsToCreate
        
    def __createSecretGPGFiles(self,secretsToCreate):
        self.__cons.log("creating GPG files.")
        self.__cons.log("Please insert the password to protect the gpg secret files")
        pwd = ConsoleUtils.requestUserPass("Password")
        for key in secretsToCreate:
            self.__createSecretGPGFiles_One(key, secretsToCreate[key], pwd)

    def __createSecretGPGFiles_One(self,secretName, secret, password):
        ConsoleUtils.runsafe("echo " + secret + " > " + self.__folder + secretName)
        ConsoleUtils.runsafe("echo " + password + " | gpg --batch --yes --passphrase-fd 0 -c " + self.__folder + secretName)
        ConsoleUtils.runsafe("rm " + self.__folder + secretName)
        
    def __createSecret(self, secretKey, secret):
        cmd = ConsoleUtils.runsafe("printf \"" + secret + "\" | docker secret create " + self.__secretDefenitions[secretKey] + " -")

    def __readSecret(self, secretKey, password):
        ConsoleUtils.runsafe("echo " + password + " | gpg --batch --yes --passphrase-fd 0 -d " + self.__folder + self.__secretDefenitions[secretKey] + ".gpg").stdout.decode('UTF-8').strip()