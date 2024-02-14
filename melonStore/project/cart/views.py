from flask import Blueprint, render_template, redirect, url_for, session
from project.models import Melon



cart_blueprint = Blueprint('cart', __name__,template_folder='templates/cart')

@cart_blueprint.route('/view_cart')
def view_cart():
    melon_list = []
    for melons in session['cart']:
        melon = Melon.from_dict(melons)
        melon_list.append(melon)

    return render_template('cart.html', melon_list=melon_list)