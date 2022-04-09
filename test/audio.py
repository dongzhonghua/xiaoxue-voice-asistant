import datetime
import wave

import numpy as np
import pyaudio


def listen():
    temp = 20  # temp为检测声音值
    channels = 1
    rate = 16000
    wave_output_filename = 'test.wav'
    chunk = 1024
    audio_format = pyaudio.paInt16
    p = pyaudio.PyAudio()
    stream = p.open(format=audio_format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)
    print("录音开始")

    frames = []
    stat = True  # 一重判断
    stat2 = False  # 二重判断
    stat3 = False  # 三重判断
    temp_num = 0  # temp_num、temp_num2、temp_num3为时间，每31.25为两秒钟
    temp_num2 = 0
    temp_num3 = 0
    while stat:
        data = stream.read(chunk, exception_on_overflow=False)  # 每次读取1024个采样，一共2048个字节
        print(len(data))
        frames.append(data)
        audio_data = np.frombuffer(data, dtype=np.short)
        temp = np.max(audio_data)
        if temp_num > 30:
            if temp < 1000 and not stat2:
                stat2 = True
                temp_num2 = temp_num
                print("xxxxxxxxxxxxxxxxx", datetime.datetime.now())
            if temp_num > temp_num2 + 5:
                print("yyyyyyyyyyyyyyyyy", datetime.datetime.now())
                if stat2 and temp < 1000:
                    stat3 = True
                else:
                    temp_num3 = temp_num
                    print("zzzzzzzzzzzz", datetime.datetime.now())
                    stat2 = False
            if temp_num > temp_num3 + 5:
                print("sssssssssssss", datetime.datetime.now())
                if stat2 and stat3 and temp < 1000:
                    stat = False
                else:
                    temp_num3 = temp_num
                    print("zzzzzzzzzzzz", datetime.datetime.now())
                    stat3 = False
        print(str(temp) + "      " + str(temp_num), datetime.datetime.now())
        temp_num = temp_num + 1
        if temp_num > 150:  # 超时直接退出
            stat = False
    print("录音结束")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(wave_output_filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(audio_format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()





if __name__ == '__main__':
    listen()
