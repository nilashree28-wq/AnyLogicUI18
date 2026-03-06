"""
CLI chat loop: load context once, then answer questions using the LLM.
Run from project root: python -m chatbot.chat
"""
from .context_builder import build_system_prompt, build_context, build_user_prompt
from .llm_client import chat


def main():
    print("Loading Ireland–UK parameter context from completed runs...")
    try:
        context = build_context()
        system = build_system_prompt()
    except FileNotFoundError as e:
        print(f"Data not found: {e}")
        print("Ensure Post-Brexit Sector Based Model - Completed runs.xlsx and parameter_names_from_completed_runs_updated.csv are in the project root.")
        return
    except Exception as e:
        print(f"Error loading data: {e}")
        return
    print("Ready. Ask about input parameters for Ireland–UK (e.g. 'What input parameters do I need for Ireland to UK direct route?'). Type 'quit' to exit.\n")
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            break
        user_prompt = build_user_prompt(context, user_input)
        reply = chat(system, user_prompt)
        print("Assistant:", reply)
        print()


if __name__ == "__main__":
    main()
