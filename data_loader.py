"""
Load Completed runs Excel and parameter list; filter to Ireland–UK / UK–Ireland only.
"""
import pandas as pd
from pathlib import Path
from .config import (
    PROJECT_ROOT,
    EXCEL_PATH,
    PARAMETER_CSV_PATH,
    COMPLETED_RUNS_SHEET,
    HEADER_ROW_EXCEL,
    INPUT_COL_END,
    OUTPUT_COL_START,
    OUTPUT_COL_END,
)


def _is_ireland_uk_parameter(parameter_name: str) -> bool:
    """Include parameters relevant to Ireland–UK / UK–Ireland flows only."""
    if not parameter_name or not isinstance(parameter_name, str):
        return False
    p = parameter_name.strip()
    # Exclude: IR–EU, GB–EU, UK East (Dover), EU Ports (Calais), Transit Landbridge
    exclude = (
        "LandBridge" in p or "Landbridge" in p or "EULB" in p
        or "Chebourg" in p or "Cherbourg" in p
        or "Rotterdam" in p or "ViaRott" in p
        or "Zeebrugge" in p or "ViaZee" in p
        or "BilBao" in p or "Bilbao" in p or "ViaBil" in p
        or "GB-EU" in p or "GBEU" in p
        or "UK East" in p or "GB-E" in p or "Exports To EU" in p or "Imports From EU" in p
        or "EU-Ports" in p
        or ("Transit" in p and "Landbridge" in p)
        or "Dover" in p or "Calais" in p
    )
    if exclude:
        return False
    # Include: IR–GB, Irish Ports (to/from GB), UK West (to/from IR), Dublin, Rosslare, GB-W, Maritime to GB, shelf life, UnAcc, check costs
    include = (
        "IR-GB" in p or "IR GB" in p
        or "Export To GB" in p or "Exports To GB" in p or "Imports From GB" in p
        or "Exports To IR" in p or "Imports From IR" in p
        or "UK West" in p or "GB-W" in p
        or "Dublin" in p or "Rosslare" in p
        or "Maritime" in p and ("GB" in p or "to GB" in p or "from GB" in p)
        or "Shelflife" in p or "Shelf life" in p or "shelflife" in p
        or "UnAcc" in p or "Unacc" in p
        or p in ("DocCheckCost", "PhyCheckCost", "SecurityCheckCost")
        or "DocCheckCost" in p or "PhyCheckCost" in p or "SecurityCheckCost" in p
    )
    return include


def load_parameter_list(csv_path: Path = None) -> pd.DataFrame:
    """Load parameter list CSV; filter to Ireland–UK input parameters only."""
    path = csv_path or PARAMETER_CSV_PATH
    df = pd.read_csv(path, skiprows=1)  # skip 'Parameter_Names,,'
    df = df.rename(columns=lambda c: c.strip())
    # Drop rows with no parameter_name (output KPIs in the list)
    df = df.dropna(subset=["parameter_name"])
    df = df[df["parameter_name"].astype(str).str.strip() != ""]
    # Ireland–UK only (input parameters: column_index 0..158)
    df = df[df["column_index"].astype(int) <= INPUT_COL_END]
    df = df[df["parameter_name"].astype(str).apply(_is_ireland_uk_parameter)]
    return df


def load_completed_runs(excel_path: Path = None) -> tuple[pd.DataFrame, list[str], list[str]]:
    """
    Load Completed runs sheet.
    Returns: (data_df, input_headers, output_headers)
    - data_df: rows = runs, columns = all (input + output)
    - input_headers: column names for 0..INPUT_COL_END
    - output_headers: column names for OUTPUT_COL_START..OUTPUT_COL_END
    """
    path = excel_path or EXCEL_PATH
    # Header in row index 1 (Excel row 2), data from row 2
    df = pd.read_excel(path, sheet_name=COMPLETED_RUNS_SHEET, header=HEADER_ROW_EXCEL - 1)
    # Trim to 333 columns if extra
    cols = list(df.columns)[: OUTPUT_COL_END + 1]
    df = df[cols].dropna(how="all")
    input_headers = [str(c) for c in cols[: INPUT_COL_END + 1]]
    output_headers = [str(c) for c in cols[OUTPUT_COL_START : OUTPUT_COL_END + 1]]
    return df, input_headers, output_headers


def get_ir_gb_input_context(
    param_df: pd.DataFrame,
    runs_df: pd.DataFrame,
    input_headers: list[str],
    max_runs: int = 10,
) -> str:
    """
    Build text context of Ireland–UK input parameters and value ranges from runs.
    """
    lines = [
        "Scope: Ireland–UK / UK–Ireland only (direct maritime route).",
        "",
        "Input parameters for Ireland–UK flows (parameter_name -> sub_parameter_name):",
    ]
    current_group = None
    for _, row in param_df.iterrows():
        pname = str(row.get("parameter_name", "")).strip()
        sname = str(row.get("sub_parameter_name", "")).strip()
        if not sname:
            continue
        if pname != current_group:
            current_group = pname
            lines.append(f"- {pname}: {sname}")
        else:
            lines.append(f"    {sname}")
    lines.append("")
    # Value ranges from runs (only for columns that exist in runs_df and are in param_df)
    sub_params = set(param_df["sub_parameter_name"].astype(str).str.strip())
    run_cols = [c for c in input_headers if c in runs_df.columns and c in sub_params]
    if run_cols:
        lines.append("Value ranges from completed runs (min – max):")
        for col in run_cols[:40]:  # limit to avoid huge context
            try:
                vals = pd.to_numeric(runs_df[col], errors="coerce").dropna()
                if len(vals) > 0:
                    mn, mx = vals.min(), vals.max()
                    if mn == mx:
                        lines.append(f"  {col}: {mn}")
                    else:
                        lines.append(f"  {col}: {mn} – {mx}")
            except Exception:
                pass
    return "\n".join(lines)
