import requests, time, keys

EDAMAM_APP_KEY = # insert app key
EDAMAM_APP_ID = # insert app ix


def get_food_options(food):
    global EDAMAM_APP_KEY
    global EDAMAM_APP_ID
    if(EDAMAM_APP_ID == "" or EDAMAM_APP_KEY == ""):
        edkeys = keys.get_key("edamam")
        EDAMAM_APP_ID = edkeys[0]
        EDAMAM_APP_KEY = edkeys[1]
    url = "https://api.edamam.com/api/food-database/parser?ingr="+food+"&app_id="+EDAMAM_APP_ID+"&app_key="+EDAMAM_APP_KEY+"&page=0"
    food_opt = requests.get(url).json()
    # print(food_opt['parsed'][0]['food']['label'])  # same as num 0 in hints below
    # print(food_opt['parsed'][0]['food']['uri'])

    # food_json = {"yield": 1, 'ingredients': [None, None, None]}   # too many ingredients...
    # food_size = min(len(food_opt['hints']), 3)
    # for i in range(0, food_size):
    #     # print(food_opt['hints'][i]['food']['label'])
    #     food_json['ingredients'][i] = {"quantity": 1,
    #                                    "measureURI": food_opt['hints'][i]['measures'][1]['uri'],
    #                                    "foodURI": food_opt['hints'][i]['food']['uri'],
    #                                    "label": food_opt['hints'][i]['food']['label']
    #                                    }

    food_size = min(len(food_opt['hints']), 3)
    food_json = {"yield": 1, 'ingredients': [{  "quantity": 1,
                                                "measureURI": food_opt['hints'][0]['measures'][1]['uri'],
                                                "foodURI": food_opt['hints'][0]['food']['uri'],
                                                "label": food_opt['hints'][0]['food']['label']
                                       }]}
    return food_json


def get_food_nutrients(food_json):
    url = "https://api.edamam.com/api/food-database/nutrients?&app_id="+EDAMAM_APP_ID+"&app_key="+EDAMAM_APP_KEY
    nutrients = requests.post(url, json=food_json).json()
    print(nutrients['calories'])
    print(nutrients['dietLabels'])
    print(nutrients['healthLabels'])
    print(nutrients['cautions'])
    print(nutrients['uri'])


def print_food_json(food_json):
    for i in food_json['ingredients']:
        # print food_list['ingredients'][i]
        print(food_json['ingredients'][i]['label'])
        print(food_json['ingredients'][i]['foodURI'])


if __name__ == '__main__':
    food_json = get_food_options('Green Tea')
    # print(food_json)
    # print_food_json(food_json)
    get_food_nutrients(food_json)
