import json
import requests
from pymongo import MongoClient


def wegwanRecipe():
    budget = 25
    sum = 0
    with open('testing1.json') as json_file:
        q = json.load(json_file)
        print(q)
    subscriptionKey = "2c623c20ad19466a8716287e72293079"
    URL = "https://api.spoonacular.com/recipes/search?subscription-key=" + subscriptionKey + "&query=<string>&cuisine=<string>&diet=<string>&excludeIngredients=<string>&intolerances=<string>&offset=<number>&number=<number>&limitLicense=<boolean>&instructionsRequired=<boolean>"
    alcoholURL = "https://api.wegmans.io/products/categories/6941-7004-3516?api-version=2018-10-18&subscription-key=2c623c20ad19466a8716287e72293079"
    alcoholics = []
    alcoholData = requests.get(alcoholURL)
    alcoholSet = alcoholData.json()
    tt = alcoholSet['products']
    for x in tt:
        alcoholics.append(x['name'])
    print(alcoholics)
    # stuff given here
    i = 0
    ingredientsArray = []
    for f in q['data'][0]['ingredients']:
        ingredientsArray.append(q['data'][0]['ingredients'][i]['name'])
        i+=1
    print(ingredientsArray)
    for i in range(len(ingredientsArray)):
        query = ingredientsArray[i]
        print(query)
        PARAMS = {
            'query': query
        }
        # URL looks like this "https://api.wegmans.io/products/search?query=Raspberry&api-version=2018-10-18&subscription-key={{Your-Subscription-Key}}"
        searchIngredientURL = "https://api.wegmans.io/products/search?query="+query+"&api-version=2018-10-18&subscription-key="+subscriptionKey

        r = requests.get(searchIngredientURL, json=PARAMS)

        #Dataset for the ID
        dataset = r.json()
        WAGWAN_SET = {
            "sku":dataset['results'][0]['sku'],
            "name":dataset['results'][0]['name']
        }
        j = 0
        while WAGWAN_SET['name'] in alcoholics or j ==0:
            WAGWAN_SET = {
                "sku":dataset['results'][j]['sku'],
                "name": dataset['results'][j]['name']
            }
            j =+ 1
        if WAGWAN_SET['name'] in alcoholics:
            print("HEllo")


        priceIngredientURL = "https://api.wegmans.io/products/"+WAGWAN_SET['sku']+"/prices?api-version=2018-10-18&subscription-key=2c623c20ad19466a8716287e72293079"
        PARAMS2 = {
            "sku":q
        }
        r2 = requests.get(priceIngredientURL, json=PARAMS2)
        dataset2 = r2.json()
        try:
            y = dataset2["stores"][0]["price"]
            print(y)
            sum = sum + float(y)
        except:
            print("that ingredient is unavailable")

    servings = q['data'][0]['weightPerServing']['servings']
    sum = round(sum,2)
    avgSum = sum/servings
    avgSum = round(avgSum,2)
    print(sum)
    print(avgSum)

def main():
    wegwanRecipe()




main()