import openfoodfacts
import requests

def data_process(products):
    '''function which keeps only data we need from the OpenFood Facts return
    we extract the first product'''
    list = []
    for i in range(6):
        dict = {
            'product_name' : products[i]['product_name_fr'],
            'nutriscore' : products[i]['nutrition_grades'].upper(),
            'img' : products[i]['image_front_thumb_url'],
            # keep the last category the most significant
            'category' : products[i]['categories'].split(',')[-1],
            'url' : products[i]['url'],
        }

        list.append(dict)

    return list

    #
    #
    #
    # for i in range(len(p)):
    #     try:
    #         p_name = result["products"][i]['product_name_fr']
    #     except KeyError:
    #         p_name = result["products"][i]['product_name']
    #
    #     #some products have no nutriscore
    #     try:
    #
    #         n_grade = result["products"][i]['nutrition_grades'].upper()
    #     except KeyError:
    #         n_grade = 'null'
    #
    #     img = result["products"][i]['image_front_thumb_url']
    #     category = result["products"][i]['categories']
    #
    #
    #     cat = category.split(',')[-1]
    #     url_off = result["products"][i]['url']
    #
    #     dict = {
    #         'product_name' : p_name,
    #         'nutriscore' : n_grade,
    #         'img' : img,
    #         'category' : cat,
    #         'url' : url_off
    #     }
    #     list.append(dict)
    #     #we remove item with no n_grade
    #     for dict_items in list:
    #         if dict_items['nutriscore'] == 'null':
    #             list.remove(dict_items)
    # return list

def query_off(query):
    '''inport the first six products from Openfoodfacts to give choice to the user'''

    url = "https://fr.openfoodfacts.org/cgi/search.pl?search_terms={}&search_simple=1&action=process&json=1".format(query)
    response = requests.get(url)
    result = response.json()
    products = result['products']

    # result = openfoodfacts.products.search(query , page=1 , page_size=1, sort_by='unique_scans' ,
    #                                               locale='fr')
    return data_process(products)


def request_off(cat, ns):
    '''look for a substitute in the same category as the selected product'''
    # url = "https://fr.openfoodfacts.org/categorie/{}/1.json".format(cat)
    url_begin = "https://fr.openfoodfacts.org/cgi/search.pl?"
    payload = {
        'action' : 'process',
         'tagtype_0' : 'categories',
         'tag_contains_0' : 'contains',
         'tag_0' : cat,
         'tagtype_1' : 'nutrition_grades',
         'tag_contains_1' : 'contains',
         'tag_1' : ns,
         'sort_by' : 'unique_scans_n',
         'page_size' : '20',
         'axis_x' : 'energy',
         'axis_y' : 'product_n',

         'json' : '1',

     }

    response = requests.get(url_begin, params=payload)
    result = response.json()
    return result['products'] # = une liste de dictionnaires


def best_substitute(cat):
    '''create a list of the top six substitute products'''
    ns_list = ["A", "B" , "C" , "D" , "E"]

    # while len(res) < 6:
    for ns in ns_list:
        #res est une liste de deux dictionnaires
        res = request_off(cat, ns)


        # products_treaty = data_process(products)

    print(res, len(res), type(res))

    # #
    # # #sort the list with n_grade id
    # # for ns in ns_list:
    # #     for dict_items in list:
    # #          if dict_items['nutriscore'] == ns:
    # #             response.append(dict_items)
    #
    # # return only the six first item to the front
    # return response[:6]




if __name__ == '__main__':

    cat = ' Pâtes à tartiner aux noisettes et au cacao'
    best_substitute(cat)

