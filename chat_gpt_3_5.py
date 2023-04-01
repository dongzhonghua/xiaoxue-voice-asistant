import os
import time
from collections import deque
from collections import namedtuple

import openai

import config

os.environ["http_proxy"] = config.global_config.get_https_proxy()
os.environ["https_proxy"] = config.global_config.get_https_proxy()

#  https://platform.openai.com/docs/guides/chat
# 需要升级到0.27.0版本的openai，最好用比较新的Python版本，3.6的版本是找不到0.27版本的

# 获取API密钥
with open(config.global_config.get_openai_key_path(), "r") as f:
    openai.api_key = f.readline().strip('\n')

OneMessage = namedtuple('OneMessage', ['time', 'q', 'a'])
user_messages: deque[OneMessage] = deque(maxlen=int(config.global_config.get_chatgpt_chat_rounds()))

system = {"role": "system", "content": config.global_config.get_chat_role()}


def get_messages(message):
    res = [system]
    for one_message in user_messages:
        if time.time() - one_message.time < config.global_config.get_chatgpt_chat_save_times() * 60:
            res.append(one_message.q)
            res.append(one_message.a)
    question = {"role": "user", "content": message}
    res.append(question)
    return res, question


def get_chat_result3_5(message):
    if message is None:
        return None
    messages, question = get_messages(message)
    print(messages)
    try:
        response = openai.ChatCompletion.create(model=config.global_config.get_chatgpt_model(),
                                                messages=messages,
                                                timeout=20,
                                                temperature=0.5,
                                                max_tokens=800,
                                                )
    except Exception as e:
        print(e)
        return None
    answer = response["choices"][0]["message"]["content"]
    one_chat_message: OneMessage = OneMessage(time.time(), question, {"role": "assistant", "content": answer})
    user_messages.append(one_chat_message)
    return answer


if __name__ == '__main__':
    rsp = get_chat_result3_5("什么是Python")
    print(rsp)
    rsp = get_chat_result3_5("那他和Java的区别是什么")
    print(rsp)
    rsp = get_chat_result3_5("这两种语言哪个好")
    print(rsp)
