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

    # removal of products without category
    result = []
    for i, e in enumerate(products):
        try:
            test1 = e['categories']
        except KeyError:
            result.append(products[i])

        # removal of products without name
        try:
            test2 = e['product_name']
        except KeyError:
            result.append(products[i])

        # removal of products without image
        try:
            test3 = e['image_front_url']
        except KeyError:
            result.append(products[i])

    products = [x for x in products if x not in result]
    # # we return a list that does not exceed 6 items
    # # otherwise it is equal to the list of returned products

    products = products[:6]

    # processing of product names
    # in some case product_names have () or, inside
    # which prevents the correct operation of the rest of the program
    for i, e in enumerate(products):

        m1 = re.search('(\,.*?$)', e['product_name'])
        if m1 is not None:

            e['product_name'] = e['product_name'].replace(m1.group(0), '')

        m2 = re.search('(\(.*?$)', e['product_name'])
        if m2 is not None:
            e['product_name'] = e['product_name'].replace(m2.group(0), '')



    # finally we extract only useful data
    list = []

    for i in range(len(products)):

        dict = {
            "product_name": products[i]['product_name'],
            "nutriscore": products[i].get('nutrition_grades', 'NC').upper(),
            "img": products[i]['image_front_url'],

            # keep the last category the most significant
            "category": products[i]['categories'].split(',')[-1],
            "url": products[i]['url'],
            "img_nutrition": products[i].get('image_nutrition_url', 'Non renseigné'),
            "magasins": products[i].get('stores', 'Non renseigné')
        }
        list.append(dict)

    return list

def query_off(query):
    '''inport the first six products from Openfoodfacts to give choice to the user'''

    url = "https://fr.openfoodfacts.org/cgi/search.pl?search_terms={}&search_simple=1&action=process&json=1".format(query)
    response = requests.get(url)
    result = response.json()
    products = result['products'][:20]
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
