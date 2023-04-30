def gpt(prompt):
    import openai
    key = "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"
    openai.api_key = key
    result = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        temperature=0.1
    )
    return result["choices"][0]["text"].strip()