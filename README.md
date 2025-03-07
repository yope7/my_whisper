# my_whisper

リアルタイム音声文字起こしツール

## 概要

このプロジェクトは、WhisperAI を使用してリアルタイムで音声を文字起こしする Python アプリケーションです。マイクからの入力をリアルタイムで取得し、日本語または英語で文字起こしを行います。

## 機能

- リアルタイム音声入力
- デバイス対応の指定機能
- 日本語・英語の文字起こし対応
- 15 秒ごとの文字起こし処理

## 必要要件

- Python 3.8 以上
- 必要なパッケージ:
  - sounddevice
  - numpy
  - openai-whisper
  - PyAudio

## 使用方法

1. リポジトリをクローン：

```bash
git clone https://github.com/yope7/my_whisper.git
cd my_whisper
```

2. 必要なパッケージをインストール：

```bash
pip install -r requirements.txt
```

3. スクリプトの実行：

```bash
python realtime.py --lang ja  # 日本語の場合
python realtime.py --lang en  # 英語の場合
```

## オプション

- `--lang`: 文字起こしの言語を指定（デフォルト: ja）
  - `ja`: 日本語
  - `en`: 英語

## 注意事項

- 音声入力デバイス（マイク）が必要です
- 処理性能によって文字起こしの遅延が発生する場合があります
- 動かない場合はモデルを変更してみてください
- Whisper モデルの初回実行時にはモデルのダウンロードが必要です

## ライセンス

MIT License

## 謝辞

このプロジェクトは[OpenAI Whisper](https://github.com/openai/whisper)を使用しています。
