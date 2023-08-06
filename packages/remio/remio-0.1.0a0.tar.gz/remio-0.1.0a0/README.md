<div align="center"><h1> RemIO </h1></div>
<div align="center">

[Documentation](https://hikki12.github.io/remio/)

[![Code Style][black-badge]][black]

</div>

A library for managing concurrent socketio, cv2, and pyserial processes. Useful for making robots or devices with Arduinos and Raspberry Pi. It was born in the context of remote laboratories, hence its name, where I used and developed several prototypes where the code began to redound. That's where I extracted the modules from this library. The hardware architecture that I used to employ was the following:

<img src="./docs/assets/images/arch-1.png" style="margin: 1rem 0;">

So I programmed the following architecture
<img src="./docs/assets/images/modules-arch.png" style="margin: 2rem 0;">

## Features
- Multiple Camera API
- Multiple Serial API
- Event-driven programming API for Serial.
- Event-driven programming API for Cameras.
- MJPEG streamer with SocketIO



## Install
Using pip:
```
pip install remio
```
Cloning the repository:
```
git clone https://github.com/Hikki12/remio

cd remio

pip install .
```

## Development
If you are a devolper, install the library as follows:
```
pip install -e .
```


## Multiple Cameras API
```python
import time
import cv2
from remio import Cameras


# Define devices
devices = {
    "webcam1": {
        "src": 0,
        "size": [400, 300],
        "fps": None,
        "reconnectDelay": 5,
        "backgroundIsEnabled": True,
        "emitterIsEnabled": False,
    },
    "webcam2": {
        "src": "http://192.168.100.70:3000/video/mjpeg",
        "size": [400, 300],
        "fps": None,
        "reconnectDelay": 5,
        "backgroundIsEnabled": True,
        "emitterIsEnabled": False,
    },
}

# Intialize Serial manager
camera = Cameras(devices=devices)

# Start device(s) connection on background
camera.startAll()

# Set a FPS speed to display image(s)
FPS = 20
T = 1 / FPS

while True:

    t0 = time.time()

    webcam1, webcam2 = camera.read(asDict=False)
    camera.clearAllFrames()  # to avoid repeated frames

    if webcam1 is not None:
        cv2.imshow("webcam1", webcam1)

    if webcam2 is not None:
        cv2.imshow("webcam2", webcam2)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    t1 = time.time()

    # Get a fixed delay value (t1 - t0) + delay = T
    delay = abs(T - (t1 - t0))
    time.sleep(delay)


# Close all Windows
cv2.destroyAllWindows()

# Stop all Running devices
camera.stopAll()

```

## Multiple Serial API
```python
import time
from remio import Serials


# Define devices
devices = {
    "arduino1": {
        "port": "/dev/cu.usbserial-1440",
        "baudrate": 9600,
        "emitterIsEnabled": True,  # Enable on/emit callbacks
        "reconnectDelay": 5,
    },
    "arduino2": {
        "port": "COM2",
        "baudrate": 9600,
        "emitterIsEnabled": True,
        "reconnectDelay": 5,
    },
}

# Intialize Serial manager
serial = Serials(devices=devices)

# Configure callbacks
serial.on("connection", lambda status: print(f"serial connected: {status}"))

# Start device(s) connection on background
serial.startAll()


while True:
    print("Doing some tasks...")
    time.sleep(1)

```

Resources
---------
- [Changelog](./CHANGELOG.md)

<!--
External URLs
-->
[black]: https://github.com/psf/black

<!--
Badges
-->
[black-badge]:https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge&logo=github

