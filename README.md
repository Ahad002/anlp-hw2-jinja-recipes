# Dietary-Aware Recipe Rewriting with Jinja Templates

A small NLP project that uses the **Jinja2** templating engine to dynamically
generate LLM prompts for the task of **rewriting recipe instructions to fit a
user's dietary restrictions, skill level, and desired output format**.

This repository was developed for **Homework 2, Part 5** of the
*Advanced Natural Language Processing (SoSe 2026)* course at Leibniz
Universität Hannover (Instructor: Dr. Jennifer D'Souza).

---

## 1. Task / Domain

**Domain:** Cooking & Recipe Rewriting (a *different* domain from the
[Lecture 5 prompting notebooks](https://github.com/jd-coderepos/advanced-nlp-course/tree/main/2026/05_prompting)).

**Task:** Given a recipe (title, ingredients, original instructions) and a user
profile (dietary restrictions, allergies, skill level, preferred output format),
generate a prompt that asks an LLM to **rewrite the recipe** so that:

- All ingredients respect the user's restrictions (e.g. vegan, gluten-free, halal, keto).
- Allergens are flagged and substitutions are suggested.
- Instructions are adapted to the user's skill level (beginner gets more detail).
- The output format matches the user's preference (numbered steps, bullet list,
  or short paragraph), with optional sections for nutrition info, prep time, or
  a shopping list.

Three real example recipes are included in `examples/recipes.json`.

---

## 2. What the Jinja Template Does

The single template `templates/recipe_prompt.jinja` builds a complete prompt
from a structured input object. It uses several Jinja features that would be
painful with plain `str.format` or f-strings:

| Jinja feature                  | Where it is used                                            |
|--------------------------------|-------------------------------------------------------------|
| `{% if %}` conditionals        | Show dietary section only if restrictions are present       |
| `{% for %}` loops              | Iterate over ingredients, allergies, restrictions, steps    |
| Filters (`upper`, `join`, `length`) | Pretty-print lists and counts                          |
| `{% macro %}`                  | Reusable "bullet list" component used in three places       |
| Whitespace control (`{%- -%}`) | Keep the rendered prompt clean                              |
| Variant selection              | Switch between `numbered`, `bulleted`, and `paragraph` output formats |
| Optional sections              | `include_nutrition`, `include_shopping_list`, `include_hints` flags |

The template renders a different prompt for each combination of these inputs
*without* changing a single line of Python code.

---

## 3. Why Jinja Is Appropriate for This Problem

Recipe rewriting prompts are not a single fixed string — they are a **family of
prompts** that change shape depending on the user. A purely Python `f-string`
solution would force us to:

- Concatenate strings with conditional logic for *each* optional section.
- Manually format lists of ingredients, allergies, and steps with `\n`.
- Duplicate code each time we want a new output format (numbered vs. bulleted vs. paragraph).
- Mix presentation logic with business logic in the Python script.

Jinja solves all of this cleanly:

1. **Separation of concerns** — prompt text lives in `.jinja` files,
   Python code only handles data and rendering.
2. **Conditional sections** — `{% if user.allergies %}` is far more readable
   than nested Python ternaries.
3. **Loops** — iterating over ingredients with a single `{% for %}` block
   beats `"\n".join([...])` chained with conditionals.
4. **Reusable macros** — the same bullet-list macro is reused for ingredients,
   allergens, and the optional shopping list.
5. **Multiple output variants** — switching the `output_format` field rewrites
   the entire instruction section without touching Python.
6. **Maintainability** — non-programmers (e.g. a chef or a domain expert)
   can edit the prompt template directly without reading Python code.

These are exactly the situations the assignment lists where "simple string
concatenation or a few Python if statements would not be an equally natural
solution".

---

## 4. Repository Layout

```
hw2-part5-jinja-recipes/
├── README.md                       <- this file
├── requirements.txt                <- pinned Python dependencies
├── generate_prompts.py             <- loads template, fills examples, prints prompts
├── templates/
│   └── recipe_prompt.jinja         <- the Jinja prompt template
├── examples/
│   └── recipes.json                <- 3 example recipes + user profiles
└── outputs/
    └── prompt_*.txt                <- generated prompts (one per example)
```

---

## 5. How to Run

```bash
# 1. Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate prompts for all three example recipes
python generate_prompts.py
```

Each generated prompt is written to `outputs/prompt_<id>.txt` and is also
printed to the terminal so you can inspect how the template adapts to each
user profile.

---

## 6. Optional Extension (not required by the assignment)

The script includes a commented-out block showing how the generated prompts
could be sent to an OpenAI-compatible LLM endpoint. It is disabled by default
so the project runs without any API key.

---

## License

MIT — free to use for teaching and learning.
