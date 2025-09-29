# Inventory Service (inventory_service.py)
#
# This service tracks the current stock level for all products.
# It is vital for preventing overselling and coordinating with the Order Service.

from flask import Flask, jsonify, request
import logging

# --- Configure Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# --- In-Memory Inventory Store (Placeholder) ---
# Maps Product ID to current stock level
INVENTORY_STORE = {
    "P001": 50,  # AMD Ryzen 5 5600X (CPU)
    "P002": 30,  # NVIDIA GeForce RTX 4070 (GPU)
    "P003": 75,  # ASUS ROG B550-F (Motherboard)
    "P004": 0,    # Out of Stock Item (for testing)
}

# --- API Endpoints ---

@app.route('/api/inventory/<product_id>', methods=['GET'])
def get_inventory(product_id):
    """
    Checks the stock level for a single product ID.
    """
    logger.info("Request received to check stock for product ID: %s", product_id)
    
    stock = INVENTORY_STORE.get(product_id)
    
    if stock is not None:
        return jsonify({"product_id": product_id, "stock_level": stock})
    
    logger.error("Product ID %s not found in inventory store.", product_id)
    return jsonify({"error": "Product not found"}), 404

@app.route('/api/inventory/check_multiple', methods=['GET'])
def check_multiple_inventory():
    """
    Checks the stock level for a comma-separated list of product IDs.
    Example: GET /api/inventory/check_multiple?ids=P001,P002,P004
    """
    product_ids_str = request.args.get('ids')
    if not product_ids_str:
        logger.warning("Attempted to check multiple inventory items without providing 'ids' parameter.")
        return jsonify({"error": "Missing 'ids' parameter"}), 400

    product_ids = [id.strip() for id in product_ids_str.split(',')]
    logger.info("Checking stock for multiple IDs: %s", product_ids)
    
    results = {}
    for product_id in product_ids:
        stock = INVENTORY_STORE.get(product_id, -1)  # Use -1 to indicate missing/unknown
        results[product_id] = {"stock_level": stock}
        
    return jsonify(results)

@app.route('/api/inventory/decrement', methods=['POST'])
def decrement_inventory():
    """
    Decrements stock for a product after a successful order is placed.
    Request body: {"product_id": "P001", "quantity": 1}
    """
    data = request.json
    product_id = data.get("product_id")
    quantity = data.get("quantity")
    
    if not product_id or not quantity:
        logger.error("Decrement failed: Missing product_id or quantity in request.")
        return jsonify({"error": "Missing required fields"}), 400

    if product_id not in INVENTORY_STORE:
        logger.error("Decrement failed: Product ID %s not found.", product_id)
        return jsonify({"error": "Product not found"}), 404
    
    current_stock = INVENTORY_STORE[product_id]
    if current_stock < quantity:
        logger.warning("Decrement failed: Insufficient stock for %s (Requested: %d, Available: %d)", product_id, quantity, current_stock)
        return jsonify({"error": "Insufficient stock"}), 409 # 409 Conflict
        
    # Perform the decrement
    INVENTORY_STORE[product_id] -= quantity
    
    logger.info("Stock decremented for %s. New stock: %d", product_id, INVENTORY_STORE[product_id])
    return jsonify({"message": "Stock updated successfully", "new_stock": INVENTORY_STORE[product_id]})


# --- Application Startup ---
if __name__ == '__main__':
    logger.info("--- Inventory Service Started (Development Mode) ---")
    app.run(debug=True, host='0.0.0.0', port=5000)
