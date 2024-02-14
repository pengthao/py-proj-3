from flask import Blueprint, render_template, redirect, url_for, session
from project.models import melon_list, Melon
from project.melons.forms import AddForm
from pprint import pprint

melons_blueprint = Blueprint('melons', __name__,template_folder='templates/melons')

@melons_blueprint.route('/all_melons')
def all_melons():

    melons = melon_list()
    for melon in melons:
        session[melon.melon_id] = melon.to_dict()
        
    pprint(session)
    return render_template('all_melons.html', melons=melons)


@melons_blueprint.route('/melon_details/<melon_id>', methods=["GET", "POST"])
def melon_details(melon_id):
    print(f'melon id {melon_id}') 
    pprint(session['cren'])
    session_melon = session.get(str(melon_id), {})
    print(f"session melon before dictionary {session_melon}")
    melon = Melon.from_dict(session_melon)

    print(type(f"type {melon}"))
    print(f'melon {melon}') 
    print(f"session melon {session_melon}")

    form = AddForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        print("Validation is successful.")
        
        melon_update = None

        if 'cart' in session:
            print('cart already in session')
            print(session['cart'])

        if 'cart' not in session:
            session['cart'] = {}
            print('cart initialized empty list')

        for melon in session['cart']:
            if melon_id == melon['melon_id']:
                melon['quantity'] += int(form.quantity.data)
                print(f'melon {melon}') 
                melon_update = melon
                break

        if melon_update is None:
            new_melon = Melon.to_dict(melon)
            new_melon['quantity'] = int(form.quantity.data)
            print(f'melon {new_melon}') 
            session['cart'].append(new_melon)
            
            print(f"session cart {session['cart']}")
            return redirect(url_for('cart.view_cart'))
        
    return render_template('melon_details.html', melon=melon, form=form)