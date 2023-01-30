"""
M5Core2AWS
"""

import socket

import unit
import wifiCfg
from m5stack_ui import *
from uiflow import *

from m5stack import *

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)

# pbhub_0 = unit.get(unit.PBHUB, unit.PORTA)
# pbhub_0.setServoPulse(0, 0, 1500) # 500 - 2500 (1500 set to stop it)

response = None
ip = ""
PORT = 80


label0 = M5Label(
    "Hello, World!", x=0, y=0, color=0x000, font=FONT_MONT_14, parent=None
)
label1 = M5Label("", x=0, y=14, color=0x000, font=FONT_MONT_14, parent=None)
label2 = M5Label("", x=0, y=28, color=0x000, font=FONT_MONT_14, parent=None)
label3 = M5Label("", x=0, y=42, color=0x000, font=FONT_MONT_14, parent=None)
label4 = M5Label("", x=0, y=56, color=0x000, font=FONT_MONT_14, parent=None)
label5 = M5Label(
    "label0", x=70, y=91, color=0x000, font=FONT_MONT_14, parent=None
)


label1.set_text("Trying to connect to Wifi ...")
try:
    wifiCfg.doConnect("", "")
    ip = str(wifiCfg.wlan_sta.ifconfig()[0])
    label1.set_text("Connected to Wifi")
except:
    label1.set_text("Connection failed")

if wifiCfg.wlan_sta.isconnected():
    label2.set_text("IP: " + ip)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, PORT))
    server_socket.listen(5)

    while True:
        client_connection, address = server_socket.accept()
        request = client_connection.recv(1024).decode()
        label3.set_text("Request: " + request)
        led_on = request.find("/?led=on")
        led_off = request.find("/?led=off")
        server_off = request.find("/?server=off")
        power_off = request.find("/?power=off")
        label4.set_text(str(led_on))

        response = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>M5Stack Control Panel</title>
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
                    <a href="/?server=off">
                        <button>Server Off</button>
                    </a>
                    <a href="/?power=off">
                        <button>Server Off</button>
                    </a>
                </nav>
                <main>
                    <h1>Hello, World!</h1>
                    <p>My first paragraph.</p>
                </main>
                <script>
                </script>
            </body>
            </html>
        """
        if led_on > 0:
            rgb.setColorFrom(1, 10, 0x3333FF)
            rgb.setColor(1, 0x33FF33)
            rgb.setColor(10, 0x33FF33)
        elif led_off > 0:
            rgb.setColorFrom(1, 10, 0x000000)
        elif server_off > 0:
            server_socket.close()
        elif power_off > 0:
            power.powerOff()
        else:
            client_connection.send("HTTP/1.1 200 OK\n")
            client_connection.send("Connection: close\n\n")
            client_connection.sendall((response).encode())
            client_connection.close()
