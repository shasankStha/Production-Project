from cvzone.FaceDetectionModule import FaceDetector
import cv2
import cvzone
from time import time

#################################
classId = 1 # 0 is for fake and 1 is for real
outputFolderPath = "DataSet/DataCollectReal"
confidence = 0.8
save = True
blurThreshold = 40 #More larger more focus

debug = False
offsetPercentageW = 10
offsetPercentageH = 20
camWidth, camHeight = 1280, 720
floatingPoint = 6
###############################

cap = cv2.VideoCapture(0)
cap.set(3,camWidth)
cap.set(4,camHeight)
detector = FaceDetector()

while True:
    success, img = cap.read()

    imageOut = img.copy()

    img, bboxs = detector.findFaces(img, draw = False)

    listBlur = [] #True False values indicating if the faces are blur or not
    listInfo = [] #The normalized value and the class name for the label txt file

    if bboxs:
        for bbox in bboxs:
            x,y,w,h = bbox["bbox"]
            score = float(bbox["score"][0])

            # Check score
            if score > confidence:
                # Adding Offset to the face Detected
                offsetW = (offsetPercentageW/100)*w
                x = int(x - offsetW)
                w = int(w + offsetW * 2)

                offsetH = (offsetPercentageH/100)*h
                y = int(y - offsetH * 3)
                h = int(h + offsetH * 3.5)

                # To avoid values below 0
                if x < 0:x=0
                if y < 0:y=0
                if w < 0:w=0
                if h < 0:h=0

                # Find Blurriness
                imgFace = img[y:y + h, x:x + w]
                blurValue = int(cv2.Laplacian(imgFace,cv2.CV_64F).var())

                if blurValue > blurThreshold:
                    listBlur.append(True)
                else:
                    listBlur.append(False)

                # Normalization
                imgHeight, imgWidth, _ = img.shape
                xCenter, yCenter = x+w/2, y+h/2

                xCenterNormalize, yCenterNormalize = round(xCenter/imgWidth, floatingPoint), round(yCenter/imgHeight, floatingPoint) 
                widthNormalize, heightNormalize = round(w/imgWidth, floatingPoint), round(h/imgHeight, floatingPoint) 

                # To avoid values above 1
                if xCenterNormalize > 1:xCenterNormalize=1
                if yCenterNormalize > 1:yCenterNormalize=1
                if widthNormalize > 1:widthNormalize=1
                if heightNormalize > 1:heightNormalize=1

                listInfo.append(f'{classId} {xCenterNormalize} {yCenterNormalize} {widthNormalize} {heightNormalize}\n')

                # Drawing
                cv2.rectangle(imageOut, (x,y,w,h), (255,0,0), 3)
                cvzone.putTextRect(imageOut, f'Score: {int(score*100)}% Blur: {blurValue}',(x,y-0), scale=2, thickness= 3)

                if debug:
                    cv2.rectangle(img, (x,y,w,h), (255,0,0), 3)
                    cvzone.putTextRect(img, f'Score: {int(score*100)}% Blur: {blurValue}',(x,y-0), scale=2, thickness= 3)
        
        # To save
        if save:
            if all(listBlur) and listBlur != []:
                # SaveImage
                timeNow = time()
                timeNow = str(timeNow).split(".")
                timeNow = timeNow[0]+timeNow[1]
                cv2.imwrite(f"{outputFolderPath}/{timeNow}.jpg", img)

                # SaveLabel Text File
                for info in listInfo:
                    f = open(f"{outputFolderPath}/{timeNow}.txt","a")
                    f.write(info)
                    f.close()




    cv2.imshow("Image", imageOut)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()