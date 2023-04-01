import json

with open("config.json", "r") as f:
    config = json.load(f)

openai_key_path = config.get("openai_key_path")
baidu_key_path = config.get("baidu_key_path")
https_proxy = config.get("https_proxy")
http_proxy = config.get("http_proxy")
chatgpt_version = config.get("chatgpt_version")
chatgpt_model = config.get("chatgpt_model")
chat_role = config.get("chat_role")
chatgpt_chat_rounds = config.get("chatgpt_chat_rounds")
chatgpt_chat_save_times = config.get("chatgpt_chat_save_times")
