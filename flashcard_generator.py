import openai
import json

def generate_flashcards(content, subject="General", model="gpt-3.5-turbo", api_key=""):
    client = openai.OpenAI(api_key=api_key)  # ✅ pass the key here

    prompt = f"""
You are an expert tutor. Convert the following {subject} study material into at least 10 high-quality question-answer flashcards.

TEXT:
\"\"\"
{content}
\"\"\"

Return only the flashcards in JSON format like:
[
  {{
    "question": "What is ...?",
    "answer": "It is ...",
    "topic": "Optional Topic Header"
  }},
  ...
]
"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    raw = response.choices[0].message.content
    try:
        flashcards = json.loads(raw)
    except Exception:
        flashcards = []
    return flashcards
