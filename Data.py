from pydub import silence
from pydub import AudioSegment

"""
    TO-DO List:
        * implement a method that work's on a specific audio
"""

class Data:
    """
        folder, it's the object Folder that you want to use
    """
    def __init__(self,folder):
        self.__folder = folder
        self.__iterFolder = iter(self.__folder)

        self.__audio = None

        self.__silenceChunks = []
        self.__soundChunks = []

        self.__silenceBufferChunks = AudioSegment.empty()
        self.__soundBufferChunks = AudioSegment.empty()
    @property
    def folder(self):
        return self.__folder
    @folder.setter
    def folder(self,folder):
        self.__folder = folder
    @property
    def silence(self):
        return self.__silenceBufferChunks
    @property
    def sound(self):
        return self.__soundBufferChunks
    def __iter__(self):
        return self
    def __next__(self):
        self.__audio = next(self.__iterFolder)
        return self
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        #should clear all
        print("do nothing")
    def splitSound(self):
        self.__soundChunks = []
        gaps = silence.detect_nonsilent(self.__audio)
        for start, final in gaps:
            self.__soundChunks.append(self.__audio[start:final])
        return self
    def splitSilence(self):
        self.__silenceChunks = []
        gaps = silence.detect_silence(self.__audio)
        for start, final in gaps:
            self.__silenceChunks.append(self.__audio[start:final])
        return self
    def storeSounds(self, src = "", name = ""):
        if name == "":
            self.__folder.writeChunks(self.__soundBufferChunks,src)
        else:
            self.__folder.writeChunks(self.__soundBufferChunks,src,name)
        self.__soundBufferChunks = AudioSegment.empty()
        return self

    def storeSilences(self,src = "",name = ""):
        if name == "":
            self.__folder.writeChunks(self.__silenceBufferChunks,src = src)
        else:
            self.__folder.writeChunks(self.__silenceBufferChunks,src = src,name = name)
        self.__silenceBufferChunks = AudioSegment.empty()
        return self
    def appendSilences(self):
        for data in self.__silenceChunks:
            self.__silenceBufferChunks += data
        return self
    def appendSounds(self):
        for data in self.__soundChunks:
            self.__soundBufferChunks += data
        return self
