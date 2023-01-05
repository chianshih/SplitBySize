from os import listdir, makedirs
from os.path import isfile, join, exists
import argparse
import shutil
import PIL.Image
import random

def SortBySize(myPath):
    if(exists(join(myPath,"_dataset"))==True): shutil.rmtree(join(myPath,"_dataset"))
    myList = []
    classes = listdir(myPath)
    for Class in classes:
        tmpList = []
        images = listdir(join(myPath, Class))
        for f in images:
            f = join(myPath, Class, f)
            if isfile(f):
                img = PIL.Image.open(f,mode="r")
                size = img.height*img.width
                tmpList.append([size,f])
        myList+=tmpList
    myList.sort()
    return myList, classes

def splitData(myList,trainPer,validPer,batch):
    trainPath,validPath,testPath = [], [], []
    start = 0
    train = trainPer*batch//100
    valid = validPer*batch//100
    for i in range(batch,len(myList),batch):
        tmpList = myList[start:i]
        random.shuffle(tmpList)
        for j,[_,f] in enumerate(tmpList):
            if j % batch < train: trainPath.append(f)
            elif j % batch < valid+train: validPath.append(f)
            else: testPath.append(f)
        start = i
    return trainPath, validPath, testPath

def createDataset(targetPath, classes, trainPath, validPath, testPath):
    datasetPath = join(targetPath,"_dataset")
    imageList = [trainPath, validPath, testPath]
    splitList =  ["train","valid","test"]
    for splitName in splitList:
        for ClassName in classes:
            makedirs(join(datasetPath, splitName, ClassName)) 
    
    for index in range(len(imageList)):
        for fn in imageList[index]:
            name = fn.split("\\")
            tmpDir = join(datasetPath, splitList[index])
            imgName = name[-1]
            CLS= name[-2]
            shutil.copy(fn, join(tmpDir, CLS, imgName))
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--Path', type=str, default= r"C:\Users\USER\Desktop\FATP\Ai_Training\_dataset\Win_2nd", help='initial weights path')
    parser.add_argument('--Train', type=int, default=75, help='Train Percentage')
    parser.add_argument('--Valid', type=int, default=20, help='Valid Percentage')
    parser.add_argument('--Batch', type=int, default=20, help='Batch size while spliting datas by image size')
    split_arg = parser.parse_args()
    res, classes = SortBySize(split_arg.Path)
    trainPath, validPath, testPath = splitData(res,split_arg.Train,split_arg.Valid, split_arg.Batch)
    createDataset(split_arg.Path, classes,trainPath, validPath, testPath)
    