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
    
    #level info centre alignment. I hate tkinter
    @staticmethod
    def getPadding(charCount):
        padding = charCount - 155
        padding = abs(padding) + 25 if charCount < 60 else abs(padding)
        padding = abs(padding) - 10 if charCount > 85 else padding
        return (0, padding) 
    
    @staticmethod
    def splitLevelsToLists(levels, splitSize = 50):
        #Splits the large levels list into smaller lists of 50 element each
        levels = list(levels)
        x = int(math.ceil(len(levels) / splitSize))
        k, m = divmod(len(levels), x)
        return list( (levels[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(x)) )
    
    @staticmethod
    def makeLabel(textVar):
        label = tk.Button(textvariable  = textVar,
                          bd            = 0,
                          bg            = GlobalVars.BGColorDark,
                          fg            = "White",
                          font          = ('Helvatical bold',10))
        return label
    
    @staticmethod
    def makeButton(text, command = 0, buttonColor = GlobalVars.BGColorLight):
        btn = tk.Button(text             = text,
                        bd               = 0,
                        fg               = "white",
                        cursor           = "hand2",
                        bg               = buttonColor,
                        activebackground = GlobalVars.logoBlue)
        if command != 0:
            btn.config(command= lambda: command())
        return btn
        