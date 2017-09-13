import net as rede
import data

#print(data.countTimeFold("/home/joseildo/SpeechDetection/musan/speech/librivox/"),"segundos")


data.loadFromFold('/home/joseildo/SpeechDetection/musan/speech/librivox/')
data.notSilence = "2"
data.loadFromFold("/home/joseildo/SpeechDetection/musan/noise/sound-bible")

data.prepareData(x,y,shuffle=True)

rede.model.save_weights('/home/joseildo/SpeechDetection/pyHumanDetect/pesosPorraa.h5')
