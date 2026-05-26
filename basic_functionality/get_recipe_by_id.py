import logging

from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.orm import selectinload

from src import Recipe
from src import RecipeIngredient
from src import RecipeOut
from src import async_session

main_log = logging.getLogger("main")


async def get_recipe_by_id(recipe_id: int):
    """
    EN:
        The function takes a parameter in the form of a recipe ID and returns all data associated with this recipe.
    RU:

    """
    main_log.debug("The function `get_recipe_by_id` started working.")
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(Recipe)
                .where(Recipe.id == recipe_id)
                .values(
                    number_of_recipe_views=Recipe.number_of_recipe_views + 1
                )
            )

            stmt = await session.execute(
                select(Recipe)
                .where(Recipe.id == recipe_id)
                .options(
                    selectinload(Recipe.ingredients).options(
                        selectinload(RecipeIngredient.ingredient)
                    )
                )
            )

            result_check = stmt.scalars().all()

         information_dish_list = []
        for information_dish in result_check:
            data_recipe = {
                "id": information_dish.id,
                "name_recipe": information_dish.name_recipe,
                "cooking_time_minutes": information_dish.cooking_time_minutes,
                "number_of_recipe_views": information_dish.number_of_recipe_views,
                "ingredients": [
                    {
                        "name_ingredient": information_ingredient.ingredient.name_ingredient,
                        "quantity_ingredient": information_ingredient.quantity_ingredient,
                    }
                    for information_ingredient in information_dish.ingredients
                ],
            }
            information_dish_list.append(
                RecipeOut(
                    id=data_recipe["id"],
                    name_recipe=data_recipe["name_recipe"],
                    cooking_time_minutes=data_recipe["cooking_time_minutes"],
                    number_of_recipe_views=data_recipe["number_of_recipe_views"],
                    ingredients=data_recipe["ingredients"],
                )
            )
        main_log.debug(
            "The function `get_recipe_by_id` successfully completed its execution."
        )
        return information_dish_list
