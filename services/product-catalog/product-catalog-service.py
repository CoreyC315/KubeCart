# Product Catalog Service (product_catalog_service.py)
#
# This service is responsible for managing all product details.
# In a real cloud-native application, this would connect to a database
# (like PostgreSQL as planned in Phase 2).
# It provides REST endpoints for the frontend to fetch product lists and details.

from flask import Flask, jsonify, request

app = Flask(__name__)

# --- In-Memory Product Database (Placeholder) ---
# In Phase 2, this data structure will be replaced by a proper database connection.
PRODUCTS = {
    "P001": {
        "id": "P001",
        "name": "AMD Ryzen 5 5600X",
        "category": "cpu",
        "price": 199.99,
        "description": "High-performance 6-core processor.",
        "socket": "AM4"
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
    Example: GET /api/products?category=cpu
    """
    category_filter = request.args.get('category')
    
    if category_filter:
        filtered_products = [
            p for p in PRODUCTS.values() 
            if p['category'].lower() == category_filter.lower()
        ]
        return jsonify(filtered_products)
    
    # Return all products if no filter is specified
    return jsonify(list(PRODUCTS.values()))

@app.route('/api/products/<product_id>', methods=['GET'])
def get_product_details(product_id):
    """
    Endpoint to fetch details for a single product.
    Example: GET /api/products/P001
    """
    product = PRODUCTS.get(product_id)
    if product:
        return jsonify(product)
    
    # Return 404 Not Found if the product ID doesn't exist
    return jsonify({"error": "Product not found"}), 404

# --- Application Startup ---
if __name__ == '__main__':
    # When deployed in Minikube (Phase 2), this will run inside a container
    # and listen on port 5000 (default Flask port).
    # The Ingress service will handle routing to this port.
    print("--- Product Catalog Service Started ---")
    app.run(debug=True, host='0.0.0.0', port=5000)
