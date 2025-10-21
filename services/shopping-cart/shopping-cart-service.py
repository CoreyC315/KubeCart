# Shopping Cart Service (shopping_cart_service.py)
#
# This service manages the contents of a user's shopping cart.

from flask import Flask, jsonify, request
from flask_cors import CORS

import logging

# --- Configure Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# --- In-Memory Cart Store (Placeholder) ---
# Maps User ID to a list of cart items:
# {
#   "user-123": [
#       {"product_id": "P001", "quantity": 2},
#       {"product_id": "P003", "quantity": 1}
#   ],
#   ...
# }
CART_STORE = {}

# --- Helper Functions ---

def get_user_cart(user_id):
    """Retrieves or initializes a user's cart."""
    if user_id not in CART_STORE:
        CART_STORE[user_id] = []
        logger.info("New cart initialized for user: %s", user_id)
    return CART_STORE[user_id]

def find_item_index(cart, product_id):
    """Finds the index of a product in the cart list."""
    for i, item in enumerate(cart):
        if item['product_id'] == product_id:
            return i
    return -1

# --- API Endpoints ---

@app.route('/api/cart/<user_id>', methods=['GET'])
def view_cart(user_id):
    """
    Retrieves the contents of the specified user's cart.
    """
    logger.info("Request received to view cart for user: %s", user_id)
    cart = get_user_cart(user_id)
    return jsonify({"user_id": user_id, "items": cart})

@app.route('/api/cart/<user_id>', methods=['POST'])
def add_or_update_item(user_id):
    """
    Adds a new item or updates the quantity of an existing item in the cart.
    Request body: {"product_id": "P001", "quantity": 1}
    """
    data = request.json
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    if not product_id or quantity <= 0:
        logger.error("Add/Update failed for user %s: Invalid product_id or quantity.", user_id)
        return jsonify({"error": "Invalid product ID or quantity"}), 400

    cart = get_user_cart(user_id)
    item_index = find_item_index(cart, product_id)

    if item_index >= 0:
        # Update existing item
        cart[item_index]['quantity'] += quantity
        logger.info("Updated item %s quantity to %d for user %s.", product_id, cart[item_index]['quantity'], user_id)
    else:
        # Add new item
        cart.append({"product_id": product_id, "quantity": quantity})
        logger.info("Added new item %s (qty: %d) to cart for user %s.", product_id, quantity, user_id)

    return jsonify({"message": "Cart updated successfully", "items": cart}), 200

@app.route('/api/cart/<user_id>/<product_id>', methods=['DELETE'])
def remove_item(user_id, product_id):
    """
    Removes a specific product completely from the cart.
    """
    logger.info("Request received to remove item %s from cart for user %s.", product_id, user_id)
    cart = get_user_cart(user_id)
    item_index = find_item_index(cart, product_id)

    if item_index >= 0:
        cart.pop(item_index)
        logger.info("Removed item %s from cart for user %s.", product_id, user_id)
        return jsonify({"message": "Item removed successfully"}), 200
    
    logger.warning("Item %s not found in cart for user %s. No action taken.", product_id, user_id)
    return jsonify({"error": "Item not found in cart"}), 404

@app.route('/api/cart/<user_id>', methods=['DELETE'])
def clear_cart(user_id):
    """
    Clears the entire cart for the specified user.
    """
    if user_id in CART_STORE:
        del CART_STORE[user_id]
        logger.info("Cart cleared successfully for user: %s", user_id)
        return jsonify({"message": "Cart cleared"}), 200
    
    logger.warning("Attempted to clear non-existent cart for user: %s", user_id)
    return jsonify({"message": "Cart already empty"}), 200

# --- Application Startup ---
if __name__ == '__main__':
    logger.info("--- Shopping Cart Service Started (Development Mode) ---")
    app.run(debug=True, host='0.0.0.0', port=5001)
