import os
import sys

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to EduGenie" in response.text
    assert "qaForm" in response.text
    assert "explainForm" in response.text
    assert "summaryForm" in response.text
    assert "quizForm" in response.text
    assert "quizNum" in response.text
    assert "recommendForm" in response.text

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "app": "EduGenie"}

def test_static_css():
    response = client.get("/static/style.css")
    assert response.status_code == 200
    assert "--primary-color" in response.text

def test_endpoints_validation():
    # Test POST /explain without topic returns 400
    res = client.post("/explain", json={})
    assert res.status_code == 400

    # Test POST /summarize without text returns 400
    res = client.post("/summarize", json={})
    assert res.status_code == 400

    # Test POST /quiz without text returns 400
    res = client.post("/quiz", json={})
    assert res.status_code == 400

if __name__ == "__main__":
    print("Running EduGenie App Tests...")
    test_home_page()
    print("[PASS] Home Page Test Passed")
    test_health_check()
    print("[PASS] Health Check Test Passed")
    test_static_css()
    print("[PASS] Static CSS Test Passed")
    test_endpoints_validation()
    print("[PASS] Endpoints Validation Test Passed")
    print("All app route and template tests completed successfully!")
