from m5stack import *
from m5stack_ui import *
from uiflow import *
import time
import unit


screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)
pir_0 = unit.get(unit.PIR, unit.PORTB)


a1 = None
a = None






def buttonA_wasPressed():
  global a1, a
  a = True
  pass
btnA.wasPressed(buttonA_wasPressed)

def buttonB_wasPressed():
  global a1, a
  a = False
  pass
btnB.wasPressed(buttonB_wasPressed)

def buttonB_wasPressed():
  global a1, a
  a = False
  pass
btnB.wasPressed(buttonB_wasPressed)


screen.set_screen_brightness(0)
while True:
  if (pir_0.state) == 1:
    screen.set_screen_brightness(100)
    speaker.playWAV('アニメ 効果音.wav', volume=1)
    while (pir_0.state) == 1:
      screen.set_screen_bg_color(0xff6666)
      wait(0.5)
      screen.set_screen_bg_color(0xff9966)
      wait(0.5)
      screen.set_screen_bg_color(0xffff66)
      wait(0.5)
      screen.set_screen_bg_color(0xffff33)
      wait(0.5)
      screen.set_screen_bg_color(0x66ff99)
      wait(0.5)
      screen.set_screen_bg_color(0x33ffff)
      wait(0.5)
      screen.set_screen_bg_color(0x66ffff)
      wait(0.5)
      screen.set_screen_bg_color(0x9999ff)
      wait(0.5)
      screen.set_screen_bg_color(0xff99ff)
      wait(0.5)
  else:
    screen.set_screen_brightness(0)
  wait_ms(2)
