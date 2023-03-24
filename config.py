import json

with open("config.json", "r") as f:
    config = json.load(f)

openai_key_path = config.get("openai_key_path")
baidu_key_path = config.get("baidu_key_path")
https_proxy = config.get("https_proxy")
http_proxy = config.get("http_proxy")
chatgpt_model = config.get("chatgpt_model")
chat_role = config.get("chat_role")
