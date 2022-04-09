import random
import signal

import requests
import traceback
import snowboydecoder
from speech import speech_get_word, word_get_speech, play_music

interrupted = False
model = "model/小雪.pmdl"  # https://snowboy.hahack.com/


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)


def handle_voice():
    # 录音并识别出录音结果
    word = speech_get_word()
    # 根据录音结果做出动作
    if word is None:
        play_music("resources/语音识别失败.mp3")
    elif '开灯'.encode() in word:
        requests.get("http://192.168.31.152/on")
        word_get_speech('已开灯')
    elif '关灯'.encode() in word:
        requests.get("http://192.168.31.152/off")
        word_get_speech('已关灯')
    elif '开客厅的灯'.encode() in word:
        requests.get("http://192.168.31.142/on")
        word_get_speech('已开客厅的灯')
    elif '关客厅的灯'.encode() in word:
        requests.get("http://192.168.31.142/off")
        word_get_speech('已关客厅的灯')


def callback():
    # 播放唤醒词
    # play_music(random.choice(["resources/你好.mp3", "resources/在呢.mp3"]))
    play_music(random.choice(["resources/ding.wav"]))

    # 唤醒之后先关掉监听
    detector.terminate()
    # 录音加后续的动作
    handle_voice()
    # 处理完之后再开启监听
    listening()


def listening():
    # main loop
    print('Listening... Press Ctrl+C to exit')
    detector.start(detected_callback=callback,
                   interrupt_check=interrupt_callback,
                   sleep_time=0.03)
    detector.terminate()


if __name__ == '__main__':
    try:
        listening()
    except Exception as e:
        listening()
        traceback.print_exc()

