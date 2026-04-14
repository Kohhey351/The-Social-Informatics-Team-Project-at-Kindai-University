from m5stack import *
from m5stack_ui import *
from uiflow import *
import urequests
import time
import unit
import network

# === 画面初期化 ===
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0x95e728)

title_label = M5Label('PIR Sensor → Firebase', x=10, y=10, color=0x000, font=FONT_MONT_18, parent=None)
status_label = M5Label('Wi-Fi connecting...', x=10, y=40, color=0x000, font=FONT_MONT_22, parent=None)
result_label = M5Label('', x=10, y=80, color=0x000, font=FONT_MONT_30, parent=None)

# === Wi-Fi接続 ===
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('SSID', 'PASSWORD')

while not wlan.isconnected():
    time.sleep(1)

status_label.set_text('Wi-Fi Connected')

# === PIRユニット接続 ===
pir = unit.get(unit.PIR, unit.PORTB)

# === Firebase URL ===
FCM_URL = 'https://us-central1-rwc25-group10.cloudfunctions.net/updateSensorStatus/'

# === 状態管理 ===
last_status = -1

# === メインループ ===
while True:
    current_status = pir.state  # 0 or 1

    if current_status != last_status:
        last_status = current_status

        if current_status == 1:
            status_label.set_text('Motion detected!')
        else:
            status_label.set_text('No motion')

        try:
            json_data = {"detected": bool(current_status)}
            response = urequests.post(FCM_URL, json=json_data)

            print('status:', response.status_code)
            print('body:', response.text)

            if response.status_code == 200:
                result_label.set_text_color(0x00ff00)
                result_label.set_text('OK!')
            else:
                result_label.set_text_color(0xff0000)
                result_label.set_text('NG!')

            response.close()

        except Exception as e:
            print('Error:', e)
            result_label.set_text_color(0xff0000)
            result_label.set_text('NG!')

    time.sleep(1)
