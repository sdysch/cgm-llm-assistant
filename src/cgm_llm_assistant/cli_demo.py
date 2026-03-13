import click
import logging
import ollama

from cgm_llm_assistant.processing import load_cgm_csv
from cgm_llm_assistant.context import build_context
from cgm_llm_assistant.llm import check_model, explain_metrics

logger = logging.getLogger(__name__)


logger = logging.getLogger("cgm_llm_assistant")


@click.command()
@click.argument("file")
@click.option("--model", default="phi3:mini", help="Model to use for inference")
def main(file, model):
    try:
        model_available = check_model(model)
    except Exception as e:
        logger.exception("Error checking model")
        try:
            models_list = ollama.list()
            available = [m.model for m in models_list.models]
        except Exception:
            available = []
        logger.error(f"Available models: {available}")
        raise click.ClickException(f"Error checking model: {e}")

    if not model_available:
        try:
            models_list = ollama.list()
            available = [m.model for m in models_list.models]
        except Exception:
            logger.exception("Failed to list available models")
            available = []
        try:
            raise RuntimeError(
                f"Model '{model}' not found, install with 'ollama pull {model}'"
            )
        except RuntimeError:
            logger.exception("Exiting due to missing model")
            raise

    logger.info(f"Using model: {model}")

    df = load_cgm_csv(file)

    if df.shape[0] == 0:
        logger.warning("No records to process, exiting")
        click.echo(
            click.style("No valid CGM records found in file, exiting.", fg="yellow")
        )
        return

    context = build_context(df)

    click.echo(
        click.style(
            "CGM assistant ready. Type questions (or 'exit'):", fg="cyan", bold=True
        )
    )

    while True:
        question = click.prompt("\n>", type=str, prompt_suffix="")
        if question.lower() in {"exit", "quit"}:
            break
        answer = explain_metrics(context, question, model=model)
        click.echo(click.style(f"\n{answer}", fg="green"))


if __name__ == "__main__":
    main()
