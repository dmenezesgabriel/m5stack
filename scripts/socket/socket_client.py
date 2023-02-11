"""
M5StickCPlus Client
"""

import socket

import unit
import wifiCfg
from m5ui import *
from uiflow import *

from m5stack import *
from socket_comm import SocketClient

setScreenColor(0x111111)
joystick_0 = unit.get(unit.JOYSTICK, unit.PORTA)

ip = ""

label0 = M5TextBox(0, 0, "Hello, World!", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label1 = M5TextBox(0, 14, "label0", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label2 = M5TextBox(0, 28, "label0", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label3 = M5TextBox(50, 103, "label3", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label4 = M5TextBox(50, 138, "label4", lcd.FONT_Default, 0xFFFFFF, rotate=0)

label1.setText("Trying to connect to Wifi ...")
try:
    wifiCfg.doConnect("M5StackCore2", "123456789")
    ip = str(wifiCfg.wlan_sta.ifconfig()[0])
    label1.setText("Connected to Wifi")
except:
    label1.setText("Connection failed")

if wifiCfg.wlan_sta.isconnected() and len(ip) > 0:
    label2.setText("IP: " + ip)


socket_client = SocketClient(
    socket.AF_INET,
    socket.SOCK_STREAM,
    "192.168.4.1",
    80,
    1,
    1024,
)
while True:
    socket_client.server_socket.connect(("192.168.4.1", 80))
    x = str(joystick_0.X)
    y = str(joystick_0.Y)
    label3.setText("X: " + x)
    label4.setText("Y: " + y)
    socket_client.server_socket.send_comm("?x=" + x + "?y=" + y)
    wait_ms(2)
