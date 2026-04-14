from m5stack_ui import *
from uiflow import *
import network
import time
import urequests
import json
import unit


screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0x2f4f4f)
pir_0 = unit.get(unit.PIR, unit.PORTB)

num = None

result = M5Label('report', x=14, y=17, color=0x000, font=FONT_MONT_30, parent=None)
now = M5Label('Zzz...', x=120, y=100, color=0x000, font=FONT_MONT_38, parent=None)
wifi = M5Label('wifi', x=261, y=20, color=0x000, font=FONT_MONT_22, parent=None)

from numbers import Number

# === Wi-Fi接続 ===
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('SSID', 'PASSWORD')  # ← 自分のSSIDとパスワードに変更

while not wlan.isconnected():
  wifi.set_text('not yet')
  time.sleep(1)

wifi.set_text('OK!')

num = 0
while True:
  now.set_text('Zzz...')
  if (pir_0.state) == 1:
    screen.set_screen_bg_color(0x9dffa5)
    num = (num if isinstance(num, Number) else 0) + 1
    result.set_text('reported')
    if num % 2 == 1:
      now.set_text('In')
    else:
      now.set_text('Out')
    wait(5)
    screen.set_screen_bg_color(0x2f4f4f)
    result.set_text('report')
  wait_ms(2)
