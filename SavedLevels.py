import threading, os,shutil
import tkinter           as tk
from   tkinter           import Frame, ttk
from   tkinter.constants import VERTICAL
from   functools         import partial
from   SFOParser         import LevelParser, ParserReturns
from   genericpath       import exists
from idlelib.tooltip     import Hovertip
from helpers.Utilities import GlobalVars as GB
from helpers.Utilities import Utilities as util

class SavedLevels():
    def __init__(self,master, RPCS3Path,  removeLevelCallBack, savedLevels = []):
        super().__init__()

        self.RPCS3Path = RPCS3Path
        #____________________________________
        self.scrollerCanvas  = tk.Canvas()
        self.scrollerFrame   = Frame()
        self.savedLevels     = savedLevels
        #____________________________________
        self.LevelParser     = LevelParser()
        #____________________________________
        self.removeLevelCallBack = removeLevelCallBack

        self.window = tk.Toplevel(background= GB.BGColorLight)
        self.window.title("Destination Folder")
        self.window.transient(master)
        
        self.canvas = tk.Canvas(master = self.window,
                                height = 100,
                                width  = 900 ,
                                bg     = GB.BGColorLight, 
                                borderwidth=0,
                                highlightthickness=0)
        self.canvas.grid(columnspan=3)

        tk.Grid.columnconfigure(self.window, (0,1,2), weight = 1)
        

        #____
        self.removeBtnImage = tk.PhotoImage(file=util.resourcePath("images\\UI\\remove.png"))

        refreshImage = tk.PhotoImage(file=util.resourcePath("images\\UI\\refresh.png"))
        self.refreshButton   = util.makeButton(master  = self.window, 
                                               image   = refreshImage,
                                               command = lambda: self.refresh(),
                                               buttonColor = GB.BGColorLight,
                                               activeColor = GB.BGColorLight)
        
        self.refreshButton.configure(height = 28, width = 160)
        self.refreshButton.grid(column=1, row=0, padx= (180, 0))


        self.openFolderBtnImage = tk.PhotoImage(file=util.resourcePath("images\\UI\\openFolder.png"))
        self.openDestFolder = util.makeButton(master   = self.window,
                                              image    = self.openFolderBtnImage,
                                              command  = lambda: util.openFile(self.RPCS3Path),
                                              buttonColor = GB.BGColorLight,
                                              activeColor = GB.BGColorLight)
        
        self.openDestFolder.configure(height = 28, width = 160)
        self.openDestFolder.grid(column=1, row=0, padx= (0, 110))

        self.window.protocol("WM_DELETE_WINDOW", self.onClose)
        threadWork = threading.Thread(target= self.fetchSavedLevels, args= ()) 
        threadWork.start()


    # fetch levels from RPCS3 savedata _____________________________________________________
    
    def fetchSavedLevels(self):
        # this event will be called from background thread to use the main thread.
        try:
            self.window.bind("<<event1>>", self.showResult)
            self.LevelParser.search(path= self.RPCS3Path, callBack= self.fetchCallBack)
        except:
            print("DEBUG: Hearted levels window is not available.")
            
    def fetchCallBack(self, response):
        if response == ParserReturns.noResult:
            # self.sendError("No result", "red")
            # No result = empty levels in RPCS3 so destroy the scroller frame.
            self.scrollerFrame.destroy()

        elif response == ParserReturns.noPath:
            # self.sendError("Please select a levels directory from the settings", "red")
            pass
        else:
            self.savedLevels = response[::-1] # flipped list to show new added levels on top
            # Calls showResult on the main thread.
            self.window.event_generate("<<event1>>")
    
    # Helper methods _______________________________________________________________________

    def _bound_to_mousewheel(self, event):
        self.scrollerCanvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

    def _unbound_to_mousewheel(self, event):
        self.scrollerCanvas.unbind_all("<MouseWheel>")

    def _on_mouse_wheel(self, event):
        self.window.update()
        self.scrollerCanvas.yview_scroll(-1 * int((event.delta / 120)), "units")
        

    # level managing _______________________________________________________________________
    
    def removeFolder(self, source, levelFolderName):
        destination = self.RPCS3Path
        destDir = os.path.join(destination,os.path.basename(source))
        if exists(destDir) == True:
            try:
                shutil.rmtree(destDir)
            except:
                print("Level folder is busy with other process")
                
            self.removeLevelCallBack(destDir, levelFolderName)
            self.refresh()
        
    def refresh(self):
        threading.Thread(target= self.fetchSavedLevels, args= ()).start()

    # window closing protocol ______________________________________________________________
    def onClose(self):
        self.window.destroy()

    def showResult(self, evt):
        # destroy the old scroll view
        self.scrollerFrame.destroy()
        
        if self.savedLevels == []:
            ### notification later here ## 
            return
        
        # build new one
        self.baseScrollerFrame = util.makeScrollerFrame(self.window)

        self.baseScrollerFrame.grid(columnspan=3, column=0, sticky= "ew")
        tk.Grid.columnconfigure(self.baseScrollerFrame, 0, weight = 1)

        self.scrollerCanvas = util.makeScrollerCanvas(master = self.baseScrollerFrame)
        self.scrollerCanvas.grid(row=0, column=0, ipadx= 250, ipady=150)

        scrollBar = ttk.Scrollbar(self.baseScrollerFrame, orient=VERTICAL, command=self.scrollerCanvas.yview)
        scrollBar.grid(row=0, column=1, sticky='ns')
        
        util.addScrollbarTo(canvas    = self.scrollerCanvas,
                            scrollBar = scrollBar,
                            boundToMouseWheel   = self._bound_to_mousewheel,
                            unboundToMouseWheel = self._unbound_to_mousewheel)
        
        scrollFrame = Frame(self.scrollerCanvas, 
                            background          = GB.BGColorDark,
                            highlightbackground = GB.BGColorDark,
                            highlightcolor      = GB.BGColorDark)

        self.scrollerCanvas.create_window((0,0), window=scrollFrame, anchor="nw")
        self.scrollerFrame = self.baseScrollerFrame

            # Loop and build level cells for the scrollable frame
        savedLevels = self.savedLevels
        
        for index, level in enumerate(savedLevels):

            labelText = util.addBreakLine(text= level.title, strIndex= "by")  
            levelImage = util.resize(level.image)

            levelImageCell = tk.Label(scrollFrame, image=levelImage, bg=GB.BGColorDark)
            levelImageCell.image = levelImage
            
            levelPath = f'...{level.path[-80:]}' if len(level.path) > 90 else level.path
            levelImageCell.grid(row = index, column=0)
            
            levelInfoButton = util.makeButton(master= scrollFrame, text= labelText + "\n" + levelPath, command= partial(util.openFile, level.path))
            levelInfoButton.configure(bg= GB.BGColorDark, width= 64)
            levelInfoButton.grid(row = index, column=1 , padx= 20, pady=(0, 38))
            
            levelDescription = "No description" if level.description == "" else level.description
            Hovertip(levelInfoButton, util.addBreakLines(levelDescription))
            removeLevelButton = util.makeButton(master = scrollFrame,  
                                                buttonColor = GB.BGColorDark,
                                                activeColor = GB.BGColorDark)
            
            removeLevelButton.configure(height = 28, width = 120, image= self.removeBtnImage, 
                                        command = partial(self.removeFolder, level.path, level.folderName))
            removeLevelButton.grid(row = index, column=1, pady=(60, 0))

