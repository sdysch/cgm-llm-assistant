import logging

import ollama

logger = logging.getLogger(__name__)


def explain_metrics(context: dict, question: str, model: str) -> str:
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
        stream=True,
    )

    full_response = ""
    # Stream response
    for chunk in response:
        content = chunk["message"]["content"]
        print(content, end="", flush=True)
        full_response += content
    print()
    return full_response


def check_ollama():
    """
    Check if ollama is running
    """
    try:
        ollama.list()
    except Exception as e:
        logger.exception("Ollama is not running")
        raise RuntimeError(
            "Ollama is not running. Start it with `ollama serve`."
        ) from e


def check_model(model: str) -> bool:
    """
    Check if the requested model is available.
    Returns True if model is found, False otherwise.
    """
    try:
        models = ollama.list()
        model_names = [m.model.split(":")[0] for m in models.models]
        available = [m.model for m in models.models]
        return model in available or model.split(":")[0] in model_names
    except Exception as e:
        logger.exception("Failed to list models")
        raise RuntimeError("Failed to list models. Is Ollama running?") from e
