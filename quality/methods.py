import requests
import re



#test integration test
def is_even(nbr):
    """
        Cette fonction teste si un nombre est pair.
        """
    return nbr % 2 == 0



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
    return result['products'] # = a list of dictionaries

def data_process(products):
    '''function which keeps only data we need from the OpenFood Facts return
    we extract the first product'''
    list = []

    # we return a list that does not exceed 6 items
    # otherwise it is equal to the list of returned products
    if len(products) < 6:
        a = len(products)
    else:
        a = 6

    for i in range(a):

        dict = {
            'product_name': products[i].get('product_name', 'Non renseigné'),
            'nutriscore': products[i].get('nutrition_grades', 'NC').upper(),
            'img': products[i].get('image_front_url', 'image_ingredients_small_url'),

            # keep the last category the most significant
            'category': products[i]['categories'].split(',')[-1],
            'url': products[i]['url'],
            'img_nutrition': products[i].get('image_nutrition_url', 'Non renseigné'),
            'magasins': products[i].get('stores', 'Non renseigné')
        }
        list.append(dict)


    # processing of product names
    # in some case product_names have () or, inside
    # which prevents the correct operation of the rest of the program
    for i in range(len(list)):     # len(list) in case lenght list < 6
        m1 = re.search('(\,.*?$)', list[i]['product_name'])
        if m1 is not None:
            list[i]['product_name'] = list[i]['product_name'].replace(m1.group(0), '')

        m2 = re.search('(\(.*?$)', list[i]['product_name'])
        if m2 is not None:
            list[i]['product_name'] = list[i]['product_name'].replace(m2.group(0), '')


    return list

def query_off(query):
    '''inport the first six products from Openfoodfacts to give choice to the user'''

    url = "https://fr.openfoodfacts.org/cgi/search.pl?search_terms={}&search_simple=1&action=process&json=1".format(query)
    response = requests.get(url)
    result = response.json()
    products = result['products']
    return data_process(products)

def best_substitut(cat):
    '''create a list of the top six substitut products'''
    ns_list = ["A", "B", "C", "D", "E"]
    list = []
    for ns in ns_list:
        if len(list)<6:
            #res is a list of dictionaries
            res = request_off(cat, ns)
            for dict in res:
                list.append(dict)
    return data_process(list)

if __name__ == '__main__':
    #
    # cat = 'Sauces Pesto'
    # data = best_substitut(cat)
    # print(len(data), data[0]['img_nutrition'], data[5]['nutriscore'], data)

    #
    query = 'Pesto'
    data = query_off(query)
    print(data)
