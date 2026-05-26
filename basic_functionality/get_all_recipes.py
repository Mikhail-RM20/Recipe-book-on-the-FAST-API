import logging
from typing import Dict, List

from sqlalchemy import desc, select, update
from sqlalchemy.orm import selectinload

from src import Recipe, RecipeIngredient, RecipeOut, async_session

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
            information_dish.append(RecipeOut(**result_data))
        main_log.debug(
            "The function `get_all_recipes` successfully completed its execution."
        )
        return information_dish
