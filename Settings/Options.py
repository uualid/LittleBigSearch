import os, json
import tkinter    as tk
import helpers.Utilities as helpers
from   tkinter    import Button, filedialog

class Options():
    
    def __init__(self, duplicatesStatus, currentArchivePath, currentRPCS3Path, includeDescriptionStatus,
                duplicatesDelegate, archiveDelegate, RPCS3Delegate, includeDescriptionDelegate, master):
        super().__init__()
        
        #___ Delegates __________
        
        self.toggleDuplicatesDelegate   = duplicatesDelegate
        self.archiveDelegate            = archiveDelegate
        self.RPCS3Delegate              = RPCS3Delegate
        self.includeDescriptionDelegate = includeDescriptionDelegate
        #________________________
        
        self.window = tk.Toplevel(background= helpers.GlobalVars.BGColorLight)
        self.window.title("Settings")
        self.window.transient(master)


        self.settingsCanvas = tk.Canvas(master= self.window,
                                height = 20,
                                width  = 850 ,
                                bg=helpers.GlobalVars.BGColorLight, 
                                borderwidth=0,
                                highlightthickness=0)

        self.settingsCanvas.grid(columnspan=3, row= 4)

        self.archiveLabelStr = tk.StringVar()
        self.archiveLabel = tk.Button(self.window,
                                    textvariable     = self.archiveLabelStr,
                                    bg               = helpers.GlobalVars.BGColorLight,
                                    cursor           = "hand2",
                                    activebackground = helpers.GlobalVars.logoBlue,
                                    command          = lambda: helpers.Utilities.openFile(self.archiveLabelStr.get()),
                                    fg               = "White",
                                    bd               = 0,
                                    font             = ('Helvatical bold',10))
                                    
        self.archiveLabel.grid(columnspan=1, column=1, row=0, pady=(20, 0))

        self.archiveBrowseBtn = tk.Button(self.window,
                                    text             ="Browse Archive",
                                    activebackground = helpers.GlobalVars.logoBlue,
                                    command          = lambda: self.openFileBrowser(self.archiveLabelStr, 
                                                                                   title    = "Select LittleBigPlanet level archive", 
                                                                                   delegate = self.archiveDelegate),
                                    bg               = helpers.GlobalVars.logoBlue,
                                    fg               = "white", height=1, width= 20, bd=0)
        self.archiveBrowseBtn.grid(columnspan=1, column=0, row=0, pady=(20, 0))
        #________
        
        self.RPCSLabelStr = tk.StringVar()
        self.RPCSLabel = tk.Button(self.window,
                                    textvariable     = self.RPCSLabelStr,
                                    bg               = helpers.GlobalVars.BGColorLight,
                                    command          = lambda: helpers.Utilities.openFile(self.RPCSLabelStr.get()),
                                    cursor           = "hand2",
                                    fg               = "White",
                                    bd               = 0,
                                    activebackground = helpers.GlobalVars.logoBlue,
                                    font=('Helvatical bold',10))
        self.RPCSLabel.grid(columnspan=1, column=1, row=1, sticky= "we", pady=(20, 0))

        self.RPCSBrowseBtn = tk.Button(self.window, 
                                    text    = "Select Destination",
                                    command = lambda: self.openFileBrowser(self.RPCSLabelStr, 
                                                                          title="Select destination folder. e.g. RPCS3 savedata",
                                                                          delegate= self.RPCS3Delegate),
                                    bg               = helpers.GlobalVars.logoBlue, 
                                    activebackground = helpers.GlobalVars.logoBlue,
                                    fg = "white", height=1, width= 20, bd=0)
        self.RPCSBrowseBtn.grid(column=0, row=1, pady=(20, 0))
        #_______
        self.dupStatus = tk.BooleanVar()
        self.dupStatus.set(True if duplicatesStatus == False else False)
        self.allowDuplicateschkBox = tk.Checkbutton(self.window,
                                             text              = 'Clear duplicate levels',
                                             onvalue           = 1,
                                             variable          = self.dupStatus,
                                             background        = helpers.GlobalVars.BGColorDark,
                                             fg                = "white",
                                             offvalue          = 0,
                                             activebackground  = helpers.GlobalVars.logoBlue,
                                             selectcolor       = "#000000",
                                             command           = self.toggleDupplicatesCheckBox)
        self.allowDuplicateschkBox.grid(column=0, row=2, pady=20)
        #______

        self.includeDescriptionStatus = tk.BooleanVar()
        self.includeDescriptionStatus.set(includeDescriptionStatus)
        self.onlySearchTitleChkBox = tk.Checkbutton(self.window,
                                             text               = 'Include level description when searching (unchecked = more accurate titles)',
                                             onvalue            = 1,
                                             variable           = self.includeDescriptionStatus,
                                             background         = helpers.GlobalVars.BGColorDark,
                                             fg                 = "white",
                                             offvalue           = 0,
                                             activebackground   = helpers.GlobalVars.logoBlue,
                                             selectcolor        = "#000000",
                                             command            = self.toggleIncludeDescription)
        self.onlySearchTitleChkBox.grid(column=1, row=2, pady=20)
        #______

        self.saveSettings = tk.Button(self.window, 
                                    text             = "Save",
                                    command          = lambda: self.saveSettingsAsJSON(),
                                    bg               = helpers.GlobalVars.logoBlue, 
                                    activebackground = helpers.GlobalVars.logoBlue,
                                    fg = "white", height=1, width= 20, bd=0)
        self.saveSettings.grid(column=0, row=3)

        self.saveSettingsLabel = Button
        
        #______
        self.setupLabels(levelArchive=currentArchivePath, RPCS3savedata= currentRPCS3Path)
        self.window.protocol("WM_DELETE_WINDOW", self.onClose)

    # Helper methods _________________________________________________________________________________________________________  

    def setupLabels(self, levelArchive, RPCS3savedata):
        self.archiveLabelStr.set("Select an archive folder for LittleBigPlanet 1, 2 or 3") if levelArchive == '' else self.archiveLabelStr.set(levelArchive)
        self.RPCSLabelStr.set("Select destination folder. e.g. RPCS3 savedata") if RPCS3savedata == '' else self.RPCSLabelStr.set(RPCS3savedata)
        
    def toggleDupplicatesCheckBox(self):
        self.toggleDuplicatesDelegate()
    
    def toggleIncludeDescription(self):
        self.includeDescriptionDelegate()

    def onClose(self):
        self.window.destroy()

    def openFileBrowser(self, labelStr, title, delegate):
        selectedFolder = filedialog.askdirectory(title=title)
        if selectedFolder:
            labelStr.set(selectedFolder)
            delegate(path = selectedFolder)
            
    # save setting to json file _________________________________________________________________________________________________ 

    def saveSettingsAsJSON(self):
        if self.archiveLabelStr.get().__contains__("/") == False or self.RPCSLabelStr.get().__contains__("/") == False:
            ############# add error notification later ####################
            print("failed")
            return
        
        archivePath        = self.archiveLabelStr.get()
        RPCS3Path          = self.RPCSLabelStr.get()
        clearDupLevels     = "True" if self.dupStatus.get() == True else "False"
        includeDescription = "True" if self.includeDescriptionStatus.get() == True else "False"

        settingsDict = {"archive": archivePath , "RPCS3" : RPCS3Path, "ClearDups": clearDupLevels, "includeDescription" : includeDescription}
        jsonString   = json.dumps(settingsDict)
        jsonFile     = open("SavedSettings.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()
        
    @staticmethod
    def getSettingsFromJSON(callBack):
        file = open("SavedSettings.json", "r")
        data = json.loads(file.read())

        callBack(archive           = data['archive'],
                RPCS3              = data['RPCS3'], 
                dupsStatus         = True if data['ClearDups'] == "False" else False,
                includeDescription = True if data['includeDescription'] == "True" else False)