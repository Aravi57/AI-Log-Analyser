import os

from openai import OpenAI


def get_client(api_key=None):
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "Missing OpenAI API key. Set the OPENAI_API_KEY environment variable."
        )
    return OpenAI(api_key=api_key)


def analyze_log(log, api_key=None):
    prompt = f"""
    Analyze this test failure log and give:
    1. Root cause
    2. Suggested fix
    3. Key next step

    Answer in 3 bullet points. Keep it under 100 words.
    If the input is not an API error log, respond only with: Provide correct log.

    Log:
    {log}
    """

    client = get_client(api_key)
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )

    return response.choices[0].message.content


def read_log_from_user():
    log = input("Paste the log and press Enter: ").strip()
    if not log:
        raise ValueError("No log content provided.")
    return log


def main():
    try:
        log = read_log_from_user()
        print("\nAnalyzing log...\n")
        result = analyze_log(log)
        print("Analysis result:\n")
        print(result)
    except Exception as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()
