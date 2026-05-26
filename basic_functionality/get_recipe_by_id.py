import logging

from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from src import Recipe, RecipeIngredient, RecipeOut, async_session

main_log = logging.getLogger("main")


async def get_recipe_by_id(recipe_id: int) -> list[RecipeOut]:
    """
    EN:
        The function takes a parameter in the form of a recipe
         ID and returns all data associated with this recipe.
    RU:

    """
    main_log.debug("The function `get_recipe_by_id` started working.")
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(Recipe)
                .where(Recipe.id == recipe_id)
                .values(number_of_recipe_views=Recipe.number_of_recipe_views + 1)
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
            ingredients = []
            for information_ingredient in information_dish.ingredients:
                ingredient_name = information_ingredient.ingredient.name_ingredient
                ingredients.append(
                    {
                        "name_ingredient": ingredient_name,
                        "quantity_ingredient": information_ingredient
                        .quantity_ingredient,
                    }

                )

        information_dish_list.append(
            RecipeOut(
                id=information_dish.id,
                name_recipe=information_dish.name_recipe,
                cooking_time_minutes=information_dish.cooking_time_minutes,
                number_of_recipe_views=information_dish.number_of_recipe_views,
                ingredients=ingredients,
            )
        )
        main_log.debug(
            "The function `get_recipe_by_id` successfully completed its execution."
        )
        return information_dish_list
