from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
from typing import List


class ingrediant(BaseModel):
    name: str
    quantity: float
    measurement: str

class ingUpdate(BaseModel):
    r_name: str
    name: str
    quantity: float
    measurement: str

class macro(BaseModel):
    protein: int
    carbs: int
    fat: int


class recipe(BaseModel):
    name: str
    ingrediants: List[ingrediant]
    macros: macro
    author: str


class recipeNameUpt(BaseModel):
    old_name: str
    new_name: str


class macroUpdate(BaseModel):
    name: str
    protein: int
    carbs: int
    fat: int


recipe1 = recipe(name="Chocolate chip baked oats", ingrediants=[ingrediant(name="oats", quantity=3, measurement="cups"),
                                                                ingrediant(name="vanilla protein powder", quantity=2,
                                                                           measurement="scoops"),
                                                                ingrediant(name="baking powder", quantity=1,
                                                                           measurement="tsp"),
                                                                ingrediant(name="banana", quantity=4, measurement=""),
                                                                ingrediant(name="honey", quantity=2,
                                                                           measurement="tbsp"),
                                                                ingrediant(name="butter", quantity=1,
                                                                           measurement="tbsp"),
                                                                ingrediant(name="egg whites", quantity=10,
                                                                           measurement="tbsp"),
                                                                ingrediant(name="2% milk", quantity=2,
                                                                           measurement="cups"),
                                                                ingrediant(name="chocolate chips", quantity=2,
                                                                           measurement="tbsp")],
                 macros=macro(protein=116, carbs=352.8, fat=51.2), author="Josh Kurtis")
recipe2 = recipe(name="Ground turkey bowl",
                 ingrediants=[ingrediant(name="white rice", quantity=2.5, measurement="cups"),
                              ingrediant(name="white onion", quantity=1, measurement=""),
                              ingrediant(name="green pepper", quantity=1, measurement=""),
                              ingrediant(name="minced garlic", quantity=1, measurement="tbsp"),
                              ingrediant(name="shredded carrots", quantity=2, measurement="cups"),
                              ingrediant(name="olive oil", quantity=2, measurement="tbsp"),
                              ingrediant(name="ground turkey", quantity=2, measurement="lbs"),
                              ingrediant(name="mushrooms", quantity=8, measurement="oz"),
                              ingrediant(name="honey", quantity=1, measurement="tbsp"),
                              ingrediant(name="sriracha", quantity=2, measurement="tsp"),
                              ingrediant(name="ground ginger", quantity=0.5, measurement="tsp"),
                              ingrediant(name="seasame oil", quantity=1, measurement="tbsp"),
                              ingrediant(name="soy sauce", quantity=3, measurement="tbsp")],
                 macros=macro(protein=202, carbs=182, fat=102), author="Josh Kurtis")
recipe3 = recipe(name="chocolate brownie",
                 ingrediants=[ingrediant(name="unsalted butter", quantity=0.5, measurement="cups"),
                              ingrediant(name="sugar", quantity=2.25, measurement="cups"),
                              ingrediant(name="eggs", quantity=2, measurement=""),
                              ingrediant(name="cocoa powder", quantity=0.75, measurement=""),
                              ingrediant(name="salt", quantity=0.5, measurement="tsp"),
                              ingrediant(name="baking powder", quantity=0.5, measurement="tsp"),
                              ingrediant(name="vanilla extract", quantity=1, measurement="tsp"),
                              ingrediant(name="all purpose flour", quantity=0.75, measurement=""),
                              ingrediant(name="chocolate chips", quantity=0.5, measurement="cups")],
                 macros=macro(protein=32, carbs=208, fat=128), author="Akash")

recipeList = {}

recipeList[len(recipeList)] = recipe1
recipeList[len(recipeList)] = recipe2
recipeList[len(recipeList)] = recipe3

app = FastAPI()


# searches dictionary for recipes that contain the ingrediant
@app.get("/recipes")
def get_recipes():
    return {"Recipes": recipeList}


@app.get("/recipeIng/{author}")
def get_recipe_ingrediants(author: str):
    recipeReturn = {}
    for key in recipeList:
        if recipeList[key].author == author:
            recipeReturn[len(recipeReturn)] = recipeList[key]

    return {"Recipes": recipeReturn}


@app.get("/recipeIngredients")
def get_recipe_ingrediants(author: str):
    print(author)
    return {"Recipes": "Hello"}

@app.get("/recipeIng")
def get_recipe_by_ingredients(ingredients: str):
    print("Hello")
    recipe_return = {}
    print(ingredients)
    print("Hello")
    for key in recipeList:
        print(key)
        recipes = recipeList[key]
        for ingredient in recipeList[key].ingrediants:
            # for recipe_ingredient in recipes.ingredients:
            if ingredient.name == ingredients:
                recipe_return[len(recipe_return)] = recipes
                break
            else:
                continue

    return {"Recipes": recipe_return}

@app.put("/ingrediants")
def update_recipe_ingrediants(ingChange: ingUpdate):
    Mess = "Error: Recipe does not exist"
    for i in recipeList:
        if recipeList[i].name == ingChange.r_name:
            recipeList[i].ingrediants.name = ingChange.name
            recipeList[i].ingrediants.quantity = ingChange.quantity
            recipeList[i].ingrediants.measurement = ingChange.measurement
            return {"message": "Recipe ingredients updated successfully"}

    return {"message": Mess}


@app.put("/recipes/{old_recipe}")
def put_recipe_name(nameChange: recipeNameUpt):
    returnMess = "Error: Recipe does not exist"
    for key in recipeList:
        if recipeList[key].name == nameChange.old_name:
            recipeList[key].name = nameChange.new_name
            returnMess = "Successfully changed the name"
            break

    return {"message": returnMess}


@app.delete("/recipes/{recipe_name}")
def delete_recipe_name(recipe_name: str):
    returnMess = "Error: Recipe does not exist"
    for key in recipeList:
        if recipeList[key].name == recipe_name:
            recipeList.pop(key, None)
            returnMess = "Successfully deleted the recipe"
            break

    return {"message": returnMess}


@app.post("/recipes")
def post_recipe(recipe: recipe):
    valid = True
    for key in recipeList:
        if recipeList[key].name == recipe.name:
            valid = False

    print(valid)
    returnMess = "Error: Recipe with that name already exists!"
    if valid:
        recipeList[len(recipeList)] = recipe
        returnMess = "Successfully Added New Recipe"

    return {"message": returnMess}


@app.get("/macros")
def getRecipesByMacros(min_protein: int, max_protein: int, min_carbs: int, max_carbs: int, min_fat: int, max_fat: int):
    matching_recipes = []
    for key in recipeList:
        macros = recipeList[key].macros
        if (macros["protein"] >= min_protein and macros["protein"] <= max_protein and
                macros["carbs"] >= min_carbs and macros["carbs"] <= max_carbs and
                macros["fat"] >= min_fat and macros["fat"] <= max_fat):
            matching_recipes.append(recipeList[key])
    if len(matching_recipes) == 0:
        return {"message": "No recipes found for given macros."}
    else:
        return {"recipes": [recipe.to_dict() for recipe in matching_recipes]}


@app.put("/macros")
def update_recipe_macros(macroChange: macroUpdate):
    returnMess = "Error: Recipe does not exist"
    for i in recipeList:
        if recipeList[i].name == macroChange.name:
            recipeList[i].macros.carbs = macroChange.carbs
            recipeList[i].macros.protein = macroChange.protein
            recipeList[i].macros.fat = macroChange.fat
            return {"message": "Recipe macros updated successfully"}

    return {"message": returnMess}

# @app.put("/recipes/macros")
# def update_recipe_macros(new_macro:macroUpdate):
#     print("Hello")
#     # for i in range(len(recipeList)):
#     #     if recipeList[i].name == recipe_name:
#     #         recipeList[i].carbs = carbs
#     #         recipeList[i].protein = protein
#     #         recipeList[i].fat = fat
#     #         return {"message": "Recipe macros updated successfully"}
#     return {"message": "Recipe not found"}