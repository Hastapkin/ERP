import os
import openpyxl
from pathlib import Path
import random

class ProductService:
    def __init__(self, excel_path=None):
        self.products = []
        self.categories = []
        self.combos = []
        
        # Thư mục chứa ảnh sản phẩm
        self.images_folder = 'app/static/images/products'
        
        if excel_path and os.path.exists(excel_path):
            self.load_from_excel(excel_path)
        else:
            self.load_sample_data()
    
    def load_from_excel(self, excel_path):
        """Load product data from Excel file"""
        try:
            wb = openpyxl.load_workbook(excel_path, data_only=True)
            sheet = wb["Structured Data "]
            
            # Process product data
            unique_products = {}
            categories = set()
            
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if len(row) < 7 or not all([row[4], row[5], row[6]]):  # Check for required fields
                    continue
                
                # Extract data from row
                name = row[4].strip() if row[4] else ""
                category = row[5].strip() if row[5] else ""
                
                # Format price to 2 decimal places
                raw_price = row[6]
                price = float(raw_price) if raw_price else 0.0
                price = round(price, 2)  # Round to 2 decimal places
                
                # Generate image filename from product name
                image_filename = self._generate_image_filename(name)
                
                # Create product object
                product = {
                    "id": len(unique_products) + 1,
                    "name": name,
                    "category": category,
                    "price": price,  # Rounded price
                    "description": f"High-quality {category} item, perfect for various occasions",
                    "image": image_filename
                }
                
                # Only add unique products
                if name and name not in unique_products:
                    unique_products[name] = product
                    categories.add(category)
            
            # Convert to lists
            self.products = list(unique_products.values())
            self.categories = list(categories)
            
            # Create gift combos
            self.create_gift_combos()
            
            # Generate list of needed images
            self._generate_needed_images_list()
            
            print(f"Loaded {len(self.products)} products from Excel")
            
        except Exception as e:
            print(f"Error loading Excel data: {e}")
            self.load_sample_data()
    
    def _generate_image_filename(self, product_name):
        """Generate image filename from product name"""
        if not product_name:
            return "placeholder.jpg"
        
        # Clean the name and convert to lowercase
        clean_name = product_name.lower()
        # Replace spaces with underscores
        clean_name = clean_name.replace(' ', '_')
        # Remove any special characters except underscores
        clean_name = ''.join(c for c in clean_name if c.isalnum() or c == '_')
        
        # Add jpg extension
        return f"{clean_name}.jpg"
    
    def _generate_needed_images_list(self):
        """Generate a list of image filenames needed for all products"""
        needed_images = []
        
        for product in self.products:
            needed_images.append(product["image"])
        
        # Also add combo images
        for combo in self.combos:
            needed_images.append(combo["image"])
        
        # Remove duplicates
        needed_images = list(set(needed_images))
        
        # Print the list for reference
        print(f"\nNeeded images for products ({len(needed_images)}):")
        for image in sorted(needed_images):
            # Check if image exists
            image_path = os.path.join(self.images_folder, image)
            status = "✓" if os.path.exists(image_path) else "✗"
            print(f"{status} {image}")
    
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
                discount_price = round(base_price * 0.9, 2)  # Round to 2 decimal places
                
                # Generate combo image name
                combo_image = f"{category.lower().replace(' ', '_').replace('&', 'and')}_combo.jpg"
                
                # Create combo
                self.combos.append({
                    "id": combo_id,
                    "name": f"{category} Gift Set",
                    "price": discount_price,
                    "description": f"A special collection of {category} items",
                    "image": combo_image,
                    "products": [p["name"] for p in combo_products],
                    "category": category
                })
                
                combo_id += 1
    
    def load_sample_data(self):
        """Load minimal sample data if Excel file is not available"""
        self.products = []
        self.categories = []
        self.combos = []
        
        print("No Excel data found. Using empty product catalog.")
    
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