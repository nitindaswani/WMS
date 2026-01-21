import requests
import time
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_workshops_performance():
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/workshops/")
    end_time = time.time()

    print(f"GET /workshops/ Status: {response.status_code}")
    print(f"GET /workshops/ Time: {end_time - start_time:.4f}s")

    if response.status_code == 200:
        data = response.json()
        print(f"Fetched {len(data)} workshops")
        # Check if sessions are loaded (potential N+1 if not eager loaded)
        # We can't strictly detect N+1 from outside without timing or db logs,
        # but we can see if the response contains nested data.
        if len(data) > 0:
            print("Sample workshop keys:", data[0].keys())

def test_workshop_detail_performance(id):
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/workshops/{id}/")
    end_time = time.time()

    print(f"GET /workshops/{id}/ Status: {response.status_code}")
    print(f"GET /workshops/{id}/ Time: {end_time - start_time:.4f}s")

if __name__ == "__main__":
    print("Testing Workshops List Performance...")
    test_workshops_performance()

    # Test a specific workshop detail if any exist
    # from previous run we know ID 29 exists, but let's just pick one dynamically or hardcode one that exists
    # List output showed IDs like 29, 20, 19...
    print("\nTesting Workshop Detail Performance...")
    test_workshop_detail_performance(20)
