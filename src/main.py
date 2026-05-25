import logging.config
from typing import List

from fastapi import FastAPI

from basic_functionality.create_recipe import add_new_recipe
from basic_functionality.get_all_recipes import get_all_recipes
from basic_functionality.get_recipe_by_id import get_recipe_by_id
from .database import Base
from .database import engine
from .logger import dict_config
from .schemas import RecipeIn
from .schemas import RecipeOut

logging.config.dictConfig(dict_config)

main_log = logging.getLogger("main")
main_log.setLevel(logging.DEBUG)

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


@app.post("/recipes", response_model=RecipeOut)
async def create_recipe(recipe: RecipeIn):
    main_log.debug("EN: The function `create_recipe` started working.")
    """
    EN:
        Creates a new recipe from the database.

        - The main logic is implemented in the `add_new_recipe` function.

    RU:
        Создаёт новый рецепт в базе данных.

        - Основная логика реализована в функции `add_new_recipe`.
    """
    return await add_new_recipe(recipe)


@app.get("/recipes", response_model=List[RecipeOut])
async def get_recipes():
    main_log.debug("EN: The function `get_recipes` started working.")
    """
    EN:
        Gets a list of all recipes, including the ingredients needed for preparation.

        - The main logic is implemented in the `get_all_recipes` function.

    RU:
        Получает список всех рецептов, а так же ингредиентов, необходимых для приготовления.

        - Основная логика реализована в функции `get_all_recipes`.
    """
    return await get_all_recipes()


@app.get("/recipes/{recipe_id}", response_model=List[RecipeOut])
async def get_recipe(recipe_id: int):
    main_log.debug("EN: The function `get_recipe` started working.")
    """
    EN:
     The endpoint accepts a number—the recipe ID—and returns information about it.

        - The main logic is implemented in the `get_recipe_by_id` function.

    RU:
        Ендпоинт принимает число - ID рецепта и отдает информацию о нем.

        - Основная логика реализована в функции `get_recipe_by_id`.
    """
    return await get_recipe_by_id(recipe_id)
