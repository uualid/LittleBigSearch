import json
import tkinter    as tk
import helpers.Utilities as helpers
from   tkinter    import filedialog

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
        self.archiveLabel = helpers.Utilities.makeLabel(master=self.window, textVar= self.archiveLabelStr, backgroundColor= helpers.GlobalVars.BGColorLight)
        self.archiveLabel.configure(cursor           = "hand2",
                                    activebackground = helpers.GlobalVars.logoBlue, 
                                    command          = lambda: helpers.Utilities.openFile(self.archiveLabelStr.get()))

        self.archiveLabel.grid(columnspan=1, column=1, row=0, pady=(20, 0))



        self.archiveBrowseBtn = helpers.Utilities.makeButton(master = self.window, 
                                                             text="Browse Archive", 
                                                             buttonColor= helpers.GlobalVars.BGColorLight,
                                                             activeColor= helpers.GlobalVars.BGColorLight)
        self.archiveBrowseBtnImage = tk.PhotoImage(file="images/UI/selectArchive.png")
        self.archiveBrowseBtn.configure(height = 28, width = 200, image= self.archiveBrowseBtnImage, 
                                      command = lambda: self.openFileBrowser(self.archiveLabelStr, 
                                                                            title    = "Select LittleBigPlanet level archive", 
                                                                            delegate = self.archiveDelegate))
        self.archiveBrowseBtn.grid(columnspan=1, column=0, row=0, pady=(20, 0))


        #________
        
        self.RPCSLabelStr = tk.StringVar()

        self.RPCSLabel = helpers.Utilities.makeLabel(master= self.window, textVar= self.RPCSLabelStr, backgroundColor= helpers.GlobalVars.BGColorLight)
        self.RPCSLabel.configure(command = lambda: helpers.Utilities.openFile(self.RPCSLabelStr.get()), cursor= "hand2", activebackground = helpers.GlobalVars.logoBlue)
        self.RPCSLabel.grid(columnspan=1, column=1, row=1, sticky= "we", pady=(20, 0))



        self.RPCSBrowseBtn = helpers.Utilities.makeButton(master = self.window, 
                                                          text="Browse Archive", 
                                                          buttonColor= helpers.GlobalVars.BGColorLight,
                                                          activeColor= helpers.GlobalVars.BGColorLight)
        self.RPCS3BrowseBtnImage = tk.PhotoImage(file="images/UI/selcetDestination.png")
        self.RPCSBrowseBtn.configure(height = 28, width = 200, image= self.RPCS3BrowseBtnImage, 
                                      command = lambda: self.openFileBrowser(self.RPCSLabelStr, 
                                                                            title="Select destination folder. e.g. RPCS3 savedata",
                                                                            delegate= self.RPCS3Delegate))
        self.RPCSBrowseBtn.grid(column=0, row=1, pady=(20, 0))

        #_______
        self.dupStatus = tk.BooleanVar()
        self.dupStatus.set(True if duplicatesStatus == False else False)
        self.allowDuplicateschkBox = tk.Checkbutton(self.window,
                                             text              = 'Clear duplicate levels',
                                             onvalue           = 1,
                                             variable          = self.dupStatus,
                                             background        = helpers.GlobalVars.BGColorDark,
                                             highlightthickness= 0,
                                             borderwidth      = 0,
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
                                             highlightthickness= 0,
                                             borderwidth      = 0,
                                             offvalue           = 0,
                                             activebackground   = helpers.GlobalVars.logoBlue,
                                             selectcolor        = "#000000",
                                             command            = self.toggleIncludeDescription)
        self.onlySearchTitleChkBox.grid(column=1, row=2, pady=20)
        #______

        self.saveSettings = helpers.Utilities.makeButton(master = self.window, 
                                                          text="save", 
                                                          buttonColor= helpers.GlobalVars.BGColorLight,
                                                          activeColor= helpers.GlobalVars.BGColorLight)
        self.saveBtnImage = tk.PhotoImage(file="images/UI/save.png")
        self.saveSettings.configure(height = 28, width = 200, image= self.saveBtnImage, 
                                      command = lambda: self.saveSettingsAsJSON())
        self.saveSettings.grid(column=0, row=3)

        self.saveSettingsTxt = tk.StringVar()
        self.saveSettingsLabel = helpers.Utilities.makeLabel(master= self.window, textVar= self.saveSettingsTxt, backgroundColor= helpers.GlobalVars.BGColorLight)
        self.saveSettingsLabel.configure(fg= "green")
        self.saveSettingsLabel.grid(column=1, row=3)
        
        #______
        self.setupLabels(levelArchive=currentArchivePath, RPCS3savedata= currentRPCS3Path)
        self.window.protocol("WM_DELETE_WINDOW", self.onClose)

    # Helper methods _________________________________________________________________________________________________________  

    def notifyUser(self, text, color):
        self.saveSettingsTxt.set(text)
        self.saveSettingsLabel.configure(fg=color)

    def setupLabels(self, levelArchive, RPCS3savedata):
        self.archiveLabelStr.set("Select an archive folder for LittleBigPlanet 1, 2 or 3") if levelArchive == '' else self.archiveLabelStr.set(levelArchive)
        self.RPCSLabelStr.set("Select destination folder. e.g. RPCS3 savedata") if RPCS3savedata == '' else self.RPCSLabelStr.set(RPCS3savedata)
        
    def toggleDupplicatesCheckBox(self):
        self.toggleDuplicatesDelegate()
        self.saveSettingsTxt.set("")
    
    def toggleIncludeDescription(self):
        self.includeDescriptionDelegate()
        self.saveSettingsTxt.set("")

    def onClose(self):
        self.window.destroy()

    def openFileBrowser(self, labelStr, title, delegate):
        self.saveSettingsTxt.set("")
        selectedFolder = filedialog.askdirectory(title=title)
        if selectedFolder:
            labelStr.set(selectedFolder)
            delegate(path = selectedFolder)
            
    # save setting to json file _________________________________________________________________________________________________ 

    def saveSettingsAsJSON(self):
        if self.archiveLabelStr.get().__contains__("/") == False or self.RPCSLabelStr.get().__contains__("/") == False:
            ############# add error notification later ####################
            self.notifyUser(text= "Please select an archive and destination folder", color= "red")
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

        self.notifyUser(text= "Saved successfully", color="green")
        
    @staticmethod
    def getSettingsFromJSON(callBack):
        file = open("SavedSettings.json", "r")
        data = json.loads(file.read())

        callBack(archive           = data['archive'],
                RPCS3              = data['RPCS3'], 
                dupsStatus         = True if data['ClearDups'] == "False" else False,
                includeDescription = True if data['includeDescription'] == "True" else False)