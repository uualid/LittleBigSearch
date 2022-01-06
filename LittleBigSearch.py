
import tkinter           as tk
import os, shutil,threading, ttkthemes, time
from   genericpath       import exists
from   tkinter           import Canvas, Frame, Label, TclError, ttk
from   tkinter.constants import VERTICAL
from   functools         import partial
from   PIL               import Image, ImageTk
from   SFOParser         import LevelParser, ParserReturns
import helpers.Utilities as     helpers

from   SavedLevels       import SavedLevels
from   os                import error, path
from Settings.OptionsManager import OptionsManager

class LittleBigSearchGUI():
    def __init__(self, master: tk.Tk, matchedLevels = [], settings = 0, savedLevels = 0) -> None:
        
        self.options = OptionsManager()

        self.scrollerCanvas  = tk.Canvas()
        self.levelScroller   = Frame()
        
        self.levelParser     = LevelParser()
        self.isSearching     = False 
        self.matchedLevels   = matchedLevels
        self.currentPage     = 0
        self.hasMoreThanOnePage = False
        
        self.startTimer = 0
        self.endTimer = 0

        self.last_frame = 0
        self.framelist = []     
        self.frame_index = 0 
        
        self.master = master
        self.master.title("By @SackBiscuit v1.1.3.2")
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

        self.canvas.grid(columnspan=3, sticky= "nsew")
        
        tk.Grid.columnconfigure(master, (0,1,2) , weight = 1)
        tk.Grid.rowconfigure(master, 7, weight = 1)

        self.logo = Image.open('images/UI/LB_Search.png')
        self.logoResize = self.logo.resize(( 500, 122 ))
        self.logo = ImageTk.PhotoImage(image= self.logoResize)

        self.logoLabel = tk.Label(image= self.logo, bg= helpers.GlobalVars.BGColorLight)
        self.logoLabel.image = self.logo
        self.logoLabel.grid(column=1, row=0)
        
        # ____ 
        
        self.settingsButton = helpers.Utilities.makeButton(text="Settings", buttonColor= helpers.GlobalVars.BGColorDark, activeColor= helpers.GlobalVars.BGColorDark)
        self.settingsBtnImage = tk.PhotoImage(file="images/UI/settings.png")
        self.settingsButton.configure(height = 28, width = 120, image= self.settingsBtnImage, command = self.openSettings)
        self.settingsButton.grid(columnspan=3, column=0, row=1, pady=10, padx= (0,130))
        
        # ____


        self.SavedLevelsButton = helpers.Utilities.makeButton(text = "Saved Levels", buttonColor= helpers.GlobalVars.BGColorDark, activeColor= helpers.GlobalVars.BGColorDark)
        self.savedLevelsBtnImage = tk.PhotoImage(file="images/UI/hearted.png")
        self.SavedLevelsButton.configure(height = 28, width = 120, image= self.savedLevelsBtnImage, command = self.openSavedLevels)
        self.SavedLevelsButton.grid(columnspan=3, column=0, row=1, pady=10, padx= (130,0))
        # ____ 
        searchLabel = tk.Label(text  = "The Search will look for level name, creator ID or any keyword in the level Description",
                               bg    = helpers.GlobalVars.BGColorDark,
                               fg    = "White",
                               font  = ('Helvatical bold',10))

        searchLabel.grid(columnspan=3, column=0, row=2)
        searchTextField = tk.Entry(bd= 0, font=15, bg="black", fg="white")
        searchTextField.grid(columnspan=3, row=3, column=0, ipadx= 250)

        searchButton = helpers.Utilities.makeButton(text="Search", buttonColor= helpers.GlobalVars.BGColorDark, activeColor= helpers.GlobalVars.BGColorDark)
        self.searchBtnImage = tk.PhotoImage(file="images/UI/search.png")
        searchButton.configure(height = 28, width = 120, image= self.searchBtnImage, 
                               command = lambda: threading.Thread(target= self.LBSsearch, args= (searchTextField.get(), self.options.archivePath)).start())
        searchButton.grid(column=1, row=4, pady=(13,13))

        self.errorText  = tk.StringVar()
        self.errorLabel = helpers.Utilities.makeLabel(self.errorText)
        self.errorText.set("")
        self.errorLabel.grid(column=1, row=5, ipadx=30, pady=(0,3))

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
        self.configureGif()
        self.earthGif = tk.Label(bg= helpers.GlobalVars.BGColorDark)
        self.earthGif.grid(column=1, row=4, padx= (200, 0) ,pady=(5,0))
        self.options.fetchSettings()
        

    # search method _____________________________________________________________________________________________________________________________________

    def configureGif(self):
        for i in range(32): #theres 32 frame to the globe animation.
            try:
                frame = Image.open(f'images/animation/earth{i + 1}.png')
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
        
        threading.Timer(10.0, self.startWaiter).start()

    def LBSsearch(self, term, path):
        if self.isSearching:
            return
        if self.options.RPCS3Path.__contains__("/") == False:
            self.sendError("Please select a destination folder", "red")
            return
        
        self.startTimer = time.time()
        self.startWaiter()
        self.currentPage = 0
        self.isSearching = True
        self.animate(0)
        
        # this event will be called from background thread to use the main thread.
        self.master.bind("<<event1>>", self.updatePage)
        self.levelParser.search(self.searchCallBack, path, term, includeDescription= self.options.includeDescription)
        
    def searchCallBack(self, response):
        if response == ParserReturns.noResult:
            self.sendError("No result", "red")

        elif response == ParserReturns.noPath:
            self.sendError("Please select a levels directory from the settings", "red")
        
        elif response == ParserReturns.wrongPath:
            self.sendError("Can't find any level archive directory", "red")
        
        else: #if levels were found.
            levels = response if self.options.includeDups == True else set(response)
            self.matchedLevels = helpers.Utilities.splitLevelsToLists(levels = levels) if len(levels) > 50 else levels
            self.endTimer = time.time()
            print(f"{self.endTimer - self.startTimer},")
            
            self.showPagingButtons()
            # Calls showResult on the main thread.
            self.master.event_generate("<<event1>>")
        self.isSearching = False

    # Saved levels _______________________________________________________________________________________________________________________________________

    def openSavedLevels(self):
        if self.options.RPCS3Path == '':
            self.sendError("Please select a destination folder", "red")
            return
        try:
            self.savedLevels.window.lift()
        except:
            self.savedLevels = SavedLevels(master        = self.master, 
                                           RPCS3Path     = self.options.RPCS3Path)

    # Settings ____________________________________________________________________________________________________________________________________________

    def openSettings(self):
        self.options.openSettings(master= self.master)
                        
    # Helper methods _____________________________________________________________________________________________________________________________________

    def moveFolder(self, source):
        destination = self.options.RPCS3Path
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
        self.master.update()
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
        mainFrame = Frame(self.master, bg= helpers.GlobalVars.BGColorDark,
                          highlightbackground  = helpers.GlobalVars.BGColorDark,
                          highlightcolor       = helpers.GlobalVars.BGColorDark)
        
        tk.Grid.columnconfigure(mainFrame, 0, weight=1)
        tk.Grid.rowconfigure(mainFrame, 0, weight=1)
        # tk.Grid.columnconfigure(mainFrame, 1, weight=1)

        mainFrame.grid(columnspan=3, sticky="nsew")
        
        
        self.scrollerCanvas = tk.Canvas(mainFrame,bg=helpers.GlobalVars.BGColorDark, borderwidth=0, highlightthickness=0, height=600, width=880)
        self.scrollerCanvas.grid(row=0, column=0, sticky= "ns")


        ScrollBar = ttk.Scrollbar(mainFrame, orient=VERTICAL, command=self.scrollerCanvas.yview)
        ScrollBar.grid(row=0, column=3, sticky='ns')
        

        self.scrollerCanvas.configure(yscrollcommand=ScrollBar.set)
        self.scrollerCanvas.bind('<Configure>', lambda e: self.scrollerCanvas.configure(scrollregion= self.scrollerCanvas.bbox("all")))
        
        self.scrollerCanvas.bind('<Enter>', self._bound_to_mousewheel)
        self.scrollerCanvas.bind('<Leave>', self._unbound_to_mousewheel)
    
        scrollerFrame = Canvas(self.scrollerCanvas, 
                             background          = helpers.GlobalVars.BGColorDark,
                             highlightbackground = helpers.GlobalVars.BGColorDark,
                             highlightcolor      = helpers.GlobalVars.BGColorDark)
        
        scrollerFrame.grid(columnspan=3, sticky= "nsew")
        self.scrollerCanvas.create_window((0,0), window=scrollerFrame, anchor="nw")
        
        self.levelScroller = mainFrame
        
        
        matchedLevelsWithPage = self.matchedLevels[self.currentPage] if self.hasMoreThanOnePage == True else self.matchedLevels
        
            # Loop and build level cells for the scrollable frame
        for index, level in enumerate(matchedLevelsWithPage):

            labelText = f'{level.title}'

            levellogo = Image.open(level.image)

            levelImage_resize = levellogo.resize(( 120, 75 ))
            levellogo = ImageTk.PhotoImage(levelImage_resize)

            levelImage_resize = tk.Label(scrollerFrame, image=levellogo, bg=helpers.GlobalVars.BGColorDark)
            levelImage_resize.image = levellogo

            #if the path for the folder is long take only part of it.
            levelPath = f'...{level.path[-80:]}' if len(level.path) > 90 else level.path  
            levelImage_resize.grid(row = index, column=0, padx= (30,0))
            
            levelInfoButton = helpers.Utilities.makeButton(master= scrollerFrame, text= labelText + "\n" + levelPath, command= partial(self.moveFolder, level.path))
            levelInfoButton.configure(bg= helpers.GlobalVars.BGColorDark, width= 84)
            
            levelInfoButton.grid(row = index, column=1, columnspan= 2, sticky="ew")
        
        # reset to page one after searching
        if isAfterSearch:
            self.currentPage = 0
            
#___________________________________________________________________________________________________________________________________________________________
    
root   = tk.Tk()
LBSGUI = LittleBigSearchGUI(master= root)
root.mainloop()

