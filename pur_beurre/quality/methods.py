import openfoodfacts

#Create a finction witch extracts item = { product_name,
#
#
# class SelectedProduct():
#     '''To enable the general use of the Product class
#      for basic filling as well as for using the program,
#      the constructor is empty and two functions are implemented
#      add (fill in the base) and select_product (create the product
#      object chosen by the user)'''
#
#     def __init__(self):
#         self.p_name = ""
#         self.n_grade = ""
#         self.cat_name = ""
#         self.url = ""
#         self.img = ""
#         self.category = ""
#         self.url_off = ""
#         self.id = 0
#         self.category_id = 0
#         self.substitut_id = 0


def query_off(query):

    # self.p_name = search_result["products"][0]['product_name_fr']
    # self.n_grade = search_result["products"][0]['nutrition_grade_fr']
    # self.img = search_result["products"][0]['image_small_url']
    # self.category = search_result["products"][0]['categories']
    # self.url_off = search_result["products"][0]['url']
    print("j'y suis")
    #We inport the first six products to give choice to the user
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

#
# def iteration(data):
#     for dict_item in data:
#         for
#         return dict_item
#
#
# if __name__ == '__main__':
#     # query = 'banane'
#     # list = query_off(query)
#     #
#     #
#     # print(list)
#
#     data = [{'category': 'Petit-déjeuners', 'nutriscore': 'e', 'url': 'https://fr.openfoodfacts.org/produit/3017620429484/nutella-ferrero', 'img': 'https://static.openfoodfacts.org/images/products/301/762/042/9484/front_fr.147.200.jpg', 'product_name': 'Nutella'}, {'category': 'Produits à tartiner', 'nutriscore': 'e', 'url': 'https://fr.openfoodfacts.org/produit/3017624047813/nutella', 'img': 'https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.200.jpg', 'product_name': 'Nutella'}, {'category': 'Produits à tartiner', 'nutriscore': 'e', 'url': 'https://fr.openfoodfacts.org/produit/3017620401473/nutella-ferrero', 'img': 'https://static.openfoodfacts.org/images/products/301/762/040/1473/front_fr.20.200.jpg', 'product_name': 'Nutella'}, {'category': 'Produits à tartiner', 'nutriscore': 'e', 'url': 'https://fr.openfoodfacts.org/produit/59032823/nutella', 'img': 'https://static.openfoodfacts.org/images/products/59032823/front_fr.48.200.jpg', 'product_name': 'Nutella'}, {'category': 'en:breakfasts', 'nutriscore': 'e', 'url': 'https://fr.openfoodfacts.org/produit/3017620402135/nutella-ferrero', 'img': 'https://static.openfoodfacts.org/images/products/301/762/040/2135/front_fr.57.200.jpg', 'product_name': 'Nutella'}]
#     dict_item = iteration(data)
#     print(dict_item)



parent_dict = [
    {'A':'val1','B':'val2', 'content': [["1.1", "2.2"]]},
    {'A':'val3','B':'val4', 'content': [["3.3", "4.4"]]}
]