import os

from openai import OpenAI

def get_client(api_key=None, base_url=None):
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "Missing OpenAI API key. Set the OPENAI_API_KEY environment variable."
        )
    client_kwargs = {"api_key": api_key}
    if base_url:
        client_kwargs["base_url"] = base_url
    return OpenAI(**client_kwargs)


def analyze_log(log, api_key=None, base_url=None, model="gpt-4o-mini"):
    prompt = f"""
    Analyze this test failure log and give:
    1. Root cause
    2. Suggested fix

    Answer in 2 bullet points. Keep it under 100 words.
    If the input is not an API error log, respond only with: Provide correct log.

    Log:
    {log}
    """

    client = get_client(api_key, base_url)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )

    return response.choices[0].message.content
