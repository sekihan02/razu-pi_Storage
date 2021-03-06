# coding:utf-8
#!/usr/bin/python
# usbカメラの映像表示
# ADRPTB8Cでラジコン戦車操作
# コマンド　python rc_cam.py

# Rasberry-pi
from Adafruit_MotorHAT import Adafruit_MotorHAT
from time import sleep
import atexit
import Adafruit_PCA9685

import cv2
import time

'''
モーター初期化処理
'''
# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x70)
myMotor1 = mh.getMotor(1)           # 一つ目のモータの設定
myMotor2 = mh.getMotor(2)           # 二つ目のモータの設定

'''
移動関数 : RCの移動方向と速度をセット
引数 : 移動設定
'''
def motor(direction):
    # direction = 0 前進
    # direction = 1 後進
    # direction = 2 右回転
    # direction = 3 左回転
    # direction = 4 停止
    # run()動作開始
    # setSpeed()モーター速度　制限0~255
    if direction == 0:
        myMotor1.run(Adafruit_MotorHAT.FORWARD)
        myMotor2.run(Adafruit_MotorHAT.FORWARD)
        myMotor1.setSpeed(130)
        myMotor2.setSpeed(130)
        sleep(0.5)

    elif direction == 1:
        myMotor1.run(Adafruit_MotorHAT.BACKWARD)
        myMotor2.run(Adafruit_MotorHAT.BACKWARD)
        myMotor1.setSpeed(130)
        myMotor2.setSpeed(130)
        sleep(0.5)

    elif direction == 2:
        myMotor1.run(Adafruit_MotorHAT.FORWARD)
        myMotor2.run(Adafruit_MotorHAT.BACKWARD)
        myMotor1.setSpeed(130)
        myMotor2.setSpeed(130)
        sleep(0.5)

    elif direction == 3:
        myMotor1.run(Adafruit_MotorHAT.BACKWARD)
        myMotor2.run(Adafruit_MotorHAT.FORWARD)
        myMotor1.setSpeed(130)
        myMotor2.setSpeed(130)
        sleep(0.5)

    elif direction == 4:
        print ("Release")
        myMotor1.run(Adafruit_MotorHAT.RELEASE)
        myMotor2.run(Adafruit_MotorHAT.RELEASE)
        sleep(0.1)

# 顔認識用のファイル
FACE_CASCADE = './haarcascades/haarcascade_frontalface_alt.xml'     # 顔
# EYE_CASCADE = './haarcascades/haarcascade_frontalface_alt.xml'     # 目

# 認識時に小さい画像は認識しない
MIN_SIZE = (150, 150)

Cascade = cv2.CascadeClassifier(FACE_CASCADE)               # 顔認識用の分類器の生成
capture = cv2.VideoCapture(0)                               # カメラセット

# 画像サイズの指定(指定する場合にのみ使う)
# ret = capture.set(3, 480)
# ret = capture.set(4, 320)

i = 0

try:
    while True:
        # キー入力
        # getch = _Getch()
        # key = getch()
        key = cv2.waitKey(1) & 0xFF                             # キー入力待ち１ms

        # ラジコン移動
        if key == ord('w'):
            # 前進
            motor(0)
            # motor(4)
            key = ''
        elif key == ord('z'):
            # 後進
            motor(1)
            # motor(4)
            key = ''
        elif key == ord('d'):
            # 右
            motor(2)
            # motor(4)
            key = ''
        elif key == ord('a'):
            # 左
            motor(3)
            key = ''
        # 's'が押されたら保存
        elif key == ord('s'):
            cv2.imwrite(str(i)+'.jpg',image)
            i += 1
            print('Save Image...' + str(i) + '.jpg')
            key = ''
        # 'q'が押されたら終了
        elif key == ord('q'):
            capture.release()
            cv2.destroyAllWindows()
            key = ''
            break
        else:
            # 停止
            motor(4)
            key = ''
        

        start = time.clock()                                    # 開始時刻
        # 画面指定の時のカメラの画像
        # ret, image = capture.read()

        _, image = capture.read()                               # カメラの画像
        # グレースケールに変換
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 顔検出
        faces = Cascade.detectMultiScale(gray, minSize=MIN_SIZE)
        # 認識
        # faces = Cascade.detectMultiScale(gray_image, scaleFactor=1.3, minNeighbors=2, minSize=MIN_SIZE)

        # key = cv2.waitKey(1) & 0xFF                             # キー入力待ち１ms

        if len(faces) > 0:
            # 検出した顔に枠を書く
            for (x, y, w, h) in faces:
                # 見つかった顔を矩形で囲む
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), thickness=8)
                
                # 認識した時の画像を保存
                # cv2.imwrite(str(i)+'.jpg',image)
                # i += 1
                # print('Save Image...' + str(i) + '.jpg')
                # print('認識しました')
                # time.sleep(3)           # 連続で認識しないように待機
                # continue               # 待機だと重いのでこっちのほうが良い？sleepnないときと変わらん

        # 映像処理
        get_image_time = int((time.clock()-start) * 1000)         # 処理時間計測
        # 1フレーム取得するのにかかった時間を表示
        cv2.putText(image, str(get_image_time) + 'ms', (10,10), 1, 1, (0,0,0))
        
        cv2.imshow('USB_Camera Test',image)
except KeyboardInterrupt:
    # キャプチャの後始末と，ウィンドウをすべて消す
    capture.release()
    cv2.destroyAllWindows()

    myMotor1.run(Adafruit_MotorHAT.RELEASE)
    myMotor2.run(Adafruit_MotorHAT.RELEASE)
    
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()

    capture.release()
    cv2.destroyAllWindows()
