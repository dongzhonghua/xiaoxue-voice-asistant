import os
import wave

import numpy as np
import pyaudio
from aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = '25905795'
API_KEY = 'pUevsjbFFpoLvZg1bwKw8ALi'
SECRET_KEY = 'jstHVVApR9oz5XKrLKlo6fv8yZG7mOqG'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
speech = 'resources/temp.wav'
audio = 'resources/temp.mp3'


# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def speech_get_word():
    get_speech()
    # 识别本地文件
    asr = client.asr(get_file_content(speech), 'wav', 16000, {'dev_pid': 1537, })
    print(asr)
    if asr['err_msg'] == 'success.':
        return asr["result"][0].encode("utf-8")
    else:
        return None


# https://ai.baidu.com/ai-doc/SPEECH/Gk4nlz8tc
def word_get_speech(word):
    result = client.synthesis(word, 'zh', 3, {
        'vol': 5,
        'per': 103
    })
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open(audio, 'wb') as f:
            f.write(result)
    play_music(audio)


# def get_speech():
#     os.system("rec -c 1 -r 16000 -b 16 resources/audio.wav trim 0 00:03")
# 根据你录音的长短决定，这里更新了录音时间，可长可短，最短2秒，最长7秒，用110/16约等于7秒
# 假如你不说话，2秒钟+1秒判断后识别，假如你说话，最多可以连续7秒钟再识别，很人性化
def get_speech():
    # 最小说话音量
    min_voice = 4000
    # 最大说话音量，+的音量
    max_voice = 28000
    # 录音判断开始时间，前面的时间可能是回复的语音音量过大导致误判断
    # start_sec = 2
    # 录音判断间隔，约等于8/16=0.5秒
    interval = 5
    # 最大录音时间,16*10=160,十秒钟
    max_record_time = 128
    temp = 20  # temp为检测声音值
    chunk = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    # 录音文件输出路径
    WAVE_OUTPUT_FILENAME = speech
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=chunk)
    print("录音开始")

    frames = []
    flag = False  # 一重判断,判断是否已经开始说话，这个判断从第5个数字开始，防止前面数字大于30000的情况
    stat2 = False  # 二重判断,第一次判断声音变小
    stat3 = False  # 三重判断,第二次判断声音变小
    tempnum = 0  # tempnum、tempnum2、tempnum3为时间
    tempnum2 = 0
    tempnum3 = 0
    while True:
        data = stream.read(chunk, exception_on_overflow=False)
        frames.append(data)
        audio_data = np.frombuffer(data, dtype=np.short)
        # 获取录音的音量
        temp = np.max(audio_data)
        # 如果时间大于其实判断时间并且音量在正常范围之内
        if not flag and min_voice < temp < max_voice:
            # 判断出开始说话
            flag = True
        # 如果已经开始说话，那么开始判断
        if flag:
            # 如果声音小于正常范围
            if temp < min_voice:
                # 如果是stat2还是False状态，证明还未开始判断
                if not stat2:
                    # 时间点2和时间点3
                    tempnum2 = tempnum + interval
                    tempnum3 = tempnum + interval
                    # 状态2开始变为True，说明第一次判断开始
                    stat2 = True
                # 开始第二次判断，stat2为True表示已经第一次判断，超过第一次时间段开始第二次判断
                elif stat2 and not stat3 and tempnum > tempnum2:
                    # 已经超过了第一个时间段，那么stat3为True,这是第二次判断
                    stat3 = True
                # stat2和stat3都为True并且超过第二个时间段，这是最后一次判断
                if stat2 and stat3 and tempnum > tempnum3:
                    print("录音完毕")
                    # 跳出循环
                    break
            else:
                # 只要声音变大了，那么就重置状态
                stat2 = False
                stat3 = False
        # 时间约1/16秒每次递增
        tempnum = tempnum + 1
        if tempnum > max_record_time:  # 超时直接退出
            print("录音结束")
            # 跳出循环
            break
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def play_music(path):
    os.system("afplay " + path)  # > /dev/null 2>&1 &


if __name__ == '__main__':
    word_get_speech("语音识别失败")
