import numpy as np
import pyaudio


# 定义函数，用于计算声音的能量
def get_audio_energy(audio):
    data = np.fromstring(audio, dtype=np.int16) / 32767.0  # 将二进制的声音数据转换为浮点数
    energy = np.sum(data ** 2) / len(data)  # 计算平均能量
    return energy


# 定义一个回调函数，在录音过程中实时获取声音数据进行处理
def callback(input_data, frame_count, time_info, status):
    if get_audio_energy(input_data) > 0.01:  # 如果声音能量大于0.01，则说明可能有人在说话，可以继续录音
        frames.append(input_data)
        return (input_data, pyaudio.paContinue)
    else:  # 否则，停止录音
        return (input_data, pyaudio.paComplete)


# 初始化PyAudio
p = pyaudio.PyAudio()
frames = []
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                stream_callback=callback)

# 启动录音
stream.start_stream()

# 监测是否录音结束
while stream.is_active():
    input()

# 停止录音
stream.stop_stream()
stream.close()
p.terminate()

# 将获取到的声音数据进行存储、处理等操作
