import openfoodfacts


def query_off(query):
    '''inport the first six products from Openfoodfacts to give choice to the user'''
    search_result = openfoodfacts.products.search(query , page=1 , page_size=6 , sort_by='unique_scans' ,
                                                  locale='fr')
    p = search_result['products']

    list = []

    for i in range(len(p)):
        p_name = search_result["products"][i]['product_name_fr']
        n_grade = search_result["products"][i]['nutrition_grade_fr']
        img = search_result["products"][i]['image_front_thumb_url']
        category = search_result["products"][i]['categories']
        #Treat just one category
        cat = category.split(',')[0]
        url_off = search_result["products"][i]['url']

        dict = {
            'product_name' : p_name,
            'nutriscore' : n_grade,
            'img' : img,
            'category' : cat,
            'url' : url_off
        }
        list.append(dict)

    return  list


def single_product(query):
    search_result = openfoodfacts.products.search(query , page=1 , page_size=1 , sort_by='unique_scans' ,
                                                  locale='fr')

    category = search_result["products"][0]['categories']
    cat = category.split(',')[0]


    return cat
