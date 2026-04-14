from m5stack_ui import *
from uiflow import *
import wifiCfg
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

wifiCfg.doConnect('SSID', 'PASSWORD')  # ← 自分のSSIDとパスワードに変更
while not (wifiCfg.wlan_sta.isconnected()):
  wait(2)
wifi.set_text('OK!')

num = 0

while True:
  now.set_text('Zzz...')
  if (pir_0.state) == 1:
    screen.set_screen_bg_color(0x9dffa5)
    num = (num if isinstance(num, Number) else 0) + 1
    try:
      req = urequests.request(method='POST', url='https://46la4d7sd0.execute-api.ap-northeast-1.amazonaws.com/dev2',json={'url':'https://script.google.com/macros/s/AKfycby5gmHnU8041FnB4jO9qjaaMwm1X4nJNO2BVuNG3gSz9pfVfzUoWquYEEbWwxywJ7yslg/exec','data':num}, headers={})
      result.set_text(str(json.loads((req.text))))
      gc.collect()
      req.close()
    except:
      result.set_text('Failure')
    if num % 2 == 1:
      now.set_text('In')
    else:
      now.set_text('Out')
    wait(5)
    screen.set_screen_bg_color(0x2f4f4f)
    result.set_text('report')
  wait_ms(2)
