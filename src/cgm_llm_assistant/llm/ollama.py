import logging

import ollama

logger = logging.getLogger(__name__)


def explain_metrics(context: dict, question: str, model: str) -> str:
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


def check_model(model: str) -> bool:
    """
    Check if the requested model is available.
    Returns True if model is found, False otherwise.
    """
    try:
        models = ollama.list()
        model_names = [
            m.get("name", "").split(":")[0] for m in models.get("models", [])
        ]
        available = [m.get("name", "") for m in models.get("models", [])]
        return model in available or model.split(":")[0] in model_names
    except Exception as e:
        logger.exception("Failed to list models")
        raise RuntimeError("Failed to list models. Is Ollama running?") from e
