
import tkinter           as tk
import os, shutil,threading, ttkthemes
from   tkinter.ttk       import Progressbar
from   genericpath       import exists
from   tkinter           import Button, Frame, ttk
from   tkinter.constants import VERTICAL
from   functools         import partial
from   PIL               import Image, ImageTk
from   SFOParser         import LevelParser, ParserReturns
from   Settings.Options  import Options
import helpers.Utilities as     helpers
from   SavedLevels       import SavedLevels
from   os                import path

class LittleBigSearchGUI():
    def __init__(self, master: tk.Tk, matchedLevels = [], settings = 0, savedLevels = 0) -> None:
        
        self.archivePath = ''
        self.RPCS3Path   = ''
        
        self.scrollerCanvas  = tk.Canvas()
        self.levelScroller   = Frame()
        
        self.levelParser     = LevelParser()
        self.matchedLevels   = matchedLevels
        self.currentPage     = 0
        self.hasMoreThanOnePage = False
        

        self.isDuplicatesAllowed = False
        self.includeDescription  = True
        
        self.master = master
        self.master.title("LittleBigSearch by @SackBiscuit v1.1.3")
        self.master.iconbitmap(default="images/icon.ico")
        self.master.configure(bg= helpers.GlobalVars.BGColorDark)

        ttkthemes.themed_style.ThemedStyle(theme="adapta")

        # _ UI _______________________

        self.canvas = tk.Canvas(master,
                                height = 150,
                                width  = 900 ,
                                bg=helpers.GlobalVars.BGColorLight, 
                                borderwidth=0,
                                highlightthickness=0)

        self.canvas.grid(columnspan=3, sticky="we")

        self.logo = Image.open('images/LBSearch.png')

        self.logoResize = self.logo.resize(( 500, 112 ))
        self.logo = ImageTk.PhotoImage(image= self.logoResize)

        self.logoLabel = tk.Label(image= self.logo, bg= helpers.GlobalVars.BGColorLight)
        self.logoLabel.image = self.logo
        self.logoLabel.grid(column=1, row=0)
        
        # ____ 
        
        self.settingButton = helpers.Utilities.makeButton(text="Settings", command= self.openSettings, buttonColor= helpers.GlobalVars.logoBlue)
        self.settingButton.config(height=1, width=13)
        self.settingButton.grid(columnspan=3, column=0, row=1, pady=10, padx= (0,105))
        
        # ____
        self.SavedLevelsButton = helpers.Utilities.makeButton(text="Saved Levels", command= self.openSavedLevels, buttonColor= helpers.GlobalVars.logoBlue)
        self.SavedLevelsButton.config(height=1, width=13)
        self.SavedLevelsButton.grid(columnspan=3, column=0, row=1, pady=10, padx= (105,0))
        # ____ 
        searchLabel = tk.Label(text  = "The Search will look for level name, creator ID or any keyword in the level Description",
                               bg    = helpers.GlobalVars.BGColorDark,
                               fg    = "White",
                               font  = ('Helvatical bold',10))

        searchLabel.grid(columnspan=3, column=0, row=2)
        searchTextField = tk.Entry(bd= 0, font=15, bg="black", fg="white")
        searchTextField.grid(columnspan=3, row=3, column=0, ipadx= 250)

        searchButton = helpers.Utilities.makeButton(text="Search", buttonColor= helpers.GlobalVars.logoBlue)
        searchButton.configure(height = 1, width = 20, command = lambda: threading.Thread(target= self.LBSsearch, args= (searchTextField.get(), self.archivePath)).start())
        searchButton.grid(column=1, row=4, pady=10)


        self.errorText  = tk.StringVar()
        self.errorLabel = helpers.Utilities.makeLabel(self.errorText)
        self.errorText.set("")
        self.errorLabel.grid(column=1, row=5, ipadx=30, pady=(0,10))

        #--- Pagination
        
        self.pageLeft     = helpers.Utilities.makeButton(text="<", command= self.nextLeftPage)
        self.pageFarLeft  = helpers.Utilities.makeButton(text="<<", command= self.farLeftPage)        
        self.pageRight    = helpers.Utilities.makeButton(text=">", command= self.nextRightPage)
        self.pageFarRight = helpers.Utilities.makeButton(text=">>", command= self.farRightPage)
        
        # _________
        self.pageNumText  = tk.StringVar()
        self.pageNumbers = helpers.Utilities.makeLabel(self.pageNumText)
        
        self.levelCounterTxt  = tk.StringVar()
        self.levelCounter     = helpers.Utilities.makeLabel(self.levelCounterTxt)
        
        #____________________________
        
        self.fetchSettingsFromJSON()
        
    # settings __________________________________________________________________________________________________________________________________________
    
    def fetchSettingCallBack(self, archive, RPCS3, dupsStatus, includeDescription):
        self.archivePath = archive
        self.RPCS3Path   = RPCS3
        self.isDuplicatesAllowed = dupsStatus
        self.includeDescription = includeDescription
    
    def fetchSettingsFromJSON(self):
        if path.exists("SavedSettings.json"):
            Options.getSettingsFromJSON(self.fetchSettingCallBack)
        else:
            print("No saved settings.")

    # search method _____________________________________________________________________________________________________________________________________

    def LBSsearch(self, term, path):
        if self.RPCS3Path.__contains__("/") == False:
            self.sendError("Please select a destination folder", "red")
            return
        self.currentPage = 0
        self.sendError("Searching...")
        # this event will be called from background thread to use the main thread.
        self.master.bind("<<event1>>", self.updatePage)
        self.levelParser.search(self.searchCallBack, term, path, includeDescription= self.includeDescription)
        
    
    def searchCallBack(self, response):
        if response == ParserReturns.noResult:
            self.sendError("No result", "red")

        elif response == ParserReturns.noPath:
            self.sendError("Please select a levels directory from the settings", "red")
        
        elif response == ParserReturns.wrongPath:
            self.sendError("Couldn't find the level archive directory", "red")
        
        else: #if levels were found.
            levels = response if self.isDuplicatesAllowed == True else set(response)
            self.matchedLevels = helpers.Utilities.splitLevelsToLists(levels = levels) if len(levels) > 50 else levels
            self.showPagingButtons()
            # Calls showResult on the main thread.
            self.master.event_generate("<<event1>>")

    # PROTOCOLS _________________________________________________________________________________________________________________________________________

    def toggleDuplicatesProtocol(self):
        self.isDuplicatesAllowed = True if self.isDuplicatesAllowed == False else False

    def toggleIncludeDescriptionProtocol(self):
        self.includeDescription = True if self.includeDescription == False else False

    def archivePathProtocol(self, path):
        self.archivePath = path
    
    def RPCS3PathProtocol(self, path):
        self.RPCS3Path = path

    # Saved levels _______________________________________________________________________________________________________________________________________

    def openSavedLevels(self):
        if self.RPCS3Path == '':
            self.sendError("Please select a destination folder", "red")
            return

        try:
            self.savedLevels.window.lift()
        except:
            self.savedLevels = SavedLevels(master        = self.master, 
                                           RPCS3Path     = self.RPCS3Path)

    # Settings ____________________________________________________________________________________________________________________________________________

    def openSettings(self):
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
                                    duplicatesStatus           = self.isDuplicatesAllowed,
                                    master=self.master)
            
            
    # Helper methods _____________________________________________________________________________________________________________________________________

    def moveFolder(self, source):
        destination = self.RPCS3Path
        destDir = os.path.join(destination,os.path.basename(source))
        if exists(destDir) == False:
            self.sendError("Level folder was copied to the destination folder.", "green")
            shutil.copytree(source, destDir)
        else:
            self.sendError("Level folder was removed from the destination folder")
            shutil.rmtree(destDir)
        
        # refresh Saved levels automatically
        try:
            self.savedLevels.refresh()
        except:
            print("DEBUG: Cant refresh. No window on the screen")

    def _bound_to_mousewheel(self, event):
        self.scrollerCanvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

    def _unbound_to_mousewheel(self, event):
        self.scrollerCanvas.unbind_all("<MouseWheel>")

    def _on_mouse_wheel(self, event):
        self.sendError("")
        self.scrollerCanvas.yview_scroll(-1 * int((event.delta / 120)), "units")

    def sendError(self, message = "", color = "white"):
        self.errorLabel.configure(fg=color)
        self.errorText.set(message)        
    
    # Pagination __________________________________________________________________________________________________________________________________________________
    
    def nextRightPage(self):
        if self.hasMoreThanOnePage == False: return
        if self.currentPage == len(self.matchedLevels) - 1: return
        
        self.currentPage += 1
        self.updatePage(evt="")

    def nextLeftPage(self):
        if self.hasMoreThanOnePage == False: return
        if self.currentPage == 0: return
        
        self.currentPage -= 1
        self.updatePage(evt="")

    def farRightPage(self):
        if self.hasMoreThanOnePage == False: return
        if self.currentPage == len(self.matchedLevels) -1: return
        
        self.currentPage = len(self.matchedLevels) -1
        self.updatePage(evt="")

    def farLeftPage(self):
        if self.hasMoreThanOnePage == False: return
        if self.currentPage == 0: return
        
        self.currentPage = 0
        self.updatePage(evt="")
    
    def updatePage(self, evt):
        
        try: # if there is a 2D list
            levelsCount = sum(len(levels) for levels in self.matchedLevels)
            self.pageNumText.set(f'{self.currentPage + 1} of {len(self.matchedLevels)}')
            self.hasMoreThanOnePage = True
        except: # else if there's only one list
            levelsCount = len(self.matchedLevels)
            self.pageNumText.set('1')
            self.hasMoreThanOnePage = False

        levelsFound = "Levels" if levelsCount > 1 else "Level"
        self.levelCounterTxt.set(f'{levelsCount} {levelsFound}')
        self.showResult(isAfterSearch= False)
    
    def showPagingButtons(self):
        self.pageLeft.grid(column=1, row=6, ipadx=15, pady=(0, 10), padx= (0, 150))
        self.pageFarLeft.grid(column=1, row=6, ipadx=10, pady=(0, 10), padx= (0, 250))
        
        self.pageRight.grid(column=1, row=6, ipadx=15, pady=(0, 10), padx= (150, 0))
        self.pageFarRight.grid(column=1, row=6, ipadx=10, pady=(0, 10), padx= (250, 0))

        self.levelCounter.grid(column=1, row=6, ipadx=10, pady=(0, 10), padx= (400, 0))
        self.pageNumbers.grid(column=1, row=6, ipadx=20, pady=(0, 10))
        
   # builds result scroller view _______________________________________________________________________________________________________________________________
   
    def showResult(self, isAfterSearch: bool= True):
        self.sendError("")
        # destroy the old scroll view
        self.levelScroller.destroy()
        
        # build new one
        self.mainFrame = Frame(self.master,
                               highlightbackground  = helpers.GlobalVars.BGColorDark,
                               highlightcolor       = helpers.GlobalVars.BGColorDark)

        self.mainFrame.grid(columnspan=3, column=0)

        self.scrollerCanvas = tk.Canvas(self.mainFrame,bg=helpers.GlobalVars.BGColorDark, borderwidth=0, highlightthickness=0)
        self.scrollerCanvas.grid(row=0, column=0, ipadx= 250, ipady=150)
        

        ScrollBar = ttk.Scrollbar(self.mainFrame, orient=VERTICAL, command=self.scrollerCanvas.yview)
        ScrollBar.grid(row=0, column=1, sticky='ns')
        

        self.scrollerCanvas.configure(yscrollcommand=ScrollBar.set, bg=helpers.GlobalVars.BGColorDark)
        self.scrollerCanvas.bind('<Configure>', lambda e: self.scrollerCanvas.configure(scrollregion= self.scrollerCanvas.bbox("all")))
        
        self.scrollerCanvas.bind('<Enter>', self._bound_to_mousewheel)
        self.scrollerCanvas.bind('<Leave>', self._unbound_to_mousewheel)

        scrollerFrame = Frame(self.scrollerCanvas,
                             background          = helpers.GlobalVars.BGColorDark,
                             highlightbackground = helpers.GlobalVars.BGColorDark,
                             highlightcolor      = helpers.GlobalVars.BGColorDark)
        
        self.scrollerCanvas.create_window((0,0), window=scrollerFrame, anchor="nw")
        
        self.levelScroller = self.mainFrame
        
        
        matchedLevelsWithPage = self.matchedLevels[self.currentPage] if self.hasMoreThanOnePage == True else self.matchedLevels
        
            # Loop and build level cells for the scrollable frame
        for index, level in enumerate(matchedLevelsWithPage):

            labelText = f'{level.title}'

            levellogo = Image.open(level.image)

            levelImage_resize = levellogo.resize(( 120, 75 ))
            levellogo = ImageTk.PhotoImage(levelImage_resize)

            levelImage_resize = tk.Label(scrollerFrame, image=levellogo, bg=helpers.GlobalVars.BGColorDark)
            levelImage_resize.image = levellogo

            levelPath = f'...{level.path[-80:]}' if len(level.path) > 90 else level.path  
            imagePadx = helpers.Utilities.getPadding(len(levelPath))
            levelImage_resize.grid(row = index, column=0, padx=imagePadx)
            
            levelInfoButton = Button(scrollerFrame,
                                    text             = labelText + "\n" + levelPath, anchor="e",
                                    bd               = 0, 
                                    command          = partial(self.moveFolder, level.path),
                                    cursor           = "hand2",
                                    bg               = helpers.GlobalVars.BGColorDark,
                                    activebackground = helpers.GlobalVars.logoBlue,
                                    fg               = "white",
                                    font             = ('Helvatical bold',10)) 
            levelInfoButton.grid(row = index, column=1)
        
        # reset to page one after searching
        if isAfterSearch:
            self.currentPage = 0
            
#___________________________________________________________________________________________________________________________________________________________
    
root   = tk.Tk()
LBSGUI = LittleBigSearchGUI(master= root)
root.mainloop()

