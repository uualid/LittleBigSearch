import tkinter           as tk
import os, shutil,threading, ttkthemes
from   genericpath       import exists
from   tkinter           import Button, Frame, ttk
from   tkinter.constants import VERTICAL
from   functools         import partial
from   PIL               import Image, ImageTk
from   tkinter           import filedialog
from   SFOParser         import LevelParser, ParserReturns

#global values ________________
backgroundColorDark  = "#1e1e1e"
backgroudnColorLight = "#2f2f2f"
logoBlue = "#2cb4e8"

class LittleBigSearchGUI():
    def __init__(self, master: tk.Tk, matchedLevels = []) -> None:
        

        self.scrollerCanvas = tk.Canvas()
        self.scrollerFrame  = Frame()
        self.levelParser    = LevelParser()
        self.matchedLevels  = matchedLevels
        
        self.master = master
        self.master.title("LittleBigSearch by @SackBiscuit v1.1.0")
        self.master.iconbitmap(default="images/icon.ico")
        self.master.configure(bg= backgroundColorDark)

        ttkthemes.themed_style.ThemedStyle(theme="adapta")

        # _ UI _______________________

        self.canvas = tk.Canvas(master,
                                height = 150,
                                width  = 900 ,
                                bg=backgroudnColorLight, 
                                borderwidth=0,
                                highlightthickness=0)

        self.canvas.grid(columnspan=3)

        self.logo = Image.open('images/LBSearch.png')

        self.logoResize = self.logo.resize(( 500, 112 ))
        self.logo = ImageTk.PhotoImage(image= self.logoResize)

        self.logoLabel = tk.Label(image= self.logo, bg= backgroudnColorLight)
        self.logoLabel.image = self.logo
        self.logoLabel.grid(column=1, row=0)
        
        # ____ 

        self.RPCSLabelStr = tk.StringVar()
        self.RPCSLabel = tk.Button(textvariable=self.RPCSLabelStr,
                                    bg=backgroundColorDark,
                                    command=lambda: self.openFile(self.RPCSLabelStr.get()),
                                    cursor= "hand2",
                                    fg="White",
                                    bd = 0,
                                    activebackground= logoBlue,
                                    font=('Helvatical bold',10))
       
        self.RPCSLabelStr.set("Select an RPCS3 savedata folder")
        self.RPCSLabel.grid(columnspan=3, column=0, row=1, sticky= "we")

        self.RPCSBrowseBtn = tk.Button( text="Browse",
                                    command=lambda: self.openFileBrowser(self.RPCSLabelStr),
                                    bg=logoBlue, 
                                    activebackground= logoBlue,
                                    fg = "white", height=1, width= 10, bd=0)
        self.RPCSBrowseBtn.grid(column=1, row=2, pady=(5, 5))
        
        # ____

        self.archiveLabelStr = tk.StringVar()
        self.archiveLabel = tk.Button(textvariable=self.archiveLabelStr,
                                    bg=backgroundColorDark,
                                    cursor= "hand2",
                                    activebackground= logoBlue,
                                    command=lambda: self.openFile(self.archiveLabelStr.get()),
                                    fg="White",
                                    bd =0,
                                    font=('Helvatical bold',10))
       
        self.archiveLabelStr.set("Select the level archive folder for LittleBigPlanet 1, 2 or 3",)
        self.archiveLabel.grid(columnspan=3, column=0, row=3, sticky= "we")

        self.archiveBrowseBtn = tk.Button( text="Browse",
                                    activebackground= logoBlue,
                                    command=lambda: self.openFileBrowser(self.archiveLabelStr),
                                    bg=logoBlue,
                                    fg = "white", height=1, width= 10, bd=0)
        self.archiveBrowseBtn.grid(column=1, row=4, pady=(5, 20))
        # ____


        searchLabel = tk.Label(text= "The Search will look for level name, creator ID or any keyword in the level Description",
                                bg=backgroundColorDark,
                                fg="White",
                                font=('Helvatical bold',10))
        searchLabel.grid(columnspan=3, column=0, row=5)
        searchTextField = tk.Entry(bd= 0, font=15, bg="black", fg="white")
        searchTextField.grid(columnspan=3, row=6, column=0, ipadx= 250)

        searchButton = tk.Button(text="Search",
                                command= lambda: threading.Thread(target= self.LBSsearch, args= (searchTextField.get(), self.archiveLabelStr.get()) ).start(),
                                bd=0,
                                bg= logoBlue, 
                                fg= "white", 
                                activebackground = logoBlue,
                                height=1, width= 10)

        searchButton.grid(column=1, row=7, pady=10)


        self.errorText  = tk.StringVar()
        self.errorLabel = Button(textvariable= self.errorText,
                            bd=0,
                            bg=backgroundColorDark,
                            activebackground=logoBlue)
        self.errorText.set("")
        self.errorLabel.grid(column=1, row=8, ipadx=30)

    # search method _____________________________________________________________________________________________________________________________________

    def LBSsearch(self, term, path):
        if self.RPCSLabelStr.get().__contains__("/") == False:
            self.editErrorLabel("Please select an RPCS3 savedata folder", "red")
            return

        self.editErrorLabel("Searching...")
        # this event will be called from background thread to use the main thread.
        self.master.bind("<<event1>>", self.showResult)
        self.levelParser.search(self.searchCallBack, 
                                term,
                                path)
    
    def searchCallBack(self, response):
        if response == ParserReturns.noResult:
            self.editErrorLabel("No result", "red")

        elif response == ParserReturns.wrongPath:
            self.editErrorLabel("Please select a level directory", "red")
        
        else:
            self.matchedLevels = response
            # Calls showResult on the main thread.
            self.master.event_generate("<<event1>>")

    # Helper methods _____________________________________________________________________________________________________________________________________

    def moveFolder(self, source):
        destination = self.RPCSLabelStr.get()
        destDir = os.path.join(destination,os.path.basename(source))
        if exists(destDir) == False:
            self.editErrorLabel("Level folder was added to RPCS3 savedata", "green")
            shutil.copytree(source, destDir)
        else:
            self.editErrorLabel("Level folder was removed from RPCS3 savedata")
            shutil.rmtree(destDir)
    
    # replaced by moveFolder
    # def copyToClipboard(self, text): 
    #     self.master.clipboard_clear()
    #     self.master.clipboard_append(text)
    #     self.editErrorLabel("Path copied!", "green")
    def openFile(self, path):
        try:
            path = os.path.realpath(path)
            os.startfile(path)
        except:
            print("Failed to open folder")

    def openFileBrowser(self, labelStr):
        selectedFolder = filedialog.askdirectory()
        if selectedFolder:
            levelsArchive = selectedFolder
            labelStr.set(levelsArchive)

    def _on_mouse_wheel(self, event):
        global canvasScroll
        self.editErrorLabel("")
        self.scrollerCanvas.yview_scroll(-1 * int((event.delta / 120)), "units")
        self.scrollerCanvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

    def editErrorLabel(self, message = "", color = "white"):
        self.errorLabel.configure(fg=color)
        self.errorText.set(message)        

    # builds result scroller view _______________________________________________________________________________________________________________________________
    
    def showResult(self, evt):
        self.editErrorLabel("")
        # destroy the old scroll view
        self.scrollerFrame.destroy()
        
        # build new one
        self.scrollFrame1 = Frame(self.master,
                            highlightbackground=backgroundColorDark,
                            highlightcolor=backgroundColorDark)

        self.scrollFrame1.grid(columnspan=3, column=0)

        self.scrollerCanvas = tk.Canvas(self.scrollFrame1,bg=backgroundColorDark, borderwidth=0, highlightthickness=0)
        self.scrollerCanvas.grid(row=0, column=0, ipadx= 250, ipady=150)

        myScrollBar = ttk.Scrollbar(self.scrollFrame1, orient=VERTICAL, command=self.scrollerCanvas.yview)
        myScrollBar.grid(row=0, column=1, sticky='ns')
        

        self.scrollerCanvas.configure(yscrollcommand=myScrollBar.set, bg=backgroundColorDark)
        self.scrollerCanvas.bind('<Configure>', lambda e: self.scrollerCanvas.configure(scrollregion= self.scrollerCanvas.bbox("all")))
        
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

        scrollFrame2 = Frame(self.scrollerCanvas, 
                            background= backgroundColorDark,
                            highlightbackground=backgroundColorDark,
                            highlightcolor=backgroundColorDark)

        self.scrollerCanvas.create_window((0,0), window=scrollFrame2, anchor="nw")

        self.scrollerFrame = self.scrollFrame1

            # Loop and build level cells for the scrollable frame
        for index, level in enumerate( set(self.matchedLevels) ):
            # ------------------------- ⬆ sets will remove duplicates.

            labelText = f'{level.title}' 

            levellogo = Image.open(level.image)

            levelImage_resize = levellogo.resize(( 120, 75 ))
            levellogo = ImageTk.PhotoImage(levelImage_resize)

            levelImage_resize = tk.Label(scrollFrame2, image=levellogo, bg=backgroundColorDark)
            levelImage_resize.image = levellogo
            levelImage_resize.grid(row = index, column=0)
            
            levelInfoButton = Button(scrollFrame2,
                                    text= labelText + "\n" + level.path, anchor="e",
                                    bd=0, command= partial(self.moveFolder, level.path),
                                    cursor= "hand2",
                                    bg= backgroundColorDark,
                                    activebackground=logoBlue,
                                    fg="white",font=('Helvatical bold',10)) 

            levelInfoButton.grid(row = index, column=1 , padx= 20, pady=10)


    
root   = tk.Tk()
LBSGUI = LittleBigSearchGUI(master= root)
root.mainloop()

