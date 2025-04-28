from flask import Flask, render_template, request, jsonify, session
import os
from pathlib import Path

app = Flask(__name__, 
           static_folder='app/static',
           template_folder='app/templates')

# Set secret key for session management
app.secret_key = 'gift_shop_secret_key'

# Initialize services
from app.services import product_service, cart_service, chatbot_service

# Load product data from Excel if it exists
excel_path = Path(os.path.join(os.path.dirname(__file__), 'Gift_Store_Data.xlsx'))
if excel_path.exists():
    product_service.load_from_excel(str(excel_path.absolute()))

@app.route('/')
def index():
    # Get featured products and combos for homepage
    products = product_service.get_all_products()[:6]
    combos = product_service.get_all_combos()[:4]
    categories = product_service.get_all_categories()
    cart_count = cart_service.get_cart_count()
    
    return render_template('index.html', 
                           products=products, 
                           combos=combos, 
                           categories=categories,
                           cart_count=cart_count)

@app.route('/products')
def products():
    # Get all products
    all_products = product_service.get_all_products()
    categories = product_service.get_all_categories()
    cart_count = cart_service.get_cart_count()
    
    # Handle category filter if provided
    category = request.args.get('category')
    if category:
        all_products = product_service.get_products_by_category(category)
    
    return render_template('products.html', 
                           products=all_products, 
                           categories=categories,
                           current_category=category,
                           cart_count=cart_count)

@app.route('/combos')
def combos():
    # Get all gift combos
    all_combos = product_service.get_all_combos()
    categories = product_service.get_all_categories()
    cart_count = cart_service.get_cart_count()
    
    # Handle category filter if provided
    category = request.args.get('category')
    if category:
        all_combos = [c for c in all_combos if c['category'] == category]
    
    return render_template('combos.html', 
                           combos=all_combos, 
                           categories=categories,
                           current_category=category,
                           cart_count=cart_count)

@app.route('/about')
def about():
    cart_count = cart_service.get_cart_count()
    return render_template('about.html', cart_count=cart_count)

@app.route('/cart')
def cart():
    # Get cart items and totals
    cart_items = cart_service.get_cart()
    cart_total = cart_service.get_cart_total()
    cart_count = cart_service.get_cart_count()
    
    # Calculate other values
    shipping = 5.00 if cart_total > 0 else 0.00
    tax = round(cart_total * 0.08, 2) if cart_total > 0 else 0.00
    total = round(cart_total + shipping + tax, 2)
    
    return render_template('cart.html', 
                           cart_items=cart_items, 
                           cart_subtotal=cart_total,
                           shipping=shipping,
                           tax=tax,
                           total=total,
                           cart_count=cart_count)

# API Endpoints
@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    data = request.json
    item_id = int(data.get('id'))
    item_type = data.get('type')
    quantity = int(data.get('quantity', 1))
    
    success = cart_service.add_to_cart(item_id, item_type, quantity)
    
    return jsonify({
        'success': success,
        'cart_count': cart_service.get_cart_count()
    })

@app.route('/api/cart/update', methods=['POST'])
def update_cart():
    data = request.json
    item_id = int(data.get('id'))
    item_type = data.get('type')
    quantity = int(data.get('quantity'))
    
    success = cart_service.update_quantity(item_id, item_type, quantity)
    
    cart_items = cart_service.get_cart()
    cart_total = cart_service.get_cart_total()
    shipping = 5.00 if cart_total > 0 else 0.00
    tax = round(cart_total * 0.08, 2) if cart_total > 0 else 0.00
    total = round(cart_total + shipping + tax, 2)
    
    return jsonify({
        'success': success,
        'cart_count': cart_service.get_cart_count(),
        'cart_subtotal': cart_total,
        'shipping': shipping,
        'tax': tax,
        'total': total
    })

@app.route('/api/cart/remove', methods=['POST'])
def remove_from_cart():
    data = request.json
    item_id = int(data.get('id'))
    item_type = data.get('type')
    
    success = cart_service.remove_from_cart(item_id, item_type)
    
    cart_items = cart_service.get_cart()
    cart_total = cart_service.get_cart_total()
    shipping = 5.00 if cart_total > 0 else 0.00
    tax = round(cart_total * 0.08, 2) if cart_total > 0 else 0.00
    total = round(cart_total + shipping + tax, 2)
    
    return jsonify({
        'success': success,
        'cart_count': cart_service.get_cart_count(),
        'cart_subtotal': cart_total,
        'shipping': shipping,
        'tax': tax,
        'total': total
    })

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    query = data.get('query', '')
    
    # Process query and get recommendations
    result = chatbot_service.process_query(query)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)