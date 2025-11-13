#!/usr/bin/env python3
"""
Incident Simulation Script
Triggers the WELCOME10 discount bug to generate reproducible error logs.
"""
import requests
import json
import sys
import time

API_URL = "http://localhost:8000"


def wait_for_api(max_retries=30, delay=1):
    """Wait for API to be ready."""
    print("Waiting for API to be ready...")
    for i in range(max_retries):
        try:
            response = requests.get(f"{API_URL}/health", timeout=2)
            if response.status_code == 200:
                print("✅ API is ready")
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(delay)
    print("❌ API did not become ready in time")
    return False


def simulate_successful_checkout():
    """Simulate a successful checkout without discount."""
    print("\n" + "="*60)
    print("TEST 1: Successful checkout (no discount)")
    print("="*60)
    
    payload = {
        "items": [
            {"name": "Laptop", "price": 999.99, "quantity": 1},
            {"name": "Mouse", "price": 29.99, "quantity": 2}
        ]
    }
    
    try:
        response = requests.post(f"{API_URL}/checkout", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("✅ Successful checkout completed")
    except Exception as e:
        print(f"❌ Error: {e}")


def simulate_incident():
    """Simulate the WELCOME10 discount bug."""
    print("\n" + "="*60)
    print("TEST 2: Triggering WELCOME10 bug (INCIDENT)")
    print("="*60)
    
    payload = {
        "items": [
            {"name": "Laptop", "price": 999.99, "quantity": 1},
            {"name": "Keyboard", "price": 79.99, "quantity": 1}
        ],
        "discount_code": "WELCOME10"
    }
    
    print(f"Sending checkout request with discount code: WELCOME10")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(f"{API_URL}/checkout", json=payload)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 500:
            print("\n❌ INCIDENT TRIGGERED: Server returned 500 error")
            print("Check logs/app.log for full stack trace")
        else:
            print("⚠️  Expected 500 error but got different status")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")


def main():
    """Run incident simulation."""
    print("="*60)
    print("INCIDENT COMMANDER AI - Incident Simulation")
    print("="*60)
    
    if not wait_for_api():
        print("\n❌ Cannot proceed - API is not running")
        print("Start the API first: cd app && uvicorn main:app --host 0.0.0.0 --port 8000")
        sys.exit(1)
    
    # Run successful checkout first
    simulate_successful_checkout()
    
    # Trigger the incident
    simulate_incident()
    
    print("\n" + "="*60)
    print("Simulation complete. Check logs/app.log for details.")
    print("="*60)


if __name__ == "__main__":
    main()
