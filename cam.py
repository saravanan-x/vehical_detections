import network
import socket
import camera

# WIFI
SSID = "bps_wifi"
PASSWORD = "sagabps@235"

# connect wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    pass

print("Connected:", wlan.ifconfig())

# camera init
camera.init(0, format=camera.JPEG)
camera.framesize(camera.FRAME_QVGA)   # 320x240
camera.quality(10)

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print("Camera Stream Ready")

while True:
    conn, addr = s.accept()
    print('Client connected')

    conn.send(b'HTTP/1.1 200 OK\r\n')
    conn.send(b'Content-Type: multipart/x-mixed-replace; boundary=frame\r\n\r\n')

    while True:
        frame = camera.capture()

        conn.send(b'--frame\r\n')
        conn.send(b'Content-Type: image/jpeg\r\n\r\n')
        conn.send(frame)
        conn.send(b'\r\n')
