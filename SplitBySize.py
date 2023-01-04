from os import listdir, makedirs
from os.path import isfile, join, exists
import argparse
import shutil
import PIL.Image

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
                img = PIL.Image.open(f)
                size = img.height*img.width
                tmpList.append([size,f])
        tmpList.sort()
        myList+=tmpList
    return myList, classes

def splitData(myList,trainPer,validPer):
    base = 20
    trainPath,validPath,testPath = [], [], []
    train = trainPer*base/100
    valid = validPer*base/100
    for i,[_,f] in enumerate(myList):
        if i % base < train: trainPath.append(f)
        elif i % base < valid+train: validPath.append(f)
        else: testPath.append(f)
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
    parser.add_argument('--Path', type=str, default= "../_dataset/Win_2nd", help='initial weights path')
    parser.add_argument('--Train', type=int, default=80, help='Train Percentage')
    parser.add_argument('--Valid', type=int, default=10, help='Valid Percentage')
    split_arg = parser.parse_args()
    res, classes = SortBySize(split_arg.Path)
    trainPath, validPath, testPath = splitData(res,split_arg.Train,split_arg.Valid)
    createDataset(split_arg.Path, classes,trainPath, validPath, testPath)
    