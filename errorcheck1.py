from m5stack import *
from m5stack_ui import *
from uiflow import *
import wifiCfg
import time
import urequests
import json
import unit

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0x9dffa5)

# PIR
pir_0 = unit.get(unit.PIR, unit.PORTB)

# Labels
lbl_result = M5Label("...", x=10, y=10, color=0x000, font=FONT_MONT_20)
lbl_now = M5Label("...", x=10, y=60, color=0x000, font=FONT_MONT_30)
lbl_wifi = M5Label("WiFi:", x=10, y=120, color=0x000, font=FONT_MONT_20)
lbl_debug = M5Label("Debug", x=10, y=180, color=0x000, font=FONT_MONT_18)

num = 0

#-------------------------
# WiFi 接続
#-------------------------
wifiCfg.doConnect("SSID", "PASSWORD")  # ← 自分のSSIDとパスワードに変更
while not wifiCfg.wlan_sta.isconnected():
    lbl_wifi.set_text("WiFi: Connecting...")
    wait(1)

lbl_wifi.set_text("WiFi: Connected")

#-------------------------
# メインループ
#-------------------------
while True:

    lbl_now.set_text("Zzz...")

    if pir_0.state == 1:

        num += 1  # カウント
        direction = "In" if num % 2 == 1 else "Out"

        lbl_now.set_text(direction)

        #-------------------------
        # 送信デバッグ開始
        #-------------------------
        lbl_result.set_text("Sending...")
        lbl_debug.set_text("Before request")

        try:
            url = "https://46la4d7sd0.execute-api.ap-northeast-1.amazonaws.com/dev2"
            payload = {
                "url": "https://script.google.com/macros/s/AKfycbzbLIpgiaSA62W8TvUHNagEFbnl5IsYfJ5pAD1hvX22FFmVtWqwt6Z54Q_NkmGJuIuC9w/exec",
                "data": num
            }

            req = urequests.post(url, json=payload)

            lbl_debug.set_text("After request")

            # ステータスチェック
            lbl_result.set_text("HTTP: " + str(req.status_code))

            # レスポンス表示
            try:
                res = req.text
                lbl_debug.set_text(res[0:30])  # 長い時は先頭だけ表示
            except:
                lbl_debug.set_text("No response body")

            req.close()

        except Exception as e:
            lbl_result.set_text("Error")
            lbl_debug.set_text(str(e))

        wait(6)
    wait_ms(10)
