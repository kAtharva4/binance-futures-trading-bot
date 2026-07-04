import logging
from binance.exceptions import BinanceAPIException

logger = logging.getLogger("TradingBot.Orders")

def place_futures_order(client, symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None):
    """Handles routing and payload formatting for sending orders to Binance Futures."""
    
    # Pre-configured 60s latency receive window safety buffer
    params = {
        "symbol": symbol,
        "side": side,
        "quantity": quantity,
        "recvWindow": 60000  
    }

    # Route and add core execution modifiers directly supported by standard /fapi/v1/order
    if order_type == "MARKET":
        params["type"] = "MARKET"
    elif order_type == "LIMIT":
        params["type"] = "LIMIT"
        params["price"] = str(price)
        params["timeInForce"] = "GTC"  # Good 'Til Cancelled
    elif order_type == "LIMIT_FOK":
        params["type"] = "LIMIT"
        params["price"] = str(price)
        params["timeInForce"] = "FOK"  # Advanced execution instruction: Fill whole size instantly or kill order.

    logger.info(f"Sending Order Request Summary: {params}")

    try:
        # Execute order via standard python-binance futures wrapper
        response = client.futures_create_order(**params)
        logger.info(f"Order Executed Successfully. OrderID: {response.get('orderId')}")
        return {
            "success": True,
            "orderId": response.get("orderId"),
            "status": response.get("status"),
            "executedQty": response.get("executedQty"),
            "avgPrice": response.get("avgPrice", "N/A"),
            "raw": response
        }
    except BinanceAPIException as e:
        logger.error(f"Binance API Error: {e.message} (Status Code: {e.status_code}, Error Code: {e.code})")
        return {"success": False, "error": e.message, "code": e.code}
    except Exception as e:
        logger.error(f"Network or systemic failure executing order: {str(e)}")
        return {"success": False, "error": str(e)}