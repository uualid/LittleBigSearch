from os import path
from Settings.OptionsController import Options

class OptionsManager():
    def __init__(self) -> None:
        
        self.archivePath = ""
        self.RPCS3Path   = ""
        self.includeDups = False
        self.includeDescription = True

    
    # protocols ________________________________
    def toggleDuplicatesProtocol(self):
        self.includeDups = True if self.includeDups == False else False
    def toggleIncludeDescriptionProtocol(self):
        self.includeDescription = True if self.includeDescription == False else False
    def archivePathProtocol(self, path):
        self.archivePath = path
    def RPCS3PathProtocol(self, path):
        self.RPCS3Path = path

    def fetchSettingCallBack(self, archive, RPCS3, dupsStatus, includeDescription):
        self.archivePath = archive
        self.RPCS3Path   = RPCS3
        self.includeDups = dupsStatus
        self.includeDescription = includeDescription
    
    # __________________________________________

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