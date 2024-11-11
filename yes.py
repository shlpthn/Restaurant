from flask import Flask, render_template, request, redirect, url_for
from  flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdefgh'
socketio = SocketIO(app)
orders = []

menu_data = {
    'Appetizers': [
        {'name': 'Samosa', 
         'description': 'Spiced potatoes and peas wrapped in pastry and deep-fried.', 
         'price': 20},
        {'name': 'Paneer Tikka', 
         'description': 'Marinated cottage cheese cubes grilled or baked, served with chutney.', 
         'price': 150},
        {'name': 'Chicken Seekh Kebab',
         'description': 'Spicy minced chicken skewers.', 
         'price': 200},
        {'name': 'Aloo Tikki',
         'description': 'Crispy potato patties served with chutney.', 
         'price': 50},
        {'name': 'Hara Bhara Kabab',
         'description': 'Green vegetable patty with spices.', 
         'price': 100}
    ],
    'Main Courses': [
        {'name': 'Butter Chicken', 
         'description': 'Creamy and mildly spiced chicken curry, often paired with naan or rice.', 
         'price': 300},
        {'name': 'Paneer Butter Masala', 
         'description': 'Rich tomato-based curry with paneer.', 
         'price': 250},
        {'name': 'Dal Makhani', 
         'description': 'Creamy, slow-cooked black lentils simmered in spices and butter.', 
         'price': 180},
        {'name': 'Chole Bhature', 
         'description': 'Spicy chickpea curry served with fluffy deep-fried bread.', 
         'price': 120},
        {'name': 'Rogan Josh', 
         'description': 'Kashmiri lamb curry with aromatic spices.', 
         'price': 350},
        {'name': 'Vegetable Biryani', 
         'description': 'Fragrant rice with spiced vegetables.', 
         'price': 200},
        {'name': 'Chicken Biryani', 
         'description': 'Classic spiced rice with marinated chicken.', 
         'price': 250},
        {'name': 'Palak Paneer', 
         'description': 'Spinach puree cooked with soft paneer cubes, flavored with spices.', 
         'price': 220}
    ],
    'Indian Breads': [
        {'name': 'Naan', 
         'description': 'Soft and fluffy leavened bread.', 
         'price': 30},
        {'name': 'Butter Naan', 
         'description': 'Leavened bread brushed with butter.', 
         'price': 40},
        {'name': 'Garlic Naan', 
         'description': 'Naan topped with garlic and herbs.', 
         'price': 50},
        {'name': 'Tandoori Roti', 
         'description': 'Whole wheat bread cooked in a tandoor.', 
         'price': 20},
        {'name': 'Missi Roti', 
         'description': 'Spiced flatbread made with gram flour.', 
         'price': 25},
        {'name': 'Paratha', 
         'description': 'Layered and flaky Indian flatbread.', 
         'price': 30},
        {'name': 'Aloo Paratha', 
         'description': 'Stuffed flatbread with spiced potatoes.', 
         'price': 40}
    ],
    'Desserts': [
        {'name': 'Gulab Jamun', 
         'description': 'Deep-fried dumplings soaked in syrup.', 
         'price': 40},
        {'name': 'Rasgulla', 
         'description': 'Soft cheese balls in sugar syrup.', 
         'price': 50},
        {'name': 'Kheer', 
         'description': 'Rice pudding with milk and dry fruits.', 
         'price': 70},
        {'name': 'Jalebi', 
         'description': 'Crispy, syrupy fried spirals.', 
         'price': 30},
        {'name': 'Rabri', 
         'description': 'Thickened sweetened milk dessert.', 
         'price': 90}
    ]
}
@app.route('/')
def menu():
    return render_template('menu.html', menu_data=menu_data)

@app.route('/order', methods=['POST'])
def order():
    order_items = []
    total_cost = 0.0
    
    for item_name, quantity in request.form.items():
        if quantity.isdigit() and int(quantity) > 0:
            for category, items in menu_data.items():
                for item in items:
                    if item['name'] == item_name:
                        item_cost = item['price'] * int(quantity)
                        total_cost += item_cost
                        order_items.append({'name': item_name, 'quantity': quantity, 'cost': item_cost})
    socketio.emit('new_order', {'order_items': order_items, 'total_cost': total_cost})

    return render_template('bill.html', order_items=order_items, total_cost=total_cost)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html',orders=orders)

@app.route('/clear_orders', methods=['POST'])
def clear_orders():
    global orders
    orders.clear()  
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    socketio.run(app, debug=True)