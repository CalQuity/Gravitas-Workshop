import json
from pathlib import Path


def test_eight_step_notebooks_exist_and_use_the_teaching_files() -> None:
    root = Path(__file__).parents[1]
    expected = [
        "01_vanilla_agent.ipynb",
        "02_instructions.ipynb",
        "03_knowledge.ipynb",
        "04_sessions.ipynb",
        "05_tools.ipynb",
        "06_guardrails.ipynb",
        "07_full_agent.ipynb",
        "08_agentos.ipynb",
    ]

    for name in expected:
        path = root / "notebooks" / name
        assert path.exists(), name
        notebook = json.loads(path.read_text(encoding="utf-8"))
        source = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])
        assert "PROJECT_ROOT" in source

    tools_source = (root / "notebooks" / "05_tools.ipynb").read_text(encoding="utf-8")
    assert "create_tools" in tools_source
    assert "market_ohlcv" in tools_source

