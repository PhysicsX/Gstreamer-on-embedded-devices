import cv2
print(cv2.__version__)

# Cam properties
fps = 21
frame_width = 1280
frame_height = 720

dispW=1280
dispH=720
flip=0
#Uncomment These next Two Line for Pi Camera
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3820, height=2464, format=(string)NV12, framerate=(fraction)21/1 ! nvvidconv flip-method=0 ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam= cv2.VideoCapture(camSet)
 
#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
#cam=cv2.VideoCapture(0)
gst_str = "appsrc ! queue ! shmsink socket-path=/tmp/foo sync=false wait-for-connection=false"


# Create videowriter as a SHM sink

fourcc = cv2.VideoWriter_fourcc('I','4','2','0')
out = cv2.VideoWriter(gst_str, fourcc, fps, (frame_width, frame_height), True)



while True:
    ret, frame = cam.read()
    cv2.imshow('nanoCam',frame)
    frame = cv2.flip(frame,1)
    out.write(frame)
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
