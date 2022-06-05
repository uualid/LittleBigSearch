from optparse import OptionContainer
from os import path
from Settings.OptionsController import Options

class OptionsManager():
    def __init__(self, errorCallback) -> None:
        
        self.errorCallback = errorCallback
        
        self.archivePath = ""
        self.RPCS3Path   = ""
        self.includeDups = False
        self.includeDescription = True
        self.heartedLevelPaths = [] # this is used to know what level is hearted so it can show or hide the heart png when it loads
        

    
    # protocols ________________________________
    def toggleDuplicatesProtocol(self):
        self.includeDups = True if self.includeDups == False else False
    def toggleIncludeDescriptionProtocol(self):
        self.includeDescription = True if self.includeDescription == False else False
    def archivePathProtocol(self, path):
        self.archivePath = path
    def RPCS3PathProtocol(self, path):
        self.RPCS3Path = path
        self.fetchHeatedPaths(path)

    def fetchSettingCallBack(self, archive, RPCS3, dupsStatus, includeDescription):
        self.archivePath = archive
        self.RPCS3Path   = RPCS3
        self.includeDups = dupsStatus
        self.includeDescription = includeDescription
        self.fetchHeatedPaths(RPCS3)
    
    # __________________________________________
    
    def fetchHeatedPaths(self, path):
        self.heartedLevelPaths = Options.getHeartedLevels(self, path)
        if self.heartedLevelPaths == None:
            self.errorCallback("An error occurred when tried to open one of the saved paths. Try selecting paths again.")
    
    def addHeartedLevel(self, path, clearPath = False):
        folderName = path
        if clearPath:
            folderName = path[len(self.RPCS3Path) + 1:]
        self.heartedLevelPaths.append(folderName)
        
    def removeHeartedLevel(self, path, clearPath = False):
        folderName = path
        if clearPath:
            folderName = path[len(self.RPCS3Path) + 1:]
        self.heartedLevelPaths.remove(folderName)
        
    
    def fetchSettings(self):
        if path.exists("SavedSettings.json"):
            Options.getSettingsFromJSON(self.fetchSettingCallBack)
        else:
            print("No saved settings.")

    # _____________________________________________
    def openSettings(self, master):
        try:
            self.settings.window.lift()
        except: 
            self.settings = Options(includeDescriptionDelegate = self.toggleIncludeDescriptionProtocol,
                                    duplicatesDelegate         = self.toggleDuplicatesProtocol,
                                    archiveDelegate            = self.archivePathProtocol,
                                    RPCS3Delegate              = self.RPCS3PathProtocol,
                                    currentArchivePath         = self.archivePath,
                                    currentRPCS3Path           = self.RPCS3Path,
                                    includeDescriptionStatus   = self.includeDescription,  
                                    duplicatesStatus           = self.includeDups,
                                    master=master)