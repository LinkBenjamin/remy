'''Core functions'''
import random
from collections import defaultdict
from pathlib import Path
from .llm import extract_recipe
from .models import Ingredient, Recipe
from .storage import load_all_recipes, save_recipe


def add_recipe_from_url(url: str) -> tuple[Recipe, Path]:
    '''Add a recipe from a URL'''
    recipe = extract_recipe(url)
    saved_path = save_recipe(recipe)
    return recipe, saved_path


def generate_meal_plan(num_meals: int) -> tuple[list[Recipe], dict[str, list[Ingredient]]]:
    '''Generate a meal plan of length n meals'''
    recipes = load_all_recipes()
    if not recipes:
        raise ValueError("No recipes found in library. Add some first with `remy add <url>`.")

    count = min(num_meals, len(recipes))
    selected = random.sample(recipes, count)

    # Aggregate quantities where (name, unit) match
    merged: dict[tuple[str, str | None], Ingredient] = {}
    for recipe in selected:
        for item in recipe.ingredients:
            key = (item.name.lower().strip(), item.unit.lower().strip() if item.unit else None)
            if key not in merged:
                merged[key] = item.model_copy()
            else:
                existing_quantity = merged[key].quantity
                item_quantity = item.quantity
                if existing_quantity is not None and item_quantity is not None:
                    merged[key].quantity = round(existing_quantity + item_quantity, 2)

    # Group shopping list by grocery aisle
    grouped_list: dict[str, list[Ingredient]] = defaultdict(list)
    for item in sorted(merged.values(), key=lambda x: x.name):
        grouped_list[item.category.capitalize()].append(item)

    return selected, dict(sorted(grouped_list.items()))
