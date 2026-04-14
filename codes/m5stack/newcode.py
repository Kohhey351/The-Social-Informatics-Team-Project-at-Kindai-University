from m5stack import *
from m5stack_ui import *
from uiflow import *
import wifiCfg
import urequests
import time
import unit

# === 画面初期化 ===
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0x95e728)

title_label = M5Label('PIR Sensor → Firebase', x=10, y=10, color=0x000, font=FONT_MONT_18, parent=None)
status_label = M5Label('Wi-Fi connecting...', x=10, y=40, color=0x000, font=FONT_MONT_22, parent=None)
result_label = M5Label('', x=10, y=80, color=0x000, font=FONT_MONT_30, parent=None)

# === Wi-Fi接続 ===
wifiCfg.doConnect('SSID', 'PASSWORD')  # ← 自分のSSIDとパスワードに変更
status_label.set_text('Wi-Fi Connected')

# === PIRユニット接続 (Port B = 26, 36) ===
pir = unit.get(unit.PIR, unit.PORTB)

# === FirebaseのURL設定 ===
FCM_URL = 'https://YOUR_FIREBASE_FUNCTION_URL'  # ← 自分のFirebase URLに変更

# === 状態管理用変数 ===
last_status = 0

# === メインループ ===
while True:
    current_status = pir.state  # 0: 検知なし, 1: 検知あり

    if current_status != last_status:
        last_status = current_status

        if current_status == 1:
            json_data = '{"detected": true}'
            status_label.set_text('Motion detected!')
        else:
            json_data = '{"detected": false}'
            status_label.set_text('No motion')

        try:
            headers = {'Content-Type': 'application/json'}
            response = urequests.post(FCM_URL, data=json_data, headers=headers)
            
            # === 成功時 ===
            if response.status_code == 200:
                result_label.set_text_color(0xff0000)  # 緑
                result_label.set_text('OK!')
            else:
                result_label.set_text_color(0xff0000)  # 赤
                result_label.set_text('NG!')
            response.close()

        except Exception as e:
            print('Error:', e)
            result_label.set_text_color(0xff0000)
            result_label.set_text('NG!')

    time.sleep(1)
