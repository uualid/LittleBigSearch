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

class LevelParser:

    #___ inits ______________________________________________

    def __init__(self, includeDescription = True) -> None:
        self.includeDescription = includeDescription
    #________________________________________________________

    @staticmethod 
    def checkIfThereIsNoMatch(list):
        if list == []:
            return ParserReturns.noResult
        else:
            return list

    @staticmethod
    def SFOStartIndex(levelInfo, folderName):    
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
    def clean(SFOstring):
            #For some reason after getting the level string from the SFO, I get alot of machine code with it.
        return SFOstring.replace('\x00', '')
    
    @staticmethod
    def getLevelTitle(SFOContent, levelFolder):
        startIndex = LevelParser.SFOStartIndex(SFOContent, levelFolder) 
        endIndex   = LevelParser.SFOEndIndex(SFOContent)
        title      = LevelParser.clean( f'{SFOContent[startIndex : endIndex]}')
        
        return title

    #__ Main search method __________________________________________________________________________________
    def guard(self, path, callBack):
        if exists(path) == False:
            callBack(ParserReturns.wrongPath)
            return True

        if path.__contains__("/") == False:
            callBack(ParserReturns.noPath)
            return True

        return False
    
    def search(self, callBack, term, path, includeDescription):
            # Empty the array for the next search.
        matchedLevels = []
        
        if self.guard(path, callBack):
            return

        for levelFolder in os.listdir(path):
            if levelFolder.__contains__("."):
                    #Skips files, only folders.
                continue
        
            for levelfile in os.listdir(path + "/" + levelFolder):
                if levelfile.endswith(".SFO"):
                    
                    openSFO = open(path + "/" + levelFolder + "/" + levelfile, 'r', encoding="utf-8", errors="ignore")
                    SFOContent = openSFO.read()
                    
                    if includeDescription == False:

                        title = LevelParser.getLevelTitle(SFOContent, levelFolder)

                        if title.lower().__contains__(term.lower()):
                            newMatchLevel = Level(title = title,
                                              path  = f'{path}/{levelFolder}',
                                              image = f'{path}/{levelFolder}/ICON0.PNG')
                            matchedLevels.append(newMatchLevel)

                    elif SFOContent.lower().__contains__(term.lower()):
                        
                        title = LevelParser.getLevelTitle(SFOContent, levelFolder)

                        newMatchLevel = Level(title = title,
                                              path  = f'{path}/{levelFolder}',
                                              image = f'{path}/{levelFolder}/ICON0.PNG')
                        matchedLevels.append(newMatchLevel)    
        
        callBack(LevelParser.checkIfThereIsNoMatch(matchedLevels))
    
    #__________________________________________________________________________________________________________

    # Fetches anything that resemble a level module.

    ###############################################
    ### Only used to fetch RPCS3 stored levels  ###
    ###############################################

    def fetchLevelsFrom(self, path, callBack):
        levels = []
        
        if exists(path) == False:
            callable(ParserReturns.wrongPath)
            return

        if path.__contains__("/") == False:
            callBack(ParserReturns.noPath)
            return
        
        for levelFolder in os.listdir(path):
            if levelFolder.__contains__("."):
                    #Skips files, only folders.
                continue
            
            for levelfile in os.listdir(path + "/" + levelFolder):
                    if levelfile.endswith(".SFO"):

                        openSFO = open(path + "/" + levelFolder + "/" + levelfile, 'r', encoding="utf-8", errors="ignore")
                        SFOContent = openSFO.read()

                        title = LevelParser.getLevelTitle(SFOContent, levelFolder)

                        newLevel = Level(title = title,
                                        path  = f'{path}/{levelFolder}',
                                        image = f'{path}/{levelFolder}/ICON0.PNG')
                        levels.append(newLevel)
        callBack(LevelParser.checkIfThereIsNoMatch(levels))

    