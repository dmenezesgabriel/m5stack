#!/usr/bin/env python
# coding: utf-8

# In[33]:


#remove_cell
get_ipython().run_line_magic('serialconnect', '--port=COM6')


# In[34]:


import json
import time

from libs.m5_espnow import M5ESPNOW
from m5ui import *
from uiflow import *
import unit
from m5stack import *


# In[35]:


pb_unit_connected = False

try:
    pbhub_0 = unit.get(unit.PBHUB, unit.PORTA)
    pb_unit_connected = True
except Exception as error:
    print(error)
    pb_unit_connected = False


# In[36]:


mac_addr = None
data = None
onetime = None
ssid = None


# In[37]:


now = M5ESPNOW(1)


# In[38]:


setScreenColor(0x222222)

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
    0, 186, "SEND DATA:", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0
)
send_data_value = M5TextBox(
    0, 202, "send_data", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0
)


# In[39]:


current_direction = "stop"
current_angle = "closed"


# In[46]:


def recv_callback(dummy):
    global mac_addr, data, onetime, ssid, current_direction, current_angle
    mac_addr, data = now.espnow_recv_str()
    remote_mac_address_value.setText(str(mac_addr))
    remote_data_value.setText(str(data))
    send_data_value.setText(str(data))
    if onetime:
        now.espnow_add_peer(mac_addr, 1, 1, False)
        onetime = 0

    now.espnow_send_str(1, data)
    received_data_json = json.loads(data)
    new_direction = str(received_data_json["direction"])
    new_angle = str(received_data_json["angle"])
    
    if int(received_data_json["count"]) %2 == 0:
        M5Led.on()
    else:
        M5Led.off()
    
    if (new_direction != current_direction):
        current_direction = new_direction
        # Move
        if (current_direction == "backward"):
            # forward
            pbhub_0.setServoPulse(1, 0, 2000)
            pbhub_0.setServoPulse(4, 0, 1000)
        elif (current_direction == "forward"):
            # backward
            pbhub_0.setServoPulse(1, 0, 1000)
            pbhub_0.setServoPulse(4, 0, 2000)
        elif (current_direction == "right"):
            # Left
            pbhub_0.setServoPulse(1, 0, 1800)
            pbhub_0.setServoPulse(4, 0, 1800)
        elif (current_direction == "left"):
            # Right
            pbhub_0.setServoPulse(1, 0, 1200)
            pbhub_0.setServoPulse(4, 0, 1200)
        elif (current_direction == "stop"):
            # Stop
            pbhub_0.setServoPulse(1, 0, 1500)
            pbhub_0.setServoPulse(4, 0, 1500)
    
    # Catch
    if (current_angle != new_angle):
        current_angle = new_angle
        if current_angle == "opened":
            pbhub_0.setServoAngle(2, 0, 45)
        else:
            pbhub_0.setServoAngle(2, 0, 90)  
    pass


# In[47]:


now.espnow_recv_cb(recv_callback)


# In[45]:


onetime = 1
ssid = "M5_Replica"
now.espnow_set_ap(ssid, "")
ssid_value.setText(str(ssid))
mac_address_value.setText(str(now.espnow_get_mac()))

