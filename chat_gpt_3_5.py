import os

import openai

import config

os.environ["http_proxy"] = config.http_proxy
os.environ["https_proxy"] = config.https_proxy

#  https://platform.openai.com/docs/guides/chat
# 需要升级到0.27.0版本的openai，最好用比较新的Python版本，3.6的版本是找不到0.27版本的

# 获取API密钥
with open(config.openai_key_path, "r") as f:
    openai.api_key = f.readline()

origin_messages = [
    {"role": "system", "content": config.chat_role},
]

question = {"role": "user", "content": ""}


def get_chat_result(message):
    return openai.ChatCompletion.create(
        model=config.chatgpt_model,
        messages=message
    )


if __name__ == '__main__':
    q = "你好"
    rsp = get_chat_result(q)
    content = rsp["choices"][0]["message"]["content"]
    print(content)
