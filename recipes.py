import json
import requests


def recipe():
    print("hello world")

    # data to write to mongodb atlas database
    # api-endpoint
    apiKey = "21be7e405b574db1bb7c1218aa4808ee"
    URL = "https://api.spoonacular.com/recipes/search?apiKey="+apiKey+"&query=<string>&cuisine=<string>&diet=<string>&excludeIngredients=<string>&intolerances=<string>&offset=<number>&number=<number>&limitLicense=<boolean>&instructionsRequired=<boolean>"
    testURL = "https://api.spoonacular.com/recipes/search?apiKey="+apiKey+"&query=&cuisine=&diet=&excludeIngredients=&intolerances=&offset=&number=&limitLicense=&instructionsRequired="
    # stuff given here
    query = ""
    cuisine = ""
    diet = ""
    excludeIngredients = ""
    intolerances = ""
    offset = ""
    number = str(100)
    limitLicense = ""
    instructionsRequired = ""
    print("hello world")
    # defining a params dict for the parameters to be sent to the APIt

    PARAMS = {
        'query': query,
        'cuisine': cuisine,
        'diet': diet,
        'excludeIngredients': excludeIngredients,
        'intolerances': intolerances,
        'offset': offset,
        'number': number,
        'limitLicense': limitLicense,
        'instructionsRequired': instructionsRequired
    }
    testURL2 = "https://api.spoonacular.com/recipes/search?apiKey="+apiKey+"&query=" + query + "&cuisine=" + cuisine + "&diet=" + diet + "&excludeIngredients=" + excludeIngredients + "&intolerances=" + intolerances + "&offset=" + offset + "&number=" + number + "&limitLicense=" + limitLicense + "&instructionsRequired=" + instructionsRequired
    # sending get request and saving the response as response object
    r = requests.get(testURL2, json=PARAMS)

    # extracting data in json format
    data = r.json()
    for i in range(100):
        try:
            que = data['results'][i]
            testURL3 = "https://api.spoonacular.com/recipes/informationBulk?apiKey="+apiKey+"&ids="+str(que["id"])+"&includeNutrition=true"
            PARAMS2 = {
                "ids" : que['id'],
                "includeNutrition": True
            }
            r = requests.get(testURL3, json=PARAMS2)
            data2 = r.json()[0]
            alogirthmScore = ((data2["weightWatcherSmartPoints"] + data2["spoonacularScore"])*0.1) + (data2["healthScore"]*0.25)
            if data2["veryHealthy"] == True:
                alogirthmScore += 1
            if data2["cheap"]==True:
                alogirthmScore += 1
            if data2["veryPopular"] == True:
                alogirthmScore += 1
            if data2["sustainable"]==True:
                alogirthmScore += 1
            print(alogirthmScore)
            tt = data2["extendedIngredients"]
            ingredientArray=[]
            for x in tt:
                ingredientArray.append( {
                    "name": x["name"],
                    "originalName": x["originalName"],
                    "image": x["image"],
                    "amount": x["amount"],
                    "unit": x["unit"]
                })
            RECIPE_PARAMS = {

                "title":data["results"][i]['title'],

                "restrictions": {
                    "vegetarian": data2['vegetarian'],
                    "vegan": data2["vegan"],
                    "glutenFree": data2["glutenFree"],
                    "dairyFree": data2["dairyFree"]
                },

                "pointSystem": alogirthmScore,

                "cookTime": {
                    "prepMin": data2["preparationMinutes"],
                    "cookMin": data2["cookingMinutes"],
                    "readyInMin": data2["readyInMinutes"]

                },

                "breakCal": {
                    "percentProtein": data2["nutrition"]["caloricBreakdown"]["percentProtein"],
                    "percentFat": data2["nutrition"]["caloricBreakdown"]["percentFat"],
                    "percentCarbs": data2["nutrition"]["caloricBreakdown"]["percentCarbs"]
                },
                "ingredients": ingredientArray,

                "weightPerServing": {
                    "amount": data2["nutrition"]['weightPerServing']["amount"],
                    "unit": data2["nutrition"]['weightPerServing']["unit"],
                    "servings": data2["servings"]
                }
            }

            if len(data2["analyzedInstructions"])!=0:
                RECIPE_PARAMS["instructions"]=data2["analyzedInstructions"][0]["steps"]
            print(RECIPE_PARAMS)
        except:
            print("uhoh")
# print(data)
#
# print("Helloworld")
# # extracting latitude, longitude and formatted address
# # of the first matching location
# latitude = data['query'][0]['cuisine']['diet']['excludeIngredients']['intolerances']['offset']['number']['limitLicense']['instructionsRequired']
# longitude = data['query']['cuisine']['diet']['excludeIngredients']['intolerances']['offset']['number']['limitLicense']['instructionsRequired']
# formatted_address = data['query']['formatted_address']
#
# # printing the output
# print("Latitude:%s\nLongitude:%s\nFormatted Address:%s"
#     %(number, longitude,formatted_address))


def main():
    # data to write to jsond
    recipe()


main()
