"""HTTP server functionalities."""
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from .stream import MJPEGEncoder


class Handler(BaseHTTPRequestHandler):
    """Custom HTTP handler for streaming video on MJPEG format."""
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
        self.end_headers()

        if self.server.camera is not None and self.server.encoder is not None:
            fps = self.server.fps
            while True:
                try:
                    frame = self.server.camera.read()
                    jpeg = self.server.encoder.encode(frame, base64=False)
                    
                    self.wfile.write(bytes("--jpgboundary\n", "utf8"))
                    self.send_header('Content-type', 'image/jpeg')
                    self.send_header('Content-length', len(jpeg))
                    self.end_headers()

                    self.wfile.write(jpeg)
                    time.sleep(1 / fps) 

                except Exception as e:
                    print("--> MJPEGHandler error: ", e)
                    break


class CustomHTTPServer(HTTPServer):
    """HTTP server with custom params."""
    def __init__(self, camera = None, encoder = None, fps: int = 12, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.camera = camera
        self.encoder = encoder
        self.fps = fps


class ThreadedHTTPServer(ThreadingMixIn, CustomHTTPServer):
    """Handle requests in a separate thread."""


class MJPEGServer:
    """A MJPEG server class based on HTTPServer and ThreadingMixIn.
    Args:
        camera: A camera instance.
        fps: server fps to stream.
        ip: ip address of the server.
        port: port value of the server.
        enconderSettings: MJPEG encoder settings.
    """
    def __init__(self, 
        camera = None,
        fps: int = 10,
        ip: str = '0.0.0.0', 
        port: int = 8080, 
        encoderSettings: dict = {
            "quality": 60,
            "colorspace": "bgr",
            "colorsubsampling": "422",
            "fastdct": True,
            "enabled": True,
        },
        *args, 
        **kwargs
    ):
        self.camera = camera
        self.ip = ip
        self.port = port
        self.fps = fps
        self.encoder = MJPEGEncoder(**encoderSettings)
        self.server = ThreadedHTTPServer(
            camera=self.camera,
            encoder=self.encoder,
            fps = self.fps,
            server_address=(ip, port),
            RequestHandlerClass=Handler
        )

    def run(self, display_url: bool = True, start_camera: bool = True):
        """Executes the streaming loop.
        Args:
            display_url: show a url with the server address?
            start_camera: call start method of the camera instance?
        """
        try:
            if display_url:
                print(f"MJPEG server running on http://{self.ip}:{self.port}")
            if start_camera:
                self.camera.start()
            self.server.serve_forever()
        except Exception as e:
            print(f"--> MJPEG server: {e}")
            self.stop()

    def stop(self, stop_camera: bool = True):
        """Stops the mjpeg server.
        Args:
            stop_camera: call the stop method of the camera?
        """
        self.server.shutdown()
        if self.camera is not None and stop_camera:
            self.camera.stop()
