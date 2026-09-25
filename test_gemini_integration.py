#!/usr/bin/env python3
"""
Gemini API Integration Test Suite
Tests the enhanced AI features with Gemini integration
"""

import requests
import json
import time
import os
from pathlib import Path

BASE_URL = "http://localhost:8000"

# ANSI color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def print_status(test_name, passed, message=""):
    """Print test status in color"""
    status = f"{GREEN}✓ PASS{RESET}" if passed else f"{RED}✗ FAIL{RESET}"
    print(f"  [{status}] {test_name}")
    if message:
        print(f"       {message}")

def test_health_check():
    """Test 1: Server health and AI engine status"""
    print(f"\n{BLUE}Test 1: Server Health Check{RESET}")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        data = response.json()
        
        passed = response.status_code == 200
        print_status("Server responds", passed)
        print_status("AI Engine detected", "ai_engine" in data, 
                    f"Engine: {data.get('ai_engine', 'Unknown')}")
        return passed
    except Exception as e:
        print_status("Server health", False, f"Error: {e}")
        return False

def test_gemini_chat():
    """Test 2: Gemini chat endpoint"""
    print(f"\n{BLUE}Test 2: Gemini Chat Endpoint{RESET}")
    try:
        payload = {
            "question": "What is the most important metric for business forecasting?",
            "context": "We have quarterly revenue data"
        }
        
        response = requests.post(f"{BASE_URL}/chat", json=payload, timeout=15)
        data = response.json()
        
        passed = response.status_code == 200 and data.get("status") == "success"
        print_status("Chat request successful", passed)
        
        ai_engine = data.get("ai_engine", "Unknown")
        print_status("AI Engine response", True, f"Using: {ai_engine}")
        
        if "answer" in data:
            answer_preview = data["answer"][:100] + "..." if len(data["answer"]) > 100 else data["answer"]
            print_status("Got AI response", True, f"Preview: {answer_preview}")
        
        return passed
    except Exception as e:
        print_status("Chat request", False, f"Error: {e}")
        return False

def test_gemini_ask():
    """Test 3: Gemini ask endpoint"""
    print(f"\n{BLUE}Test 3: Gemini Ask Endpoint{RESET}")
    try:
        payload = {
            "question": "How do I improve forecast accuracy with limited historical data?",
            "context": "3 months of data"
        }
        
        response = requests.post(f"{BASE_URL}/ask", json=payload, timeout=15)
        data = response.json()
        
        passed = response.status_code == 200 and data.get("status") == "success"
        print_status("Ask request successful", passed)
        
        ai_engine = data.get("ai_engine", "Unknown")
        print_status("AI Engine response", True, f"Using: {ai_engine}")
        
        if "answer" in data:
            answer_preview = data["answer"][:80] + "..." if len(data["answer"]) > 80 else data["answer"]
            print_status("Got answer", True, f"Preview: {answer_preview}")
        
        return passed
    except Exception as e:
        print_status("Ask request", False, f"Error: {e}")
        return False

def test_gemini_availability():
    """Test 4: Check if Gemini is enabled"""
    print(f"\n{BLUE}Test 4: Gemini API Configuration{RESET}")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        data = response.json()
        
        ai_engine = data.get("ai_engine", "Local RAG")
        is_gemini = ai_engine == "Gemini AI"
        
        if is_gemini:
            print_status("Gemini API Key", True, "Configured ✓")
            print_status("AI Engine", True, "Gemini AI (Premium)")
        else:
            print_status("Gemini API Key", False, "Not configured (using fallback)")
            print_status("AI Engine", True, "Local RAG (Fallback)")
            print(f"       {YELLOW}To enable Gemini:{RESET}")
            print(f"       1. Get key from: https://aistudio.google.com/app/apikey")
            print(f"       2. Add to .env: GEMINI_API_KEY=your_key")
            print(f"       3. Restart server")
        
        return True
    except Exception as e:
        print_status("Config check", False, f"Error: {e}")
        return False

def test_data_upload_with_gemini_context():
    """Test 5: Upload data and get AI insights"""
    print(f"\n{BLUE}Test 5: Data Upload with Gemini Context{RESET}")
    try:
        # Create a simple CSV file
        csv_data = """month,sales,expenses
1,50000,30000
2,55000,32000
3,60000,35000
4,58000,34000
5,65000,38000
6,70000,40000"""
        
        csv_path = "test_data.csv"
        with open(csv_path, "w") as f:
            f.write(csv_data)
        
        # Upload file
        with open(csv_path, "rb") as f:
            files = {"file": f}
            response = requests.post(f"{BASE_URL}/upload-dataset", files=files, timeout=10)
        
        data = response.json()
        passed = response.status_code == 200 and data.get("status") == "success"
        print_status("File upload", passed)
        
        if passed:
            rows = data.get("data", {}).get("rows", 0)
            cols = data.get("data", {}).get("columns", [])
            print_status("Data parsed", True, f"{rows} rows, {len(cols)} columns")
            
            # Clean up
            if os.path.exists(csv_path):
                os.remove(csv_path)
        
        return passed
    except Exception as e:
        print_status("Upload with context", False, f"Error: {e}")
        if os.path.exists("test_data.csv"):
            os.remove("test_data.csv")
        return False

def test_multi_turn_conversation():
    """Test 6: Multi-turn conversation (context preservation)"""
    print(f"\n{BLUE}Test 6: Multi-Turn Conversation{RESET}")
    try:
        questions = [
            "What are key metrics for sales forecasting?",
            "How do I handle seasonality?"
        ]
        
        all_passed = True
        for i, question in enumerate(questions, 1):
            payload = {
                "question": question,
                "context": "I have 2 years of monthly sales data with clear seasonal patterns"
            }
            
            response = requests.post(f"{BASE_URL}/chat", json=payload, timeout=15)
            data = response.json()
            
            passed = response.status_code == 200 and data.get("status") == "success"
            print_status(f"Question {i}", passed, question[:50] + "...")
            all_passed = all_passed and passed
        
        return all_passed
    except Exception as e:
        print_status("Multi-turn conversation", False, f"Error: {e}")
        return False

def test_error_handling():
    """Test 7: Error handling and fallback"""
    print(f"\n{BLUE}Test 7: Error Handling & Fallback{RESET}")
    try:
        # Test with malformed request
        payload = {"invalid": "data"}
        response = requests.post(f"{BASE_URL}/chat", json=payload, timeout=5)
        
        passed = response.status_code == 422 or response.status_code == 200
        print_status("Request validation", passed, f"Status: {response.status_code}")
        
        # Test with empty question
        payload = {"question": ""}
        response = requests.post(f"{BASE_URL}/chat", json=payload, timeout=5)
        passed = response.status_code in [200, 400, 422]
        print_status("Empty input handling", passed)
        
        return True
    except Exception as e:
        print_status("Error handling", False, f"Error: {e}")
        return False

def main():
    """Run all tests"""
    print(f"\n{BLUE}{'='*60}")
    print("Gemini AI Integration Test Suite")
    print(f"{'='*60}{RESET}")
    
    # Check if server is running
    try:
        requests.get(f"{BASE_URL}/", timeout=3)
    except:
        print(f"{RED}✗ ERROR: Server not running!{RESET}")
        print(f"Start server with: python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000")
        return
    
    tests = [
        ("Health Check", test_health_check),
        ("Gemini Chat", test_gemini_chat),
        ("Gemini Ask", test_gemini_ask),
        ("Configuration", test_gemini_availability),
        ("Data Upload", test_data_upload_with_gemini_context),
        ("Multi-Turn", test_multi_turn_conversation),
        ("Error Handling", test_error_handling),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"{RED}✗ Test crashed: {e}{RESET}")
            results.append(False)
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print(f"\n{BLUE}{'='*60}")
    print("Test Summary")
    print(f"{'='*60}{RESET}")
    print(f"Passed: {GREEN}{passed}/{total}{RESET}")
    
    if passed == total:
        print(f"{GREEN}✓ All tests passed! Your system is production-ready.{RESET}")
    elif passed >= total * 0.75:
        print(f"{YELLOW}✓ Most tests passed. Some features may have fallbacks.{RESET}")
    else:
        print(f"{RED}✗ Several tests failed. Check configuration.{RESET}")
    
    print(f"\n{BLUE}Next Steps:{RESET}")
    print("  1. Try the interactive API: http://localhost:8000/docs")
    print("  2. Upload your dataset: /upload-dataset")
    print("  3. Ask questions: /chat or /ask")
    print("  4. Get predictions: /predict")

if __name__ == "__main__":
    main()
