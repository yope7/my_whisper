import sounddevice as sd
import numpy as np
import whisper
import queue
import threading
import time
import argparse

# コマンドライン引数の解析
parser = argparse.ArgumentParser(description='音声のリアルタイム文字起こし')
parser.add_argument('--lang', type=str, default='ja', choices=['ja', 'en'], 
                    help='文字起こしの言語（ja: 日本語, en: 英語）')
args = parser.parse_args()

# Whisperモデルの読み込み
model = whisper.load_model("small")

# 入力デバイス選択
def select_input_device():
    devices = sd.query_devices()
    input_devices = []
    
    print("利用可能な入力デバイス:")
    for i, device in enumerate(devices):
        if device['max_input_channels'] > 0:  # 入力チャンネルがあるデバイスのみ
            input_devices.append(device)
            print(f"[{len(input_devices)-1}] {device['name']}")
    
    if not input_devices:
        print("入力デバイスが見つかりません。")
        exit(1)
    
    while True:
        try:
            selection = int(input(f"使用する入力デバイスの番号を選択してください (0-{len(input_devices)-1}): "))
            if 0 <= selection < len(input_devices):
                return input_devices[selection]['name']
            else:
                print(f"0から{len(input_devices)-1}までの番号を入力してください。")
        except ValueError:
            print("数字を入力してください。")

# デバイス設定
samplerate = 16000
block_duration = 15  # 何秒ごとに文字起こしするか
device_name = select_input_device()
print(f"選択されたデバイス: {device_name}")

# 録音データ用キュー
q = queue.Queue()

# コールバック関数
def callback(indata, frames, time_info, status):
    if status:
        print("Status:", status)
    q.put(indata.copy())

# 音声取得と文字起こし
def transcribe_audio():
    buffer = np.empty((0, 1), dtype=np.float32)
    with sd.InputStream(samplerate=samplerate, channels=1, dtype='float32',
                        device=device_name, callback=callback):
        print(f"文字起こし開始（言語: {args.lang}）")
        while True:
            try:
                # 音声データを収集
                block = q.get()
                buffer = np.append(buffer, block, axis=0)

                # 指定時間分たまったら処理
                if len(buffer) >= samplerate * block_duration:
                    audio_chunk = buffer[:samplerate * block_duration]
                    buffer = buffer[samplerate * block_duration:]

                    # Whisperで文字起こし
                    result = model.transcribe(audio_chunk.flatten(), language=args.lang, fp16=False)
                    print(f"{result['text']}")

            except KeyboardInterrupt:
                print("\n停止します。")
                break

# 実行
transcribe_thread = threading.Thread(target=transcribe_audio)
transcribe_thread.start()

