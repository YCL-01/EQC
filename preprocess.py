import pandas as pd
import os
import pickle
import matplotlib.pyplot as plt

# data csv file name
accFile = 'acc.csv'
gyroFile = 'gyro.csv'
lightFile = 'light.csv'
surveyFile = 'surveyData.txt'

def surveyFilter(surveyData):
    keys, values = surveyData[:, 0], surveyData[:, 1]
    return {key:value for key, value in zip(keys, values)}

def createDataset(baseDir):
    dataset = []
    for date in os.listdir(baseDir):
        dateDir = os.path.join(baseDir, date)
        for user in sorted(os.listdir(dateDir)):
            userDir = os.path.join(dateDir, user)
            #print(userDir)
            accData, gyroData, lightData, surveyData = userDataRead(userDir)
            dataset.append([accData, gyroData, lightData, surveyData])
    return dataset
                
def userDataRead(filePath):
    accPath = os.path.join(filePath,accFile)
    accData = pd.read_csv(accPath, nrows=100)
    accData.drop(['time'], inplace = True, axis = 1)
    
    gyroPath = os.path.join(filePath,gyroFile)
    gyroData = pd.read_csv(gyroPath, nrows=100)
    gyroData.drop(['time'], inplace = True, axis = 1)
    
    lightPath = os.path.join(filePath,lightFile)
    lightData = pd.read_csv(lightPath, nrows=3000)
    lightData.drop(['time'], inplace = True, axis = 1)
    
    surveyPath = os.path.join(filePath,surveyFile)
    surveyData = pd.read_table(surveyPath, sep = ':', header = None)
    surveyData = surveyFilter(surveyData.values)
    #print(surveyData)
    
    return accData, gyroData, lightData, surveyData

def pickleFile(pickleFilePath):
    if not os.path.exists(pickleFilePath):
        dataset = createDataset('Dataset')
        with open(pickleFilePath, "wb") as f:
            pickle.dump(dataset, f)
    else:
        dataset = pickle.load(open(pickleFilePath, "rb"))
    return dataset

#dataset = pickleFile("parsed_dataset.pkl")
dataset = createDataset('./Dataset')


accSample, gyroSample, lightSample, surveySample = dataset[0]

print(accSample.describe())


