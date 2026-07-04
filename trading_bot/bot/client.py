import os
import time
import logging
from binance import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("TradingBot.Client")

def get_futures_client():
    """Initializes and returns a Binance Client with absolute automatic clock synchronization."""
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        logger.error("API Credentials missing in environment variables.")
        raise ValueError("Missing BINANCE_API_KEY or BINANCE_API_SECRET in .env file")

    try:
        # 1. Initialize client base wrapper instance
        client = Client(api_key, api_secret, testnet=True)
        
        # 2. Programmatically fetch the absolute real-time server clock state
        logger.info("Synchronizing local timeline parameters with Binance servers...")
        server_time = client.get_server_time()
        local_time_ms = int(time.time() * 1000)
        
        # 3. Calculate structural delta difference gaps
        server_offset = server_time['serverTime'] - local_time_ms
        client.timestamp_offset = server_offset
        
        logger.info(f"Clock Sync Complete. Server offset detected & applied: {server_offset}ms")
        
        # Verify connection capability
        client.futures_ping()
        logger.info("Successfully connected to Binance Futures Testnet API.")
        return client
    except BinanceAPIException as e:
        logger.error(f"Failed to connect to Binance Testnet: {e.message} (Code: {e.code})")
        raise
    except Exception as e:
        logger.error(f"Unexpected connection error: {str(e)}")
        raise