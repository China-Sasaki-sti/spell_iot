import socket
import xml.etree.ElementTree as ET

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 10500))

def main():
    try:
        data = ''
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
                        elif command == u'ルーモスマキシマ':
                            print('【ツヨメノデンキツケル】')
                    print('\n')  # 改行
                    data = ''
            else:
                data = data + client.recv(1024).decode('utf-8')  # バイト列を文字列に変更してから連結
    except KeyboardInterrupt:
        clliant.close()

# If run this script directly, do:
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        cliant.close()
