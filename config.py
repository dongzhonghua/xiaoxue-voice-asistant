import configparser
import threading
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class Config(object):
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.read_config()

    def read_config(self):
        with open('config.ini', 'r') as f:
            self.config.read_file(f)

    def get_openai_key_path(self):
        return self.config.get('default', 'openai_key_path')

    def get_baidu_key_path(self):
        return self.config.get('default', 'baidu_key_path')

    def get_https_proxy(self):
        return self.config.get('default', 'https_proxy')

    def get_http_proxy(self):
        return self.config.get('default', 'http_proxy')

    def get_chat_role(self):
        return self.config.get('default', 'chat_role')

    def get_chatgpt_version(self):
        return self.config.get('default', 'chatgpt_version')

    def get_chatgpt_model(self):
        return self.config.get('default', 'chatgpt_model')

    def get_chatgpt_chat_rounds(self):
        return self.config.getint('default', 'chatgpt_chat_rounds')

    def get_chatgpt_chat_save_times(self):
        return self.config.getint('default', 'chatgpt_chat_save_times')


class ConfigHandler(FileSystemEventHandler):
    def __init__(self, config: Config):
        self.config = config

    def on_modified(self, event):
        print("Config file changed")
        self.config.read_config()


def listen_config():
    observer = Observer()
    handler = ConfigHandler(global_config)
    observer.schedule(handler, ".", recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


global_config = Config()

if __name__ == "__main__":
    t1 = threading.Thread(target=listen_config)
    t1.start()
    print(global_config.get_chatgpt_chat_save_times())
    t1.join()
