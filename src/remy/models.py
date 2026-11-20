'''Pydantic data model structures'''

from pydantic import BaseModel, Field  # pylint: disable=import-error

class Ingredient(BaseModel):
    '''Ingredients'''
    name: str = Field(
        description="Normalized singular lowercase ingredient name, " \
        "e.g. 'chicken breast', 'garlic', 'olive oil'"
    )
    quantity: float | None = Field(
        default=None,
        description="Numeric quantity (e.g. 0.5 for 1/2, 1.5 for 1 1/2). " \
        "Null if 'to taste' or unspecified.",
    )
    unit: str | None = Field(
        default=None,
        description="Standardized lowercase unit (cup, tbsp, tsp, lb, oz, clove, can) "
        "or null for whole items.",
    )
    category: str = Field(
        default="other",
        description="Grocery store section: produce, meat, dairy, pantry, spices, bakery, or other",
    )


class Recipe(BaseModel):
    '''Recipe'''
    title: str
    source_url: str | None = None
    prep_time_minutes: int | None = None
    cook_time_minutes: int | None = None
    servings: int | None = None
    ingredients: list[Ingredient]
    instructions: list[str]
