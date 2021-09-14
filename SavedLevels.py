import threading
import tkinter           as tk
from   Utilities         import GlobalVars
from   tkinter           import Frame, ttk, Button
from   tkinter.constants import VERTICAL
from   PIL               import Image, ImageTk
from   functools         import partial
from   SFOParser         import LevelParser, ParserReturns

class SavedLevels():
    def __init__(self,master, RPCS3Path, closeDelegate, savedLevels = []):
        super().__init__()
        
        #___ Delegates ______________________
        self.closeDelegate  = closeDelegate
        #____________________________________

        self.RPCS3Path = RPCS3Path
        #____________________________________
        self.scrollerCanvas  = tk.Canvas()
        self.scrollerFrame   = Frame()
        self.savedLevels     = savedLevels
        #____________________________________
        self.LevelParser     = LevelParser()
        #____________________________________

        self.window = tk.Toplevel(background= GlobalVars.backgroudnColorLight)
        self.window.title("RPCS3 savedata levels")
        self.window.transient(master)
        
        self.canvas = tk.Canvas(master= self.window,
                                height = 100,
                                width  = 850 ,
                                bg=GlobalVars.backgroudnColorLight, 
                                borderwidth=0,
                                highlightthickness=0)
        self.canvas.grid(columnspan=3)

        #____
        self.refreshButton = tk.Button(master        = self.window,
                                    text             ="Refresh",
                                    command          = lambda: self.refresh(),
                                    bg               = GlobalVars.logoBlue,
                                    activebackground = GlobalVars.logoBlue,
                                    fg = "white", height=1, width= 13, bd=0)
        self.refreshButton.grid(column=1, row=0)

        self.window.protocol("WM_DELETE_WINDOW", self.onClose)
        threadWork = threading.Thread(target= self.fetchSavedLevels, args= ()) 
        threadWork.start()


    # fetch levels from RPCS3 savedata _____________________________________________________
    
    def fetchSavedLevels(self):
        # this event will be called from background thread to use the main thread.
        self.window.bind("<<event1>>", self.showResult)
        self.LevelParser.fetchLevelsFrom(path=self.RPCS3Path, callBack= self.fetchCallBack)
    
    def fetchCallBack(self, response):
        if response == ParserReturns.noResult:
            # self.sendError("No result", "red")
            pass

        elif response == ParserReturns.wrongPath:
            # self.sendError("Please select a levels directory from the settings", "red")
            pass
        else:
            self.savedLevels = response
            # Calls showResult on the main thread.
            self.window.event_generate("<<event1>>")
    
    # Helper methods _______________________________________________________________________

    def _on_mouse_wheel(self, event):
        self.scrollerCanvas.yview_scroll(-1 * int((event.delta / 120)), "units")
        self.scrollerCanvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

    def moveFolder(self, path):
        pass
    
    def refresh(self):
        threading.Thread(target= self.fetchSavedLevels, args= ()).start() 
        
    # window closing protocol ______________________________________________________________
    def onClose(self):
        self.closeDelegate()
        self.window.destroy()

    def showResult(self, evt):
        # destroy the old scroll view
        self.scrollerFrame.destroy()
        
        # build new one
        self.scrollFrame1 = Frame(self.window,
                                  highlightbackground = GlobalVars.backgroundColorDark,
                                  highlightcolor      = GlobalVars.backgroundColorDark)

        self.scrollFrame1.grid(columnspan=3, column=0)

        self.scrollerCanvas = tk.Canvas(self.scrollFrame1,
                                        bg=GlobalVars.backgroundColorDark,
                                        borderwidth=0,
                                        highlightthickness=0)

        self.scrollerCanvas.grid(row=0, column=0, ipadx= 250, ipady=150)

        myScrollBar = ttk.Scrollbar(self.scrollFrame1, 
                                    orient=VERTICAL,
                                    command=self.scrollerCanvas.yview)

        myScrollBar.grid(row=0, column=1, sticky='ns')
        self.scrollerCanvas.configure(yscrollcommand = myScrollBar.set, bg = GlobalVars.backgroundColorDark)

        self.scrollerCanvas.bind('<Configure>', lambda e: self.scrollerCanvas.configure(scrollregion= self.scrollerCanvas.bbox("all")))
        
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

        scrollFrame2 = Frame(self.scrollerCanvas, 
                            background          = GlobalVars.backgroundColorDark,
                            highlightbackground = GlobalVars.backgroundColorDark,
                            highlightcolor      = GlobalVars.backgroundColorDark)

        self.scrollerCanvas.create_window((0,0), window=scrollFrame2, anchor="nw")
        self.scrollerFrame = self.scrollFrame1

            # Loop and build level cells for the scrollable frame
        savedLevels = self.savedLevels
        
        for index, level in enumerate(savedLevels):

            labelText = f'{level.title}' 

            levellogo = Image.open(level.image)

            levelImage_resize = levellogo.resize(( 120, 75 ))
            levellogo = ImageTk.PhotoImage(levelImage_resize)

            levelImage_resize = tk.Label(scrollFrame2, 
                                        image=levellogo,
                                        bg=GlobalVars.backgroundColorDark)
            levelImage_resize.image = levellogo
            levelImage_resize.grid(row = index, column=0)
            
            levelInfoButton = Button(scrollFrame2,
                                    text= labelText + "\n" + level.path, anchor="e",
                                    bd=0, command= partial(self.moveFolder, level.path),
                                    cursor= "hand2",
                                    bg= GlobalVars.backgroundColorDark,
                                    activebackground=GlobalVars.logoBlue,
                                    fg="white",font=('Helvatical bold',10)) 

            levelInfoButton.grid(row = index, column=1 , padx= 20, pady=10)
