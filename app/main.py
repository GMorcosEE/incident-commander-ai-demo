"""
E-commerce Checkout API
FastAPI service with intentional bug for incident simulation.
"""
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Ensure logs directory exists
Path("logs").mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Checkout API", version="1.0.0")


class Item(BaseModel):
    name: str
    price: float
    quantity: int


class CheckoutRequest(BaseModel):
    items: List[Item]
    discount_code: Optional[str] = None


class CheckoutResponse(BaseModel):
    subtotal: float
    discount: float
    tax: float
    total: float
    timestamp: str


@app.on_event("startup")
async def startup_event():
    logger.info("Starting Checkout API service")
    logger.info("Service initialized successfully")


@app.get("/health")
async def health():
    """Health check endpoint."""
    logger.info("Health check requested")
    return {"status": "healthy", "service": "checkout-api", "version": "1.0.0"}


def calculate_discount(subtotal: float, discount_code: str) -> float:
    """
    Calculate discount based on code.
    
    BUG: Division by zero when discount_code is 'WELCOME10'
    This simulates a production bug in discount calculation logic.
    """
    logger.info(f"Calculating discount - code: {discount_code}, subtotal: ${subtotal:.2f}")
    
    discount_rates = {
        'SAVE20': 0.20,
        'WELCOME10': 0.10,
        'FLASH50': 0.50,
        'SUMMER25': 0.25
    }
    
    if discount_code not in discount_rates:
        logger.warning(f"Invalid discount code attempted: {discount_code}")
        return 0.0
    
    rate = discount_rates[discount_code]
    logger.debug(f"Discount rate for {discount_code}: {rate}")
    
    # BUG: Intentional division by zero for WELCOME10
    # The calculation (rate * 10 - 1) equals (0.10 * 10 - 1) = 0
    if discount_code == 'WELCOME10':
        multiplier = 1 / (rate * 10 - 1)  # This will be 1 / 0
        discount = subtotal * multiplier
    else:
        discount = subtotal * rate
    
    logger.info(f"Discount calculated: ${discount:.2f}")
    return discount


@app.post("/checkout", response_model=CheckoutResponse)
async def checkout(request: CheckoutRequest):
    """
    Process checkout with items and optional discount code.
    
    Returns calculated totals including tax and discount.
    """
    try:
        logger.info(f"Checkout request received - {len(request.items)} items")
        
        # Log items for debugging
        for idx, item in enumerate(request.items):
            logger.debug(f"Item {idx + 1}: {item.name} - ${item.price} x {item.quantity}")
        
        # Calculate subtotal
        subtotal = sum(item.price * item.quantity for item in request.items)
        logger.info(f"Subtotal calculated: ${subtotal:.2f}")
        
        # Apply discount if code provided
        discount = 0.0
        if request.discount_code:
            logger.info(f"Applying discount code: {request.discount_code}")
            discount = calculate_discount(subtotal, request.discount_code)
        else:
            logger.info("No discount code provided")
        
        # Calculate tax (8%)
        tax_rate = 0.08
        discounted_subtotal = subtotal - discount
        tax = discounted_subtotal * tax_rate
        
        # Calculate total
        total = discounted_subtotal + tax
        
        result = CheckoutResponse(
            subtotal=round(subtotal, 2),
            discount=round(discount, 2),
            tax=round(tax, 2),
            total=round(total, 2),
            timestamp=datetime.utcnow().isoformat()
        )
        
        logger.info(f"Checkout completed successfully - Total: ${result.total:.2f}")
        return result
        
    except ZeroDivisionError as e:
        logger.error(f"CRITICAL ERROR: Division by zero in discount calculation")
        logger.error(f"Discount code: {request.discount_code}")
        logger.error(f"Subtotal: ${subtotal:.2f}")
        logger.exception("Full stack trace:")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during discount calculation. Error code: DISCOUNT_CALC_ERROR"
        )
    
    except Exception as e:
        logger.error(f"Unexpected error during checkout: {str(e)}")
        logger.exception("Full stack trace:")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting server on port 8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
