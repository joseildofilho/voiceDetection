from pydub import AudioSegment as AS
from pydub import silence as dub
from keras.utils import np_utils
import numpy as np
import pandas as pd
import os
import p #loading bar
from random import shuffle as shuf
#corrigir o problema que esta sendo gerado por cirar um array com todo o o audio
#sendo que deve ser cirado um array de array com todo os audios e adaptar a rede para poder receber esse tipo de coisa
db = -44
tempo = 100 #ms
frameRate = 16000 # the default number of frame rate used to current neural net
notSilence = "1"
silence = "0"
#carregando audio

nb = 0
path = ""


sound = None
dataList = []
labelsList = []


"""
	* this function will change the frame rate to the default 
		frame rate, when the loaded value is not equals
"""
def loadAudio(audio):
	global sound
	sound = AS.from_file(audio)
	if not sound.frame_rate == frameRate:
		sound = sound.set_frame_rate(frameRate)
def iterateOnFold(fold,shuffle = False):
	global lista
	nb = 0
	lista = os.listdir(fold)
	global path
	path = fold
	if shuffle:
		shuf(lista)
def next():
	global nb
	global notSilence
	name = lista[nb]
	nb += 1
	dataList = []
	labelsList = []
	if "speech" in name:
		notSilence = "1"
	elif "music" in name:
		notSilence = "2"
	else:
		notSilence = "3"
	loadAudio(path+name)
	generateData()
	p.progress(nb,len(lista),"loading and running fold\n")
	return prepareData()
def hasNext():
	return nb < len(lista)
"""
	Forces de program to create a file csv with the data and resturn a iterable dataframe
	Not implemented:
	* must to fix ehere de dataframe would be or if it going to be returned
"""
def loadFromFold(fold,onDisk = False):
	global nb
	nb = 0
	global lista
	lista = []
	os.chdir(fold)
	listDir = os.listdir()
	for i in listDir:
		if i.endswith('.wav'):
			loadAudio(i)
			generateData()
			if onDisk:
				d = pd.DataFrame(dataList)
				d.insert(0, column = "labels", value = labelsList)
				d.to_csv("/home/joseildo/SpeechDetection/pyHumanDetect/data.csv",mode="a",chunksize=100000,index=None,header = False)
				clear()
			j += 1
	if onDisk:
		global dataFrame
		dataFrame = pd.read_csv("/home/joseildo/SpeechDetection/pyHumanDetect/data.csv",chunksize=100000)
def countTimeFold(fold):
	totalTime = 0
	loadFromFold(fold)
	for i in lista:
		loadAudio(i)
		totalTime += sound.duration_seconds
	return totalTime
## works but must to be generic
def generateData():
	generateLabels(silenceInterval())
	for i in range(0, len(sound) - tempo, tempo):
		dataList.append(sound[i:i+tempo].get_array_of_samples())
def prepareData():
	return np.asarray([dataList]),np.asarray([np_utils.to_categorical(labelsList,4)])
def silenceInterval():
	return dub.detect_nonsilent(sound, silence_thresh = db)
def generateLabels(silenceGaps):
	j = 0
	n = False
	for i in range(0,len(sound)-tempo, tempo):
                if inside(silenceGaps[j],i):
                        labelsList.append(notSilence)#voice
                        n = True
                else:
                        labelsList.append(silence)#not human
                        if(n) and (j+1 < len(silenceGaps)):
                                n = False
                                j += 1
def inside(interval,i):
	return ((interval[0] < i) and (interval[1] > i))
def clear():
	lista = []
	dataList = []
	labelsList = []

