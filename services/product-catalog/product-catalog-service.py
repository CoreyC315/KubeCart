from flask import Flask, jsonify, request
from flask_cors import CORS  # <-- ADD THIS LINE
import logging

# --- Configure Logging ---
# Create a logger object
# Setting level to INFO ensures all INFO, WARNING, and ERROR messages are captured
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # <-- AND ADD THIS LINE

# --- In-Memory Product Database (Placeholder) ---
PRODUCTS = {
    "P001": {
        "id": "P001",
        "name": "AMD Ryzen 5 5600X",
        "category": "cpu",
        "price": 199.99,
        "description": "High-performance 6-core processor.",
        "socket": "AM4",
        "version": "CI/CD Test 1.4"
    },
    "P002": {
        "id": "P002",
        "name": "NVIDIA GeForce RTX 4070",
        "category": "gpu",
        "price": 599.99,
        "description": "Next-gen ray tracing graphics card.",
        "vram": "12GB"
    },
    "P003": {
        "id": "P003",
        "name": "ASUS ROG B550-F",
        "category": "motherboard",
        "price": 159.99,
        "description": "ATX Motherboard with PCIe 4.0 support.",
        "socket": "AM4"
    }
}

# --- API Endpoints ---

@app.route('/api/products', methods=['GET'])
def get_products():
    """
    Endpoint to fetch all products or filter by category.
    """
    category_filter = request.args.get('category')
    
    if category_filter:
        # Using logger.info() instead of print()
        logger.info("Fetching products filtered by category: %s", category_filter)
        
        filtered_products = [
            p for p in PRODUCTS.values() 
            if p['category'].lower() == category_filter.lower()
        ]
        logger.info("Found %d products for category '%s'.", len(filtered_products), category_filter)
        return jsonify(filtered_products)
    
    # Using logger.info() instead of print()
    logger.info("Fetching ALL products.")
    
    # Return all products if no filter is specified
    return jsonify(list(PRODUCTS.values()))

@app.route('/api/products/<product_id>', methods=['GET'])
def get_product_details(product_id):
    """
    Endpoint to fetch details for a single product.
    """
    # Using logger.info() instead of print()
    logger.info("Request received for product ID: %s", product_id)
    
    product = PRODUCTS.get(product_id)
    if product:
        logger.info("Successfully retrieved details for %s.", product_id)
        return jsonify(product)
    
    # Using logger.error() for errors
    logger.error("Product ID %s not found in catalog.", product_id)
    return jsonify({"error": "Product not found"}), 404

# --- Application Startup ---
if __name__ == '__main__':
    # This block only runs if executed directly (e.g., during development), not in Gunicorn
    logger.info("--- Product Catalog Service Started (Development Mode) ---")
    app.run(debug=True, host='0.0.0.0', port=5000)