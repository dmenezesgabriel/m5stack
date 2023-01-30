"""
M5StickC Plus
"""

import json

from libs.m5_espnow import M5ESPNOW
from m5ui import *
from uiflow import *

from m5stack import *

setScreenColor(0x222222)

mac_addr = None
data = None
onetime = None
ssid = None

now = M5ESPNOW(1)

# UI
app_title = M5Title(
    title="ESPNOW-REPLICA",
    x=1,
    fgcolor=0xFFFFFF,
    bgcolor=0xFF7C00,
)

mac_address_title = M5TextBox(
    1, 28, "MAC ADDR:", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0
)
mac_address_value = M5TextBox(
    1, 42, "mac_addr_value", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0
)

remote_mac_address_title = M5TextBox(
    1, 56, "REMOTE MAC:", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0
)
remote_mac_address_value = M5TextBox(
    0, 70, "remote_mac", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0
)

ssid_title = M5TextBox(0, 84, "SSID:", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0)
ssid_value = M5TextBox(
    0, 98, "ssid_value", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0
)

remote_data_title = M5TextBox(
    0, 112, "REMOTE DATA:", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0
)
remote_data_value = M5TextBox(
    0, 126, "remote_data", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0
)

send_data_title = M5TextBox(
    0, 140, "SEND DATA:", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0
)
send_data_value = M5TextBox(
    0, 154, "send_data", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0
)


def recv_callback(dummy):
    global mac_addr, data, onetime, ssid
    mac_addr, data = now.espnow_recv_str()
    remote_mac_address_value.setText(str(mac_addr))
    remote_data_value.setText(str(data))
    send_data_value.setText(str(data))
    if onetime:
        now.espnow_add_peer(mac_addr, 1, 1, False)
        onetime = 0

    now.espnow_send_str(1, data)
    received_data_json = json.loads(data)
    pass


now.espnow_recv_cb(recv_callback)


onetime = 1
ssid = "M5_Replica"
now.espnow_set_ap(ssid, "")
ssid_value.setText(str(ssid))
mac_address_value.setText(str(now.espnow_get_mac()))
