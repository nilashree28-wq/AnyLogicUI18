"""LLM client: OpenAI (or mock when no API key)."""
from .config import OPENAI_API_KEY, OPENAI_MODEL


def chat(system_prompt: str, user_prompt: str) -> str:
    """
    Send system + user prompt to LLM; return assistant reply.
    Uses OpenAI API if OPENAI_API_KEY is set; otherwise returns a mock reply.
    """
    if not OPENAI_API_KEY or OPENAI_API_KEY.strip() == "":
        return _mock_reply(user_prompt)
    return _openai_chat(system_prompt, user_prompt)


def _mock_reply(user_prompt: str) -> str:
    """When no API key: suggest setting OPENAI_API_KEY and summarize what would be sent."""
    return (
        "[Mock mode: no OPENAI_API_KEY set. Set it in .env or environment to use the real LLM.]\n\n"
        "For your question, the chatbot would use the Ireland–UK parameter list and "
        "value ranges from 10 completed runs, then ask the LLM to answer from that context only."
    )


def _openai_chat(system_prompt: str, user_prompt: str) -> str:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        resp = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=1024,
        )
        return resp.choices[0].message.content or ""
    except Exception as e:
        return f"[Error calling LLM: {e}]"
