import os
from pydub import AudioSegment
import random


"""
    TO-DO:
        * search for descent loading bar
        * sklearn cross validation
"""


class Folder:
    def __init__(self, src="", shuffle=False, putBack=False, folderSlice = 1.0):
        
        self.__src = src if not src.endswith("/") src += "/"
        
        os.chdir(src)
        
        self.__folderSrcList = random.shuffle(Folder.os.listdir()) if shuffle else self.__folderSrcList = os.listdir()

        self.__shuffle = shuffle
        self.__putBack = putBack
		
        self.__slice = folderSlice if not ((0.0 <= folderSlice) and (folderSlice <= 1.0)) else raise ValueError("slice is supose to be inside of a range (0,1)")

        # Iterator stuff
        self.i = 0
        self.size = len(self.__folderSrcList)
        
        #Slice stuff
        self.sizeSlice = int(self.__size * self.__slice)
        self.__auxSliceLowerList = list(self.__folderSrcList[0:self.sizeSlice])
        self.__auxSliceUpperList = list(self.__floderSrcList[self.sizeSlice+1:self.__size])
        

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

    def next(self):
        if self.i < self.size:
        	i += 1
            name = self.__folderSrcList[i - 1]
            if self.__putBack:
            	name = choice(self.__folderSrcList)
           	return loadAudio(name)
      	else:
        	raise StopIteration()


    """
        Get list of files of a class.
    """
    def getFilesOfClass(self, classification):
        classList = []
        for f in self.__folderSrcList:
            if f.startswith(classification):
                classList.append(f)
        return classList
