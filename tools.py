import sys
import math
import json
import io
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

search_engine = DuckDuckGoSearchRun()

@tool
def web_search(query: str) -> str:
    """Search the internet for current, real-time information.
    Use for news, recent events, facts, or anything needing up-to-date data."""
    try:
        results = search_engine.run(query)
        return results[:2000]
    except Exception as e:
        return f"Search error: {str(e)}"


@tool
def code_executor(code: str) -> str:
    """Execute Python code and return the output.
    Use for data analysis, calculations, or any programming task.
    Always print() your results."""
    try:
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        exec_globals = {"__builtins__": __builtins__, "math": math, "json": json}
        try:
            import pandas as pd
            exec_globals["pd"] = pd
        except ImportError:
            pass
        try:
            import numpy as np
            exec_globals["np"] = np
        except ImportError:
            pass
        exec(code, exec_globals)
        output = buffer.getvalue()
        sys.stdout = old_stdout
        return output if output else "Code executed successfully (no output)"
    except Exception as e:
        sys.stdout = old_stdout
        return f"Error: {str(e)}"


@tool
def file_reader(file_path: str) -> str:
    """Read and extract text content from files (TXT, CSV, JSON, PDF).
    Input: the file path as a string."""
    try:
        if file_path.endswith(".csv"):
            import pandas as pd
            df = pd.read_csv(file_path)
            return f"CSV: {len(df)} rows, {len(df.columns)} columns\nColumns: {list(df.columns)}\n\n{df.head().to_string()}"
        elif file_path.endswith(".json"):
            with open(file_path, "r") as f:
                return json.dumps(json.load(f), indent=2)[:3000]
        else:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()[:3000]
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def calculator(expression: str) -> str:
    """Perform precise mathematical calculations.
    Input: a math expression like '2**10' or 'math.sqrt(144)'."""
    try:
        allowed = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        allowed.update({"abs": abs, "round": round, "sum": sum, "min": min, "max": max})
        return f"Result: {eval(expression, {'__builtins__': {}}, allowed)}"
    except Exception as e:
        return f"Error: {str(e)}"


DEMO_DATA = {
    "sales": [
        {"month": "Jan", "revenue": 84000}, {"month": "Feb", "revenue": 92000},
        {"month": "Mar", "revenue": 88000}, {"month": "Apr", "revenue": 105000},
        {"month": "May", "revenue": 118000}, {"month": "Jun", "revenue": 124000},
        {"month": "Jul", "revenue": 115000}, {"month": "Aug", "revenue": 130000},
        {"month": "Sep", "revenue": 126000}, {"month": "Oct", "revenue": 138000},
        {"month": "Nov", "revenue": 145000}, {"month": "Dec", "revenue": 142000},
    ],
    "users": [
        {"id": 1, "name": "Alice Chen", "plan": "enterprise", "mrr": 2400},
        {"id": 2, "name": "Bob Smith", "plan": "pro", "mrr": 299},
        {"id": 3, "name": "Carol Jones", "plan": "pro", "mrr": 299},
        {"id": 4, "name": "David Kim", "plan": "enterprise", "mrr": 2400},
        {"id": 5, "name": "Eve Davis", "plan": "starter", "mrr": 49},
    ]
}

@tool
def database_query(query: str) -> str:
    """Query structured database tables. Available: 'sales', 'users'."""
    q = query.lower()
    if "sales" in q or "revenue" in q:
        data = DEMO_DATA["sales"]
        total = sum(r["revenue"] for r in data)
        best = max(data, key=lambda x: x["revenue"])
        return f"Sales data:\n{json.dumps(data, indent=2)}\n\nTotal: ${total:,}\nBest: {best['month']} (${best['revenue']:,})"
    elif "user" in q or "customer" in q:
        data = DEMO_DATA["users"]
        return f"Users:\n{json.dumps(data, indent=2)}\n\nTotal MRR: ${sum(u['mrr'] for u in data):,}"
    return f"Tables available: {list(DEMO_DATA.keys())}"


def get_all_tools():
    return [web_search, code_executor, file_reader, calculator, database_query]
