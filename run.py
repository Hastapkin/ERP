from flask import Flask, render_template, request, jsonify, session
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, 
           static_folder='app/static',
           template_folder='app/templates')

# Set secret key for session management
app.secret_key = 'gift_shop_secret_key'

# Import services directly to avoid circular dependencies
from app.services.product_service import product_service
from app.services.cart_service import cart_service

# Try to import gemini chatbot only if needed
try:
    from app.services.gemini_chatbot_service import gemini_chatbot_service
    if gemini_chatbot_service is not None:
        print("✅ Gemini chatbot service loaded successfully")
    else:
        print("❌ Gemini chatbot service was imported but is None - will use fallback")
except ImportError as e:
    gemini_chatbot_service = None
    print(f"❌ Gemini chatbot service not available: {e}")

# Load product data from Excel if it exists
excel_path = Path(os.path.join(os.path.dirname(__file__), 'Gift_Store_Data.xlsx'))
if excel_path.exists():
    product_service.load_from_excel(str(excel_path.absolute()))
    print(f"✅ Loaded product data from Excel: {len(product_service.get_all_products())} products")
else:
    print("⚠️ Excel file not found, using sample data")

# Routes
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
    
    # Get user ID from session (or use a default)
    user_id = session.get('user_id', 'anonymous')
    
    try:
        # Check if Gemini service exists
        if gemini_chatbot_service is None:
            raise ValueError("Chatbot service is not available")
        
        # Process the query using Gemini
        result = gemini_chatbot_service.process_query(query, user_id)
        return jsonify(result)
    
    except Exception as e:
        error_msg = str(e)
        print(f"Error in chatbot: {error_msg}")
        
        # Handle different types of errors with appropriate responses
        if "API_RATE_LIMIT_EXCEEDED" in error_msg:
            fallback_response = "I'm currently experiencing high demand. Please try again in a few minutes. Meanwhile, check out these popular products:"
        elif "API_TIMEOUT" in error_msg:
            fallback_response = "Connection is taking longer than expected. Let me suggest some popular products while we wait:"
        elif "API_BAD_REQUEST" in error_msg:
            fallback_response = "I'm having some technical difficulties understanding your request. Here are some products you might be interested in:"
        elif "API_ERROR" in error_msg:
            fallback_response = "I'm experiencing some technical issues. Here are some popular products from our catalog:"
        elif "Failed to load product data" in error_msg:
            fallback_response = "I'm having trouble accessing our product catalog right now. Please try again in a moment."
        else:
            fallback_response = "I'm sorry, I couldn't process your request at the moment. Here are some popular products you might like:"
        
        # Get popular products as fallback recommendations
        try:
            recommendations = []
            all_products = product_service.get_all_products()
            all_combos = product_service.get_all_combos()
            
            # Mix of products and combos for variety
            if all_products:
                for product in all_products[:2]:
                    recommendations.append({
                        "id": product["id"],
                        "name": product["name"],
                        "price": product["price"],
                        "image": product["image"],
                        "description": product["description"],
                        "type": "product",
                        "relevance_scores": {"suggestion": "Popular item"}
                    })
            
            if all_combos:
                for combo in all_combos[:1]:
                    recommendations.append({
                        "id": combo["id"],
                        "name": combo["name"],
                        "price": combo["price"],
                        "image": combo["image"],
                        "description": combo["description"],
                        "type": "combo",
                        "relevance_scores": {"suggestion": "Gift bundle"}
                    })
                    
        except Exception as fallback_error:
            print(f"Error getting fallback recommendations: {fallback_error}")
            recommendations = []
            
        return jsonify({
            "response": fallback_response,
            "recommendations": recommendations,
            "fallback": True,
            "error_type": "service_unavailable"
        })

@app.route('/api/chatbot/reset', methods=['POST'])
def reset_chatbot():
    """Reset chatbot conversation context for current user"""
    user_id = session.get('user_id', 'anonymous')
    
    try:
        if gemini_chatbot_service is None:
            raise ValueError("Chatbot service is not available")
            
        result = gemini_chatbot_service.reset_conversation(user_id)
        return jsonify(result)
    except Exception as e:
        print(f"Error resetting chatbot conversation: {e}")
        return jsonify({
            "success": False, 
            "message": "Failed to reset conversation",
            "error": str(e)
        })

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify service status"""
    health_status = {
        "status": "healthy",
        "services": {
            "product_service": True,
            "cart_service": True,
            "gemini_chatbot": gemini_chatbot_service is not None
        },
        "product_count": len(product_service.get_all_products()),
        "category_count": len(product_service.get_all_categories()),
        "combo_count": len(product_service.get_all_combos())
    }
    
    return jsonify(health_status)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Initialize session for anonymous users
@app.before_request
def before_request():
    if 'user_id' not in session:
        import uuid
        session['user_id'] = str(uuid.uuid4())

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 GIFT SHOP APPLICATION STARTING")
    print("="*50)
    
    # Check if Gemini API key is set
    if gemini_chatbot_service is None:
        print("\n⚠️ WARNING: Gemini chatbot service not available.")
        print("The application will run with limited chatbot functionality.")
    elif not os.environ.get("GEMINI_API_KEY"):
        print("\n⚠️ WARNING: GEMINI_API_KEY environment variable not set.")
        print("The Gemini chatbot will not function correctly.")
    else:
        print("\n✅ Gemini API key found. Advanced chatbot is ready to use.")
    
    # Display service status
    print(f"\n📊 SERVICE STATUS:")
    print(f"   Products loaded: {len(product_service.get_all_products())}")
    print(f"   Categories: {len(product_service.get_all_categories())}")
    print(f"   Gift combos: {len(product_service.get_all_combos())}")
    print(f"   Cart service: ✅ Ready")
    print(f"   Chatbot service: {'✅ Ready' if gemini_chatbot_service else '❌ Not available'}")
    
    print(f"\n🌐 APPLICATION READY")
    print("   URL: http://localhost:5000")
    print("   Debug mode: ON")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)