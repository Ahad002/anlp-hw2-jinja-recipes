"""
generate_prompts.py
-------------------
Load the Jinja recipe-rewriting template, fill it with each example from
examples/recipes.json, and write the rendered prompt to outputs/.

Course:  Advanced NLP (SoSe 2026), Homework 2, Part 5
Author:  [your name]
"""

from __future__ import annotations

import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent
TEMPLATE_DIR = PROJECT_ROOT / "templates"
EXAMPLES_FILE = PROJECT_ROOT / "examples" / "recipes.json"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
TEMPLATE_NAME = "recipe_prompt.jinja"


def build_environment() -> Environment:
    """Configure Jinja with strict undefined variables and trim/lstrip blocks
    so the rendered prompt does not contain stray blank lines."""
    return Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=select_autoescape(disabled_extensions=("jinja", "j2")),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )


def load_examples(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def render_prompt(env: Environment, example: dict) -> str:
    template = env.get_template(TEMPLATE_NAME)
    return template.render(
        recipe=example["recipe"],
        user=example["user"],
        options=example["options"],
    )


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    env = build_environment()
    examples = load_examples(EXAMPLES_FILE)

    print(f"Loaded {len(examples)} example(s) from {EXAMPLES_FILE.name}\n")

    for example in examples:
        prompt = render_prompt(env, example)
        out_path = OUTPUT_DIR / f"prompt_{example['id']}.txt"
        out_path.write_text(prompt, encoding="utf-8")

        banner = "=" * 72
        print(banner)
        print(f"EXAMPLE: {example['id']}  ->  {out_path.relative_to(PROJECT_ROOT)}")
        print(banner)
        print(prompt)
        print()

    # -----------------------------------------------------------------------
    # Optional extension: send the prompts to an LLM.
    # Disabled by default — uncomment and set OPENAI_API_KEY to enable.
    # -----------------------------------------------------------------------
    # import os
    # from openai import OpenAI
    # client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    # for example in examples:
    #     prompt = render_prompt(env, example)
    #     resp = client.chat.completions.create(
    #         model="gpt-4o-mini",
    #         messages=[{"role": "user", "content": prompt}],
    #     )
    #     print(example["id"], "->", resp.choices[0].message.content[:200], "...")


if __name__ == "__main__":
    main()
