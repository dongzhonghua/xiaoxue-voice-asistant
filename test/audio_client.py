# -*- coding: utf-8 -*-
# create time    : 2021-01-06 15:52
# author  : CY
# file    : voice_client.py
# modify time:
import socket

import pyaudio


class Client:
    def __init__(self):
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while 1:
            try:
                self.target_ip = '192.168.31.56'
                self.target_port = 9808

                self.socket_client.connect((self.target_ip, self.target_port))
                break
            except:
                print("Couldn't connect to server")

        chunk_size = 1024  # 512
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000

        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True,
                                          frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True,
                                            frames_per_buffer=chunk_size)

        print("Connected to Server")

        # start threads
        # receive_thread = threading.Thread(target=self.receive_server_data).start()
        self.send_data_to_server()

    def receive_server_data(self):
        while True:
            try:
                data = self.socket_client.recv(1024)
                print("client recv data: {}".format(len(data)))
                self.playing_stream.write(data)
            except:
                pass

    def send_data_to_server(self):
        while True:
            try:
                data = self.recording_stream.read(1024)
                print("client send data: {}".format(len(data)))
                self.socket_client.sendall(data)
            except:
                pass


if __name__ == '__main__':
    client = Client()
