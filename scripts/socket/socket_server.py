"""
M5Core2AWS
"""
import socket

import network
import unit
import wifiCfg
from m5stack_ui import *
from socket_comm import SocketServer
from uiflow import *

from m5stack import *

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)

pbhub_0 = unit.get(unit.PBHUB, unit.PORTA)

# ACCESS POINT 192.168.4.1
# ap = network.WLAN(network.AP_IF)
# ap.active(True)
# ap.config(essid="M5StackCore2")
# ap.config(authmode=3, password="123456789")

label0 = M5Label(
    "Hello, World!", x=0, y=0, color=0x000, font=FONT_MONT_14, parent=None
)
label1 = M5Label("", x=0, y=14, color=0x000, font=FONT_MONT_14, parent=None)
label2 = M5Label("", x=0, y=28, color=0x000, font=FONT_MONT_14, parent=None)
label3 = M5Label("", x=0, y=42, color=0x000, font=FONT_MONT_14, parent=None)
label4 = M5Label("", x=0, y=56, color=0x000, font=FONT_MONT_14, parent=None)

response = None
ip = ""
PORT = 80

label1.set_text("Trying to connect to Wifi ...")
try:
    wifiCfg.doConnect("", "")
    ip = str(wifiCfg.wlan_sta.ifconfig()[0])
    label1.set_text("Connected to Wifi")
except:
    label1.set_text("Connection failed")

if wifiCfg.wlan_sta.isconnected():
    label2.set_text("IP: " + ip)


label0.set_text(str(wifiCfg.wlan_sta.ifconfig()[0]))

response = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>M5Stack Access Point</title>
        <style>
        </style>
    </head>
    <body>
            <nav>
                <a href="/?led=on">
                    <button>Led On</button>
                </a>
                <a href="/?led=off">
                    <button>Led Off</button>
                </a>
        </nav>
        <main>
            <h1>Hello, World!</h1>
            <ul>
                <li>
                    <a href="/?forward=true">
                        <button>Move Forward</button>
                    </a>
                </li>
                <li>
                    <a href="/?backward=true">
                        <button>Move backward</button>
                    </a>
                </li>
                <li>
                    <a href="/?left=true">
                        <button>Move Left</button>
                    </a>
                </li>
                <li>
                    <a href="/?right=true">
                        <button>Move Right</button>
                    </a>
                </li>
                <li>
                    <a href="/?stop=true">
                        <button>Stop</button>
                    </a>
                </li>
            </ul>
        </main>
        <script>
        </script>
    </body>
    </html>
"""


def callback(server_instance, response_comm):
    """
    callback function always will receive the socket_server instance and
    response.
    """
    if response_comm:
        label1.set_text("Request: " + response_comm)
        led_on = response_comm.find("/?led=on")
        led_off = response_comm.find("/?led=off")
        move_forward = response_comm.find("/?forward=true")
        move_backward = response_comm.find("/?backward=true")
        move_left = response_comm.find("/?left=true")
        move_right = response_comm.find("/?right=true")
        move_stop = response_comm.find("/?stop=true")
        if led_on > 0:
            label4.set_text("Led on: " + str(led_on))
            rgb.setColorFrom(1, 10, 0x3333FF)
            rgb.setColor(1, 0x33FF33)
            rgb.setColor(10, 0x33FF33)
        elif led_off > 0:
            label4.set_text("Led off: " + str(led_off))
            rgb.setColorFrom(1, 10, 0x000000)
        elif move_forward > 0:
            label4.set_text("Move forward: " + str(move_forward))
            pbhub_0.setServoPulse(1, 0, 2000)
            pbhub_0.setServoPulse(4, 0, 1000)
        elif move_backward > 0:
            label4.set_text("Move backward: " + str(move_backward))
            pbhub_0.setServoPulse(1, 0, 1000)
            pbhub_0.setServoPulse(4, 0, 2000)
        elif move_left > 0:
            label4.set_text("Move left: " + str(move_left))
            pbhub_0.setServoPulse(1, 0, 1800)
            pbhub_0.setServoPulse(4, 0, 1800)
        elif move_right > 0:
            label4.set_text("Move right: " + str(move_right))
            pbhub_0.setServoPulse(1, 0, 1200)
            pbhub_0.setServoPulse(4, 0, 1200)
        elif move_stop > 0:
            label4.set_text("Move stop: " + str(move_stop))
            pbhub_0.setServoPulse(1, 0, 1500)
            pbhub_0.setServoPulse(4, 0, 1500)
    server_instance.client_socket.send("HTTP/1.1 200 OK\n")
    server_instance.client_socket.send("Connection: close\n\n")
    server_instance.client_socket.sendall((response).encode())
    server_instance.client_socket.close()


socket_server = SocketServer(
    socket.AF_INET,
    socket.SOCK_STREAM,
    ip,
    80,
    5,
    1024,
)
socket_server.listen(callback)
