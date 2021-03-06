# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 17:33:34 2020

@author: Maria
"""
from algorithms import importDataset, splitAndScale, ANNregression, randomForest, svr
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
import tensorflow as tf
import joblib


###############################################
#              Choosing Dataset               #
###############################################
def selectDataset():
    print("Select a file to use:")
    print("1 - Regression Original 1437 rows")
    print("2 - Regression Balanced (83% deleted)")
    print("3 - Regression Encoded variables all 1437 rows")
    print("4 - Regression Encoded variables balanced (83% deleted)")
    print("5 - Regression no 365 days")
    print("6 - Regression only 365 days")
    print("7 - Regression only synthetic 3211 rows")
    print("8 - Regression synthetic plus 365 days")
    print("9 - Another dataset")

    number = 0
    acceptedDataset = False
    while acceptedDataset is False:
        number = int(input("Select number to import dataset: "))
        if number > 0 and number < 10:
            acceptedDataset = True
        else:
            print("Invalid number, select a dataset by selecting its number (1 to 9)")

    choice = ""
    if number == 1: choice = "regression/regAll.csv"
    if number == 2: choice = "regression/regBalanced.csv"
    if number == 3: choice = "regression/regEncoded.csv"
    if number == 4: choice = "regression/regEncodedBalanced.csv"
    if number == 5: choice = "regression/regNo365.csv"
    if number == 6: choice = "regression/regOnly365.csv"
    if number == 7: choice = "regression/regSynthetic.csv"
    if number == 8: choice = "regression/regSyntheticWith365.csv"
    if number == 9: choice = input("input full path of dataset: ")

    print("dataset chosen:", choice)
    # Import the Dataset and separate X and y
    X_before, y_before = importDataset(choice)
    # Split the dataset
    X_train, X_test, y_train, y_test = splitAndScale(X_before, y_before)

    return X_before, y_before, X_train, X_test, y_train, y_test, choice


def newRFdataset(importances, dataset):
    new_variables = [] # new list of column names to create dataset
    for i,j in importances:
        if j > 0:
            new_variables.append(i)
    dataset = pd.read_csv('datasets/'+dataset)
    dataset = pd.concat([dataset[new_variables], dataset['Dias']], axis=1)
    print("\nNew dataset:\n",dataset)
    
    import os
    file_dir = os.path.dirname(os.path.abspath(__file__))
    csv_folder = 'datasets'
    file_path = os.path.join(file_dir, csv_folder, 'newRFdata.csv')
    dataset[new_variables].to_csv(file_path, header=True, index=None)
    
    print("\n\tNEW CSV SAVED as datasets/newRFdata.csv")
    
    

###############################################
#            Choosing Algorithm               #
###############################################
def chooseAlgorithm(X_before, X_train, X_test, y_train, y_test, dataset):
    print()
    print("\033[4mChoose an algorithm to run on the dataset:\033[0m")
    print("1 - Artificial Neural Network")
    print("2 - Random Forest")
    print("3 - Support Vector Regression")

    number = 0
    acceptedAlgorithm = False
    while acceptedAlgorithm is False:
        number = int(input("Select number of algorithm to run: "))
        if number > 0 and number < 4:
            acceptedAlgorithm = True
        else:
            print("Invalid number, select an algorithm by selecting its number (1 to 3)")
    if number == 1:
        mae = ANNregression(X_train, y_train, X_test, y_test)
        model = tf.keras.models.load_model('models/ann.h5')
        return model, int(mae)
    if number == 2:
        mae, importances = randomForest(X_train, y_train, X_test, y_test, X_before)
        model = joblib.load('models/rf.sav')
        newData = input("Would you like to export a new dataset with only the variables that have a higher importance than 0? [y/n] > ")
        if newData == "y":
            newRFdataset(importances, dataset)
        return model, int(mae)
    if number == 3:
        mae = svr(X_train, y_train, X_test, y_test)
        model = joblib.load('models/svr.sav')
        return model, int(mae)

def ask():
    print("\nWhat do you want to do now?")
    print("1 - Choose another dataset to train or a different model")
    print("2 - Predict from manual input of donor and recipient variables")
    print("3 - Predict from file")
    print("4 - exit")
    keepWorkin = input("> ")
    return keepWorkin

def inputManual():
    to_predict = []
    try:
        print()
        print("\033[4mInsert recipient's values: \033[0m")
        while True:
            age = float(input("- Age: "))
            if age > 9 and age < 81: break
            else: print("Invalid value, must be between 10 and 80")

        while True:
            gender = float(input("- Gender (1 - Male, 0 - Female): "))
            if gender == 1 or gender == 0: break
            else: print("Invalid value, must be 1 for male or 0 for female")

        while True:
            bmibasal = float(input("- Body-Mass Index (in kg/m2): "))
            if bmibasal > 12 and bmibasal < 76: break
            else: print("Invalid value, must be between 13 and 75")

        while True:
            diabetesPreTx = float(input("- diabetes (1 - yes, 0 - no): "))
            if diabetesPreTx == 1 or diabetesPreTx == 0: break
            else: print("Invalid value, must be 0 for no or 1 for yes")

        while True:
            htabasal = float(input("- Arterial hypertension (1 - yes, 0 - no): "))
            if htabasal == 1 or htabasal == 0: break
            else: print("Invalid value, must be 0 for no or 1 for yes")

        while True:
            dialisis = float(input("- Dialysis requirement pre-transplant (1 - yes, 0 - no): "))
            if dialisis == 1 or dialisis == 0: break
            else: print("Invalid value, must be 0 for no or 1 for yes")

        while True:
            etiologiaprincipal = float(input("- Etiology justifying transplant need:\n\t\t0 - Virus C cirrhosis\n\t\t1- Alcohol cirrhosis\n\t\t2 - Virus B cirrhosis\n\t\t3 - Fulminant hepatic failure\n\t\t4 - Primary biliary cirrhosis\n\t\t5 - Primary sclerosing cholangitis\n\t\t6 - Others\n> "))
            if etiologiaprincipal == 0 or (etiologiaprincipal > 0 and etiologiaprincipal < 7): break
            else: print("Invalid value, must be between 0 and 6")

        while True:
            trombosisportal = float(input("- Portal thrombosis:\n\t\t0 - No portal thrombosis\n\t\t1 - Partial\n\t\t2 - Complete\n> "))
            if trombosisportal == 0 or (trombosisportal > 0 and trombosisportal < 3): break
            else: print("Invalid value, must be between 0 and 2")

        while True:
            tiempolistaespera = float(input("- Waiting list time (in days): "))
            if tiempolistaespera > 0 and tiempolistaespera < 2000: break
            else: print("Invalid value, must be between 1 and 2000")

        while True:
            meldinclusion = float(input("- MELD score at waiting list inclusion: "))
            if meldinclusion > 0 and meldinclusion < 50: break
            else: print("Invalid value, must be between 1 and 50")

        while True:
            meldtx = float(input("- MELD at transplant time: "))
            if meldinclusion > 0 and meldinclusion < 50: break
            else: print("Invalid value, must be between 1 and 60")

        while True:
            tips = float(input("- TIPS at transplant (1 - yes, 0 - no): "))
            if tips == 1 or tips == 0: break
            else: print("Invalid value, must be 0 for no or 1 for yes")

        while True:
            sindromehepatorrenal = float(input("- Hepatorrenal syndrome (1 - yes, 0 - no): "))
            if sindromehepatorrenal == 1 or sindromehepatorrenal == 0: break
            else: print("Invalid value, must be 0 for no or 1 for yes")

        while True:
            apcirugiaabdosuperior = float(input("- History of previous upper abdominal surgery (1 - yes, 0 - no): "))
            if apcirugiaabdosuperior == 1 or apcirugiaabdosuperior == 0: break
            else: print("Invalid value, must be 0 for no or 1 for yes")

        while True:
            sfiptx = float(input("- Pre-transplant status performance:\n\t\t0 - At home\n\t\t1 - Hospitalised\n\t\t2 - Hospitalised in ICU\n\t\t3 - Hospitalised in ICU with mechanical ventilation\n> "))
            if sfiptx == 0 or (sfiptx > 0 and sfiptx < 3): break
            else: print("Invalid value, must be between 0 and 2")

        while True:
            cmvbasal = float(input("- Cytomegalovirus (1 - yes, 0 - no): "))
            if cmvbasal == 1 or cmvbasal == 0: break
            else: print("Invalid value, must be 0 for no or 1 for yes")

        print()
        print("\033[4mInsert donor's values:\033[0m")
        while True:
            edaddon = float(input("- Age: "))
            if edaddon > 10 and edaddon < 80: break
            else: print("Invalid value, must be between 10 and 80")

        while True:
            sexodon = float(input("- Gender (1 - Male, 0 - Female): "))
            if sexodon == 1 or sexodon == 0: break
            else: print("Invalid value, must be 1 for male or 0 for female")

        while True:
            bmiestdon = float(input("- Body-Mass Index (in kg/m2): "))
            if bmiestdon > 12 and bmiestdon < 76: break
            else: print("Invalid value, must be between 13 and 75")

        while True:
            diabetesmelitusdon = float(input("- Diabetes (1 - yes, 0 - no): "))
            if diabetesmelitusdon == 1 or diabetesmelitusdon == 0: break
            else: print("Invalid value, must be 0 for no or 1 for yes")

        while True:
            htadon = float(input("- Arterial hypertension (1 - yes, 0 - no): "))
            if htadon == 1 or htadon == 0: break
            else: print("Invalid value, must be 0 for no or 1 for yes")

        while True:
            causaexitus = float(input("- Cause of death:\n\t\t0 - Brain trauma\n\t\t1 - Cerebral vascular accident (CVA)\n\t\t2 - Anoxia\n\t\t3 - Deceased vascular after cardiac arrest\n\t\t4 - Others\n> "))
            if causaexitus == 0 or (causaexitus > 0 and causaexitus < 5): break
            else: print("Invalid value, must be between 0 and 4")

        while True:
            diasuci = float(input("- Hospitalised length in ICU (days): "))
            if diasuci > -1 and diasuci < 61: break
            else: print("Invalid value, must be between 1 and 60")

        while True:
            hipotension = float(input("- Hypotension episodes (1 - yes, 0 - no): "))
            if hipotension == 1 or hipotension == 0: break
            else: print("Invalid value, must be 0 for no or 1 for yes")

        while True:
            inotropos = float(input("- High inotropic drug use (1 - yes, 0 - no): "))
            if inotropos == 1 or inotropos == 0: break
            else: print("Invalid value, must be 0 for no or 1 for yes")

        while True:
            creatinina = float(input("- Creatinine plasma level (in mg/dl): "))
            if (creatinina == 0) or (creatinina > 0 and creatinina < 12): break
            else: print("Invalid value, must be between 0 and 11")

        while True:
            na = float(input("- Sodium plasma level (in mEq/l): "))
            if na > 89 and na < 201: break
            else: print("Invalid value, must be between 90 and 200")

        while True:
            ast = float(input("- Aspartate transaminase level: (in UI/l): "))
            if ast > 0 and ast < 1501: break
            else: print("Invalid value, must be between 0 and 1500")

        while True:
            alt = float(input("- Alanine aminotransferase plasma level (in UI/l): "))
            if alt > 0 and alt < 1501: break
            else: print("Invalid value, must be between 0 and 1500")

        while True:
            bit = float(input("- Total bilirubin (in mg/dl): "))
            if bit > -1 and bit < 7: break
            else: print("Invalid value, must be between 0 and 6")

        while True:
            antihbc = float(input("- Hepatitis B (1 - yes, 0 - no): "))
            if antihbc == 1 or antihbc == 0: break
            else: print("Invalid value, must be 0 for no or 1 for yes")

        while True:
            vhc = float(input("- Hepatitis C (1 - yes, 0 - no): "))
            if vhc == 1 or vhc == 0: break
            else: print("Invalid value, must be 0 for no or 1 for yes")

        while True:
            cmvdon = float(input("- Cytomegalovirus (1 - yes, 0 - no): "))
            if cmvdon == 1 or cmvdon == 0: break
            else: print("Invalid value, must be 0 for no or 1 for yes")

        print()
        print("\033[4mInsert transplant info:\033[0m")
        while True:
            multiorganico = float(input("- Multi-organ harvesting (1 - yes, 0 - no): "))
            if multiorganico == 1 or multiorganico == 0: break
            else: print("Invalid value, must be 0 for no or 1 for yes")

        while True:
            txcombinado = float(input("- Combined transplant (1 - yes, 0 - no): "))
            if txcombinado == 1 or txcombinado == 0: break
            else: print("Invalid value, must be 0 for no or 1 for yes")

        while True:
            injertocompletoparcial = float(input("- Complete or partial graft (1 - complete, 0 - partial): "))
            if injertocompletoparcial == 1 or injertocompletoparcial == 0: break
            else: print("Invalid value, must be 0 for partial or 1 for complete")

        while True:
            tiempoisquemiafria = float(input("- Cold ischemia time:\n\t\t0 - Less than 6 hours\n\t\t1 - Between 6 and 12 hours\n\t\t2 - More than 6 hours\n> "))
            if tiempoisquemiafria == 0 or (tiempoisquemiafria > 0 and tiempoisquemiafria < 3): break
            else: print("Invalid value, must be between 0 and 2")

        while True:
            compatibilidadabo = float(input("- AB0 compatible transplant (1 - yes, 0 - no): "))
            if compatibilidadabo == 1 or compatibilidadabo == 0: break
            else: print("Invalid value, must be 0 for no or 1 for yes")



        to_predict = [age, gender, bmibasal, diabetesPreTx, htabasal, dialisis,
                  etiologiaprincipal, trombosisportal, tiempolistaespera,
                  meldinclusion, meldtx, tips, sindromehepatorrenal,
                  apcirugiaabdosuperior, sfiptx, cmvbasal,
                  edaddon, sexodon, bmiestdon, diabetesmelitusdon, htadon,
                  causaexitus, diasuci, hipotension, inotropos, creatinina,
                  na, ast, alt, bit, antihbc, vhc, cmvdon,
                  multiorganico, txcombinado, injertocompletoparcial,
                  tiempoisquemiafria, compatibilidadabo
                 ]

        print("\n",to_predict)
    except Exception as e:
        print(e)
    return to_predict

def nextSteps(model, choice, mae, dataset):
    #choose another dataset to train a different model
    if int(choice) == 1:
        X_before, y_before, X_train, X_test, y_train, y_test, dataset = selectDataset()
        model, mae = chooseAlgorithm(X_before, X_train, X_test, y_train, y_test, dataset)

    # predict from manual input
    if int(choice) == 2:
        to_predict = inputManual()
        if len(to_predict) == 38:
            scaler = MinMaxScaler()
            new_prediction = model.predict(scaler.fit_transform(np.array([to_predict])))
            print("\nPredicted days: ", abs(int(new_prediction)), "+/-", mae, "days")
        else:
            print("Incorrect input, try again.")

    # predict from file
    if int(choice) == 3:
        print("Predicting from file...")
        while True:
            try:
                readDataset = input("Full name of dataset to import: ")
                dataset = pd.read_csv('datasets/' + readDataset)
                to_predict = dataset.iloc[:, :-1].values # get all columns except last one (actual value)

                scaler = MinMaxScaler()
                predictions = []
                for row in to_predict:
                    transform = scaler.fit_transform(row.reshape(-1, 1))
                    new_pred = model.predict(transform.reshape(1, -1))
                    predictions.append(new_pred[0])
                print("\nPredictions: +/-", mae, "days:\n", predictions)

                break
            except Exception as e:
                print(e)

    # exit
    if int(choice) == 4:
        return True
    return False

def main():
    # Print initial title of program
    from pyfiglet import Figlet
    f = Figlet(font='slant')
    print (f.renderText('LiverTransplant Survival Predictor'))

    # Select dataset and ML algorithm
    print("\033[4mStep 1:\033[0m Select dataset to be used to train the Machine Learning model\n\033[4mStep 2:\033[0m Select Machine Learning model to train\n")
    X_before, y_before, X_train, X_test, y_train, y_test, dataset = selectDataset()
    model, mae = chooseAlgorithm(X_before, X_train, X_test, y_train, y_test, dataset)

    finished = False
    while finished == False:
        x = ask()
        four = nextSteps(model, x, mae, dataset)
        if four == True:
            print("\n\tBYE BYE")
            break



if __name__ == "__main__":
    main()
