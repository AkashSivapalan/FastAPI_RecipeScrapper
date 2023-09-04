import requests
import json
from pydantic import BaseModel
from typing import List
from dataclasses import asdict


class ingrediant(BaseModel):
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


# class CustomJSONEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, ingrediant):
#             return obj.__dict__
#         elif isinstance(obj, macro):
#             return obj.__dict__
#         return super().default(obj)


url = "https://coe892recipeproject.azurewebsites.net/"


def getRecipes():
    x = requests.get(url + "/recipes").json()
    for recp in x['Recipes']:
        print("")
        rec = x['Recipes'][recp]
        print("Name:" + rec['name'])
        ingrediantsprint = "Ingrediants:"
        for ing in rec['ingrediants']:
            ingrediantsprint += "\n" + "\t" + ing['name'] + ": " + str(ing['quantity']) + " " + ing['measurement']
        print(ingrediantsprint)
        print("Protein:" + str(rec['macros']['protein']))
        print("Carbs:" + str(rec['macros']['carbs']))
        print("Fat:" + str(rec['macros']['fat']))
        print("Author:" + rec['author'])
        print("")


def getAuthorRecipes(author):
    x = requests.get(url + "/recipeIng/" + author).json()
    print("this:", x["Recipes"])
    for recp in x["Recipes"]:
        print("")
        rec = x["Recipes"][recp]
        print("Name:" + rec['name'])
        ingrediantsprint = "Ingrediants:"
        for ing in rec['ingrediants']:
            ingrediantsprint += "\n" + "\t" + ing['name'] + ": " + str(ing['quantity']) + " " + ing['measurement']
        print(ingrediantsprint)
        print("Protein:" + str(rec['macros']['protein']))
        print("Carbs:" + str(rec['macros']['carbs']))
        print("Fat:" + str(rec['macros']['fat']))
        print("Author:" + rec['author'])
        print("")


def getRecipesByIngrediants(ingrediants):
    x = requests.get(url + "/recipeIng",params={"ingredients":ingrediants}).json()
    # if not x["Recipes"]:
    #     print(f"No recipes found containing {ingrediants}")
    # else:
    for recp in x["Recipes"]:
        print("")
        rec = x["Recipes"][recp]
        print("Name:" + rec['name'])
        ingrediantsprint = "Ingrediants:"
        for ing in rec['ingrediants']:
            ingrediantsprint += "\n" + "\t" + ing['name'] + ": " + str(ing['quantity']) + " " + ing['measurement']
        print(ingrediantsprint)
        print("Protein:" + str(rec['macros']['protein']))
        print("Carbs:" + str(rec['macros']['carbs']))
        print("Fat:" + str(rec['macros']['fat']))
        print("Author:" + rec['author'])
        print("")

def update_recipe_ingrediants(recipe_name, name, quantity, measurement):
    response = requests.put(f"{url}/recipe",
                            json={"recipe name": recipe_name, "name": name, "quantity": quantity, "measurement": measurement}).json()

    print(response['message'])


def put_recipe_name(old_recipe_name, new_recipe_name):
    x = requests.put(url + "/recipes/" + old_recipe_name,
                     json={"old_name": old_recipe_name, "new_name": new_recipe_name}).json()
    print(x['message'])
    print()


def delete_recipe_name(recipe_name):
    x = requests.delete(url + "/recipes/" + recipe_name).json()
    print(x['message'])
    print()


def post_recipe(r):
    recipe_dict = {
        "name": r.name,
        "author": r.author,
        "macros": {
            "protein": r.macros.protein,
            "carbs": r.macros.carbs,
            "fat": r.macros.fat
        },
        "ingrediants": [
            {
                "name": i.name,
                "quantity": i.quantity,
                "measurement": i.measurement
            }
            for i in r.ingrediants
        ]
    }

    x = requests.post(url + "/recipes", json=recipe_dict).json()

    print("Finished")
    print(x)
    print()


def getRecipesByMacros():
    # take user inputs for macro ranges
    min_protein = int(input("Enter minimum protein (in grams):\n"))
    max_protein = int(input("Enter maximum protein (in grams):\n"))
    min_carbs = int(input("Enter minimum carbs (in grams):\n"))
    max_carbs = int(input("Enter maximum carbs (in grams):\n"))
    min_fat = int(input("Enter minimum fat (in grams):\n"))
    max_fat = int(input("Enter maximum fat (in grams):\n"))

    # send GET request to API with macro ranges as query params
    url = "http://127.0.0.1:8000"
    params = {
        "min_protein": min_protein,
        "max_protein": max_protein,
        "min_carbs": min_carbs,
        "max_carbs": max_carbs,
        "min_fat": min_fat,
        "max_fat": max_fat,
    }
    response = requests.get(f"{url}/recipes", params=params)

    # print returned recipes
    recipes = response.json().get("recipes", [])
    if len(recipes) == 0:
        print("No recipes found for given macros.")
    else:
        for recipe in recipes:
            print("Name:", recipe["name"])
            ingredients = recipe.get("ingredients", [])
            ingrediantsprint = "Ingredients:"
            for ing in ingredients:
                ingrediantsprint += "\n" + "\t" + ing["name"] + ": " + str(ing["quantity"]) + " " + ing["measurement"]
            print(ingrediantsprint)
            macros = recipe.get("macros", {})
            print("Protein:" + str(macros.get("protein", "")))
            print("Carbs:" + str(macros.get("carbs", "")))
            print("Fat:" + str(macros.get("fat", "")))
            print("Author:" + recipe.get("author", ""))
            print("")


def update_recipe_macros(recipe_name, protein, carbs, fat):
    response = requests.put(f"{url}/macros",
                            json={"name": recipe_name, "protein": protein, "carbs": carbs, "fat": fat}).json()

    print(response['message'])


while True:
    print(
        "Enter a number to select a command to execute:\n 1.)Get Recipes\n 2.)Get Recipes by an Author\n 3.)Update a recipe name\n 4.)Delete a recipe by name\n 5.)Post a recipe\n 6.)Update macros\n 7.)Get receipe ingredients\n")
    inp = ""
    inp = input('Enter a command\n')
    if (inp == 'q'):
        break
    elif (inp == '1'):
        getRecipes()

    elif (inp == '2'):
        author = ""
        author = input("Enter an author name\n")
        getAuthorRecipes(author)
    elif (inp == '3'):
        old_recipe_name = ""
        old_recipe_name = input("Enter a recipe name to update\n")
        new_recipe_name = ""
        new_recipe_name = input("Enter a new recipe name for the update\n")
        put_recipe_name(old_recipe_name, new_recipe_name)
    elif (inp == '4'):
        recipe_name_delete = ""
        recipe_name_delete = input("Enter a recipe name to delete\n")
        delete_recipe_name(recipe_name_delete)
    elif (inp == '5'):
        recipeAdd = recipe(name="", ingrediants=[], macros=macro(protein=0, carbs=0, fat=0), author="")

        recipe_name = ""
        recipe_name = input("Enter a recipe name\n")

        recipeAdd.name = recipe_name

        recipe_ingrediants = []
        ValidRecipe = True
        doneIngList = False
        while (ValidRecipe and (not doneIngList)):
            ingrediantName = ""
            ingrediantName = input("Enter an ingrediant name\n")
            quant = 0
            try:
                quantityInp = ""
                quantityInp = input("Enter quantity of ingrediant\n")
                quant = int(quantityInp)
            except:
                ValidRecipe = False
            ingrediantMeasurement = ""
            ingrediantMeasurement = input("Enter a unit for measurements(Type enter to leave out measurement)\n")

            if ValidRecipe:
                recipeAdd.ingrediants.append(
                    ingrediant(name=ingrediantName, quantity=quant, measurement=ingrediantMeasurement))
                cont = input("Type 'Y' to enter another ingrediant. Else, continue to macro input\n")
                if cont != 'Y':
                    doneIngList = True
        mac = None
        if ValidRecipe:
            try:
                proteinInp = ""
                proteinInp = input("Enter protein(in grams) for the recipe\n")
                proteinnum = int(proteinInp)
                carbInp = ""
                carbInp = input("Enter carbs(in grams) for the recipe\n")
                carbnum = int(carbInp)
                fatInp = ""
                fatInp = input("Enter fat(in grams) for the recipe\n")
                fatnum = int(fatInp)

                mac = macro(protein=proteinnum, carbs=carbnum, fat=fatnum)
                recipeAdd.macros = mac
            except:
                ValidRecipe = False
        if ValidRecipe:
            new_author = ""
            new_author = input("Enter the name of the author\n")

            recipeAdd.author = new_author
            post_recipe(recipeAdd)
        else:
            print("Make sure you enter a valid recipe")
    elif inp == '6':
        recipe_name = input("Enter the name of the recipe to update\n")
        new_protein = input("Enter the new protein value (in grams) for the recipe\n")
        new_carbs = input("Enter the new carbs value (in grams) for the recipe\n")
        new_fat = input("Enter the new fat value (in grams) for the recipe\n")
        update_recipe_macros(recipe_name, int(new_protein), int(new_carbs), int(new_fat))
    elif (inp == '7'):
        ingrediants = ""
        ingrediants = input("Enter ingredients\n")
        getRecipesByIngrediants(ingrediants)
    else:
        print("Invalid command")