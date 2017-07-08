from pydub import silence
from pydub import AudioSegment as AS
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils
import numpy as np

def dentro(intervalo,i):
	return ((intervalo[0] < i) and (intervalo[1] > i))

#variaveis de estudo

db = -44
tempo = 100 #em ms

#carregando audio

sound = AS.from_file('/home/joseildo/SpeechDetection/musan/speech/librivox/speech-librivox-0172.wav')

#criando espaços para estudo

#silen = silence.detect_silence(sound, silence_thresh = db)
nsilen = silence.detect_nonsilent(sound, silence_thresh = db)

j = 0
n = False
datalabels = []
#criando datalabels
for i in range(0,len(sound)-tempo, tempo):	
	if dentro(nsilen[j],i):
		datalabels.append('1')#voice
		n = True
	else:
		datalabels.append('0')#silence
		if(n) and (j+1 < len(nsilen)):
			n = False
			j += 1

modelo = Sequential()
modelo.add(Dense(100, input_shape=(None,1600)))
modelo.add(Dense(100,activation="relu"))
modelo.add(Dense(2,activation = 'softmax'))
modelo.compile(loss='categorical_crossentropy',optimizer = 'sgd',metrics=['acc'])

labels = np_utils.to_categorical(datalabels, nb_classes=2)

data = []
for i in range(0, len(sound) - tempo, tempo):
	data.append(sound[i:i+tempo].get_array_of_samples())


modelo.fit(np.asarray([data]),np.asarray([labels]),nb_epoch=100)