import click
import sys
from bot.logging_config import setup_logging
from bot.client import get_futures_client
from bot.validators import validate_inputs
from bot.orders import place_futures_order

# Initialize logging infrastructure
setup_logging()

@click.command()
@click.option('--symbol', type=str, help='Trading pair symbol (e.g., BTCUSDT).')
@click.option('--side', type=click.Choice(['BUY', 'SELL', 'buy', 'sell']), help='Order side.')
@click.option('--type', 'order_type', type=click.Choice(['MARKET', 'LIMIT', 'LIMIT_FOK', 'market', 'limit', 'limit_fok']), help='Order type.')
@click.option('--qty', type=float, help='Quantity to trade.')
@click.option('--price', type=float, default=None, help='Price (Required for LIMIT/LIMIT_FOK).')
@click.option('--stop-price', type=float, default=None, help='Stop Price (Deprecated due to API changes).')
def run_bot(symbol, side, order_type, qty, price, stop_price):
    """Simplified Trading Bot for Binance Futures Testnet."""
    
    # Enhanced CLI UX Bonus: Fallback to interactive prompts if arguments are omitted
    if not all([symbol, side, order_type, qty]):
        click.secho("=== Interactive Mode Activated ===", fg="cyan", bold=True)
        symbol = symbol or click.prompt("Enter Symbol (e.g., BTCUSDT)")
        side = side or click.prompt("Enter Side", type=click.Choice(['BUY', 'SELL']))
        order_type = order_type or click.prompt("Enter Order Type", type=click.Choice(['MARKET', 'LIMIT', 'LIMIT_FOK']))
        qty = qty or click.prompt("Enter Quantity", type=float)
        
        if order_type.upper() in ["LIMIT", "LIMIT_FOK"] and not price:
            price = click.prompt("Enter Limit Price", type=float)

    # 1. Validation Layer
    try:
        symbol, side, order_type = validate_inputs(symbol, side, order_type, qty, price, stop_price)
    except ValueError as val_err:
        click.secho(f"\n❌ Validation Error: {val_err}", fg="red", bold=True)
        sys.exit(1)

    # 2. Client Initialization Layer
    try:
        client = get_futures_client()
    except Exception:
        click.secho("\n❌ Authentication Failure. Check your log file or .env configuration.", fg="red", bold=True)
        sys.exit(1)

    # 3. Execution Layer
    click.echo("\n--------------------------------------------------")
    click.secho("🚀 Sending order to Binance Futures Testnet...", fg="yellow")
    
    result = place_futures_order(client, symbol, side, order_type, qty, price, stop_price)

    click.echo("--------------------------------------------------")
    if result["success"]:
        click.secho("✅ ORDER PLACED SUCCESSFULLY", fg="green", bold=True)
        click.echo(f"🔹 Order ID:     {result['orderId']}")
        click.echo(f"🔹 Status:       {result['status']}")
        click.echo(f"🔹 Executed Qty: {result['executedQty']}")
        click.echo(f"🔹 Avg Price:    {result['avgPrice']}")
    else:
        click.secho("❌ ORDER EXECUTION FAILED", fg="red", bold=True)
        click.echo(f"Reason: {result['error']}")
    click.echo("--------------------------------------------------\n")

if __name__ == '__main__':
    run_bot()