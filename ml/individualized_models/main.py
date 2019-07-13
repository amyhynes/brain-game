csvs = [
            ["X_data001.csv", #008
            "y_data001.csv",
            ],
            ["X_data005.csv", #001
            "y_data005.csv",
            ],
            ["X_data008",  #009
            "y_data008.csv",
            ],
            ["X_data009.csv",  #011
            "y_data009.csv",
            ],
            ["X_data0011.csv",
            "y_data0011.csv",
            ],
        ]

import numpy as np    
import pandas as pd
from sklearn import metrics as sm
from keras.utils import to_categorical
from keras.models import load_model, Sequential
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from cm_clr import plot_classification_report, plot_confusion_matrix
from keras.callbacks import ModelCheckpoint, CSVLogger, ReduceLROnPlateau
from keras.layers import Dense, Conv1D, MaxPooling1D, Flatten, Dropout, BatchNormalization

for i in csvs:
    
    X = np.array(pd.read_csv(i[0]))
    y = np.array(pd.read_csv(i[1]))
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

    classifier = Sequential()
    
    classifier.add(Conv1D(128, X_train.shape[1], activation='relu', input_shape=(X_train.shape[1], 1)))
    classifier.add(MaxPooling1D(pool_size = (1), strides=(10)))
    classifier.add(Conv1D(64, 1, strides=1, padding='valid', activation="relu", kernel_initializer='glorot_uniform'))
    classifier.add(MaxPooling1D(pool_size = (1), strides=(10)))
    classifier.add(Conv1D(32, 1, strides=1, padding='valid', activation="relu", kernel_initializer='glorot_uniform'))
    classifier.add(MaxPooling1D(pool_size = (1), strides=(10)))
    
    classifier.add(Dropout(0.166))
    classifier.add(Flatten())
    classifier.add(Dropout(0.166))
    
    classifier.add(Dense(activation="relu", units=256, kernel_initializer="uniform"))
    classifier.add(BatchNormalization())
    classifier.add(Dense(activation="relu", units=128, kernel_initializer="uniform"))
    classifier.add(BatchNormalization())
    classifier.add(Dense(activation="relu", units=64, kernel_initializer="uniform"))
    classifier.add(BatchNormalization())
    classifier.add(Dense(activation="relu", units=32, kernel_initializer="uniform"))
    classifier.add(BatchNormalization())
    classifier.add(Dense(activation="relu", units=16, kernel_initializer="uniform"))
    classifier.add(BatchNormalization())
    classifier.add(Dense(activation="relu", units=3, kernel_initializer="uniform"))
    
    classifier.compile(optimizer = "adam", loss = 'categorical_crossentropy', metrics = ['accuracy'])
    
    checkpoint = ModelCheckpoint(i[0].replace(".csv",'')+"_model.hdf5", monitor='val_acc', verbose=1, save_weights_only=False, save_best_only=True)
    csv_logger = CSVLogger(i[0].replace(".csv",'')+"_history.csv", separator=',', append=False)
    reduce_lr = ReduceLROnPlateau(monitor='val_acc', factor=0.5, patience=4, verbose=1, mode='max', min_lr=0.0001)
    
    history = classifier.fit(X_train, y_train, validation_data=(X_test, y_test), batch_size = 10, 
                             callbacks=[checkpoint, csv_logger, reduce_lr], epochs = 25)
    
    model = load_model(i[0].replace(".csv",'')+"_model.hdf5")
    
    y_pred = model.predict(X_test)
    
    print(sm.accuracy_score(y_test, y_pred))
    print(sm.roc_auc_score(y_test, y_pred))