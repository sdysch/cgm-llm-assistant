import click

from cgm_llm_assistant.processing import load_cgm_csv
from cgm_llm_assistant.context import build_context
from cgm_llm_assistant.llm import explain_metrics


@click.command()
@click.argument("file")
def main(file):
    df = load_cgm_csv(file)
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
        answer = explain_metrics(context, question)
        click.echo(click.style(f"\n{answer}", fg="green"))


if __name__ == "__main__":
    main()
