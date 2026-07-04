def validate_inputs(symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None):
    """Validates basic business logic constraints before calling the API."""
    errors = []

    normalized_symbol = symbol.upper().strip()
    normalized_side = side.upper().strip()
    normalized_type = order_type.upper().strip()

    # 1. Validate Order Side
    if normalized_side not in ["BUY", "SELL"]:
        errors.append(f"Invalid side '{side}'. Must be BUY or SELL.")
        
    # 2. Validate Order Type (Swapped out restricted conditional triggers for LIMIT_FOK)
    if normalized_type not in ["MARKET", "LIMIT", "LIMIT_FOK"]:
        errors.append(f"Invalid order type '{order_type}'. Must be MARKET, LIMIT, or LIMIT_FOK.")

    # 3. Validate Quantity Bound Check
    if quantity <= 0:
        errors.append("Quantity must be greater than 0.")

    # 4. Validate Price parameters on LIMIT based variants
    if normalized_type in ["LIMIT", "LIMIT_FOK"] and (price is None or price <= 0):
        errors.append(f"Price must be greater than 0 for {normalized_type} orders.")

    if errors:
        raise ValueError(" | ".join(errors))

    return normalized_symbol, normalized_side, normalized_type