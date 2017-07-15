from keras.models import Sequential
from keras.layers import Dense


model = Sequential()
model.add(Dense(100, input_shape=(None,1600)))
model.add(Dense(100,activation="relu"))
model.add(Dense(2,activation = 'softmax'))
model.compile(loss='categorical_crossentropy',optimizer = 'sgd',metrics=['acc'])