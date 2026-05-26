import logging
from typing import Dict
from typing import List

from sqlalchemy import desc
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.orm import selectinload

from src import Recipe
from src import RecipeIngredient
from src import RecipeOut
from src import async_session

main_log = logging.getLogger("main")


async def get_all_recipes() -> List[Dict[str, str]]:
    """
    EN:
        The function takes all recipes from the database, as well as the ingredients for this recipe,
         and returns the collected data.

    RU:
        Функция, беред из базы данных все рецепт, а так же ингредиенты для этого рецепта и возрващает собранные данные.
    """
    main_log.debug("The function `get_all_recipes` started working.")
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(Recipe).values(
                    number_of_recipe_views=Recipe.number_of_recipe_views + 1
                )
            )

            stmt = await session.execute(
                select(Recipe)
                .options(
                    selectinload(Recipe.ingredients).options(
                        selectinload(RecipeIngredient.ingredient)
                    )
                )
                .order_by(desc(Recipe.number_of_recipe_views))
            )

            result = stmt.scalars().all()

        information_dish = []
        for data in result:
            result_data = {
                "id": data.id,
                "name_recipe": data.name_recipe,
                "cooking_time_minutes": data.cooking_time_minutes,
                "number_of_recipe_views": data.number_of_recipe_views,
                "ingredients": [
                    {
                        "name_ingredient": d.ingredient.name_ingredient,
                        "quantity_ingredient": str(d.quantity_ingredient),
                    }
                    for d in data.ingredients
                ],
            }
            information_dish.append(
                RecipeOut(
                    id=result_data["id"],
                    name_recipe=result_data["name_recipe"],
                    cooking_time_minutes=result_data["cooking_time_minutes"],
                    number_of_recipe_views=result_data["number_of_recipe_views"],
                    ingredients=result_data["ingredients"],
                )
            )
        main_log.debug(
            "The function `get_all_recipes` successfully completed its execution."
        )
        return information_dish
