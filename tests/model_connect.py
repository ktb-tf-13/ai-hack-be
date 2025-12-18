from openai import OpenAI

# Ngrok 주소 사용 (위에서 생성된 public_url)
public_url = "https://unresumed-maya-hyperaccurately.ngrok-free.dev"
model_name = "Qwen/Qwen2.5-32B-Instruct-AWQ"

client = OpenAI(
    base_url=f"{public_url}/v1",
    api_key="EMPTY"
)

# 대화 요청
completion = client.chat.completions.create(
    model=model_name,
    messages=[
        {"role": "system", "content": "당신은 친절한 한국어 AI 비서입니다."},
        {"role": "user", "content": "애국가 가사를 알려줘"}
    ],
    temperature=0.7
)

print("🤖 답변 결과:")
print(completion.choices[0].message.content)