import importlib.util
import sys
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[3]
    / "plugins"
    / "pipes"
    / "github-copilot-sdk"
    / "github_copilot_sdk.py"
)
SPEC = importlib.util.spec_from_file_location("github_copilot_sdk", MODULE_PATH)
github_copilot_sdk = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = github_copilot_sdk
SPEC.loader.exec_module(github_copilot_sdk)

PIPE = github_copilot_sdk.Pipe()


def test_pipe_parse_skill_md_meta_supports_folded_multiline_description():
    content = (
        "---\r\n"
        "name: persona-selector\r\n"
        "description: >\r\n"
        "  Two-step persona picker.\r\n"
        "  Step 2 provides persona options.\r\n"
        "---\r\n\r\n"
        "# Persona Selector\r\n\r\n"
        "Body content.\r\n"
    )

    name, description, body = PIPE._parse_skill_md_meta(content, "fallback-skill")

    assert name == "persona-selector"
    assert description == "Two-step persona picker. Step 2 provides persona options."
    assert body == "# Persona Selector\n\nBody content."


def test_pipe_build_skill_md_content_round_trips_multiline_description():
    content = PIPE._build_skill_md_content(
        "Data Storyteller",
        "First line.\nSecond line.\n\nThird paragraph.",
        "Explain how to turn analysis into a narrative.",
    )

    assert (
        "description: |\n"
        "  First line.\n"
        "  Second line.\n"
        "\n"
        "  Third paragraph.\n"
    ) in content

    name, description, body = PIPE._parse_skill_md_meta(content, "fallback-skill")

    assert name == "Data Storyteller"
    assert description == "First line.\nSecond line.\n\nThird paragraph."
    assert body == (
        "# Data Storyteller\n\nExplain how to turn analysis into a narrative."
    )
