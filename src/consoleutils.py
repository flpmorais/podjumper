import subprocess
import getpass


class LogOptions:
    Silent = 1
    Normal = 2
    Verbose = 3


class LogType:
    Console = 1
    File = 2

LOG_OPTIONS = ['VERBOSE', 'SILENT']

class ConsoleUtils:
    def __init__(self, logOptions, logType, logfile =""):
        self.__logOptions = logOptions
        self.__logType = logType
        if logType == LogType.File:
            if logfile == "":
                self.__logfile = "podjumper_log.txt"
            else:
                 self.__logfile = logfile

            ConsoleUtils.run("logtrace" + ">" + self.__logfile)
            
    
    def log(self, log, logLevel):
        if logLevel >= self.__logOptions:
            if self.__logType == LogType.File:
                ConsoleUtils.run(log + ">>" + self.__logfile)
            else:
                print(log)
        

    def run(cmd):
        return subprocess.run(
            cmd,
            shell=True,
            capture_output = True
        )

    def runsafe(cmd):
        res = ConsoleUtils.run(cmd)
        
        if res.returncode != 0:
            raise Exception("Failed to run command: " + cmd)
        else:
            return res

    def requestUserPass(passwordLabel):
        secret = getpass.getpass(passwordLabel + ":")
        secretRepeat = getpass.getpass("Repeat " + passwordLabel + ":")

        if secret != secretRepeat:
            print("Strings do not match. Try again.")
            return ConsoleUtils.requestUserPass(passwordLabel)
        else:
            return secret