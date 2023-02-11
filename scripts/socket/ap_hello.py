"""
M5Core2AWS
"""
import socket

import network
import wifiCfg
from m5stack_ui import *
from uiflow import *

from m5stack import *

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="M5StackCore2")
ap.config(authmode=3, password="123456789")

response = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>M5Stack Control Panel</title>
        <style>
        </style>
    </head>
    <body>
        <main>
            <h1>Hello, World!</h1>
        </main>
        <script>
        </script>
    </body>
    </html>
"""

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("192.168.4.1", 80))
server_socket.listen(5)


label0 = M5Label(
    "Hello, World!", x=0, y=0, color=0x000, font=FONT_MONT_14, parent=None
)
label1 = M5Label("", x=0, y=14, color=0x000, font=FONT_MONT_14, parent=None)

label0.set_text(str(wifiCfg.wlan_sta.ifconfig()[0]))

while True:
    client_connection, address = server_socket.accept()
    request = client_connection.recv(1024).decode()
    label1.set_text("Request: " + request)
    client_connection.send("HTTP/1.1 200 OK\n")
    client_connection.send("Connection: close\n\n")
    client_connection.sendall((response).encode())
    client_connection.close()
import socket

import network
import wifiCfg
from m5stack_ui import *
from uiflow import *

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="M5StackCore2")
ap.config(authmode=3, password="123456789")

response = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>M5Stack Control Panel</title>
        <style>
        </style>
    </head>
    <body>
        <main>
            <h1>Hello, World!</h1>
            <p>My first paragraph.</p>
        </main>
        <script>
        </script>
    </body>
    </html>
"""

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("192.168.4.1", 80))
server_socket.listen(5)


label0 = M5Label(
    "Hello, World!", x=0, y=0, color=0x000, font=FONT_MONT_14, parent=None
)
label1 = M5Label("", x=0, y=14, color=0x000, font=FONT_MONT_14, parent=None)

label0.set_text(str(wifiCfg.wlan_sta.ifconfig()[0]))

while True:
    client_connection, address = server_socket.accept()
    request = client_connection.recv(1024).decode()
    label1.set_text("Request: " + request)
    client_connection.send("HTTP/1.1 200 OK\n")
    client_connection.send("Connection: close\n\n")
    client_connection.sendall((response).encode())
    client_connection.close()
