from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'dev-secret-key'

# Static data for demonstration purposes
USERS = {
    1: {"id": 1, "username": "demo", "email": "demo@example.com", "password": "password"}
}

CATEGORIES = {
    1: {"id": 1, "name": "Electronics", "description": "Gadgets and electronic devices"},
    2: {"id": 2, "name": "Clothing", "description": "Apparel and fashion items"},
    3: {"id": 3, "name": "Books", "description": "Books and literature"},
    4: {"id": 4, "name": "Home & Kitchen", "description": "Home appliances and kitchen items"}
}

PRODUCTS = {
    1: {"id": 1, "name": "Smartphone X", "description": "Latest smartphone with advanced features", "price": 999.99, "category_id": 1, "image_url": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8c21hcnRwaG9uZXxlbnwwfHwwfHx8MA%3D%3D"},
    2: {"id": 2, "name": "Laptop Pro", "description": "Powerful laptop for professionals", "price": 1299.99, "category_id": 1, "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8bGFwdG9wfGVufDB8fDB8fHww"},
    3: {"id": 3, "name": "Wireless Earbuds", "description": "High-quality wireless earbuds", "price": 149.99, "category_id": 1, "image_url": "https://images.unsplash.com/photo-1606220588913-b3aacb4d2f46?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8ZWFyYnVkc3xlbnwwfHwwfHx8MA%3D%3D"},
    4: {"id": 4, "name": "Smart Watch", "description": "Fitness tracker and smartwatch", "price": 249.99, "category_id": 1, "image_url": "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8c21hcnQlMjB3YXRjaHxlbnwwfHwwfHx8MA%3D%3D"},
    5: {"id": 5, "name": "Blue Jeans", "description": "Classic blue denim jeans", "price": 59.99, "category_id": 2, "image_url": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8amVhbnN8ZW58MHx8MHx8fDA%3D"},
    6: {"id": 6, "name": "White T-Shirt", "description": "Comfortable cotton t-shirt", "price": 19.99, "category_id": 2, "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dCUyMHNoaXJ0fGVufDB8fDB8fHww"},
    7: {"id": 7, "name": "Winter Jacket", "description": "Warm jacket for cold weather", "price": 129.99, "category_id": 2, "image_url": "https://images.unsplash.com/photo-1614031679232-0dae776a72ee?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8d2ludGVyJTIwamFja2V0fGVufDB8fDB8fHww"},
    8: {"id": 8, "name": "Running Shoes", "description": "Lightweight shoes for running", "price": 89.99, "category_id": 2, "image_url": "https://images.unsplash.com/photo-1575537302964-96cd47c06b1b?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8cnVubmluZyUyMHNob2VzfGVufDB8fDB8fHww"},
    9: {"id": 9, "name": "The Great Novel", "description": "Bestselling fiction novel", "price": 24.99, "category_id": 3, "image_url": "https://images.unsplash.com/photo-1599940824399-b87987ceb72a?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OXx8bm92ZWx8ZW58MHx8MHx8fDA%3D"},
    10: {"id": 10, "name": "Cooking Basics", "description": "Cookbook for beginners", "price": 34.99, "category_id": 3, "image_url": "https://images.unsplash.com/photo-1589820754482-8e56171afddb?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8Y29va2Jvb2t8ZW58MHx8MHx8fDA%3D"},
    11: {"id": 11, "name": "History of Science", "description": "Comprehensive history book", "price": 44.99, "category_id": 3, "image_url": "https://images.unsplash.com/photo-1544640808-32ca72ac7f37?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8c2NpZW5jZSUyMGJvb2t8ZW58MHx8MHx8fDA%3D"},
    12: {"id": 12, "name": "Programming Guide", "description": "Learn to code with this guide", "price": 49.99, "category_id": 3, "image_url": "https://images.unsplash.com/photo-1517148815978-75f6acaaf32c?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fHByb2dyYW1taW5nJTIwYm9va3xlbnwwfHwwfHx8MA%3D%3D"},
    13: {"id": 13, "name": "Coffee Maker", "description": "Automatic coffee brewing machine", "price": 79.99, "category_id": 4, "image_url": "https://images.unsplash.com/photo-1599679200082-9081e6c9f789?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fGNvZmZlZSUyMG1ha2VyfGVufDB8fDB8fHww"},
    14: {"id": 14, "name": "Blender", "description": "Powerful blender for smoothies", "price": 69.99, "category_id": 4, "image_url": "https://images.unsplash.com/photo-1578105631865-5a5694266c9c?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8YmxlbmRlcnxlbnwwfHwwfHx8MA%3D%3D"},
    15: {"id": 15, "name": "Toaster", "description": "2-slice toaster with multiple settings", "price": 39.99, "category_id": 4, "image_url": "https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8dG9hc3RlcnxlbnwwfHwwfHx8MA%3D%3D"},
    16: {"id": 16, "name": "Knife Set", "description": "Professional kitchen knife set", "price": 149.99, "category_id": 4, "image_url": "https://images.unsplash.com/photo-1593618998160-e34014e67546?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fGtuaWZlJTIwc2V0fGVufDB8fDB8fHww"}
}

RATINGS = []

# Helper functions
def get_user_id():
    """Get the current user ID from session"""
    return session.get('user_id')

def is_authenticated():
    """Check if user is authenticated"""
    return 'user_id' in session

def get_product_category(product_id):
    """Get category for a product"""
    product = PRODUCTS.get(product_id)
    if product:
        return CATEGORIES.get(product['category_id'])
    return None

def get_products_in_category(category_id):
    """Get all products in a category"""
    return [p for p in PRODUCTS.values() if p['category_id'] == category_id]

def get_similar_products(product_id, n=4):
    """Get similar products based on category"""
    product = PRODUCTS.get(product_id)
    if not product:
        return []
    
    # Get other products in the same category
    category_products = [p for p in PRODUCTS.values() if p['category_id'] == product['category_id'] and p['id'] != product_id]
    
    # Get up to n random products from the same category
    return random.sample(category_products, min(n, len(category_products)))

def get_popular_products(n=10):
    """Get popular products"""
    # Just return some random products
    return random.sample(list(PRODUCTS.values()), min(n, len(PRODUCTS)))

def get_recent_products(n=8):
    """Get recent products"""
    # Just return a random selection of products
    return random.sample(list(PRODUCTS.values()), min(n, len(PRODUCTS)))

def get_user_recommendations(user_id, n=10):
    """Get recommended products for a user"""
    # Just return some random products
    return random.sample(list(PRODUCTS.values()), min(n, len(PRODUCTS)))

# Routes
@app.route('/')
def index():
    """Home page with product categories and featured products"""
    # Get all categories
    categories = list(CATEGORIES.values())
    
    # Get recent products
    recent_products = get_recent_products(8)
    
    # Get recommended products for the current user
    recommended_products = []
    user_id = get_user_id()
    
    if user_id:
        recommended_products = get_user_recommendations(user_id, n=4)
    else:
        # For non-logged in users, show popular products
        recommended_products = get_popular_products(n=4)
    
    return render_template(
        'index.html',
        categories=categories,
        recent_products=recent_products,
        recommended_products=recommended_products,
        is_authenticated=is_authenticated()
    )

@app.route('/category/<int:category_id>')
def category(category_id):
    """View products in a category"""
    # Get the category
    category = CATEGORIES.get(category_id)
    if not category:
        return redirect(url_for('index'))
    
    # Get products in the category
    products = get_products_in_category(category_id)
    
    # Get recommended products in this category for the user
    user_recommended_products = []
    user_id = get_user_id()
    
    if user_id:
        # Get general user recommendations
        user_recs = get_user_recommendations(user_id, n=20)
        # Filter to this category
        user_recommended_products = [p for p in user_recs if p['category_id'] == category_id][:4]
    
    return render_template(
        'category.html',
        category=category,
        products=products,
        user_recommended_products=user_recommended_products,
        is_authenticated=is_authenticated()
    )

@app.route('/product/<int:product_id>')
def product(product_id):
    """View a product's details"""
    # Get the product
    product = PRODUCTS.get(product_id)
    if not product:
        return redirect(url_for('index'))
    
    # Get product's category
    product_category = get_product_category(product_id)
    product['category'] = product_category
    
    # Get user's rating for this product if they've rated it
    user_rating = None
    user_id = get_user_id()
    
    # Get all ratings for this product (for this demo, we don't have any)
    ratings = []
    
    # Calculate average rating (0 for this demo)
    avg_rating = 0
    
    # Get similar products
    similar_products = get_similar_products(product_id, n=4)
    
    return render_template(
        'product.html',
        product=product,
        user_rating=user_rating,
        ratings=ratings,
        avg_rating=avg_rating,
        similar_products=similar_products,
        is_authenticated=is_authenticated()
    )

@app.route('/search')
def search():
    """Search for products"""
    query = request.args.get('q', '').strip().lower()
    
    if not query:
        return redirect(url_for('index'))
    
    # Search for products matching the query
    products = [p for p in PRODUCTS.values() if query in p['name'].lower() or query in p['description'].lower()]
    
    return render_template(
        'search_results.html',
        query=query,
        products=products,
        is_authenticated=is_authenticated()
    )

@app.route('/recommendations')
def recommendations():
    """View all recommendations for the current user"""
    if not is_authenticated():
        return redirect(url_for('login'))
    
    user_id = get_user_id()
    
    # Get all recommendations for the user
    recommended_products = get_user_recommendations(user_id, n=20)
    
    # Get recommendations by category
    category_recommendations = {}
    categories = list(CATEGORIES.values())
    
    for category in categories:
        # Filter user recommendations by category
        category_products = [p for p in recommended_products if p['category_id'] == category['id']]
        if category_products:
            category_recommendations[category['name']] = category_products[:4]
    
    return render_template(
        'recommendations.html',
        recommended_products=recommended_products,
        category_recommendations=category_recommendations,
        is_authenticated=is_authenticated()
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if is_authenticated():
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # For demo, just check if username is 'demo' and password is 'password'
        if username == 'demo' and password == 'password':
            # Set user session
            session['user_id'] = 1
            
            return redirect(url_for('index'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user"""
    if is_authenticated():
        return redirect(url_for('index'))
    
    # For demo, just redirect to login
    return render_template('register.html')

@app.route('/admin')
def admin():
    """Admin dashboard"""
    if not is_authenticated():
        return redirect(url_for('login'))
    
    user_count = len(USERS)
    product_count = len(PRODUCTS)
    category_count = len(CATEGORIES)
    rating_count = len(RATINGS)
    
    return render_template(
        'admin.html',
        user_count=user_count,
        product_count=product_count,
        category_count=category_count,
        rating_count=rating_count,
        is_authenticated=is_authenticated()
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)