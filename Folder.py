from __future__ import print_function
import os
from pydub import AudioSegment
import random
import re
"""
    TO-DO:
        * search for descent loading bar
        * sklearn cross validation
        * make a full suport for regex
"""


class Folder:

    """

    Usable variables are:

    * i, that count on the iterator how many itens pass throw the iterator.(Obviously i it's not a good name for a variable of a class)
    * size, the size of a folder the it's has been used
    * sizeSlice, the the quantity of itens that it's going to be used when sliced
    
    """

    def __init__(self, src="",output = "", shuffle=False, putBack=False, folderSlice = 1.0, regex = "",verbose = 1):
        
        self.__src = src if src.endswith("/") else (src + "/")

        os.chdir(src)

        self.__outputSrc = self.__src + "output/" if output == "" else output

        if not os.path.exists(self.__outputSrc):
            os.makedirs(self.__outputSrc)       
               
        self.__folderSrcList = os.listdir()
        for i in self.__folderSrcList:
            if not ".wav" in i:
                self.__folderSrcList.remove(i)
        if shuffle:
            random.shuffle(self.__folderSrcList) 

        self.__shuffle = shuffle
        self.__putBack = putBack


        if ((0.0 > folderSlice) and (folderSlice > 1.0)):
            raise ValueError("slice is supose to be inside of a range (0,1)")
        
        # Iterator stuff
        self.i = 0
        self.size = len(self.__folderSrcList)
        
        #Slice stuff
        self.__slice = folderSlice
        self.sizeSlice = int(self.size * self.__slice)
        self.__auxSliceLowerList = list(self.__folderSrcList[0:self.sizeSlice])
        self.__auxSliceUpperList = list(self.__folderSrcList[self.sizeSlice+1:self.size])
        
        #Regex Stuff
        self.__regexFunction = re.compile(regex)
        self.__regexExpression = regex

        self.__verbose = 1
    @property
    def output(self):
        return self.__outputSrc
    @output.setter
    def output(self,path):
        self.__outputSrc = path if not path.endswith("/") else (path + "/")
        if not os.path.exists(self.__outputSrc):
            os.makedirs(self.__outputSrc)
        return self
    @property
    def regex(self):
        return self.__regexExpression
    @regex.setter
    def regex(self,reg):
        self.__regexFunction = re.compile(reg)
        self.__regexExpression = reg
        self.__folderSrcList = []
        for i in os.listdir():
           if bool(self.__regexFunction.match(i)) and not ("output" in i):
                self.__folderSrcList.append(i)
        self.size = len(self.__folderSrcList)
        return self
    @property
    def srcList(self):
        return self.__folderSrcList
    """
        Loads one audio
    """
    def loadAudio(self, audio=""):
        try:
            return AudioSegment.from_file(audio)
        except ValueError:
            print("Not found or invalid Audio") # must to raise a error


    """
        It will load the whole folder to your memory, sooo be careful
    """
    def loadAllToMemory(self):
        audiosList = []
        if self.__putBack:
            for i in self.__folderSrcList:
                audiosList.append(self.loadAudio(choice(self.__folderSrcList)))
        else:
            for i in self.__folderSrcList:
                audiosList.append(self.loadAudio(i))
        return audiosList
	
    def loadByRegexToMemory(self,regex = ""):
        if not regex == self.__regexExpression:
            self.__regexExpression = regex
            self.__regexFunction = re.compile(regex)
        for i in self.__folderSrcList:
            if self.__regexFunction.match(i):
                audiosList.append(self.loadAudio(i))
        return audiosList
    """
    	Loads part of the src files with indexes lower than sizeSlice.
    """
    def loadLowerSlicedToMemory(self):
        audiosList = []
        if self.__putBack:
            for i in self.__auxSliceLowerList:
              	audiosList.append(self.loadAudio(choice(self.__auxSliceLoweList)))
        else:
            for i in self.__auxSliceLowerList:
              	audiosList.append(self.loadAudio(i))
        return audiosList
     
    """
    	Loads the part of src to memory, but it's the rest of src.
    """
    def loadUpperSlicedToMemory(self):
        audiosList = []
        if self.__putBack:
            for i in self.__auxSliceUpperList:
                audiosList.append(self.loadAudio(choice(self.__auxSliceUpperList)))
        else:
            for i in self.__auxSliceUpperList:
                audiosList.append(self.loadAudio(i))
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
        This method tastes like in a wrong place :/
        But for now it's what I need
    """
    def sliceF(self,percentage):
        self.__slice = percentage
        self.sizeSlice = int(self.size * self.__slice)
        self.__auxSliceLowerList = list(self.__folderSrcList[0:self.sizeSlice])
        self.__auxSliceUpperList = list(self.__folderSrcList[self.sizeSlice+1:self.size])
        return self

    """
        By instance, the iterator it's completely sequential
        TO-DO:
        	* implement slice here
    """
    def __iter__(self):
        self.i = 0
        self.__size = len(self.__folderSrcList)
        return self

    def __next__(self):
        if self.i < self.__size:
            name = self.__folderSrcList[self.i]
            if self.__putBack:
                name = choice(self.__folderSrcList)
            self.i += 1
            print("\r%s/%s    %s"%(self.i,self.__size,"loading"),end = "")
            return self.loadAudio(name), name
        else:
            print("")
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
        data.export(((self.__outputSrc + name) if src == "" else (src + name)), format="wav", bitrate="16k")
