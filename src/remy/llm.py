import json
import subprocess
import urllib.request
from .models import Recipe


def fetch_clean_text(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"},
    )
    with urllib.request.urlopen(req, timeout=15) as response:
        html_bytes = response.read()

    result = subprocess.run(
        ["textutil", "-stdin", "-format", "html", "-convert", "txt", "-stdout"],
        input=html_bytes,
        capture_output=True,
        check=True,
    )
    text = result.stdout.decode("utf-8", errors="ignore")

    # Trim comment sections so large food blogs don't slow down local inference
    for cutoff in ("Leave a Comment", "Leave a Reply"):
        if cutoff in text:
            text = text.split(cutoff)[0]

    return text.strip()


def _extract_json_object(raw_text: str) -> str:
    """Finds the first valid JSON object in raw_text and ignores any trailing text or fences."""
    start = raw_text.find("{")
    if start == -1:
        raise ValueError(f"No JSON object found in fm output:\n{raw_text}")

    decoder = json.JSONDecoder()
    obj, _ = decoder.raw_decode(raw_text, start)
    return json.dumps(obj)


def extract_recipe(url: str) -> Recipe:
    page_text = fetch_clean_text(url)

    example_format = json.dumps(
        {
            "title": "Creamy Macaroni and Cheese",
            "prep_time_minutes": 15,
            "cook_time_minutes": 120,
            "servings": 6,
            "ingredients": [
                {
                    "name": "elbow macaroni",
                    "quantity": 2.0,
                    "unit": "cup",
                    "category": "pantry",
                }
            ],
            "instructions": ["Boil macaroni until tender.", "Mix with cheese and cook."],
        },
        indent=2,
    )

    prompt = (
        "Extract the recipe from the provided webpage content into a JSON object matching this exact structure. "
        "Normalize ingredient names to singular lowercase (e.g. 'elbow macaroni', 'cheddar cheese') and convert fractions to decimals (e.g. 0.5). "
        "Use null if prep time, cook time, servings, quantity, or unit is not specified. "
        "Valid categories: produce, meat, dairy, pantry, spices, bakery, other.\n\n"
        f"Example JSON structure:\n{example_format}"
    )

    result = subprocess.run(
        ["fm", "respond", prompt, f"--text={page_text}"],
        capture_output=True,
        text=True,
        check=True,
    )

    clean_json = _extract_json_object(result.stdout)
    recipe = Recipe.model_validate_json(clean_json)
    recipe.source_url = url
    return recipe
