import importlib.util
import sys
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[3]
    / "plugins"
    / "tools"
    / "openwebui-skills-manager"
    / "openwebui_skills_manager.py"
)
SPEC = importlib.util.spec_from_file_location("openwebui_skills_manager", MODULE_PATH)
openwebui_skills_manager = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = openwebui_skills_manager
SPEC.loader.exec_module(openwebui_skills_manager)


def test_parse_skill_md_meta_supports_folded_multiline_description():
    content = (
        "---\r\n"
        "name: persona-selector\r\n"
        "description: >\r\n"
        "  Two-step persona picker. Step 1: numbered category list.\r\n"
        "  Step 2: numbered persona list. 160 personas + Custom.\r\n"
        "---\r\n\r\n"
        "# Persona Selector\r\n\r\n"
        "Body content.\r\n"
    )

    name, description, body = openwebui_skills_manager._parse_skill_md_meta(
        content, "fallback-skill"
    )

    assert name == "persona-selector"
    assert description == (
        "Two-step persona picker. Step 1: numbered category list. "
        "Step 2: numbered persona list. 160 personas + Custom."
    )
    assert body == "# Persona Selector\n\nBody content."


def test_parse_skill_md_meta_supports_literal_multiline_description_and_title_fallback():
    content = (
        "---\n"
        'title: "Data Storyteller"\n'
        "description: |\n"
        "  First line.\n"
        "  Second line.\n"
        "\n"
        "  Third paragraph.\n"
        "---\n\n"
        "Explain how to turn analysis into a narrative.\n"
    )

    name, description, body = openwebui_skills_manager._parse_skill_md_meta(
        content, "fallback-skill"
    )

    assert name == "Data Storyteller"
    assert description == "First line.\nSecond line.\n\nThird paragraph."
    assert body == "Explain how to turn analysis into a narrative."
