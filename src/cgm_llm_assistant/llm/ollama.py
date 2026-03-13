import logging

import ollama

logger = logging.getLogger(__name__)


def explain_metrics(context: dict, question: str, model: str = "llama3.2") -> str:
    """
    Send structured CGM context + question to local LLM.
    """
    logger.info(f"Calling LLM with model: {model}")

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
