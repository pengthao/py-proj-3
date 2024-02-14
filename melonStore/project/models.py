import os
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from project import login_manager





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



#######USERS###########

bcrypt = Bcrypt()

customers = {
    'mel': {'username': 'mel', 'password': 'password', 'name': 'Mel Wilson'},
    'squash': {'username': 'squash', 'password': '1234', 'name': 'Sara Squash'},
    'bunsen': {'username': 'bunsen', 'password': 'muppet', 'name': 'Bunsen Honeydew'},
    'hoon': {'username': 'hoon', 'password': 'blindmelon', 'name': 'Shannon Hoon'}
}



class User(UserMixin):
    def __init__(self, username, password, name):
        self.id = username
        self.username = username
        self.password_hash = bcrypt.generate_password_hash(password)
        self.name = name

    def to_dict(self):
        return {
            'username' : self.username,
            'password' : self.password_hash,
            'name' : self.name
        }

    @classmethod
    def from_dict(cls, user):
        return cls(
            user['username'],
            user['password'],
            user['name']
        )

    def check_password(self,password):
        return bcrypt.check_password_hash(self.password_hash, password=password)

@login_manager.user_loader
def get_by_username(username):
    user_data = customers.get(username)
    return User.from_dict(user_data) if user_data else None