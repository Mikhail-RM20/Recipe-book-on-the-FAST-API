import logging

from sqlalchemy import select

from src import (
    Ingredient,
    Recipe,
    RecipeIn,
    RecipeIngredient,
    RecipeOut,
    async_session,
)

main_log = logging.getLogger("main")


async def add_new_recipe(recipe: RecipeIn) -> RecipeOut:
    """
    EN:
        A function that adds a new recipe and its ingredients to the database.
        If the recipe already exists, the function will throw an exception.

        Accepts data from the shemas.py module after successfully checking for validity.

    RU:
        Функция, добавляющая новый рецепт и его ингредиенты в базу данных.
        Если рецепт уже существует, функция выбросит исключение.

        Принимает данные из модуля shemas.py после успешной проверки на корректность.
    """
    main_log.debug("The function `add_new_recipe` started working.")
    async with async_session() as session:
        async with session.begin():
            result_check_name = await session.execute(
                select(Recipe).where(Recipe.name_recipe == recipe.name_recipe)
            )
            check_name = result_check_name.scalar_one_or_none()
            if check_name:
                main_log.error("Recipe already exists in database.")
                raise ValueError("Recipe already exists")

            new_dish = Recipe(
                name_recipe=recipe.name_recipe,
                cooking_time_minutes=recipe.cooking_time_minutes,
            )
            session.add(new_dish)
            main_log.info("Name recipe created successfully.")
            await session.flush()

            list_ingredients = []

            for ingredient in recipe.ingredients:
                result_check_ingredient = await session.execute(
                    select(Ingredient).where(
                        Ingredient.name_ingredient == ingredient.name_ingredient
                    )
                )
                check_ingredient = result_check_ingredient.scalars().first()

                information_ingredient = {}

                if check_ingredient:
                    recipe_ing = RecipeIngredient(
                        recipe_id=new_dish.id,
                        ingredient_id=check_ingredient.id,
                        quantity_ingredient=ingredient.quantity_ingredients,
                    )
                    session.add(recipe_ing)
                    main_log.info("The ingredient is already in the database.")
                    information_ingredient[ingredient.name_ingredient] = str(
                        ingredient.quantity_ingredients
                    )
                    list_ingredients.append(information_ingredient)
                    main_log.info("Recipe created successfully.")
                else:
                    new_ingredient = Ingredient(
                        name_ingredient=ingredient.name_ingredient
                    )
                    session.add(new_ingredient)
                    main_log.info("Ingredient created successfully.")
                    await session.flush()

                    recipe_ing = RecipeIngredient(
                        recipe_id=new_dish.id,
                        ingredient_id=new_ingredient.id,
                        quantity_ingredient=ingredient.quantity_ingredients,
                    )
                    session.add(recipe_ing)
                    information_ingredient[new_ingredient.name_ingredient] = str(
                        ingredient.quantity_ingredients
                    )
                    list_ingredients.append(information_ingredient)
                    main_log.info("Recipe created successfully.")
            await session.flush()

        await session.refresh(new_dish)
        main_log.debug(
            "The function `get_all_recipes` successfully completed its execution."
        )
        return RecipeOut(
            id=new_dish.id,
            name_recipe=new_dish.name_recipe,
            cooking_time_minutes=new_dish.cooking_time_minutes,
            number_of_recipe_views=new_dish.number_of_recipe_views,
            ingredients=list_ingredients,
        )
