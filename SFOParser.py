from genericpath import exists
from Modules.LevelModule import Level
import enum, os

class ParserReturns(enum.Enum):
    noResult   = 1
    noPath     = 2
    wrongPath  = 3


#  ______________________ LevelParser _______________________________________________________________________________________________________

# To get the level name + the user id, I had to know the start index for the level name and end index for the user id. 
# if you open the SFO file you will realize that before every level name you'll see the folder name, ex: BCES00850LEVEL5BE0A8A3random Level....
# so to solve this problem I gave 'SFOStartIndex' the folder name as string parameter to get the index for it and I added the
# number of char of that folder name to remove it from the return.
# and the same goes for the end index. for lbp1 levels, they always end up with 'LittleBigPlanet' or 'LittleBigPlanet™2' for lbp2. etc...
# so I choose these to find my end index. It's very basic but it worked very well so far for this project.

machineCode = ['\x01', '\x02', '\x07u', '\x19+0', '\x12', '\x1bq', '\x1f', '\x16', '\n', 
               '\x07ffffffffffffffff', '\x08u', '\x08ffffffffffffffff', 'uffffffffffffffff', 
               'P\ue004', '\ue004P', 'x06ffffffffffffffff', '\x06u', '\x03ffffffffffffffff',
               '\x03u', '\x06ffffffffffffffff', '\tXț7ef60160379655bc', '\x03[I+Z', 'x18SD_Gk'
               ,'\x037ef60160379655bc', '\x03',  '\x03M', '\x0eq' , '\x05', '\x14lY',  '\x13', 
               '\x0e=510a61ebfdb8f8c9', '\x0bu', 'x0bffffffffffffffff', '\x18SD_Gk', '\x0bu', 
               '\x0bffffffffffffffff', "\'=", "=\'"]

class LevelParser:

    #___ inits ______________________________________________

    def __init__(self, includeDescription = True) -> None:
        self.includeDescription = includeDescription
    #________________________________________________________

    @staticmethod 
    def checkIfThereIsNoMatch(list: list):
        if list == []:
            return ParserReturns.noResult
        else:
            return list

    @staticmethod
    def SFOStartIndex(levelInfo: str, folderName: str):    
        return levelInfo.index(folderName) + len(folderName)

    @staticmethod
    def SFOEndIndex(levelInfo):
        if levelInfo.__contains__("LittleBigPlanet™2"):
            return levelInfo.index("LittleBigPlanet™2")

        elif levelInfo.__contains__("LittleBigPlanet™3"):
            return levelInfo.index("LittleBigPlanet™3")

        else:
            return levelInfo.index("LittleBigPlanet")
    
    @staticmethod
    def clean(SFOstring: str):
            #For some reason after getting the level string from the SFO, I get alot of machine code with it.
        return SFOstring.replace('\x00', '')
    
    @staticmethod
    def getLevelTitle(SFOContent: str, levelFolder: str):
        startIndex = LevelParser.SFOStartIndex(SFOContent, levelFolder) 
        endIndex   = LevelParser.SFOEndIndex(SFOContent)
        title      = LevelParser.clean( f'{SFOContent[startIndex : endIndex]}')
        
        return title

    #__ Main search method __________________________________________________________________________________
    def guard(self, path: str, callBack):
        if exists(path) == False:
            callBack(ParserReturns.wrongPath)
            return True

        if path.__contains__("/") == False:
            callBack(ParserReturns.noPath)
            return True

        return False
    
    def search(self, callBack, path, term: str = "", includeDescription: bool = True):
            # Empty the array for the next search.
        matchedLevels = []
        matchedLeveAppend = matchedLevels.append 
        term = term.lower()
        
        if self.guard(path, callBack):
            return

        for levelFolder in os.listdir(path):
            if "." in levelFolder:
                    #Skips files, only folders.
                continue
        
            for levelfile in os.listdir(path + "/" + levelFolder):
                if levelfile.endswith(".SFO"):
                    
                    openSFO = open(path + "/" + levelFolder + "/" + levelfile, 'r', encoding="utf-8", errors="ignore")
                    SFOContent = openSFO.read()
                    cleanSFPContent = LevelParser.clean(SFOContent)
                    
                    title = LevelParser.getLevelTitle(cleanSFPContent, levelFolder)
                    description = self.getDescription(cleanSFPContent, levelFolder)

                    if includeDescription == False:
                        if term in title.lower():
                            newMatchLevel = Level(title = title,
                                                description = description,
                                                path  = f'{path}/{levelFolder}',
                                                image = f'{path}/{levelFolder}/ICON0.PNG',
                                                folderName= levelFolder)
                            matchedLeveAppend(newMatchLevel)
                            
                    elif term in cleanSFPContent.lower():
                        newMatchLevel = Level(title = title,
                                              description = description,
                                              path  = f'{path}/{levelFolder}',
                                              image = f'{path}/{levelFolder}/ICON0.PNG',
                                              folderName= levelFolder)
                        matchedLeveAppend(newMatchLevel)                   
        
        callBack(LevelParser.checkIfThereIsNoMatch(matchedLevels))
    
    def cleanAllMachineCode(self, conten):
        for code in machineCode:
            conten = conten.replace(code, '')
            
        return conten
    
    def getDescription(self, content: str, levelFolder):
        startIndex = self.SFOStartIndex(content, "SD")
        endIndex   = content.index(levelFolder)
        

        descrition = self.cleanAllMachineCode(f'{content[startIndex : endIndex]}')
        try:
            if descrition[-1] == "M":
                descrition = descrition[:-1]
        except:
            # level has no Description.
            pass
        
        return descrition


        
        
    