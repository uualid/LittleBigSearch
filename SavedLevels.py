from GlobalVars import GlobalVars
import tkinter    as tk


class SavedLevels():
    def __init__(self,master, RPCS3Path, closeDelegate):
        super().__init__()
        
        #___ Delegates __________
        self.closeDelegate  = closeDelegate
        #________________________

        RPCS3Path = RPCS3Path
        
        self.window = tk.Toplevel(background= GlobalVars.backgroudnColorLight)
        self.window.title("RPCS3 savedata levels")
        self.window.transient(master)
        
        self.canvas = tk.Canvas(master= self.window,
                                height = 100,
                                width  = 850 ,
                                bg=GlobalVars.backgroudnColorLight, 
                                borderwidth=0,
                                highlightthickness=0)
        self.canvas.grid(columnspan=3, row= 3)

        self.window.protocol("WM_DELETE_WINDOW", self.onClose)

    def onClose(self):
        self.closeDelegate()
        self.window.destroy()