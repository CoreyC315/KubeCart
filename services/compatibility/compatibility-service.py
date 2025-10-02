# Compatibility Service (compatibility_service.py)
#
# This service checks if a list of computer parts are compatible with each other,
# primarily focusing on socket matching (CPU <-> Motherboard).

from flask import Flask, jsonify, request
import logging

# --- Configure Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# --- Helper Functions ---

def get_required_specs(items):
    """Extracts critical specification items (CPU, Motherboard) and their sockets."""
    
    cpu_info = [item for item in items if item.get('name', '').lower() == 'cpu' and 'socket' in item]
    motherboard_info = [item for item in items if item.get('name', '').lower() == 'motherboard' and 'socket' in item]
    
    return cpu_info, motherboard_info

# --- API Endpoints ---

@app.route('/api/compatibility/check', methods=['POST'])
def check_compatibility():
    """
    Receives a list of parts and checks for required compatibility rules (e.g., socket match).
    """
    data = request.json
    items = data.get("items", [])
    
    logger.info("Request received to check compatibility for %d items.", len(items))

    # 1. Start with the assumption that everything is compatible
    is_compatible = True
    incompatibility_reasons = []

    # 2. Extract CPU and Motherboard specs
    cpus, motherboards = get_required_specs(items)
    
    # --- Check Logic: CPU to Motherboard Socket Match ---
    
    if cpus and motherboards:
        # For simplicity, we assume one CPU and one Motherboard are being checked.
        # In a real app, this would iterate through all combinations.
        cpu_socket = cpus[0]['socket'].upper()
        mb_socket = motherboards[0]['socket'].upper()
        
        logger.info("Checking socket compatibility: CPU Socket %s vs MB Socket %s", cpu_socket, mb_socket)

        if cpu_socket != mb_socket:
            is_compatible = False
            incompatibility_reasons.append(f"CPU socket ({cpu_socket}) does not match Motherboard socket ({mb_socket}).")
            logger.warning("INCOMPATIBILITY FOUND: Socket mismatch.")
            
    elif cpus and not motherboards:
        logger.info("Only CPU present. Skipping socket check.")
    elif motherboards and not cpus:
        logger.info("Only Motherboard present. Skipping socket check.")
    else:
        logger.info("Neither CPU nor Motherboard present. Check not applicable.")


    # 3. Compile the final result
    if is_compatible:
        status_message = "All core components appear compatible based on available data."
    else:
        status_message = "Incompatibility found. Review details."
        
    return jsonify({
        "compatible": is_compatible,
        "message": status_message,
        "reasons": incompatibility_reasons
    })

# --- Application Startup ---
if __name__ == '__main__':
    logger.info("--- Compatibility Service Started (Development Mode) ---")
    app.run(debug=True, host='0.0.0.0', port=5000)
