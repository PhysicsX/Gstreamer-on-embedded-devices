## Gstreamer on raspberry pi and jetson nano
This page demonsrates example of gst-lauch tool with some applications using pi camera, web-cam on the raspberry pi and nvidia jetson nano board

Youtube video:

[![Youtube video link](https://img.youtube.com/vi/rPcQiDHyGnI/0.jpg)](//www.youtube.com/watch?v=rPcQiDHyGnI?t=0s "ulas dikme")


![](https://github.com/PhysicsX/Gstreamer-on-embedded-devices/blob/main/intro.gif)


## Installation
On both board installation is same. 

```bash
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt-get install gstreamer1.0-tools
$ sudo apt-get install gstreamer1.0-plugins-good
$ sudo apt-get install gstreamer1.0-plugins-bad
$ sudo apt-get install gstreamer1.0-plugins-ugly
$ sudo apt-get install libglib2.0-dev
$ sudo apt-get install libgstreamer1.0-dev
$ sudo apt-get install libgstreamer-plugins-base1.0-dev
```

## Hello World
For first Hello World application we can use built in elements like videotestsrc.

```bash
$ gst-launch-1.0 videotestsrc ! ximagesink
```
The videotestsrc element is used to produce test video data in a wide variety of formats. The video test data produced can be controlled with the "pattern" property.
It is possible to check capabilities of the elements using gst-inspect-1.0
```bash
$ gst-inspect1.0 videotestsrc
```
This will print useful informations about the element. These informations can be also get for pi camera or other elements. For instance even ximagesink. When you want to change the format of the video it will be very clever to check firt with this command.

To change the size of the vide we can use caps.
```bash
$ gst-launch-1.0 videotestsrc ! "video/x-raw,width=300, height=300, framerate=30/1! ximagesink
```
If you want to run this test application in gray color format ximagesink will not allow to create the pipeline. It is needed to convert the format for ximagesink that it can understand it. To do it videconvert element can be used easily.

```bash
$ gst-launch-1.0 videotestsrc ! "video/x-raw,width=300, height=300, framerate=30/1, format=GRAY16_LE" ! videoconvert ! ximagesink
```
Gstreamer give you abilty to send the frames over socket, network, and more.
For instance we can create a shared memory and read it over socket.
for server:
```bash
$ gst-launch-1.0 videotestsrc ! 'video/x-raw,width=300,height=300,format=(string)I420,framerate=(fraction)60/1' ! videoconvert ! shmsink socket-path=/tmp/foo shm-size=20000000
```
for client:
```bash
$ gst-launch-1.0 shmsrc socket-path=/tmp/foo !     'video/x-raw, format=(string)I420, width=(int)300, height=(int)300, framerate=(fraction)15/1' ! videoconvert ! ximagesink
```

## Pi camera usage  
To run the picamera on the jetson nano nvarguscamerasrc element can be used.

before run first check the capabilities of the element using:
```bash
gst-inspect1.0 nvarguscamerasrc
```
get the view from camera:

```bash
$ gst-launch-1.0 nvarguscamerasrc ! "video/x-raw(memory:NVMM),width=300, height=300, framerate=30/1, format=NV12" ! nvvidconv flip-method=1 ! nvegltransform ! nveglglessink -e
```
To run the pi camera on the raspberry pi ( not forget to enable it first ) it is possible to use v4l2src element.
v4l2src can be used to capture video from v4l2 devices, like webcams and tv cards.
```bash
$ gst-launch-1.0 v4l2src ! "video/x-raw,height=300,width=300,framerate=30/1" ! xvimagesink`
```
As it is seen we used xvimagesink instead of ximagesink. -ximagesink supports rgb format, not yuv format; xvimagesink supports yuv and other formats. So xvimagesink can support more formats than the ximagesink. ( that means no need to use videoconvert with xvimagesink)

To run the pi camera on the raspberry pi with rpicamsrc:
First install the rpicamsrc
```bash
$ git clone https://github.com/thaytan/gst-rpicamsrc.git
$ sudo apt-get install autoconf automake libtool pkg-config libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libraspberrypi-dev 

$ ./autogen.sh --prefix=/usr --libdir=/usr/lib/arm-linux-gnueabihf/
$ make
$ sudo make install
```
Then run the command:
```bash
$ gst-launch-1.0 rpicamsrc preview=false ! 'video/x-raw, width=320, height=320, framerate=30/1' ! videoconvert ! ximagesink
```

## Rtsp usage on raspberry pi  
These commands for rasppbery pi only.
We can use rpicamsrc element for rtsp.
first install rpicamsrc if you do not do already (previous step)
```bash
$ git clone https://github.com/thaytan/gst-rpicamsrc.git
$ sudo apt-get install autoconf automake libtool pkg-config libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libraspberrypi-dev 

$ ./autogen.sh --prefix=/usr --libdir=/usr/lib/arm-linux-gnueabihf/
$ make
$ sudo make install
```
then install rtsp 
```bash
$ wget https://gstreamer.freedesktop.org/src/gst-rtsp-server/gst-rtsp-server-1.10.4.tar.xz
$ tar -xf gst-rtsp-server-1.10.4.tar.xz 
$ cd gst-rtsp-server-1.10.4
$ ./configure
$ make
$ sudo make install
```
run the rtsp server:
```bash
$ cd ../gst-rtsp-server-1.10.4/examples
$ ./test-launch --gst-debug=3 "( rpicamsrc bitrate=8000000 awb-mode=tungsten preview=false ! video/x-h264, width=640, height=480, framerate=30/1 ! h264parse ! rtph264pay name=pay0 pt=96 )"
```
run this on another machine:
```bash
$ gst-launch-1.0 -v rtspsrc location=rtsp://<your_Pi's_IP>:8554/test latency=0 buffer-mode=auto ! decodebin ! videoconvert ! autovideosink sync=false
```

## USB camera usage
connect your usb camera run the command to list the connected cameras
```bash
$ v4l2-ctl --list-devices
bcm2835-codec-decode (platform:bcm2835-codec):
        /dev/video10
        /dev/video11
        /dev/video12

bcm2835-isp (platform:bcm2835-isp):
        /dev/video13
        /dev/video14
        /dev/video15
        /dev/video16

mmal service 16.1 (platform:bcm2835-v4l2-0):
        /dev/video0

Trust Webcam: Trust Webcam (usb-0000:01:00.0-1.2):
        /dev/video1
        /dev/video2
```
This is my output. As it is seen I am using trust webcam which has path video1 and video2

To run the camera with gst-launch:
```bash
$ gst-launch-1.0 v4l2src device=/dev/video1 ! decodebin ! videoconvert ! ximagesink
```
In my case I need to use decodebin element otherwise it will give error.
decodebin auto-magically constructs a decoding pipeline using available decoders and demuxers via auto-plugging.

## Opencv and gstreamer usage with python3
For this example I think you need opencv version 4 at least. I tried it on the raspbery pi which has a version of opencv is 3.2.0
and it gives this error:

```bash
3.2.0
OpenCV Error: Assertion failed (size.width>0 && size.height>0) in imshow, file /build/opencv-L65chJ/opencv-3.2.0+dfsg/modules/highgui/src/window.cpp, line 304
Traceback (most recent call last):
  File "gstreamerPython.py", line 24, in <module>
    cv2.imshow('nanoCam',frame)
cv2.error: /build/opencv-L65chJ/opencv-3.2.0+dfsg/modules/highgui/src/window.cpp:304: error: (-215) size.width>0 && size.height>0 in function imshow
```
To run the hello world example with python and opencv:
```bash
$ python3 helloWorldGstreamerPython.py
```
It is possible to add another drawing to the active frames.
This will draw a circle on frames :
```bash
$ python3 GstreamerDrawing.py
```
## Shm with Opencv and gstreamer and python3
We can send the frames one process to another using shared memory over socket.
To do that we need to use shmsink and shmsrc elements.
There is a server and client. For server:
```bash
$ gst-launch-1.0 nvarguscamerasrc ! 'video/x-raw(memory:NVMM), width=1920, height=1080,format=NV12, framerate=30/1'  ! nvvidconv flip-method=2  ! videoconvert  !  'video/x-raw, format=(string)I420,  width=(int)1024, height=(int)768, framerate=(fraction)30/1' !     queue !  identity !     shmsink wait-for-connection=1 socket-path=/tmp/tmpsock  shm-size=20000000 sync=true
```
This command is used for nvidia nano. You should convert it for raspberry pi accordingly. You will not see any visual output in the screen.
But frames are avaiable for shmsrc and on the /tmp/tmpsock
For client:
```bash
$ gst-launch-1.0 shmsrc socket-path=/tmp/tmpsock !     'video/x-raw, format=(string)I420, width=(int)1024, height=(int)768, framerate=(fraction)15/1' ! videoconvert ! ximagesink
```
When you run the above command you should see the camera output. So now lets try this between two python application.

shmServer.py script will create a shm memory for pi camera output on the nvdia jetson board.
```bash
$ python3 shmServer.py
```
So now lets use another binary which is Qt application to see the output in the shm.
You should have at least version 2.12 for the qt. Multimedia modul is used so old versions do not have this module.

For installation I really recommend you to watch my video to set up the qt for nvdia jetson nano.
```bash
# ./shmClient -platform eglfs
```
So you should see the camera output, which is shared from python script, in the screen.

Let's make more interesting. Run the face detection example with shared memory usage. Then with the same client
try to see the output with Qt.

```bash
$ python3 faceDetectionShm.py
```
After runnin the client qt application you should be able to see the rectangle around your face on the screen.
With qml we can make more interesting things. 
Compile and run the application which is in shmClient_2 then you will see a red rectangle which can be movable at the 
same time with face detection is running.
With Qml Can you imagine what kind of designs can be applied to the python AI applications? Nice !

![](https://github.com/PhysicsX/Gstreamer-on-embedded-devices/blob/main/out.gif)

to be continued....










