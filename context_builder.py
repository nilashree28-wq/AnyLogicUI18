"""Build LLM context from Ireland–UK parameters and completed runs."""
from .data_loader import (
    load_parameter_list,
    load_completed_runs,
    get_ir_gb_input_context,
)
from .config import EXCEL_PATH, PARAMETER_CSV_PATH


def build_system_prompt() -> str:
    return """You are an assistant for a post-Brexit supply chain simulation (Ireland–UK focus).
Answer only using the provided context (parameter list and/or run data).
If the context does not contain the answer, say so. Do not invent parameter names or values.
Direct route here means Ireland–UK maritime (Dublin/Rosslare ↔ UK West ports), no EU landbridge."""


def build_context(include_run_values: bool = True) -> str:
    """Load data and build context string for Ireland–UK input parameters (and optional run values)."""
    param_df = load_parameter_list(PARAMETER_CSV_PATH)
    runs_df, input_headers, _ = load_completed_runs(EXCEL_PATH)
    return get_ir_gb_input_context(
        param_df,
        runs_df.head(10),
        input_headers,
        max_runs=10,
    )


def build_user_prompt(context: str, user_question: str) -> str:
    return f"""Context (Ireland–UK input parameters and value ranges from completed runs):

{context}

User question: {user_question}"""
