
import requests

def data_process(products):
    '''function which keeps only data we need from the OpenFood Facts return
    we extract the first product'''
    list = []
    for i in range(6):
        try:
            dict = {
                'product_name' : products[i]['product_name'],
                'nutriscore' : products[i]['nutrition_grades'].upper(),
                'img' : products[i]['image_thumb_url'],

                # keep the last category the most significant
                'category' : products[i]['categories'].split(',')[-1],
                'url' : products[i]['url'],
            }
        # some products in OFF database have no image, we get image_igredients
        except KeyError:
            dict = {
                'product_name' : products[i]['product_name'],
                'nutriscore' : products[i]['nutrition_grades'].upper(),
                'img' : products[i]['image_ingredients_small_url'],
                # keep the last category the most significant
                'category' : products[i]['categories'].split(',')[-1],
                'url' : products[i]['url'],
            }
        list.append(dict)

    return list



def query_off(query):
    '''inport the first six products from Openfoodfacts to give choice to the user'''

    url = "https://fr.openfoodfacts.org/cgi/search.pl?search_terms={}&search_simple=1&action=process&json=1".format(query)
    response = requests.get(url)
    result = response.json()
    products = result['products']

    return data_process(products)


def request_off(cat, ns):
    '''look for a substitute in the same category as the selected product'''

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
    list = []
    while len(list) < 2:
        for ns in ns_list:
            #res est une liste de deux dictionnaires
            res = request_off(cat, ns)
            for dict in res:
                list.append(dict)
    return data_process(list)




if __name__ == '__main__':

    cat = ' Pâtes à tartiner aux noisettes et au cacao'
    best_substitute(cat)

