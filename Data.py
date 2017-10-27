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

        self.__chunks = []

        self.__bufferChunks = AudioSegment.empty()
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
    def splitSilence(self):
        self.__chunks = []
        gaps = silence.detect_silence(self.__audio)
        for start, final in gaps:
            self.__chunks.append(self.__audio[start:final])
            #print(self.__audio[start:final].duration_seconds)
        return self.__chunks
    def storeSilences(self,src = "",name = ""):
        if name == "":
            self.__folder.writeChunks(self.__bufferChunks,src)
        else:
            self.__folder.writeChunks(self.__bufferChunks,src,name)
        self.__bufferChunks = AudioSegment.empty()
        return self
    def appendSilences(self):
        for data in self.__chunks:
            self.__bufferChunks += data
        print(self.__bufferChunks.duration_seconds)
        return self
