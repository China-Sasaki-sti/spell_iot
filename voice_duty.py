import socket
import xml.etree.ElementTree as ET
import RPi.GPIO as GPIO
import time

PWM = 17
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 10500))

def setup():
    # Set the GPIO modes to BCM Numbering
    GPIO.setmode(GPIO.BCM)
    # Set LedPin's mode to output, and initial level to High(3.3v)
    GPIO.setup(PWM, GPIO.OUT)

def main():
    data = ''
    pwm = GPIO.PWM(PWM,1000)
    pwm.start(0)
    while True:
        if '</RECOGOUT>\n.' in data:
            root = ET.fromstring('<?xml version="1.0"?>\n' + data[data.find('<RECOGOUT>'):].replace('\n.', ''))
            for whypo in root.findall('./SHYPO/WHYPO'):
                command = whypo.get('WORD')
                score = float(whypo.get('CM'))
                # 認識された単語と点数を表示
                print(command + ':' + str(score))
                # 0.9以上の場合、認識と表示
                if score >= 0.9:
                    if command == u'ウィンガーディアムレビオーサ':
                        print('【モノガウク】')
                    elif command == u'ルーモス':
                        print('【デンキツケル】')
                        pwm.ChangeDutyCycle(40)
                        time.sleep(4)
                        pwm.ChangeDutyCycle(0)
                    elif command == u'ルーモスマキシマ':
                        print('【ツヨメノデンキツケル】')
                        pwm.ChangeDutyCycle(80)
                        time.sleep(4)
                        pwm.ChangeDutyCycle(0)
                print('\n')  # 改行
                data = ''
        else:
            data = data + client.recv(1024).decode('utf-8')  # バイト列を文字列に変更してから連結

# Define a destroy function for clean up everything after the script finished
def destroy():
    # Release resource
    GPIO.cleanup()

# If run this script directly, do:
if __name__ == '__main__':
    setup()
    try:
        main()
    except KeyboardInterrupt:
        destroy()

