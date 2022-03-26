from doctest import master
import os, math
import tkinter as tk


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
        if image   != None: btn.config(image= image)
       
        btn.config(text             = text,
                    bd               = 0,
                    fg               = "white",
                    cursor           = "hand2",
                    bg               = buttonColor,
                    activebackground = activeColor)
            
        return btn
        