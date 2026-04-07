import network
import socket
import camera
from machine import Pin

# BUZZER PIN
buzzer = Pin(12, Pin.OUT)
buzzer.value(0)

# WIFI
SSID = "Mastak"
PASSWORD = "9842588997"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    pass

ip = wlan.ifconfig()[0]
print("ESP32 IP:", ip)

# camera init
camera.init(0, format=camera.JPEG)
camera.framesize(camera.FRAME_QVGA)
camera.quality(10)

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print("Camera Stream Ready")

while True:
    conn, addr = s.accept()
    print("Client connected:", addr)

    request = conn.recv(1024)
    request = str(request)

    # BUZZER CONTROL
    if "/buzzer_on" in request:
        buzzer.value(1)
        print("BUZZER STATUS: ON")

    if "/buzzer_off" in request:
        buzzer.value(0)
        print("BUZZER STATUS: OFF")

    # STREAM HEADER
    conn.send(b'HTTP/1.1 200 OK\r\n')
    conn.send(b'Content-Type: multipart/x-mixed-replace; boundary=frame\r\n\r\n')

    while True:
        try:
            frame = camera.capture()

            conn.send(b'--frame\r\n')
            conn.send(b'Content-Type: image/jpeg\r\n\r\n')
            conn.send(frame)
            conn.send(b'\r\n')

        except:
            print("Client disconnected")
            break
