import unit
from m5stack_ui import *
from uiflow import *

from m5stack import *

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)
joystick_0 = unit.get(unit.JOYSTICK, unit.PORTA)
dual_button_0 = unit.get(unit.DUAL_BUTTON, unit.PORTC)


joystick_x = None
joystick_y = None


joystick_x_label = M5Label(
    "label0", x=38, y=22, color=0x000, font=FONT_MONT_14, parent=None
)
joystick_y_label = M5Label(
    "label1", x=42, y=53, color=0x000, font=FONT_MONT_14, parent=None
)
button_red_label = M5Label(
    "label0", x=41, y=90, color=0x000, font=FONT_MONT_14, parent=None
)
button_blue_label = M5Label(
    "label0", x=36, y=129, color=0x000, font=FONT_MONT_14, parent=None
)


def btnRed0_wasReleased():
    global joystick_x, joystick_y
    button_red_label.set_text(str(dual_button_0.btnRed.wasReleased()))
    pass


dual_button_0.btnRed.wasReleased(btnRed0_wasReleased)


def btnBlue0_wasReleased():
    global joystick_x, joystick_y
    button_blue_label.set_text(str(dual_button_0.btnBlue.wasReleased()))
    pass


dual_button_0.btnBlue.wasReleased(btnBlue0_wasReleased)

while True:
    joystick_x = joystick_0.X
    joystick_y = joystick_0.Y
    joystick_x_label.set_text(str(joystick_x))
    joystick_y_label.set_text(str(joystick_y))
    wait_ms(2)
