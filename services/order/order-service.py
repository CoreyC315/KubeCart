# Order Service (order_service.py)
#
# This service handles the core transaction logic: receiving a final order,
# generating an ID, and storing the order record.

from flask import Flask, jsonify, request
import logging
import uuid
from datetime import datetime

# --- Configure Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# --- In-Memory Order Store (Placeholder) ---
# Stores all orders, indexed by order_id
ORDER_STORE = {}

# Maps User ID to a list of their Order IDs
USER_ORDERS = {}

# --- API Endpoints ---

@app.route('/api/order', methods=['POST'])
def place_order():
    """
    Handles a request to finalize a purchase.
    In a real system, this would:
    1. Call Payment Service (dummy).
    2. Call Inventory Service to decrement stock.
    3. Call Customer Notification Service.
    """
    data = request.json
    user_id = data.get("user_id")
    items = data.get("items", [])
    shipping_address = data.get("shipping_address")

    if not user_id or not items or not shipping_address:
        logger.error("Order placement failed for user %s: Missing user_id, items, or shipping_address.", user_id)
        return jsonify({"error": "Missing required order information"}), 400

    # 1. Generate unique Order ID
    order_id = str(uuid.uuid4())
    total_amount = sum(item.get('qty', 0) * item.get('price', 0.0) for item in items)
    
    # 2. Create Order Record
    order_record = {
        "order_id": order_id,
        "user_id": user_id,
        "items": items,
        "shipping_address": shipping_address,
        "total_amount": round(total_amount, 2),
        "status": "Processing",
        "created_at": datetime.now().isoformat()
    }
    
    # 3. Store the order
    ORDER_STORE[order_id] = order_record
    
    # 4. Update User History mapping
    if user_id not in USER_ORDERS:
        USER_ORDERS[user_id] = []
    USER_ORDERS[user_id].append(order_id)

    logger.info("Order successfully placed. ID: %s, User: %s, Total: $%.2f", order_id, user_id, total_amount)
    
    # 5. Return confirmation data
    return jsonify({
        "message": "Order placed successfully", 
        "order_id": order_id,
        "total": order_record["total_amount"],
        "status": order_record["status"]
    }), 201

@app.route('/api/orders/<user_id>', methods=['GET'])
def get_order_history(user_id):
    """
    Retrieves a list of all orders placed by the specified user.
    """
    logger.info("Request received to fetch order history for user: %s", user_id)
    
    order_ids = USER_ORDERS.get(user_id, [])
    
    history = [ORDER_STORE[oid] for oid in order_ids if oid in ORDER_STORE]
    
    logger.info("Found %d orders for user %s.", len(history), user_id)
    
    return jsonify({"user_id": user_id, "orders": history})

# --- Application Startup ---
if __name__ == '__main__':
    logger.info("--- Order Service Started (Development Mode) ---")
    app.run(debug=True, host='0.0.0.0', port=5000)
