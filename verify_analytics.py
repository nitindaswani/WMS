
import requests
import json
import sys

# Constants
BASE_URL = "http://127.0.0.1:8000/api"
ADMIN_EMAIL = "nitindaswani771@gmail.com"
ADMIN_PASSWORD = "admin123"

def log(msg, status="INFO"):
    print(f"[{status}] {msg}")

def test_analytics():
    # 1. Login
    log(f"Logging in as {ADMIN_EMAIL}...")
    res = requests.post(f"{BASE_URL}/auth/login/", json={
        "username": ADMIN_EMAIL, 
        "password": ADMIN_PASSWORD, 
        "role": "admin"
    })
    
    if res.status_code != 200:
        log(f"Login Failed: {res.text}", "ERROR")
        return

    data = res.json()
    token = data.get('token')
    role = data.get('role')
    log(f"Login Success. Token: {token[:10]}... Role: {role}", "SUCCESS")

    # 2. Get Analytics
    log("Fetching Analytics...")
    headers = {"Authorization": f"Token {token}"}
    res = requests.get(f"{BASE_URL}/workshops/analytics/", headers=headers)
    
    if res.status_code == 200:
        log("Analytics Response:", "SUCCESS")
        print(json.dumps(res.json(), indent=2))
    else:
        log(f"Analytics Failed: {res.status_code}", "ERROR")
        print(res.text)

if __name__ == "__main__":
    test_analytics()
