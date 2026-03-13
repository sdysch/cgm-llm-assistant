import argparse

from cgm_llm_assistant.processing import load_cgm_csv
from cgm_llm_assistant.context import build_context
from cgm_llm_assistant.llm import explain_metrics


def main(args):
    df = load_cgm_csv(args.file)
    context = build_context(df)

    print("CGM assistant ready. Type questions (or 'exit'):")

    while True:
        question = input("\n> ")
        if question.lower() in {"exit", "quit"}:
            break
        answer = explain_metrics(context, question)
        print("\n", answer)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="CGM CSV file")

    args = parser.parse_args()
    main(args)
