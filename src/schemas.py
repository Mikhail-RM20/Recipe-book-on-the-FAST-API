from typing import Dict, List

from pydantic import BaseModel, Field


class RecipeIn(BaseModel):
    name_recipe: str = Field(
        ...,
        title="Recipe name",
        description="The need to write the name recipe that you want to add",
        min_length=2,
        max_length=50,
    )
    cooking_time_minutes: int = Field(
        ...,
        title="Cooking time",
        description="The amount of time the recipe needs to be cooking",
    )

    ingredients: List["IngredientIn"] = Field(
        ...,
        title="Ingredient name",
        min_length=1,
    )


class RecipeOut(BaseModel):
    id: int
    name_recipe: str
    cooking_time_minutes: int
    number_of_recipe_views: int
    ingredients: List[Dict[str, str]]

    class Config:
        orm_mode = True


class IngredientIn(BaseModel):
    name_ingredient: str = Field(
        ...,
        title="Ingredient name",
        description="The need to write the name ingredient that you want to add",
        min_length=2,
        max_length=50,
    )
    quantity_ingredients: str = Field(
        ...,
        title="Quantity ingredients",
        description="Amount of the ingredient needed",
    )
