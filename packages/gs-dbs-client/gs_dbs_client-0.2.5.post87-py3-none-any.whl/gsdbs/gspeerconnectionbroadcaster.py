import ast
import json
import logging
import platform
import time

import socketio
from aiortc import RTCPeerConnection, RTCRtpSender
from aiortc.contrib.media import MediaPlayer, MediaRelay
from gsdbs.pitrack import PiH264StreamTrack

raspberry =True
try:
    import picamera
except ImportError:
    raspberry = False

relay = None
webcam = None
camera = None
videotrack = None


class GSPeerConnectionBroadcaster:

    def create_pi_track(self):
        global relay, camera, webcam, videotrack
        if relay is None:
            videotrack = PiH264StreamTrack(30)
            camera = picamera.PiCamera()
            camera.resolution = (1280, 720)
            camera.framerate = 30
            target_bitrate = camera.resolution[0] * \
                             camera.resolution[1] * \
                             camera.framerate * 0.150
            camera.start_recording(
                videotrack,
                format="h264",
                profile="constrained",
                bitrate=int(target_bitrate),  # From wowza recommended settings
                inline_headers=True,
                sei=False,
            )
            relay = MediaRelay()
        return relay.subscribe(videotrack)

    def create_local_tracks(self, device, transcode=True):
        global relay, webcam
        if relay is None:
            if platform.system() == "Darwin":
                options = {
                    "video_size": f"{str(self.gsdbs.credentials['hres'])}x{str(self.gsdbs.credentials['vres'])}",
                    "preset": "veryfast",
                    "framerate": str(self.gsdbs.credentials["framerate"]),
                    "c:v": "h264_v4l2m2m",
                    "input_format": "h264",
                    "pixelformat": "H264"
                }
                webcam = MediaPlayer("default:none", format="avfoundation", options=options)
            elif platform.system() == "Windows":
                webcam = MediaPlayer(f"video={device}", format="dshow")
            else:
                options = {
                    "video_size": f"{str(self.gsdbs.credentials['hres'])}x{str(self.gsdbs.credentials['vres'])}",
                    "preset": "veryfast",
                    "framerate": str(self.gsdbs.credentials["framerate"]),
                    "c:v": "h264_v4l2m2m",
                    "input_format": "h264",
                    "pixelformat": "H264"
                }
                webcam = MediaPlayer(device, format="v4l2", options=options, transcode=False)
            relay = MediaRelay()
        return relay.subscribe(webcam.video, buffered=False)

    @classmethod
    async def create(cls, gsdbs):
        self = GSPeerConnectionBroadcaster()
        self.gsdbs = gsdbs
        self.sio = socketio.AsyncClient()
        self.peerConnections = {}
        self._logger = logging.getLogger(__name__)
        self.webcam = None
        self.relay = None

        @self.sio.event
        async def connect():
            self._logger.info('connection established')

        @self.sio.event
        async def answer(id, description):
            if type(description) == str:
                description = ast.literal_eval(description)
            desc = type('new_dict', (object,), description)
            await self.peerConnections[id].setRemoteDescription(desc)

        @self.sio.event
        async def watcher(id):
            pc = RTCPeerConnection()
            self.peerConnections[id] = pc


            video = self.create_local_tracks(self.gsdbs.credentials["device"])
            pc.addTrack(video)
            if raspberry :
                codecs = RTCRtpSender.getCapabilities("video").codecs
                preferences = [codec for codec in codecs if codec.mimeType == "video/H264"]
                transceiver = pc.getTransceivers()[0]
                transceiver.setCodecPreferences(preferences)
            # pc.addTrack(self.create_local_tracks(
            #     self.gsdbs.credentials["framerate"],
            #     self.gsdbs.credentials["hres"],
            #     self.gsdbs.credentials["vres"],
            #     self.gsdbs.credentials["rtbufsize"],
            #     self.gsdbs.credentials["device"]
            # ))

            channel = pc.createDataChannel("message")

            # def send_data():
            #     channel.send("test123")
            # channel.on("open", send_data)

            @pc.on("iceconnectionstatechange")
            async def on_iceconnectionstatechange():
                # self._logger.info("ICE connection state is %s", pc.iceConnectionState)
                if pc.iceConnectionState == "failed":
                    await pc.close()
                    self.peerConnections.pop(id, None)

            await pc.setLocalDescription(await pc.createOffer())
            await self.sio.emit("offer", {"id": id,
                                          "message": json.dumps(
                                              {"type": pc.localDescription.type, "sdp": pc.localDescription.sdp})})
            # self._logger.info(pc.signalingState)

        @self.sio.event
        async def disconnectPeer(id):
            if id in self.peerConnections:
                await self.peerConnections[id].close()
                self.peerConnections.pop(id, None)

        @self.sio.event
        async def disconnect():
            self._logger.info('disconnected from server')

        connectURL = ""

        if "localhost" in self.gsdbs.credentials["signalserver"]:
            connectURL = f'{self.gsdbs.credentials["signalserver"]}:{str(self.gsdbs.credentials["signalport"])}'
        else:
            connectURL = self.gsdbs.credentials["signalserver"]

        await self.sio.connect(
            f'{connectURL}?gssession={self.gsdbs.cookiejar.get("session")}.{self.gsdbs.cookiejar.get("signature")}{self.gsdbs.credentials["cnode"]}')
        await self.sio.wait()
