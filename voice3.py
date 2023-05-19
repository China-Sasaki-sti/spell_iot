import socket
import xml.etree.ElementTree as ET
import RPi.GPIO as GPIO
import time

LedPin = 17
ServoPin = 18
SERVO_MIN_PULSE = 500
SERVO_MAX_PULSE = 2500
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 10500))

def map(value, inMin, inMax, outMin, outMax):
    return (outMax - outMin) * (value - inMin) / (inMax - inMin) + outMin

def led_setup():
    # Set the GPIO modes to BCM Numbering
    GPIO.setmode(GPIO.BCM)
    # Set LedPin's mode to output, and initial level to High(3.3v)
    GPIO.setup(LedPin, GPIO.OUT)

def servo_setup():
    global p
    GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by BCM
    GPIO.setup(ServoPin, GPIO.OUT)   # Set ServoPin's mode is output
    GPIO.output(ServoPin, GPIO.LOW)  # Set ServoPin to low
    p = GPIO.PWM(ServoPin, 50)     # set Frequecy to 50Hz
    p.start(0)                     # Duty Cycle = 0

def setAngle(angle):      # make the servo rotate to specific angle (0-180 degr>
    angle = max(0, min(180, angle))
    pulse_width = map(angle, 0, 180, SERVO_MIN_PULSE, SERVO_MAX_PULSE)
    pwm = map(pulse_width, 0, 20000, 0, 100)
    p.ChangeDutyCycle(pwm)#map the angle to duty cycle and output it

def main():
    data = ''
    led=GPIO.PWM(LedPin,1000)
    led.start(100)
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
                        for i in range(0, 181, 5):   #make servo rotate from 0 to 180 deg
                            setAngle(i)     # Write to servo
                            time.sleep(0.002)
                        time.sleep(4)
                        for i in range(180, -1, -5): #make servo rotate from 180 to 0 deg
                            setAngle(i)
                            time.sleep(0.001)
                    elif command == u'ルーモス':
                        print('【デンキツケル】')
                        led.ChangeDutyCycle(90)
                        time.sleep(3)
                        led.ChangeDutyCycle(100)
                    elif command == u'ルーモスマキシマ':
                        print('【ツヨメノデンキツケル】')
                        led.ChangeDutyCycle(10)
                        time.sleep(3)
                        led.ChangeDutyCycle(100)
                print('認識準備OK\n')  # 処理の終了を報告
                data = ''
        else:
            data = data + client.recv(1024).decode('utf-8')  # バイト列を文字列に変更してから連結

# Define a destroy function for clean up everything after the script finished
def destroy():
    # Release resource
    GPIO.cleanup()

# If run this script directly, do:
if __name__ == '__main__':
    led_setup()
    servo_setup()
    try:
        main()
    except KeyboardInterrupt:
        destroy()

