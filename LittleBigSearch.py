from cmath import exp
from tabnanny import check
import tkinter           as tk
import os, shutil,threading, ttkthemes, time
from   genericpath       import exists
from   tkinter           import Canvas, Frame, ttk
from   tkinter.constants import VERTICAL
from   functools         import partial
from   PIL               import Image, ImageTk
from   SFOParser         import LevelParser, ParserReturns
from idlelib.tooltip     import Hovertip

from helpers.Utilities import GlobalVars as GB
from helpers.Utilities import Utilities as util
from SavedLevels       import SavedLevels
from Settings.OptionsManager import OptionsManager

class LittleBigSearchGUI():
    def __init__(self, master: tk.Tk, matchedLevels = [], settings = 0, savedLevels = 0) -> None:
        
        self.options = OptionsManager(self.errorCallback)
        
        self.scrollerCanvas  = tk.Canvas()
        self.scrollerFrame   = Frame()
        
        self.levelParser     = LevelParser()
        self.isSearching     = False 
        self.matchedLevels   = matchedLevels
        self.currentPage     = 0
        self.hasMoreThanOnePage = False
        self.isFirstRun         = True
        self.currentPageLevels       = []
        
        
        self.startTimer = 0
        self.endTimer = 0

        self.framelist = []     
        self.frame_index = 0 
        
        self.master = master
        self.master.title("By @SackBiscuit v1.1.4")
        self.master.iconbitmap(default=util.resourcePath("images\\icon.ico"))
        self.master.configure(bg= GB.BGColorDark)

        ttkthemes.themed_style.ThemedStyle(theme="adapta")

        self.levelHeart = util.resize(image = util.resourcePath("images\\UI\\lbpLevelHeart.png"), height=30, width=30)
        
        # _ UI _______________________

        self.canvas = tk.Canvas(master,
                                height = 150,
                                width  = 900 ,
                                bg=GB.BGColorLight, 
                                borderwidth=0,
                                highlightthickness=0)

        self.canvas.grid(columnspan=3, sticky= "nsew")
        
        tk.Grid.columnconfigure(master, (0,1,2) , weight = 1)
        tk.Grid.rowconfigure(master, 7, weight = 1)

        self.logo = Image.open(util.resourcePath('images\\UI\\LB_Search.png'))
        self.logoResize = self.logo.resize(( 500, 122 ))
        self.logo = ImageTk.PhotoImage(image= self.logoResize)

        self.logoLabel = tk.Label(image= self.logo, bg= GB.BGColorLight)
        self.logoLabel.image = self.logo
        self.logoLabel.grid(column=1, row=0)
        
        # ____ 
        settingsBtnImage = tk.PhotoImage(file=util.resourcePath("images\\UI\\settings.png"))
        self.settingsButton = util.makeButton(buttonColor = GB.BGColorDark, 
                                              activeColor = GB.BGColorDark,
                                              image       = settingsBtnImage,
                                              command     = self.openSettings)
        
        self.settingsButton.configure(height = 28, width = 120)
        self.settingsButton.grid(columnspan=3, column=0, row=1, pady=10, padx= (0,130))
        
        # ____
        
        heartedImage = tk.PhotoImage(file=util.resourcePath("images\\UI\\hearted.png"))
        self.SavedLevelsButton = util.makeButton(buttonColor = GB.BGColorDark, 
                                                 activeColor = GB.BGColorDark,
                                                 image       = heartedImage,
                                                 command     = self.openSavedLevels)
        
        self.SavedLevelsButton.configure(height = 28, width = 120)
        self.SavedLevelsButton.grid(columnspan=3, column=0, row=1, pady=10, padx= (130,0))
        # ____ 
        
        searchLabel = tk.Label(text  = "The Search will look for level name, creator ID or any keyword in the level Description",
                               bg    = GB.BGColorDark,
                               fg    = "White",
                               font  = ('Helvatical bold',10))
        searchLabel.grid(columnspan=3, column=0, row=2)
        
        searchTextField = tk.Entry(bd= 0, font=15, bg="black", fg="white")
        searchTextField.grid(columnspan=3, row=3, column=0, ipadx= 250)

        searchBtnImage = tk.PhotoImage(file=util.resourcePath("images/UI/search.png"))
        searchButton = util.makeButton(buttonColor = GB.BGColorDark,
                                       activeColor = GB.BGColorDark,
                                       image       = searchBtnImage,
                                       command = lambda: threading.Thread(target = self.LBSsearch, 
                                                                          args   = (searchTextField.get(), self.options.archivePath)).start())
        searchButton.configure(height = 28, width = 120)
        searchButton.grid(column=1, row=4, pady=(13,13))

        self.errorText  = tk.StringVar()
        self.errorLabel = util.makeLabel(self.errorText)
        self.errorText.set("")
        self.errorLabel.grid(column=1, row=5, ipadx=30, pady=(0,3))

        #--- Pagination
        
        self.pageLeft     = util.makeButton(text="<",  command= self.nextLeftPage)
        self.pageFarLeft  = util.makeButton(text="<<", command= self.farLeftPage)        
        self.pageRight    = util.makeButton(text=">",  command= self.nextRightPage)
        self.pageFarRight = util.makeButton(text=">>", command= self.farRightPage)
        
        # _________
        self.pageNumText  = tk.StringVar()
        self.pageNumbers = util.makeLabel(self.pageNumText)
        
        self.levelCounterTxt  = tk.StringVar()
        self.levelCounter     = util.makeLabel(self.levelCounterTxt)
        #____________________________
        
        self.configureGif()
        self.earthGif = tk.Label(bg= GB.BGColorDark)
        self.earthGif.grid(column=1, row=4, padx= (200, 0) ,pady=(5,0))
        self.options.fetchSettings()
        
        
        self.dragId = ''
        master.bind('<Configure>', self.dragging)
        #___________________________________
        
    def dragging(self, event):
        if event.widget is root: 
            if self.dragId != '':
                self.master.after_cancel(self.dragId)
            # schedule resetDrag
            self.dragId = root.after(100, self.resetDrag)
            

    def resetDrag(self):
        self.dragId = '' 
            
    # search method _____________________________________________________________________________________________________________________________________

    def configureGif(self):
        for i in range(32): #theres 32 frame to the globe animation.
            try:
                frame = Image.open(util.resourcePath(f'images/animation/earth{i + 1}.png'))
                frameResized = frame.resize(( 45, 45 ))
                frame = ImageTk.PhotoImage(image= frameResized)
                self.framelist.append(frame)
                 
            except:
                break
    
    def animate(self, frameNumber):
        if self.isSearching == False:
            self.earthGif.config(image="")# remove the image
            return

        if frameNumber == 32: # Loops the animation when it hits the last frame.
            frameNumber = 0
        
        try:
            self.earthGif.config(image=self.framelist[frameNumber]) 
            self.master.after(50, self.animate, frameNumber+1)
        except:
            pass

    def startWaiter(self):
        if self.isSearching == True:
            self.sendError("First run takes longer time")
            return

        elif self.isFirstRun == True:
            threading.Timer(10.0, self.startWaiter).start()
            

    def LBSsearch(self, term, path):
        if self.isSearching:
            return
        if self.options.RPCS3Path.__contains__("/") == False:
            self.sendError("Please select a destination folder", "red")
            return
        self.clearNotification()
        self.startTimer = time.time()
        self.startWaiter()
        self.currentPage = 0
        self.isSearching = True
        self.animate(0)
        
        # this event will be called from background thread to use the main thread.
        self.master.bind("<<event1>>", self.updatePage)
        self.levelParser.search(self.searchCallBack, path, term, includeDescription= self.options.includeDescription)
        
    def searchCallBack(self, response):
        self.isFirstRun = False
        if self.options.heartedLevelPaths == None:
            self.sendError("An error occurred when tried to open one of the saved paths. Try selecting paths again.", "red")
            self.isSearching = False
            return
        
        if response == ParserReturns.noResult:
            self.sendError("No result", "red")

        elif response == ParserReturns.noPath:
            self.sendError("Please select a levels directory from the settings", "red")
        
        elif response == ParserReturns.wrongPath:
            self.sendError("Can't find any level archive directory", "red")
        
        else: #if levels were found.
            levels = response if self.options.includeDups == True else set(response)
            self.matchedLevels = util.splitLevelsToLists(levels = levels) if len(levels) > 50 else levels
            self.endTimer = time.time()
            print(f"{self.endTimer - self.startTimer},")
            
            self.showPagingButtons()
            # Calls showResult on the main thread.
            self.master.event_generate("<<event1>>")
        self.isSearching = False

    # Hearted levels _______________________________________________________________________________________________________________________________________
    
    def removeLevelCallBack(self, path, removedLevelFolderName):
        try: # it will check if the removed level is in the current page, if so it will update the heart image in the ui
            tuple =  [tuple for tuple in self.currentPageLevels if tuple[0] == removedLevelFolderName][0]
            levelFolderName = tuple[0]
            levelCanvas     = tuple[1]
            self.toggleLevelHeart(check        = levelFolderName is self.options.heartedLevelPaths, 
                                  levelFolder = levelFolderName, 
                                  imageCanvas = levelCanvas)
            self.clearNotification()
            return
        except: # other wise it wil just remove the level from the hearted list
            print("DEBUG: Level cell is not on the current page")
        self.options.removeHeartedLevel(removedLevelFolderName)
        
    
    def currentLevels(self):
        if self.hasMoreThanOnePage == False: return self.matchedLevels
        
        
    def openSavedLevels(self):
        if self.options.RPCS3Path == '':
            self.sendError("Please select a destination folder", "red")
            return
        try:
            self.savedLevels.window.lift()
        except:
            self.savedLevels = SavedLevels(master     = self.master, 
                                           removeLevelCallBack = self.removeLevelCallBack,
                                           RPCS3Path  = self.options.RPCS3Path)

    # Settings ____________________________________________________________________________________________________________________________________________
    
    def errorCallback(self, errorText, color = "red"):
        self.sendError(errorText, color)
        
    def openSettings(self):
        self.options.openSettings(master= self.master)
                        
    # Level Helpers _______________________________________________________________________________________________________________________________________
    
    def manageLevel(self, source, levelFolder, levelImageCanvas):
        destination = self.options.RPCS3Path
        destDir = os.path.join(destination,os.path.basename(source))
        try:
            if self.moveFolder(source, destDir):
                self.toggleLevelHeart(True, levelFolder, levelImageCanvas)
            else:
                self.toggleLevelHeart(False, levelFolder, levelImageCanvas)
        except:
            self.sendError("Could not handle folder properly because it is being used by another process", "red") 
            self.options.fetchHeatedPaths(destination)
            self.toggleLevelHeart(check = levelFolder is self.options.heartedLevelPaths, levelFolder = levelFolder, imageCanvas = levelImageCanvas)
            self.refreshLevels()  
    
    
    def toggleLevelHeart(self, check, levelFolder, imageCanvas):
        if check:
            imageCanvas.itemconfig(2, state='normal')
            self.options.addHeartedLevel(levelFolder)
        else:
            imageCanvas.itemconfig(2, state='hidden')
            try:
                self.options.removeHeartedLevel(levelFolder)
            except:
                print("DEBUG: Level is not in the list")
            
    def checkIfFolderIsEmpty(self, pathToCheck):
        try:
            if len(os.listdir(pathToCheck)) == 0:
                shutil.rmtree(pathToCheck)
                print("DEBUG: removed empty file.")
        except:
            print("DEBUG: Folder is not available in destination folder, it is safe to copy it.")  
                  
    def moveFolder(self, source, destDir):
        self.checkIfFolderIsEmpty(destDir)
        if exists(destDir) == False:
            shutil.copytree(source, destDir)
            self.sendError("Level folder was copied to the destination folder.", "green")
            self.refreshLevels()
            return True
        else:
            shutil.rmtree(destDir)
            self.sendError("Level folder was removed from the destination folder")
            self.refreshLevels()
            return False
        
    def refreshLevels(self):
        # refresh Saved levels automatically
        try:
            self.savedLevels.refresh()
        except:
            print("DEBUG: Cant refresh. No window on the screen")
    
    # Curser helpers __________________________________________________________________________________________________________________________________________________
    
    def _bound_to_mousewheel(self, event):
        self.scrollerCanvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

    def _unbound_to_mousewheel(self, event):
        self.scrollerCanvas.unbind_all("<MouseWheel>")

    def _on_mouse_wheel(self, event):
        self.clearNotification()
        self.master.update()
        self.scrollerCanvas.yview_scroll(-1 * int((event.delta / 120)), "units")

    def sendError(self, message = "", color = "white"):
        self.errorLabel.configure(fg=color)
        self.errorText.set(message)        
    
    def clearNotification(self):
        self.sendError("")
    # Pagination __________________________________________________________________________________________________________________________________________________
    
    def nextPage(self, pageLimit, moveNear = None, moveFar = None):
        if self.hasMoreThanOnePage == False     : return
        if self.currentPage        == pageLimit : return
        
        if moveNear != None: self.currentPage += moveNear
        if moveFar  != None: self.currentPage = moveFar
        self.updatePage(evt="")
    
    def nextRightPage(self):
        self.nextPage(moveNear  = 1, 
                      pageLimit = len(self.matchedLevels) - 1)
        
    def nextLeftPage(self):
        self.nextPage(moveNear  =-1,
                      pageLimit = 0)
        
    def farRightPage(self):
        self.nextPage(moveFar   = len(self.matchedLevels) -1,
                      pageLimit = len(self.matchedLevels) -1)
    
    def farLeftPage(self):
        self.nextPage(moveFar   = 0,
                      pageLimit = 0)
        
    
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
        self.pageFarLeft.grid(column=1, row=6, ipadx=10, pady=(0, 10), padx= (0, 260))
        
        self.pageRight.grid(column=1, row=6, ipadx=15, pady=(0, 10), padx= (150, 0))
        self.pageFarRight.grid(column=1, row=6, ipadx=10, pady=(0, 10), padx= (260, 0))

        self.levelCounter.grid(column=1, row=6, ipadx=10, pady=(0, 10), padx= (420, 0))
        self.pageNumbers.grid(column=1, row=6, ipadx=20, pady=(0, 10))
        
   # builds result scroller view _______________________________________________________________________________________________________________________________
     
     
    def showResult(self, isAfterSearch: bool= True):        
        refreshWindow = False
        if self.dragId != "":
            self.master.overrideredirect(True)
            refreshWindow = True
        
        self.clearNotification()
        self.currentPageLevels = []
        
        # destroy the old scroll view
        self.scrollerFrame.destroy()
                
        # # build new one        
        baseScrollerFrame = util.makeScrollerFrame(self.master)
        baseScrollerFrame.grid(columnspan=3, sticky="nsew")
        
        self.scrollerCanvas = util.makeScrollerCanvas(master= baseScrollerFrame, height= 600, width= 800)
        self.scrollerCanvas.grid(row=0, column=0, sticky= "ns")
        
        scrollBar = ttk.Scrollbar(baseScrollerFrame, orient=VERTICAL, command=self.scrollerCanvas.yview)
        scrollBar.grid(row=0, column=3, sticky='ns')
        
        util.addScrollbarTo(canvas= self.scrollerCanvas, 
                            scrollBar= scrollBar, 
                            boundToMouseWheel = self._bound_to_mousewheel, 
                            unboundToMouseWheel = self._unbound_to_mousewheel)
            
        scrollerFrame = Canvas(self.scrollerCanvas, 
                               background          = GB.BGColorDark,
                               highlightbackground = GB.BGColorDark,
                               highlightcolor      = GB.BGColorDark)
        
        scrollerFrame.grid(columnspan=3, sticky= "nsew")
        self.scrollerCanvas.create_window((0,0), window=scrollerFrame, anchor="nw")
        
        self.scrollerFrame = baseScrollerFrame
        
        matchedLevelsWithPage = self.matchedLevels[self.currentPage] if self.hasMoreThanOnePage == True else self.matchedLevels
        
            # Loop and build level cells for the scrollable frame
        for index, level in enumerate(matchedLevelsWithPage):
            
            labelText = util.addBreakLine(text= level.title, strIndex= "by")         
            
            levelImageCanvas = Canvas(scrollerFrame, height=100, width=125, bg= GB.BGColorDark, bd=0, highlightthickness = 0)
            levelImageCanvas.grid(row = index, column=0)
            
            levelImage = util.resize(level.image)
            
            levelImageCanvas.create_image(55, 50, image = levelImage)
            levelImageCell = tk.Label(scrollerFrame, image=levelImage, bg=GB.BGColorDark)
            levelImageCell.image = levelImage
            
            levelImageCanvas.create_image(25, 60, image = self.levelHeart)
            
            heartState = "normal" if level.folderName in self.options.heartedLevelPaths else "hidden"
            levelImageCanvas.itemconfig(2, state=heartState) # the number 2 item is the heart png.
            
            self.currentPageLevels.append((level.folderName, levelImageCanvas))
            
            levelInfoButton = util.makeButton(master= scrollerFrame, text= labelText , command= partial(self.manageLevel, 
                                                                                                        level.path, level.folderName, levelImageCanvas))
            levelInfoButton.configure(bg= GB.BGColorDark, width= 56)
            
            hasJPNChars = False
            hasJPNChars = util.detectJPChars(labelText)
            textLength  = len(labelText)
            
            if textLength > 65  and hasJPNChars: levelInfoButton.config(font= "Helvetica 10 bold" )
            if textLength >= 70 and hasJPNChars: levelInfoButton.config(font= "Helvetica 9 bold" )
            if textLength > 85: levelInfoButton.config(font= "Helvetica 11 bold" )
            
            levelInfoButton.grid(row = index, column=1, columnspan= 2, sticky="ew")

            levelDescription = "No description" if level.description == "" else level.description
            Hovertip(levelInfoButton, util.addBreakLines(levelDescription))
            
        if refreshWindow:
            self.master.overrideredirect(False)
            refreshWindow = False
        # reset to page one after searching
        
        if isAfterSearch:
            self.currentPage = 0
            
#___________________________________________________________________________________________________________________________________________________________
    
root   = tk.Tk()
LBSGUI = LittleBigSearchGUI(master= root)
root.mainloop()

