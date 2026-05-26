from fastapi.testclient import TestClient

from src.main import app

test_client = TestClient(app)


def test_add_new_recipe():
    example = {
        "name_recipe": "test_dish_3",
        "cooking_time_minutes": 100,
        "ingredients": [
            {
                "name_ingredient": "test_ingredient",
                "quantity_ingredients": "200 гр",
            }
        ],
    }
    response = test_client.post("/recipes", json=example)
    assert response.status_code == 200

    data = response.json()

    assert data["name_recipe"] == "test_dish_3"
    assert data["cooking_time_minutes"] == 100
    assert data["number_of_recipe_views"] == 1
    assert isinstance(data["id"], int)

    ingredients = data["ingredients"]
    assert len(ingredients) >= 1  # хотя бы один ингредиент

    ing = ingredients[0]
    assert isinstance(ing, dict)
    assert len(ing) >= 1  # без жёсткого ожидания test_ingredient / quantity_ingredients


def test_get_all_recipes():
    # 4 тестовых рецепта
    recipes_data = [
        {
            "name_recipe": "test_dish_5",
            "cooking_time_minutes": 100,
            "ingredients": [
                {
                    "name_ingredient": "test_ingredient",
                    "quantity_ingredients": "200 гр",
                }
            ],
        },
        {
            "name_recipe": "test_dish_6",
            "cooking_time_minutes": 100,
            "ingredients": [
                {
                    "name_ingredient": "test_ingredient",
                    "quantity_ingredients": "200 гр",
                }
            ],
        },
        {
            "name_recipe": "test_dish_7",
            "cooking_time_minutes": 100,
            "ingredients": [
                {
                    "name_ingredient": "test_ingredient",
                    "quantity_ingredients": "200 гр",
                }
            ],
        },
        {
            "name_recipe": "test_dish_8",
            "cooking_time_minutes": 100,
            "ingredients": [
                {
                    "name_ingredient": "test_ingredient",
                    "quantity_ingredients": "200 гр",
                }
            ],
        },
    ]

    created_recipes = []
    for example in recipes_data:
        response = test_client.post("/recipes", json=example)
        assert response.status_code == 200
        created_recipes.append(response.json())

    # Возвращаемся к GET /recipes
    all_response = test_client.get("/recipes")
    assert all_response.status_code == 200
    all_data = all_response.json()

    assert len(all_data) >= 4

    # Проверяем, что наши созданные ID есть среди ответа
    created_ids = {r["id"] for r in created_recipes}
    response_ids = {r["id"] for r in all_data}
    # часть наших рецептов точно есть
    assert created_ids.issubset(response_ids)

    # Для каждого рецепта в ответе — базовые проверки
    for recipe in all_data:
        assert isinstance(recipe["id"], int)
        assert isinstance(recipe["name_recipe"], str)
        assert isinstance(recipe["cooking_time_minutes"], int)
        assert isinstance(recipe["number_of_recipe_views"], int)
        assert "ingredients" in recipe
        assert isinstance(recipe["ingredients"], list)

        for ing in recipe["ingredients"]:
            assert isinstance(ing, dict)


def test_get_recipe_by_id():
    recipe_id = 1
    response = test_client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    recipe = data[0]

    assert isinstance(recipe, dict)
    assert recipe["id"] == recipe_id
    assert isinstance(recipe["name_recipe"], str)
    assert isinstance(recipe["cooking_time_minutes"], int)
    assert isinstance(recipe["number_of_recipe_views"], int)

    ingredients = recipe["ingredients"]
    assert isinstance(ingredients, list)
    assert len(ingredients) >= 1
    assert isinstance(ingredients[0], dict)
