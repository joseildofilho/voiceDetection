import net
import data


data.loadAudio('/home/joseildo/SpeechDetection/musan/speech/librivox/speech-librivox-0172.wav')
data.loadFromFold('/home/joseildo/SpeechDetection/musan/speech/librivox/')

while(data.hasNext()):
	x, y = data.next()
	rede.modelo.fit(x,y,nb_epoch=10)