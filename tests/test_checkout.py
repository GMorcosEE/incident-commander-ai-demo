"""
Tests for Checkout API
Ensures baseline functionality works correctly.
"""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from main import app

client = TestClient(app)


def test_health_endpoint():
    """Test that health endpoint returns 200."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "checkout-api"


def test_checkout_without_discount():
    """Test successful checkout without discount code."""
    payload = {
        "items": [
            {"name": "Laptop", "price": 999.99, "quantity": 1},
            {"name": "Mouse", "price": 29.99, "quantity": 2}
        ]
    }
    
    response = client.post("/checkout", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "subtotal" in data
    assert "tax" in data
    assert "total" in data
    assert data["discount"] == 0.0
    assert data["subtotal"] == 1059.97


def test_checkout_with_save20_discount():
    """Test checkout with SAVE20 discount code (working code)."""
    payload = {
        "items": [
            {"name": "Laptop", "price": 1000.00, "quantity": 1}
        ],
        "discount_code": "SAVE20"
    }
    
    response = client.post("/checkout", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["subtotal"] == 1000.00
    assert data["discount"] == 200.00  # 20% of 1000
    assert data["tax"] == 64.00  # 8% of 800
    assert data["total"] == 864.00


def test_checkout_with_invalid_discount():
    """Test checkout with invalid discount code."""
    payload = {
        "items": [
            {"name": "Laptop", "price": 1000.00, "quantity": 1}
        ],
        "discount_code": "INVALID"
    }
    
    response = client.post("/checkout", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["discount"] == 0.0


def test_checkout_missing_items():
    """Test that checkout fails without items."""
    payload = {}
    
    response = client.post("/checkout", json=payload)
    assert response.status_code == 422  # Validation error
