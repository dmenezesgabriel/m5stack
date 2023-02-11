#!/usr/bin/env python
# coding: utf-8

# In[88]:


#remove_cell
get_ipython().run_line_magic('serialconnect', '--port=COM7')


# In[89]:


import json
import time

import unit
from libs.m5_espnow import M5ESPNOW
from m5stack_ui import *
from uiflow import *

from m5stack import *


# In[91]:


# print(dir(unit))


# In[92]:


# import m5stack_ui
# print(dir(m5stack_ui))


# In[93]:


# import m5stack
# print(dir(m5stack))


# In[94]:


joystick_0 = unit.get(unit.JOYSTICK, unit.PORTA)

dual_button_0 = unit.get(unit.DUAL_BUTTON, unit.PORTC)


# In[114]:


flag_callback = None
replica_mac = None
replica_data = None
run = None
cnt_succes = None
count_send = None
peer_mac = None
replica_ssid = None
btn_red_active = False
btn_blue_active = False


# In[115]:


now = M5ESPNOW(1)


# In[116]:


screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)

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


# In[117]:


def get_direction(x_axis, y_axis):
    current_direction = "stop"
    directions = {
        "forward": 50 > y_axis,
        "backward": y_axis > 200,
        "left": x_axis > 200,
        "right": 50 > x_axis,
        "stop": (200 > x_axis > 50) & (200 > y_axis > 50)
    }
    for key, value in directions.items():
        if value == True:
            current_direction = key
            break
    return key


# In[118]:


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


def btnRed0_wasPressed():
    global btn_red_active
    btn_red_active = True
    pass


def btnRed0_wasReleased():
    global btn_red_active
    btn_red_active = False
    pass


def btnBlue0_wasPressed():
    global btn_blue_active
    btn_blue_active = True
    pass


def btnBlue0_wasReleased():
    global btn_blue_active
    btn_blue_active = False
    pass


# In[119]:


now.espnow_send_cb(send_callback)
now.espnow_recv_cb(recv_callback)

btnA.wasPressed(buttonA_wasPressed)
btnC.wasPressed(buttonC_wasPressed)

dual_button_0.btnRed.wasPressed(btnRed0_wasPressed)
dual_button_0.btnRed.wasReleased(btnRed0_wasReleased)

dual_button_0.btnBlue.wasPressed(btnBlue0_wasPressed)
dual_button_0.btnBlue.wasReleased(btnBlue0_wasReleased)


# In[120]:


count_send = 0
cnt_succes = 0
flag_callback = 0
run = 1
replica_ssid = "M5_Replica"


# In[121]:


while peer_mac == None:
    peer_mac = now.espnow_scan(1, replica_ssid)
replica_ssid_value.set_text(str(replica_ssid))
replica_mac_value.set_text(str(peer_mac))
now.espnow_add_peer(peer_mac, 1, 0, False)


# In[122]:


print(peer_mac)


# In[123]:


print(get_direction(joystick_0.X, joystick_0.Y))


# In[ ]:


# TODO
# Bring here the direction logic from receiver and send only the direction as state
# ex: forward
# send message only if state changed

current_direction = "stop"
current_angle = "closed"
while run:
    x_axis = joystick_0.X
    y_axis = joystick_0.Y
    new_direction = get_direction(joystick_0.X, joystick_0.Y)
    
    if btn_red_active == True:
        new_angle = "closed"
    elif btn_blue_active == True:
        new_angle = "opened"
    else:
        new_angle = current_angle
    
    if (new_direction != current_direction) or (new_angle != current_angle):
        current_angle = new_angle
        current_direction = new_direction
        message = json.dumps(
            {
                "count": str(count_send),
                "direction": current_direction,
                "angle": current_angle
            }
        )
        count_send = count_send + 1
        now.espnow_send_str(1, message)
        replica_send_count_value.set_text(message)        
        wait_ms(1)

