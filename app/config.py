"""
Configuration for Checkout API
"""
import os


class Config:
    """Application configuration."""
    
    # API settings
    API_VERSION = "1.0.0"
    SERVICE_NAME = "checkout-api"
    
    # Logging
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    LOG_DIR = "logs"
    
    # Business logic
    TAX_RATE = 0.08
    MAX_ITEMS_PER_CHECKOUT = 100
    
    # Valid discount codes
    DISCOUNT_CODES = {
        'SAVE20': 0.20,
        'WELCOME10': 0.10,
        'FLASH50': 0.50,
        'SUMMER25': 0.25
    }
