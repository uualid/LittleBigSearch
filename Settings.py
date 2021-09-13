import os
import tkinter    as tk
from   GlobalVars import GlobalVars
from   tkinter    import filedialog

class Settings ():
    
    def __init__(self, duplicatesStatus, currentArchivePath, currentRPCS3Path, includeDescriptionStatus,
                duplicatesDelegate, archiveDelegate, RPCS3Delegate, closeDelegate, includeDescriptionDelegate):
        super().__init__()
        
        #___ Delegates __________
        self.closeDelegate              = closeDelegate
        self.toggleDuplicatesDelegate   = duplicatesDelegate
        self.archiveDelegate            = archiveDelegate
        self.RPCS3Delegate              = RPCS3Delegate
        self.includeDescriptionDelegate = includeDescriptionDelegate
        #________________________
        
        self.window = tk.Toplevel(background= GlobalVars.backgroudnColorLight)
        self.window.title("Settings")

        self.settingsCanvas = tk.Canvas(master= self.window,
                                height = 50,
                                width  = 850 ,
                                bg=GlobalVars.backgroudnColorLight, 
                                borderwidth=0,
                                highlightthickness=0)

        self.settingsCanvas.grid(columnspan=3, row= 3)

        self.archiveLabelStr = tk.StringVar()
        self.archiveLabel = tk.Button(self.window,
                                    textvariable=self.archiveLabelStr,
                                    bg=GlobalVars.backgroudnColorLight,
                                    cursor= "hand2",
                                    activebackground= GlobalVars.logoBlue,
                                    command=lambda: self.openFile(self.archiveLabelStr.get()),
                                    fg="White",
                                    bd =0,
                                    font=('Helvatical bold',10))
                                    
        self.archiveLabel.grid(columnspan=1, column=1, row=0, pady=(20, 0))

        self.archiveBrowseBtn = tk.Button(self.window,
                                    text="Browse (Archive)",
                                    activebackground= GlobalVars.logoBlue,
                                    command=lambda: self.openFileBrowser(self.archiveLabelStr, 
                                                                        title="Select LittleBigPlanet level archive", 
                                                                        delegate= self.archiveDelegate),
                                    bg=GlobalVars.logoBlue,
                                    fg = "white", height=1, width= 20, bd=0)
        self.archiveBrowseBtn.grid(columnspan=1, column=0, row=0, pady=(20, 0))
        #________
        
        self.RPCSLabelStr = tk.StringVar()
        self.RPCSLabel = tk.Button(self.window,
                                    textvariable=self.RPCSLabelStr,
                                    bg=GlobalVars.backgroudnColorLight,
                                    command=lambda: self.openFile(self.RPCSLabelStr.get()),
                                    cursor= "hand2",
                                    fg="White",
                                    bd = 0,
                                    activebackground= GlobalVars.logoBlue,
                                    font=('Helvatical bold',10))
        self.RPCSLabel.grid(columnspan=1, column=1, row=1, sticky= "we", pady=(20, 0))

        self.RPCSBrowseBtn = tk.Button(self.window, 
                                    text="Browse (RPCS3 Savedata)",
                                    command=lambda: self.openFileBrowser(self.RPCSLabelStr, 
                                                                        title="Select RPCS3 savedata folder",
                                                                        delegate= self.RPCS3Delegate),
                                    bg= GlobalVars.logoBlue, 
                                    activebackground= GlobalVars.logoBlue,
                                    fg = "white", height=1, width= 20, bd=0)
        self.RPCSBrowseBtn.grid(column=0, row=1, pady=(20, 0))
        #_______
        self.dupStatus = tk.BooleanVar()
        self.dupStatus.set(True if duplicatesStatus == False else True)
        self.allowDuplicateschkBox = tk.Checkbutton(self.window,
                                             text='Clear duplicate levels',
                                             onvalue=1,
                                             variable= self.dupStatus,
                                             background= GlobalVars.backgroundColorDark,
                                             fg= "white",
                                             offvalue=0,
                                             activebackground= GlobalVars.logoBlue,
                                             selectcolor="#000000",
                                             command=self.toggleDupplicatesCheckBox)
        self.allowDuplicateschkBox.grid(column=0, row=2, pady=20)
        #______

        self.searchTitleOnlyStatus = tk.BooleanVar()
        self.searchTitleOnlyStatus.set(includeDescriptionStatus)
        self.onlySearchTitleChkBox = tk.Checkbutton(self.window,
                                             text='Include level description when searching (unchecked is more accurate)',
                                             onvalue=1,
                                             variable= self.searchTitleOnlyStatus,
                                             background= GlobalVars.backgroundColorDark,
                                             fg= "white",
                                             offvalue=0,
                                             activebackground= GlobalVars.logoBlue,
                                             selectcolor="#000000",
                                             command=self.toggleIncludeDescription)
        self.onlySearchTitleChkBox.grid(column=1, row=2, pady=20)
        #______

        self.setupLabels(levelArchive=currentArchivePath, RPCS3savedata= currentRPCS3Path)
        self.window.protocol("WM_DELETE_WINDOW", self.onClose)

    # Helper methods _________________________________________________________________________________________________________  

    def setupLabels(self, levelArchive, RPCS3savedata):
        self.archiveLabelStr.set("Select the level archive folder for LittleBigPlanet 1, 2 or 3") if levelArchive == '' else self.archiveLabelStr.set(levelArchive)
        self.RPCSLabelStr.set("Select an RPCS3 savedata folder") if RPCS3savedata == '' else self.RPCSLabelStr.set(RPCS3savedata)

        self.window.lift()
        
    def toggleDupplicatesCheckBox(self):
        self.toggleDuplicatesDelegate()
    
    def toggleIncludeDescription(self):
        self.includeDescriptionDelegate()

    def onClose(self):
        self.closeDelegate()
        self.window.destroy()

    def openFileBrowser(self, labelStr, title, delegate):
        selectedFolder = filedialog.askdirectory(title=title)
        if selectedFolder:
            labelStr.set(selectedFolder)
            delegate(path = selectedFolder)
            
    
    def openFile(self, path):
        try:
            path = os.path.realpath(path)
            os.startfile(path)
        except:
            print("Failed to open folder")