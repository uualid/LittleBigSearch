import os, math, sys, re
import tkinter as tk
from tkinter import Frame
from tkmacosx import Button
from PIL import ImageTk, Image
import subprocess

class GlobalVars:
    BGColorDark   = "#1e1e1e"
    BGColorLight  = "#2f2f2f"
    logoBlue      = "#2cb4e8"
    
    GLOBE_GIF_FRAME_COUNT = 32
    
    SCROLLER_BASE  = 1
    SCROLLER_FRAME = 0

    CURRENT_MACOS_PATH = os.getcwd()


class Utilities:
    
    @staticmethod
    def openFile(path):
        try:
            subprocess.call(["open", "-R", path])
        except:
            print("Failed to open folder")
    
    @staticmethod
    def detectJPChars(texts):
        # japanese
        if re.search("[\u3040-\u30ff]", texts):
            return True
        # chinese
        if re.search("[\u4e00-\u9FFF]", texts):
            return True
        return False
    
    @staticmethod
    def splitLevelsToLists(levels, splitSize = 50):
        #Splits the large levels list into smaller lists of 50 element each
        levels = list(levels)
        x = int(math.ceil(len(levels) / splitSize))
        k, m = divmod(len(levels), x)
        return list( (levels[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(x)) )
    
    @staticmethod
    def addBreakLine(text, strIndex):
        try:
            breakLineIndex = text.index(strIndex)
            return text[:breakLineIndex] + "\n" + text[breakLineIndex:]
        except:
            return text
    
                
    @staticmethod
    def makeCheckBox(command, 
                     text, 
                     variable, 
                     background= GlobalVars.BGColorDark,
                     activeColor = GlobalVars.logoBlue,
                     master = None):
        
        chkBox = tk.Checkbutton()
        if master != None: chkBox = tk.Checkbutton(master= master)
        
        chkBox.config(text               = text,
                      onvalue            = 1,
                      background         = background,
                      fg                 = "white",
                      offvalue           = 0,
                      activebackground   = activeColor,
                      selectcolor        = "#000000",
                      variable           = variable,
                      command            = command)
        return chkBox
        
    @staticmethod
    def makeLabel(textVar,
                  master      = None,
                  activeColor = None,
                  cursor      = None,
                  image       = None,
                  command     = None,
                  backgroundColor = GlobalVars.BGColorDark):
        
        label = tk.Button()
        if master  != None: label = tk.Button(master= master)
        if cursor  != None: label.config(cursor= cursor)
        if image   != None: label.config(image = image)
        if command != None: label.config(command= command)
        if activeColor != None: label.config(activebackground= activeColor)
        
        
        label.config(textvariable  = textVar,
                    bd             = 0,
                    bg             = backgroundColor,
                    fg             = "black",
                    font           = ('Helvatical bold',13))
        return label
    
    @staticmethod
    def makeMacLabel(textVar,
                  master      = None,
                  activeColor = None,
                  cursor      = None,
                  image       = None,
                  command     = None,
                  backgroundColor = GlobalVars.BGColorDark):
        
        label = tk.Button()
        if master  != None: label = tk.Button(master= master)
        if cursor  != None: label.config(cursor= cursor)
        if image   != None: label.config(image = image)
        if command != None: label.config(command= command)
        if activeColor != None: label.config(activebackground= activeColor)
        
        
        label.config(textvariable  = textVar,
                    bd             = 0,
                    background     = "black",
                    bg             = "black",
                    fg             = "black",
                    font           = ('Helvatical bold',13))
        return label
        
    @staticmethod
    def makeButton(master     = None, 
                  text        = None,
                  command     = None,
                  image       = None,
                  font   = "Helvetica 13 bold",
                  buttonColor = GlobalVars.BGColorLight,
                  activeColor = GlobalVars.logoBlue):

        btn = Button()
        if master  != None: btn = Button(master= master)
        if command != None: btn.config(command= lambda: command())
        if text    != None: btn.config(text = text)
        if image   != None: btn.config(image= image); btn.image = image
        
        btn.config( bd                  = 0,
                    borderless          = 1,
                    focuscolor          = '',
                    bordercolor         = 'blue',
                    fg                  = "white",
                    cursor              = "hand2",
                    font                = font,
                    highlightbackground = GlobalVars.BGColorDark,
                    bg                  = buttonColor,
                    activebackground    = activeColor)
        
        return btn   
    
    @staticmethod
    def makeFrame(master = None):
        frame = Frame()
        if master != None: frame = Frame(master)
        
        frame.config(bg                   = GlobalVars.BGColorDark,
                     highlightbackground  = GlobalVars.BGColorDark,
                     highlightcolor       = GlobalVars.BGColorDark)
       
        tk.Grid.columnconfigure(frame, 0, weight=1)
        tk.Grid.rowconfigure(frame, 0, weight=1)
        return frame
    
    @staticmethod
    def makeScrollerCanvas(height = None, width = None, master = None):
        scrollerCanvas = tk.Canvas()
        if master != None: scrollerCanvas = tk.Canvas(master)
        if height != None: scrollerCanvas.config(height= height) 
        if width  != None: scrollerCanvas.config(width= width) 
        
        scrollerCanvas.config(bg = GlobalVars.BGColorDark, 
                              borderwidth        = 0, 
                              highlightthickness = 0)
        return scrollerCanvas
    
    @staticmethod
    def resize(image, height = 135, width = 80):
        '''Resizes image and returns PhotoImage from ImageTK'''
        img = Image.open(image)
        imgResized = img.resize((height, width))
        finalImage = ImageTk.PhotoImage(imgResized)
        
        return finalImage
    
    @staticmethod    
    def addScrollbarTo(canvas, scrollBar, boundToMouseWheel, unboundToMouseWheel):
        canvas.configure(yscrollcommand=scrollBar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion= canvas.bbox("all")))
        canvas.bind('<Enter>', boundToMouseWheel)
        canvas.bind('<Leave>', unboundToMouseWheel)
    
    # @staticmethod
    # def resourcePath(relative_path):
    #     '''Returns the path for all the app resources. Images, icon... etc 
    #     For Windows only'''
    #     if hasattr(sys, '_MEIPASS'):
    #         return os.path.join(sys._MEIPASS, relative_path)
    #     return os.path.join(os.path.abspath("."), relative_path)
    
    @staticmethod
    def addBreakLines(content):
        '''Adds a break point every 70 charecter if it has japanese characters (Japanes charecters take larger spaces) 
        or every 100 for English characters'''
        breakLine = 70 if Utilities.detectJPChars(content) == True else 100
        if len(content) < 50: return content
        finalContent = content
        index = breakLine
        while True:
            beginningContent = finalContent[:index]
            endContent       = finalContent[index:]
            finalContent = beginningContent + " \n " + endContent
            index += breakLine
            if index > len(content):
                return finalContent
    @staticmethod
    def resizeStringToFit(string):
        '''Resize text according to its length and if it has a Japanes charecters. (Japanes charecters take larger spaces)'''
        hasJPNChars = Utilities.detectJPChars(string)
        textLength  = len(string)
        
        if textLength > 65  and hasJPNChars: return "Helvetica 10 bold"
        if textLength >= 70 and hasJPNChars: return "Helvetica 9 bold"
        if textLength > 85: return "Helvetica 11 bold"
        return "Helvetica 13 bold"
    
    @staticmethod
    def loadGif(framesCount, gifDir, gifName):
        '''Loads gif into a list'''
        frameList = []
        for i in range(framesCount):
            try:
                frame = Image.open(gifDir + gifName + f'{i + 1}' + ".png")
                frameResized = frame.resize((45, 45))
                frame = ImageTk.PhotoImage(image= frameResized)
                frameList.append(frame)
                 
            except:
                break
        return frameList
        