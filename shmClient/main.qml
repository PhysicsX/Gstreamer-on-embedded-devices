import QtQuick 2.15
import QtQuick.Window 2.12
import QtMultimedia 5.12
import QtQuick.Controls.Styles 1.2
import QtQuick.VirtualKeyboard 2.4
import QtQuick.Controls 2.3
import QtQuick.VirtualKeyboard.Settings 2.2
import QtQuick.Layouts 1.12
import QtGraphicalEffects 1.12

Window {
    visible: true
    width: 640
    height: 480
    title: qsTr("Hello World")

    Rectangle {
        id:streaming
        objectName: "streaming"
        width: parent.width
        height: parent.height
        z:40
        color: "black"


        MediaPlayer {
            id: player

            source: "gst-pipeline: shmsrc socket-path=/tmp/foo do-timestamp=true ! video/x-raw, format=(string)BGR, width=(int)1280, height=(int)720, framerate=(fraction)30/1 ! autovideoconvert ! qtvideosink"
            //source: "gst-pipeline: videotestsrc pattern=snow ! qtvideosink"
            //source: "gst-pipeline: playbin uri=https://www.freedesktop.org/software/gstreamer-sdk/data/media/sintel_trailer-480p.webm"
            autoPlay: true

        }

        VideoOutput {
            id: videoOutput
            source: player
            anchors.fill: parent
        }

        }
}
