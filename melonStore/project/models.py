import os
from flask import request
from flask_bcrypt import Bcrypt
from flask_restful import Resource, Api
from flask_login import UserMixin
#from flask_jwt import JWT, jwt_required
from project import login_manager, app

api = Api(app)

class Melon:
    def __init__(self, melon_id, common_name, price, image_url, color, seedless):
        self.melon_id = melon_id
        self.common_name = common_name
        self.price = price
        self.image_url = image_url
        self.color = color
        self.seedless = seedless

    def to_dict(self):
        return {
            'melon_id' : self.melon_id,
            'common_name' : self.common_name,
            'price' : self.price,
            'image_url' : self.image_url,
            'color' : self.color,
            'seedless' : self.seedless
        }
    
    @classmethod
    def from_dict(cls, melon):
        return cls(
            melon['melon_id'],
            melon['common_name'],
            melon['price'],
            melon['image_url'],
            melon['color'],
            melon['seedless']
        )
    
    def __str__(self):
        return f"{self.common_name} (ID: {self.melon_id})"
    
    def display_img(self):
        return self.image_url
    
    def all_melon_display(self):
        return f"Melon: {self.common_name}\n Price:{self.price}\n Seedless: {self.seedless}"
    
    def display_details(self):
        return f"""
            Name: {self.common_name}
            Price: {self.price}
            Color: {self.color}
            Seedless: {self.seedless}
        """
    
    def to_csv(self):
        return f"{self.melon_id},{self.common_name},{self.price},{self.image_url},{self.color},{str(self.seedless).lower()}"
    

def melon_list():
    melons = []
    file_path = os.path.join(os.path.dirname(__file__), "melons.csv")
    with open(file_path) as csvfile:
        next(csvfile)
        for line in csvfile:
            melon_data = line.strip().split(',')
            melon = Melon(
                melon_data[0],
                melon_data[1],
                float(melon_data[2]),
                melon_data[3],
                melon_data[4],
                melon_data[5].lower() == 'true'
            )
            melons.append(melon)
    return melons

def write_melon(melons, output_file="melons.csv"):
    file_path = os.path.join(os.path.dirname(__file__), output_file)
    with open(file_path, 'w') as csvfile:
        csvfile.write("melon_id,common_name,price,image_url,color,seedless\n")
        for melon in melons:
            csvfile.write(melon.to_csv() + "\n")

#######USERS###########

bcrypt = Bcrypt()

customers = {
    'mel': {'username': 'mel', 'password': 'password', 'name': 'Mel Wilson'},
    'squash': {'username': 'squash', 'password': '1234', 'name': 'Sara Squash'},
    'bunsen': {'username': 'bunsen', 'password': 'muppet', 'name': 'Bunsen Honeydew'},
    'hoon': {'username': 'hoon', 'password': 'blindmelon', 'name': 'Shannon Hoon'}
}



class User(UserMixin):
    def __init__(self, username, password_hash, name):
        self.id = username
        self.username = username
        self.password_hash = password_hash
        self.name = name

    def to_dict(self):
        return {
            'username' : self.username,
            'password' : self.password_hash,
            'name' : self.name
        }
    
    def __str__(self):
        return f"User Id: {self.id}"

    @classmethod
    def from_dict(cls, user):
        return cls(
            user['username'],
            user['password'],
            user['name']
        )

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

@login_manager.user_loader
def get_by_username(username):
    user_data = customers.get(username)
    return User.from_dict(user_data) if user_data else None


'''username_table = {u.username: u for u in customers}
userid_table = {u.id: u for u in customers}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and bcrypt.check_password_hash(user.password_hash, password=password) == True:
        return user
    
def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)'''

#jwt = JWT(app, authenticate, identity)

########### REST #########################

class MelonInfo(Resource):
    #@jwt_required()
    def get(self, name):
        m_list = melon_list()
        
        for melon in m_list:
            if melon.common_name == name:
                return melon.to_dict()  
                
        return {'name': None}, 404
            
class AddMelon(Resource):
    #@jwt_required()
    def post(self):

        data = request.get_json()

        melon_id = data.get('melon_id')
        common_name = data.get('common_name')
        price = data.get('price')
        image_url = data.get('image_url')
        color = data.get('color')
        seedless = data.get('seedless')

        m_list = melon_list()
        melon = Melon(
            melon_id,
            common_name,
            price,
            image_url,
            color,
            seedless
        )
        m_list.append(melon)
        write_melon(m_list)

        return {'status': 'Melon added successfully'}, 201
            
        
class deleteMelon(Resource):
    #@jwt_required()
    def delete(self, id):
        m_list = melon_list()
        deleted_melons = [melon for melon in m_list if melon.melon_id == id]
        for melon in deleted_melons:
            m_list.remove(melon)

        write_melon(m_list)
        return {'note': 'delete success'}


class AllMelons(Resource):
    #@jwt_required()
    def get(self):
        m_list = melon_list()
        return [melon.to_dict() for melon in m_list]
    


api.add_resource(AllMelons, '/allmelons')
api.add_resource(MelonInfo, '/meloninfo/<string:name>')
api.add_resource(AddMelon, '/addmelon/')
api.add_resource(deleteMelon, '/deletemelon/<string:id>')

