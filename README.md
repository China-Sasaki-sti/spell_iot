# spell_iot
ハリーポッターの呪文を使えるようにするためのプログラムです。

## 事前準備
ブレッドボードの接続を行う
- LED
  - GPIO17 - LEDアノード(長い方) - LEDカソード(短い方) - 抵抗(220Ω) - 3V3
- サーボ
  - オレンジ GPIO18
  - 黒 GND
  - 赤 3V3

## 実行と遊び方
ターミナル1で以下を実行し音声認識を開始
```
julius -C voice.jconf -charconv EUC-JP UTF-8 -module
```
ターミナル2で以下を実行しプログラムを開始
```
python3 voice3.py 
```
**使用可能な呪文**
- ルーモス
- ルーモスマキシマ
- ウィンガ―ディアムレビオ―サ

※呪文が読み込まれて処理を行っている間に新たな呪文を認識してしまうとエラーが出ます。なぜなら、このプログラムでは呪文が読み込まれた後の処理を行っていない間だけ、受信したデータをUTFエンコーディングして既存のデータに連結する処理を行っているためです。エラーが出た場合は再度実行してください。
