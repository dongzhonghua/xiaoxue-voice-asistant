import openai

openai.organization = "org-irLfRXYHIV7TUVtE2I37Lhj4"
# 获取API密钥
with open("openai", "r") as f:
    openai.api_key = f.readline().strip()


def get_chat3_result(prompt: str) -> str:
    if len(prompt) == 0:
        return ""
    model = "text-davinci-003"  # ChatGPT模型
    print("开始请求chatgpt，请稍候...")

    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=800,
        n=1,
        stop=None,
        temperature=0.5,
    )
    summary = response.choices[0].text.strip()
    print("chatgpt返回结果：" + summary)
    return summary


if __name__ == '__main__':
    print(get_chat_result("test"))
