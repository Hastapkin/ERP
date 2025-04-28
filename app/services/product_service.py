import os
import json
import openpyxl
from pathlib import Path
from flask import current_app

class ProductService:
    def __init__(self, excel_path=None):
        self.products = []
        self.categories = []
        self.combos = []
        
        if excel_path and os.path.exists(excel_path):
            self.load_from_excel(excel_path)
        else:
            self.load_sample_data()
    
    def load_from_excel(self, excel_path):
        """Load product data from Excel file"""
        try:
            wb = openpyxl.load_workbook(excel_path, data_only=True)
            sheet = wb["Structured Data "]
            
            # Extract header row
            headers = []
            for cell in sheet[1]:
                headers.append(cell.value)
            
            # Process product data
            unique_products = {}
            categories = set()
            
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if len(row) < 7 or not all([row[4], row[5], row[6]]):  # Check for required fields
                    continue
                
                # Create product object
                product = {
                    "id": len(unique_products) + 1,
                    "name": row[4].strip() if row[4] else "",
                    "category": row[5].strip() if row[5] else "",
                    "price": float(row[6]) if row[6] else 0.0,
                    "description": f"{row[5]} gift, perfect for ages {row[1]}-{row[1]+2}",
                    "image": self._generate_image_filename(row[4])
                }
                
                # Only add unique products
                product_name = product["name"]
                if product_name and product_name not in unique_products:
                    unique_products[product_name] = product
                    categories.add(product["category"])
            
            # Convert to lists
            self.products = list(unique_products.values())
            self.categories = list(categories)
            
            # Create gift combos
            self.create_gift_combos()
            
        except Exception as e:
            print(f"Error loading Excel data: {e}")
            self.load_sample_data()
    
    def _generate_image_filename(self, product_name):
        """Generate image filename from product name"""
        if not product_name:
            return "default.jpg"
        
        filename = product_name.lower().replace(" ", "_")
        filename = ''.join(c for c in filename if c.isalnum() or c == '_')
        return f"{filename}.jpg"
    
    def create_gift_combos(self):
        """Create gift combo packages from products"""
        self.combos = []
        combo_id = 1
        
        # Create one combo for each category
        for category in self.categories:
            # Get products in this category
            category_products = [p for p in self.products if p["category"] == category]
            
            if len(category_products) >= 2:
                # Select up to 3 products for the combo
                combo_products = category_products[:min(3, len(category_products))]
                
                # Calculate combo price (10% discount)
                base_price = sum(p["price"] for p in combo_products)
                discount_price = round(base_price * 0.9, 2)
                
                # Create combo
                self.combos.append({
                    "id": combo_id,
                    "name": f"{category} Gift Set",
                    "price": discount_price,
                    "description": f"A special collection of {category} items",
                    "image": f"{category.lower().replace(' ', '_')}_combo.jpg",
                    "products": [p["name"] for p in combo_products],
                    "category": category
                })
                
                combo_id += 1
    
    def load_sample_data(self):
        """Load sample product data if Excel file is not available"""
        self.products = [
            {
                "id": 1,
                "name": "Birthday Card",
                "price": 4.99,
                "description": "A beautiful birthday card for your loved ones",
                "image": "birthday_card.jpg",
                "category": "Cards"
            },
            {
                "id": 2,
                "name": "Chocolate Box",
                "price": 14.99,
                "description": "Premium assorted chocolates",
                "image": "chocolate_box.jpg",
                "category": "Food"
            },
            {
                "id": 3,
                "name": "Teddy Bear",
                "price": 19.99,
                "description": "Soft plush teddy bear",
                "image": "teddy_bear.jpg",
                "category": "Toys"
            },
            {
                "id": 4,
                "name": "Wine Bottle",
                "price": 24.99,
                "description": "Red wine bottle, vintage 2018",
                "image": "wine.jpg",
                "category": "Drinks"
            }
        ]
        
        self.categories = ["Cards", "Food", "Toys", "Drinks"]
        
        self.combos = [
            {
                "id": 1,
                "name": "Birthday Special",
                "price": 29.99,
                "description": "Perfect birthday gift combo for your loved ones",
                "image": "birthday_combo.jpg",
                "products": ["Birthday Card", "Chocolate Box", "Teddy Bear"],
                "category": "Birthday"
            },
            {
                "id": 2,
                "name": "Anniversary Delight",
                "price": 39.99,
                "description": "Romantic anniversary combo for special celebrations",
                "image": "anniversary_combo.jpg",
                "products": ["Chocolate Box", "Wine Bottle"],
                "category": "Anniversary"
            }
        ]
    
    def get_all_products(self):
        """Return all products"""
        return self.products
    
    def get_product_by_id(self, product_id):
        """Return product by ID"""
        for product in self.products:
            if product["id"] == product_id:
                return product
        return None
    
    def get_all_categories(self):
        """Return all categories"""
        return self.categories
    
    def get_products_by_category(self, category):
        """Return products filtered by category"""
        return [p for p in self.products if p["category"] == category]
    
    def get_all_combos(self):
        """Return all gift combos"""
        return self.combos
    
    def get_combo_by_id(self, combo_id):
        """Return combo by ID"""
        for combo in self.combos:
            if combo["id"] == combo_id:
                return combo
        return None

# Create singleton instance
product_service = ProductService()