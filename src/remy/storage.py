'''Handling storage of recipes'''
import re
from pathlib import Path
from .models import Recipe


def get_recipes_dir() -> Path:
    '''Finds the recipe storage directory'''
    base_dir = Path.home() / "Library" / "Application Support" / "remy" / "recipes"
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir


def slugify(text: str) -> str:
    '''Makes a slug for the recipe'''
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "untitled-recipe"


def save_recipe(recipe: Recipe) -> Path:
    '''Saves a recipe in the storage area'''
    file_path = get_recipes_dir() / f"{slugify(recipe.title)}.json"
    file_path.write_text(recipe.model_dump_json(indent=2), encoding="utf-8")
    return file_path


def load_all_recipes() -> list[Recipe]:
    '''Loads all recipes'''
    recipes: list[Recipe] = []
    for file_path in sorted(get_recipes_dir().glob("*.json")):
        recipes.append(Recipe.model_validate_json(file_path.read_text(encoding="utf-8")))
    return recipes
