from flask import Flask,request,jsonify
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

#define to_do_list objects
restaurants = []
menus = []
menu_items = []


#define to do list
#code 2XX means: Ok 200, created 201, accepted 202
#code 4XX means: bad request 400, not found 404

class Restaurant(Resource):
    @classmethod
    def get(cls, restaurant_name):
        restaurant = next(filter(lambda rest: rest['restaurant_name'] == restaurant_name, restaurants), None)
        if restaurant:
            return {'restaurant': 'restaurant'}, 200
        else:
            return 404

    @classmethod
    def post(cls, restaurant_name):
        if next(filter(lambda rest: rest['restaurant_name'] == restaurant_name, restaurants), None):
            return {'Error': 'This restaurant already exist'}, 400
        restaurant = {'restaurant_name': restaurant_name}
        restaurants.append(restaurant)
        return restaurant, 201

    @classmethod
    def delete(cls, restaurant_name):
        global restaurants
        restaurants = list(filter(lambda rest: rest['restaurant_name'] != restaurant_name, restaurants))
        return {'Delete': 'successfully'}


class Menu(Resource):
    @classmethod
    def get(cls, restaurant_menu):
        menu = next(filter(lambda menu: menu['restaurant_menu'] == restaurant_menu, menus), None)
        if menu:
            return {'menu': 'menu'}, 200
        else:
            return {'Error': 'Nothing can be found'}, 404

    @classmethod
    def post(cls, restaurant_menu):
        if next(filter(lambda menu: menu['restaurant_menu'] == restaurant_menu, menus), None):
            return {'Error': 'This menu already exists.'}, 400
        else:
            menu = {'restaurant_menu': 'restaurant_menu'}
            menus.append(menu)
            return menu, 201

    @classmethod
    def delete(cls, restaurant_menu):
        global menus
        menus = list(filter(lambda menu: menu['restaurant_menu'] != restaurant_menu, menus))
        return {'Delete': 'successfully'}


class MenuItem(Resource):
    @classmethod
    def get(cls, name):
        menu_item = next(filter(lambda item: item['name'] == name, menu_items), None)
        if menu_item:
            return {'menu_item': menu_item}, 200
        else:
            return 404

    menu_parser = reqparse.RequestParser()
    menu_parser.add_argument('price', type=float, required=True, help="The price is required.")

    @classmethod
    def post(cls, name):
        if next(filter(lambda item: item['name'] == name, menu_items), None):
            return {'Error': 'This item  already exists'}, 400
        data = MenuItem.menu_parser.parse_args()
        menu_item = {'name': name, 'price': data['price']}
        menu_items.append(menu_item)
        return menu_item, 201

    @classmethod
    def delete(cls, name):
        global menu_items
        menu_items = list(filter(lambda item: item['name'] != name, menu_items))
        return {'Delete': 'successfully'}

class AllMenuItems(Resource):
    @classmethod
    def get(cls):
        # returns all the menu items
        return {'All Menu Items': menu_items}


class AllMenus(Resource):
    @classmethod
    def get(cls):
        return {'All Menus': menus}


class AllRestaurants(Resource):
    @classmethod
    def get(cls):
        return {'Restaurants': restaurants}


## Actually setup the Api resource routing here
api.add_resource(AllMenus, '/menus')
api.add_resource(MenuItem, '/item/<string:name>')
api.add_resource(AllMenuItems, '/items')
api.add_resource(AllRestaurants, '/restaurants')
api.add_resource(Menu, '/menu/<string:name>')
api.add_resource(Restaurant, '/restaurant/<string:name>')

if __name__ == '__main__':
    app.run(port=5000, debug=True)