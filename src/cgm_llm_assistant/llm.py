import ollama


def explain_metrics(context: dict, question: str, model: str = "llama3.2") -> str:
    """
    Send structured CGM context + question to local LLM.
    """
    prompt = f"""
    You are a health assistant analysing continuous glucose monitor data.

    Context:
    {context}

    User question:
    {question}

    Explain patterns clearly and concisely.
    """

    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )

    return response["message"]["content"]
