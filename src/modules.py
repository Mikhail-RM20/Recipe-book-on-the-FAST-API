from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .database import Base


class Recipe(Base):
    __tablename__ = "recipe"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name_recipe: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True
    )
    cooking_time_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    number_of_recipe_views: Mapped[int] = mapped_column(Integer, default=1)

    ingredients: Mapped[List["RecipeIngredient"]] = relationship(
        "RecipeIngredient", back_populates="recipe", lazy="joined"
    )


class Ingredient(Base):
    __tablename__ = "ingredient"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name_ingredient: Mapped[str] = mapped_column(String(100), nullable=False)

    recipes: Mapped[List["RecipeIngredient"]] = relationship(
        "RecipeIngredient", back_populates="ingredient", lazy="joined"
    )


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredient"

    quantity_ingredient: Mapped[str] = mapped_column(String, nullable=False)

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipe.id"), primary_key=True
    )
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredient.id"), primary_key=True
    )

    recipe: Mapped["Recipe"] = relationship(
        "Recipe", back_populates="ingredients"
    )
    ingredient: Mapped["Ingredient"] = relationship(
        "Ingredient",
        back_populates="recipes",
    )
