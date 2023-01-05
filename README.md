# SplitBySize
When you get a huge dataset and ready to split it into train, valid and test data, we usually use train_test_split() function by scikit learn to split it randomly.
But in some cases, spliting data randomly isn't the best way to do, so i wrote this function which sorts the dataset by image size and split it, so you can garuntee all kind of image appears in train, valid and test.

## Instruction
For example, we got a dataset classified into NG and OK folder
```
NG
|--1.bmp, 2.bmp, 3.bmp...1000.bmp
OK
|--1.bmp, 2.bmp, 3.bmp...1000.bmp
```
We read all the images and multiply image width and height as there image size, then append it into list.
Then we sort the list by the image size.
```
myList = [ [23500,"NG/10.bmp"], [23500,"OK/24.bmp"]....[500000,"NG/197.bmp"] ]
```
After all, we start to split the list into batches according to the Batch param you've set, then shuffle the tmpList and asign the filename to train, valid or test according to the train and valid param.
```
tmpList=[ [23500,"NG/10.bmp"], [23500,"OK/24.bmp"]....[24000,"OK/59.bmp"] ]
len(tmpList) = Batch
```
It will create a _dataset folder which is under the target folder.

## Command Line
```
python SplitBySize.py --Path targetpath --Train 80 --Valid 10 --Batch 20
```
```
Target Folder
|
|---class1
|---class2
.
.
.
|--class N
```
