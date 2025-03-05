import os
import random
import shutil
from itertools import islice

outputFolderPath = "Dataset/SplitData"
inputFolderPath = "Dataset/all"
splitRatio = {"train":0.7,"val":0.2,"test":0.1}
classes = ["fake","real"]
YamlFilePath = '/Users/shashrestha/Documents/Shasank/Production Project/New Face Detection/DataSet/SplitData/'


try:
    shutil.rmtree(outputFolderPath)
except OSError as e:
    os.mkdir(outputFolderPath)

# Directories to create
os.makedirs(f"{outputFolderPath}/train/images",exist_ok=True)
os.makedirs(f"{outputFolderPath}/train/labels",exist_ok=True)
os.makedirs(f"{outputFolderPath}/val/images",exist_ok=True)
os.makedirs(f"{outputFolderPath}/val/labels",exist_ok=True)
os.makedirs(f"{outputFolderPath}/test/images",exist_ok=True)
os.makedirs(f"{outputFolderPath}/test/labels",exist_ok=True)

# Get Names of Images
listName = os.listdir(inputFolderPath)
uniqueNames = set()
for names in listName:
    uniqueNames.add(names.split(".")[0])

uniqueNames=list(uniqueNames)
print("" in uniqueNames)


print(len(uniqueNames))

# Shuffle
random.shuffle(uniqueNames)

# Find number of images for each folder
lenData = len(uniqueNames)
lenTrain = int(lenData * splitRatio["train"])
lenVal = int(lenData * splitRatio["val"])
lenTest = int(lenData * splitRatio["test"])

# Put remaining in Training
if lenData!=lenTrain+lenVal+lenTest:
    remaining = lenData - (lenTrain+lenVal+lenTest)
    lenTrain += remaining


# Split the list
lengthToSplit = [lenTrain,lenVal,lenTest]
Input = iter(uniqueNames)
Output = [list(islice(Input,elem)) for elem in lengthToSplit]

print(f"Total Images: {lenData}\nTrain Images: {len(Output[0])}, Vaidation Images: {len(Output[1])}, Test Images: {len(Output[2])}")

#Copy files
sequence = ["train","val","test"]
for i,out in enumerate(Output):
    for fileName in out:
        if fileName != '':
            jpg_path = f'{inputFolderPath}/{fileName}.jpg'
            txt_path = f'{inputFolderPath}/{fileName}.txt'

            if os.path.exists(jpg_path) and os.path.exists(txt_path):
                shutil.copy(f'{inputFolderPath}/{fileName}.jpg',f'{outputFolderPath}/{sequence[i]}/images/{fileName}.jpg')
                shutil.copy(f'{inputFolderPath}/{fileName}.txt',f'{outputFolderPath}/{sequence[i]}/labels/{fileName}.txt')

print("Split Process Completed")

# Creating data.yaml file

dataYaml = f'path: ../Data\n\
train: ../train/images\n\
val: ../val/images\n\
test: ../test/images\n\
\n\
nc: {len(classes)}\n\
names: {classes}'

f = open(f"{outputFolderPath}/data.yaml","a")
f.write(dataYaml)
f.close()

print("Data.yaml File Created...")