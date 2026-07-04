import logging
import os

def setup_logging():
    """Configures logging to both a file and the console."""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_format = logging.Formatter(
        '%(asctime).19s [%(levelname)s] %(name)s: %(message)s'
    )

    # File Handler
    file_handler = logging.FileHandler(os.path.join(log_dir, "bot.log"))
    file_handler.setFormatter(log_format)
    file_handler.setLevel(logging.DEBUG)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    console_handler.setLevel(logging.INFO)

    # Root Logger Config
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Silence verbose third-party logs
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("binance").setLevel(logging.WARNING)