import cv2
print(cv2.__version__)


# Cam properties
fps = 30.
frame_width = 1920
frame_height = 1080



dispW=640
dispH=480
flip=2

coordinate = (200,200)

#Uncomment These next Two Line for Pi Camera
camSet = ('videotestsrc pattern=snow ! videoconvert ! appsink')
          
cam= cv2.VideoCapture(camSet)
 


while True:
    ret, frame = cam.read()
    cv2.circle(frame,center=coordinate, radius=100, color=(0,0,0), thickness=10)
    cv2.imshow('nanoCam',frame)
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
