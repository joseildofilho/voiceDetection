import os
from pydub import AudioSegment
import random


"""
    TO-DO:
        * search for descent loading bar
        * sklearn cross validation
"""


class Folder:

    """

    Usable variables are:

    * i, that count on the iterator how many itens pass throw the iterator.(Obviously i it's not a good name for a variable of a class)
    * size, the size of a folder the it's has been used
    * sizeSlice, the the quantity of itens that it's going to be used when sliced
    
    """

    def __init__(self, src="", shuffle=False, putBack=False, folderSlice = 1.0):
        
        self.__src = src if src.endswith("/") else (src + "/")

        os.chdir(src)

        self.__outputSrc = self.__src + "output"

        if not os.path.exists(self.__outputSrc):
            os.makedirs(self.__outputSrc)       
               
        self.__folderSrcList = os.listdir()
        if shuffle:
            random.shuffle(self.__folderSrcList) 

        self.__shuffle = shuffle
        self.__putBack = putBack

        self.__slice = folderSlice

        if ((0.0 > folderSlice) and (folderSlice > 1.0)):
            raise ValueError("slice is supose to be inside of a range (0,1)")
        
        # Iterator stuff
        self.i = 0
        self.size = len(self.__folderSrcList)
        
        #Slice stuff
        self.sizeSlice = int(self.size * self.__slice)
        self.__auxSliceLowerList = list(self.__folderSrcList[0:self.sizeSlice])
        self.__auxSliceUpperList = list(self.__folderSrcList[self.sizeSlice+1:self.size])
    
    @property
    def output(self):
        return self.__outputSrc
    @output.setter
    def output(self,path):
        self.__outputSrc = path if not path.endswith("/") else (path + "/")
        if not os.path.exists(self.__outputSrc):
            os.makedirs(self.__outputSrc)
        return self

    """
        Loads one audio
    """
    def loadAudio(self, audio=""):
        try:
            return AudioSegment.from_file(audio)
        except ValueError:
            print("Not found or invalid Audio")


    """
        It will load the whole folder to your memory, sooo be careful
    """
    def loadAllToMemory(self):
        audiosList = []
        if self.__putBack:
            for i in self.__folderSrcList:
                audiosList.append(loadAudio(choice(self.__folderSrcList)))
        else:
            for i in self.__folderSrcList:
                audiosList.append(loadAudio(i))
        return audiosList
	
    
    """
    	Loads part of the src files with indexes lower than sizeSlice.
    """
    def loadLowerSlicedToMemory(self):
        audiosList = []
        if self.__putBack:
            for i in self.__auxSliceLowerList:
              	audiosList.append(loadAudio(choice(self.__auxSliceLoweList)))
        else:
            for i in self.__auxSliceLowerList:
              	audiosList.append(loadAudio(i))
        return audiosList
     
    """
    	Loads the part of src to memory, but it's the rest of src.
    """
    def loadUpperSlicedToMemory(self):
        audiosList = []
        if self.__putBack:
            for i in self.__auxSliceUpperList:
                audiosList.append(loadAudio(choice(self.__auxSliceUpperList)))
        else:
            for i in self.__auxSliceUpperList:
                audiosList.append(loadAudio(i))
        return audiosList

      
    """
    	Shuffle the data.
    """
    def shuffle(self):
       	self.__folderSrcList = random.shuffle(self.__folderSrcList)


    """
    	Sort the data like a Folder
    """
    def sort(self):
       	self.__folderSrcList = os.listdir()


    """
        By instance, the iterator it's completely sequential
        TO-DO:
        	* implement slice here
    """
    def __iter__(self):

        return self

    def __next__(self):
        if self.i < self.size:
            self.i += 1
            name = self.__folderSrcList[self.i - 1]
            print(name)
            if self.__putBack:
                name = choice(self.__folderSrcList)
            return self.loadAudio(name)
        else:
            raise StopIteration()

    """
        Get list of files of a class.
        PS: with callback work's better
    """
    def getFilesOfClass(self, classification):
        classList = []
        for f in self.__folderSrcList:
            if f.startswith(classification):
                classList.append(f)
        return classList

    def writeChunks(self,data,src = "",name = "output.wav"):
        print(data.duration_seconds)
        data.export((self.__outputSrc + name) if src == "" else (src + name), format="wav", bitrate="16k")
