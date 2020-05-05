import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
from keras.preprocessing.text import Tokenizer, text_to_word_sequence
from sklearn.model_selection import train_test_split	
%matplotlib inline
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize
import os

path = 'D:/labeled.csv'
df = pd.read_csv(path)
df.head()

def delete_new_line_symbols(text):
    text = text.replace('\n', ' ')
    return text
df['comment'] = df['comment'].apply(delete_new_line_symbols)
df.head()

target = np.array(df['toxic'].astype('uint8'))
target[:5]

tokenizer = Tokenizer(num_words=5000, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', 
                      lower=True, 
                      split=' ', 
                      char_level=False)

tokenizer.fit_on_texts(df['comment'])
matrix = tokenizer.texts_to_matrix(df['comment'], mode='count')
matrix.shape
def get_model():
    
    model = Sequential()
    
    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(16, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    
    model.compile(optimizer=RMSprop(lr=0.0001), 
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    
    return model

X = normalize(matrix)
y = target

X_train, X_test, y_train, y_test = train_test_split(X, 
                                                    y,
                                                    test_size=0.2)

X_train.shape, y_train.shape

model = get_model()

history = model.fit(X_train, 
                    y_train, 
                    epochs=150, 
                    batch_size=400,
                    validation_data=(X_test, y_test))