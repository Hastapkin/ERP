from flask import Flask, render_template, request, jsonify, session
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, 
           static_folder='app/static',
           template_folder='app/templates')

app.secret_key = 'gift_shop_secret_key'

# Import services
from app.services.product_service import product_service
from app.services.cart_service import cart_service

# Import Gemini chatbot
try:
    from app.services.gemini_chatbot_service import gemini_chatbot_service
    print("✅ Gemini chatbot service loaded")
except ImportError as e:
    gemini_chatbot_service = None
    print(f"❌ Gemini chatbot not available: {e}")

# Load Excel data
excel_path = Path('Gift_Store_Data.xlsx')
if excel_path.exists():
    product_service.load_from_excel(str(excel_path))
    print(f"✅ Loaded {len(product_service.get_all_products())} products")
else:
    print("⚠️ Excel file not found")

# Routes
@app.route('/')
def index():
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
    all_products = product_service.get_all_products()
    categories = product_service.get_all_categories()
    cart_count = cart_service.get_cart_count()
    
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
    all_combos = product_service.get_all_combos()
    categories = product_service.get_all_categories()
    cart_count = cart_service.get_cart_count()
    
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
    cart_items = cart_service.get_cart()
    cart_total = cart_service.get_cart_total()
    cart_count = cart_service.get_cart_count()
    
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

# Cart API
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

# Chatbot API
@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    query = data.get('query', '')
    user_id = session.get('user_id', 'anonymous')
    
    try:
        if gemini_chatbot_service is None:
            raise ValueError("Gemini chatbot not available")
        
        result = gemini_chatbot_service.process_query(query, user_id)
        print(f"✅ Chatbot response: {len(result.get('recommendations', []))} recommendations")
        return jsonify(result)
    
    except Exception as e:
        print(f"❌ Chatbot error: {e}")
        
        # Fallback
        fallback_products = product_service.get_all_products()[:3]
        recommendations = []
        
        for product in fallback_products:
            recommendations.append({
                "id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "image": product["image"],
                "description": product["description"],
                "type": "product",
                "relevance_scores": {"suggestion": "Popular choice"}
            })
        
        return jsonify({
            "response": "Sorry, I'm having technical difficulties. Here are some popular products:",
            "recommendations": recommendations,
            "fallback": True
        })

@app.route('/api/chatbot/reset', methods=['POST'])
def reset_chatbot():
    user_id = session.get('user_id', 'anonymous')
    
    try:
        if gemini_chatbot_service is None:
            raise ValueError("Gemini chatbot not available")
            
        result = gemini_chatbot_service.reset_conversation(user_id)
        return jsonify(result)
    except Exception as e:
        print(f"❌ Error resetting: {e}")
        return jsonify({
            "success": False, 
            "message": "Failed to reset conversation"
        })

# Health check
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "services": {
            "product_service": True,
            "cart_service": True,
            "gemini_chatbot": gemini_chatbot_service is not None
        },
        "product_count": len(product_service.get_all_products()),
        "category_count": len(product_service.get_all_categories()),
        "combo_count": len(product_service.get_all_combos())
    })

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Initialize session
@app.before_request
def before_request():
    if 'user_id' not in session:
        import uuid
        session['user_id'] = str(uuid.uuid4())

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 GIFT SHOP APPLICATION STARTING")
    print("="*50)
    
    if gemini_chatbot_service is None:
        print("\n⚠️ WARNING: Gemini chatbot not available")
        print("Set GEMINI_API_KEY environment variable")
    else:
        print("\n🧠 GEMINI AI CHATBOT: ✅ ACTIVE")
        print("Features: Age, Gender, Category, Budget")
    
    print(f"\n📊 LOADED DATA:")
    print(f"   Products: {len(product_service.get_all_products())}")
    print(f"   Categories: {len(product_service.get_all_categories())}")
    print(f"   Combos: {len(product_service.get_all_combos())}")
    
    print(f"\n🌐 Ready: http://localhost:5000")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)