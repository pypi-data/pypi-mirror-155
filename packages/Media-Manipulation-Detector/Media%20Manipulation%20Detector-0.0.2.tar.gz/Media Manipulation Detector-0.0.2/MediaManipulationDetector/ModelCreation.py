import os
import pickle
import time
import cv2
import pylab as py
import glob
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.metrics import classification_report, confusion_matrix
from scipy.interpolate import griddata
import tensorflow as tf
from keras import layers, models
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
from keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split


class ModelCreation:

    @staticmethod
    def create_model(algo="svm", k_fold=0, src_file="input.pkl", testfile="none"):
        if algo == "svm":
            ModelCreation.run_svm(k_fold, src_file, testfile)
        else:
            ModelCreation.run_cnn(k_fold, src_file, testfile)
        pass

    @staticmethod
    def run_svm(k_fold, train_file, test_file):
        # Train
        # Choose file to train the model
        pkl_file = open(train_file, 'rb')
        data = pickle.load(pkl_file)
        pkl_file.close()
        x_train = data["data"]
        y_train = data["label"]
        print(k_fold)

        print("Starting processing phase......")
        print("")
        start_time = time.time()

        if k_fold == -1:
            print("Using test file")
            # Test
            # Optional- Choose file to test the model
            # test_file="test_train.pkl"
            pkl_file = open(test_file, 'rb')
            data_test = pickle.load(pkl_file)
            pkl_file.close()

            x_test = data_test["data"]
            y_test = data_test["label"]

        if k_fold == 0:
            print("splitting training dataset to test")

            # To train and test with the same dataset
            x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.33)

        if k_fold == 5 or k_fold == 10:
            print("running k-fold")

            tprs = []
            base_fpr = np.linspace(0, 1, 101)

            # To use 10-fold cross validation
            # 10-fold
            number = 1
            kfold = KFold(n_splits=int(k_fold), shuffle=True, random_state=1)
            for train, test in kfold.split(data["data"]):
                # print('train: %s, test: %s' % (data["data"][train], data["data"][test]))
                x_train, x_test = data["data"][train], data["data"][test]
                y_train, y_test = data["label"][train], data["label"][test]

                # Create SVM model
                svclassifier_r = SVC(C=6.37, kernel='rbf', gamma=0.86, probability=True)
                clf = svclassifier_r.fit(x_train, y_train)

                # To visualization of ROC CURVE
                # plot_roc_curve(svclassifier_r, X_test, y_test, ax=ax_roc)

                # Get evaluation of SVM model
                SVM = svclassifier_r.score(x_test, y_test)
                y_score = clf.predict_proba(x_test)
                x_decision = svclassifier_r.decision_function(x_test)
                x_pred = svclassifier_r.predict(x_test)
                print(y_score)
                print(x_pred)
                print()
                print(classification_report(y_test, x_pred))
                print("")
                print("confusion matrix")
                print(confusion_matrix(y_test, x_pred))
                print("")
                print("True Positives: ", confusion_matrix(y_test, x_pred)[0][0])
                print("False Negatives: ", confusion_matrix(y_test, x_pred)[0][1])
                print("False Positives: ", confusion_matrix(y_test, x_pred)[1][0])
                print("True Negatives: ", confusion_matrix(y_test, x_pred)[1][1])

                # Create SVM model
        svclassifier_r = SVC(C=6.37, kernel='rbf', gamma=0.86, probability=True)
        clf = svclassifier_r.fit(x_train, y_train)

        # To visualization of ROC CURVE
        # plot_roc_curve(svclassifier_r, X_test, y_test, ax=ax_roc)

        # Get evaluation of SVM model
        SVM = svclassifier_r.score(x_test, y_test)
        y_score = clf.predict_proba(x_test)
        x_decision = svclassifier_r.decision_function(x_test)
        x_pred = svclassifier_r.predict(x_test)
        print(y_score)
        print(x_pred)
        print()
        print(classification_report(y_test, x_pred))
        print("")
        print("confusion matrix")
        print(confusion_matrix(y_test, x_pred))
        print("")
        print("True Positives: ", confusion_matrix(y_test, x_pred)[0][0])
        print("False Negatives: ", confusion_matrix(y_test, x_pred)[0][1])
        print("False Positives: ", confusion_matrix(y_test, x_pred)[1][0])
        print("True Negatives: ", confusion_matrix(y_test, x_pred)[1][1])

        # ProjectUtils.write_score_report(classification_report(y_test, x_pred), confusion_matrix(y_test, x_pred), dir)

        end_time = time.time()
        print(f"Runtime of the program is {end_time - start_time} seconds")

    @staticmethod
    def run_cnn(k_fold, src_file, testfile):
        # tf.compat.v1.enable_eager_execution()

        # teste
        # src_path_train = "dataset-train-small/train/"
        # src_path_test = "dataset-train-small/test/"

        # Para fotos
        src_path_train = "test_cnn_photos/train/"
        # src_path_test = "test_cnn_photos/test"

        train_datagen = ImageDataGenerator(
            rescale=1 / 255.0)
        # rotation_range=20,
        # zoom_range=0.05,
        # width_shift_range=0.05,
        # height_shift_range=0.05,
        # shear_range=0.05,
        # horizontal_flip=True,
        # fill_mode="nearest",
        # validation_split=0.20)

        # test_datagen = ImageDataGenerator(rescale=1 / 255.0)

        # batch_size=2

        train_generator = train_datagen.flow_from_directory(
            directory=src_path_train,
            target_size=(300, 300),
            color_mode="rgb",
            # batch_size=batch_size,
            class_mode="binary",
            subset='training',
            shuffle=False
            # seed=42
        )

        """ test_generator = test_datagen.flow_from_directory(
            directory=src_path_test,
            target_size=(300, 300),
            color_mode="rgb",
            batch_size=1,
            class_mode="binary",
            shuffle=False
            #seed=42
        )  """

        # X_train=np.concatenate([train_generator.next()[0] for i in range(train_generator.__len__())])
        # y_train=np.concatenate([train_generator.next()[1] for i in range(train_generator.__len__())])
        X = np.concatenate([train_generator.next()[0] for i in range(train_generator.__len__())])
        y = np.concatenate([train_generator.next()[1] for i in range(train_generator.__len__())])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10)

        """ labels=[]

        for label in train_generator.classes:
            temp=[]
            temp.append(label)
            labels.append(temp)
         """

        # y_train=np.array(labels)

        # classes = ["fake","real"]

        """ def plot_sample(X,y,index):
            plt.figure(figsize= (15,2))
            plt.imshow(X[index])
            plt.xlabel(classes[int(y[index])])
            plt.show() """

        # print(X_train[0]) #imagem 32x32,3 rgb channels
        # print(y_train[0])
        # plot_sample(X_train,y_train,0)

        # construir a cnn
        # A ReLu activation is applied after every convolution to transform the output values between the range 0 to 1.
        # #Max pooling is used to downsample the input representation
        cnn = models.Sequential([
            layers.Conv2D(filters=32, kernel_size=(3, 3), activation='relu', input_shape=(300, 300, 3)),
            layers.MaxPooling2D((2, 2)),

            layers.Conv2D(filters=64, kernel_size=(3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),

            layers.Flatten(),  # converts 3d feature map to 1d
            layers.Dense(64, activation='relu'),
            layers.Dense(10, activation='softmax')
        ])

        cnn.compile(optimizer='adam',
                    loss='sparse_categorical_crossentropy',
                    metrics=['accuracy'])

        cnn.fit(train_generator, epochs=10)

        # print(cnn.evaluate(X_test,y_test))
        # filenames= test_generator.filenames
        # nb_samples = len(filenames)

        # To use specific files to test
        """ y_test=test_generator.classes
        predict= cnn.predict(test_generator, steps=nb_samples)
        print(predict)
        y_pred = cnn.predict(X_test)
        y_pred=cnn.predict(test_generator)
        y_pred_classes = [np.argmax(element) for element in y_pred]
        print(y_pred)
        shape = len(y_pred)
        value = 0
        y_test = np.empty(shape, dtype=np.int)
        y_test.fill(value) 

        #print("Classification Report: \n", classification_report(y_test,predict))

        #print(cnn.evaluate(test_generator,steps=nb_samples))"""

        # To use the same dataset to train and test
        predict = cnn.predict(X_test)
        y_pred = np.argmax(predict, axis=1)
        print("")
        print('Confusion Matrix')
        print(confusion_matrix(y_test, y_pred))
        print("")
        print('Classification Report')
        target_names = ['Fake', 'Real']
        print(classification_report(y_test, y_pred, target_names=target_names, zero_division=1))

        pass
