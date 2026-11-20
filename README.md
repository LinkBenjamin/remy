# Remy

Remy is a local macOS meal planning CLI powered by Apple Foundation Models. It
extracts recipes from web pages, stores them as JSON, and creates meal plans
with grouped shopping lists.

## Requirements

- macOS
- Python 3.11 or newer
- The `textutil` command included with macOS
- The `fm` Foundation Models command-line tool available on your `PATH`

## Set up after cloning

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

Verify that the CLI is installed:

```bash
remy --help
```

## Try it out

Add a recipe by passing the URL of a recipe page:

```bash
remy add "https://example.com/a-recipe"
```

View the titles in your recipe library:

```bash
remy list
```

View one recipe by its numbered position:

```bash
remy list 1
```

Generate a meal plan and grouped shopping list for three meals:

```bash
remy plan 3
```

Saved recipes are stored in:

```text
~/Library/Application Support/remy/recipes
```
