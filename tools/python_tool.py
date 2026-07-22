import pandas as pd


class PythonTool:
    """
    Executes safe Pandas expressions on the loaded DataFrame.
    The DataFrame is available as 'df'.
    """

    def __init__(self):
        pass

    def execute(self, code: str, df: pd.DataFrame):
        if df is None:
            return "No dataset loaded."

        # Safe execution environment
        safe_globals = {
            "__builtins__": {},
        }

        safe_locals = {
            "df": df,
            "pd": pd,
            "len": len,
            "sum": sum,
            "min": min,
            "max": max,
            "round": round,
        }

        try:
            result = eval(code, safe_globals, safe_locals)
            return result

        except Exception as e:
            return f"Execution Error:\n{e}"