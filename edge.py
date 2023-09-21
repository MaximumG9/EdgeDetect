import cv2 as cv
import os
from PIL import Image

edges = None
mode = "DOG"

def updateImg():
    global edges
    
    e1 = cv.getTickCount()

    if mode == "CANNY":
        blurImg = cv.blur(currImg,((2*blur)+1,(2*blur)+1))
        edges = cv.Canny(blurImg,minVal,maxVal)

        edges = cv.applyColorMap(edges,cv.COLORMAP_WINTER)
    elif mode == "DOG":
        grayImg = currImg
        #grayImg = cv.cvtColor(grayImg, cv.COLOR_BGR2GRAY)
        blurImg = cv.blur(grayImg,((2*blur)+1,(2*blur)+1))
        blurImg2 = cv.blur(grayImg,((2*blur2)+1,(2*blur2)+1))
        if blur2 > blur:
            edges = blurImg2 - blurImg
        else:
            edges = blurImg - blurImg2
    elif mode == "REMGAUS":
        grayImg = currImg
        grayImg = cv.cvtColor(currImg, cv.COLOR_BGR2GRAY)
        blurImg = cv.blur(grayImg,((2*blur)+1,(2*blur)+1))
        edges = blurImg - grayImg
    
    if postBlur != 0:
        edges = cv.blur(edges,((2*postBlur)+1,(2*postBlur)+1))

    e2 = cv.getTickCount()

    cv.imshow("img",currImg)
    cv.imshow("edges",edges)
    
    time = (e2 - e1)/ cv.getTickFrequency() #time to run code inbetween e1 & e2
    print(time)
    

def updateImgMaxVal(newMaxVal):
    global maxVal
    maxVal = newMaxVal
    updateImg()

def updateBlurVal2(newBlur2):
    global blur2
    blur2 = newBlur2
    updateImg()

def updateImgMinVal(newMinVal):
    global minVal
    minVal = newMinVal
    updateImg()

def updateBlurVal(newBlurVal):
    global blur
    blur = newBlurVal
    updateImg()

def updatePostBlurVal(newPostBlurVal):
    global postBlur
    postBlur = newPostBlurVal
    updateImg()


dirList = os.listdir("Images")

print(dirList)

currImg = None
blurImg = None

minVal = 100
maxVal = 200
postBlur = 0

cv.namedWindow('controls')
cv.createTrackbar('minVal','controls',0,255,updateImgMinVal)
cv.createTrackbar('maxVal','controls',0,255,updateImgMaxVal)
cv.createTrackbar('blur','controls',0,20,updateBlurVal)
cv.createTrackbar('blur2','controls',0,20,updateBlurVal2)
cv.createTrackbar('postBlur','controls',0,20,updatePostBlurVal)

cv.namedWindow('img',cv.WINDOW_NORMAL)
cv.resizeWindow("img", 720, 960)

cv.namedWindow('edges',cv.WINDOW_NORMAL)
cv.resizeWindow("edges", 720, 960)

blur = 2
blur2 = 5

skip = False

for imgName in dirList:
    imgPath = os.path.join("Images",imgName)

    currImg = cv.imread(imgPath, cv.IMREAD_ANYCOLOR)
    assert currImg is not None, "file couldn't be read"

    blurImg = cv.blur(currImg,(5,5))

    updateImg()
    while True:
        key = cv.waitKey() & 0xFF
        if key == 27:
            cv.imwrite("A"+imgName.split(".")[0]+".png",edges)
            break
            


