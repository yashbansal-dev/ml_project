import requests
import json

def test_url(url):
    print(f"\n[TESTING URL]: {url}")
    try:
        response = requests.post("http://localhost:8000/predict", json={"url": url})
        if response.status_code == 200:
            result = response.json()
            print(f"Prediction: {result['prediction']}")
            print(f"Risk Score: {result['risk_score']}")
            print(f"Features Detected: {len(result['features'])} metrics analyzed")
            return result
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Connection failed: {e}")

# 1. Test Whitelist (Should be 0% risk)
test_url("https://www.google.com")

# 2. Test Typosquatting (Should be caught by heuristic)
test_url("https://g00gle.com")

# 3. Test Common Benign
test_url("https://github.com/yashbansal-dev")

# 4. Test Malicious Pattern (Suspicious length + dots + symbols)
test_url("http://secure-login-update-account-verification.check-info.top/login?id=99283")
