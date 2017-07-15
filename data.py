from pydub import AudioSegment as AS
from pydub import silence
from keras.utils import np_utils
import numpy as np
import os

db = -44
tempo = 100 #ms

#carregando audio

sound = None
lista = []
nb = 0

#criando espaços para estudo


def generateData():
	j = 0
	n = False
	datalabels = []
	nsilen = silence.detect_nonsilent(sound, silence_thresh = db)
	#criando datalabels
	for i in range(0,len(sound)-tempo, tempo):	
		if inside(nsilen[j],i):
			datalabels.append('1')#voice
			n = True
		else:
			datalabels.append('0')#silence
			if(n) and (j+1 < len(nsilen)):
				n = False
				j += 1
	labels = np_utils.to_categorical(datalabels, nb_classes=2)
	data = []
	for i in range(0, len(sound) - tempo, tempo):
		data.append(sound[i:i+tempo].get_array_of_samples())
	return np.asarray([data]),np.asarray([labels])


def loadAudio(audio):
	global sound
	sound = AS.from_file(audio)

def inside(interval,i):
	return ((interval[0] < i) and (interval[1] > i))

def loadFromFold(fold):
	global nb
	nb = 0
	global lista
	lista = []
	os.chdir(fold)
	for i in os.listdir():
		if i.endswith('.wav'):
			lista.append(i)
def next():
	loadAudio(lista[nb])
	global nb
	nb += 1
	print(lista[nb])
	return generateData()
def hasNext():
	return not(nb == len(lista))