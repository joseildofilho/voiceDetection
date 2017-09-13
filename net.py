from keras.models import Sequential
from keras.layers import Dense,Dropout


model = Sequential()
model.add(Dense(1600, input_shape=(None,1600)))
model.add(Dense(800,activation="sigmoid"))
#model.add(Dropout(0.5))
#model.add(Dense(1600,activation="relu"))
model.add(Dense(3,activation = 'softmax'))
model.compile(loss='categorical_crossentropy',optimizer = 'sgd',metrics=['acc'])
