import imp
import os, math, sys
import tkinter as tk
from tkinter import Frame
from PIL import ImageTk, Image

class GlobalVars:
    BGColorDark   = "#1e1e1e"
    BGColorLight  = "#2f2f2f"
    logoBlue      = "#2cb4e8"


class Utilities:
    
    @staticmethod
    def openFile(path):
        try:
            path = os.path.realpath(path)
            os.startfile(path)
        except:
            print("Failed to open folder")
    
    
    @staticmethod
    def splitLevelsToLists(levels, splitSize = 50):
        #Splits the large levels list into smaller lists of 50 element each
        levels = list(levels)
        x = int(math.ceil(len(levels) / splitSize))
        k, m = divmod(len(levels), x)
        return list( (levels[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(x)) )
    
    @staticmethod
    def addBreakLineIfNeeded(text, strIndex):
        if len(text) > 60:
            breakLineIndex = text.index(strIndex)
            return text[:breakLineIndex] + "\n" + text[breakLineIndex:]
        else:
            return f'{text}'  
                
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
                    fg             = "White",
                    font           = ('Helvatical bold',10))
        return label
    
    @staticmethod
    def makeButton(text = None,
                command = None,
                 master = None,
                 image  = None,
                buttonColor = GlobalVars.BGColorLight,
                activeColor = GlobalVars.logoBlue):
        
        btn = tk.Button()
        if master  != None: btn = tk.Button(master)
        if command != None: btn.config(command= lambda: command())
        if text    != None: btn.config(text= text)
        if image   != None: btn.config(image= image); btn.image = image
       
        btn.config(text             = text,
                    bd               = 0,
                    fg               = "white",
                    cursor           = "hand2",
                    font= "Helvetica 12 bold",
                    bg               = buttonColor,
                    activebackground = activeColor)
            
        return btn
    
    @staticmethod
    def makeScrollerFrame(master = None):
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
    
    @staticmethod
    def resourcePath(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)
    
    @staticmethod
    def addBreakLines(content):
        if len(content) < 50: return content
        finalContent = content
        index = 100
        while True:
            beginningContent = finalContent[:index]
            endContent       = finalContent[index:]
            finalContent = beginningContent + " \n " + endContent
            index += 100
            if index > len(content):
                return finalContent