"""
M5Core2AWS
"""
import json
import time

import unit
from libs.m5_espnow import M5ESPNOW
from m5stack_ui import *
from uiflow import *

from m5stack import *

joystick_0 = unit.get(unit.JOYSTICK, unit.PORTA)
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)


flag_callback = None
replica_mac = None
replica_data = None
run = None
cnt_succes = None
count_send = None
peer_mac = None
replica_ssid = None

now = M5ESPNOW(1)


replica_mac_title = M5Label(
    "REPLICA MAC:", x=1, y=14, font=FONT_MONT_14, parent=None
)
replica_mac_value = M5Label(
    "replica_mac", x=0, y=28, font=FONT_MONT_14, parent=None
)

replica_ssid_title = M5Label(
    "REPLICA SSID:", x=0, y=42, font=FONT_MONT_14, parent=None
)
replica_ssid_value = M5Label(
    "replica_ssid", x=0, y=56, font=FONT_MONT_14, parent=None
)

replica_send_count_title = M5Label(
    "SEND COUNT:", x=0, y=70, font=FONT_MONT_14, parent=None
)
replica_send_count_value = M5Label(
    "replica_send_count", x=0, y=84, font=FONT_MONT_14, parent=None
)

replica_received_count_title = M5Label(
    "REVC COUNT:", x=0, y=98, font=FONT_MONT_14, parent=None
)
replica_received_count_value = M5Label(
    "replica_received_count", x=0, y=112, font=FONT_MONT_14, parent=None
)

replica_success_count_title = M5Label(
    "SUCCESS COUNT:", x=0, y=126, font=FONT_MONT_14, parent=None
)
replica_success_count_value = M5Label(
    "replica_success_count", x=0, y=140, font=FONT_MONT_14, parent=None
)


def send_callback(flag):
    global flag_callback, replica_mac, replica_data, run, cnt_succes, count_send, peer_mac, replica_ssid
    flag_callback = flag
    if flag_callback:
        cnt_succes = cnt_succes + 1
        replica_success_count_value.set_text(str(cnt_succes))

    pass


def recv_callback(dummy):
    global flag_callback, replica_mac, replica_data, run, cnt_succes, count_send, peer_mac, replica_ssid
    replica_mac, replica_data = now.espnow_recv_str()
    replica_received_count_value.set_text(str(replica_data))

    pass


def buttonA_wasPressed():
    global flag_callback, replica_mac, replica_data, run, cnt_succes, count_send, peer_mac, replica_ssid
    run = 1
    pass


def buttonC_wasPressed():
    global flag_callback, replica_mac, replica_data, run, cnt_succes, count_send, peer_mac, replica_ssid
    run = 0
    pass


now.espnow_send_cb(send_callback)
now.espnow_recv_cb(recv_callback)

btnA.wasPressed(buttonA_wasPressed)
btnC.wasPressed(buttonC_wasPressed)

count_send = 0
cnt_succes = 0
flag_callback = 0
run = 0
replica_ssid = "M5_Replica"

# Find mac address by ssid
while peer_mac == None:
    peer_mac = now.espnow_scan(1, replica_ssid)
replica_ssid_value.set_text(str(replica_ssid))
replica_mac_value.set_text(str(peer_mac))
now.espnow_add_peer(peer_mac, 1, 0, False)

# start
while True:
    if run:
        count_send = count_send + 1
        now.espnow_send_str(
            1,
            json.dumps(
                {
                    "property": str(count_send),
                    "joystick_x_pos": joystick_0.X,
                    "joystick_y_pos": joystick_0.Y,
                }
            ),
        )
        replica_send_count_value.set_text(str(count_send))
        wait_ms(1)
    wait_ms(2)
