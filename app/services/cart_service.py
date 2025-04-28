from flask import session
from .product_service import product_service

class CartService:
    def __init__(self):
        self.session_key = 'cart'
    
    def _ensure_cart_exists(self):
        """Ensure cart exists in session"""
        if self.session_key not in session:
            session[self.session_key] = []
    
    def get_cart(self):
        """Get current cart with product details"""
        self._ensure_cart_exists()
        cart = session[self.session_key]
        
        # Populate with full product details
        cart_items = []
        for item in cart:
            product_data = None
            
            if item['type'] == 'product':
                product_data = product_service.get_product_by_id(item['id'])
            elif item['type'] == 'combo':
                product_data = product_service.get_combo_by_id(item['id'])
            
            if product_data:
                # Create a new dictionary with both cart item and product data
                cart_item = {
                    'id': item['id'],
                    'type': item['type'],
                    'quantity': item['quantity'],
                    'name': product_data['name'],
                    'price': product_data['price'],
                    'image': product_data['image'],
                    'subtotal': round(product_data['price'] * item['quantity'], 2)
                }
                cart_items.append(cart_item)
        
        return cart_items
    
    def add_to_cart(self, item_id, item_type, quantity=1):
        """Add item to cart or increase quantity if already exists"""
        self._ensure_cart_exists()
        cart = session[self.session_key]
        
        # Check if product/combo exists
        product = None
        if item_type == 'product':
            product = product_service.get_product_by_id(item_id)
        elif item_type == 'combo':
            product = product_service.get_combo_by_id(item_id)
        
        if not product:
            return False
        
        # Check if item already in cart
        for item in cart:
            if item['id'] == item_id and item['type'] == item_type:
                item['quantity'] += quantity
                session.modified = True
                return True
        
        # Add new item to cart
        cart.append({
            'id': item_id,
            'type': item_type,
            'quantity': quantity
        })
        session.modified = True
        return True
    
    def update_quantity(self, item_id, item_type, quantity):
        """Update item quantity in cart"""
        self._ensure_cart_exists()
        cart = session[self.session_key]
        
        for item in cart:
            if item['id'] == item_id and item['type'] == item_type:
                if quantity > 0:
                    item['quantity'] = quantity
                else:
                    # Remove item if quantity <= 0
                    cart.remove(item)
                session.modified = True
                return True
        
        return False
    
    def remove_from_cart(self, item_id, item_type):
        """Remove item from cart"""
        self._ensure_cart_exists()
        cart = session[self.session_key]
        
        for i, item in enumerate(cart):
            if item['id'] == item_id and item['type'] == item_type:
                del cart[i]
                session.modified = True
                return True
        
        return False
    
    def clear_cart(self):
        """Clear all items from cart"""
        session[self.session_key] = []
        session.modified = True
    
    def get_cart_total(self):
        """Calculate cart total"""
        cart_items = self.get_cart()
        return round(sum(item['subtotal'] for item in cart_items), 2)
    
    def get_cart_count(self):
        """Get total number of items in cart"""
        self._ensure_cart_exists()
        cart = session[self.session_key]
        return sum(item['quantity'] for item in cart)

# Create singleton instance
cart_service = CartService()