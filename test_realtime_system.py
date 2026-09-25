#!/usr/bin/env python
"""
Comprehensive test of real-time data integration
Run this file to verify the system is working correctly

Usage:
    python test_realtime_system.py
"""
import requests
import json
import pandas as pd
import os
import sys

BASE_URL = "http://localhost:8000"

def print_header(title):
    """Print formatted header"""
    print("\n" + "="*70)
    print(title)
    print("="*70)

def test_health():
    """Test 1: API Health Check"""
    print_header("TEST 1: API Health Check")
    try:
        r = requests.get(f"{BASE_URL}/")
        assert r.status_code == 200, f"Status code: {r.status_code}"
        data = r.json()
        assert "message" in data
        print("✓ API is running")
        print(f"  Version: {data.get('version', 'N/A')}")
        print(f"  Features: {', '.join(data.get('features', []))}")
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False

def test_upload():
    """Test 2: Upload Dataset"""
    print_header("TEST 2: Upload Dataset")
    try:
        # Create sample data
        data = {
            'date': pd.date_range('2023-01-01', periods=12, freq='MS'),
            'revenue': list(range(50000, 62000, 1000)),
            'units': list(range(1000, 1120, 10))
        }
        df = pd.DataFrame(data)
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        
        csv_path = 'test_upload_sample.csv'
        df.to_csv(csv_path, index=False)
        
        # Upload
        with open(csv_path, 'rb') as f:
            r = requests.post(f"{BASE_URL}/upload-dataset", files={'file': f})
        
        assert r.status_code == 200, f"Status: {r.status_code}"
        result = r.json()
        assert result["status"] == "success", f"Status: {result.get('status')}"
        assert result["data"]["rows"] == 12, f"Rows: {result['data']['rows']}"
        
        os.remove(csv_path)
        print("✓ File uploaded successfully")
        print(f"  Filename: {result['data']['filename']}")
        print(f"  Rows: {result['data']['rows']}")
        print(f"  Columns: {result['data']['columns']}")
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False

def test_list_datasets():
    """Test 3: List Datasets"""
    print_header("TEST 3: List Available Datasets")
    try:
        r = requests.get(f"{BASE_URL}/datasets")
        assert r.status_code == 200, f"Status: {r.status_code}"
        result = r.json()
        datasets = result.get("datasets", [])
        print(f"✓ Found {len(datasets)} dataset(s)")
        for ds in datasets[:5]:  # Show first 5
            print(f"  - {ds['name']} ({ds['type']}, {ds['rows']} rows)")
        if len(datasets) > 5:
            print(f"  ... and {len(datasets) - 5} more")
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False

def test_realtime_data():
    """Test 4: Stream Real-Time Data"""
    print_header("TEST 4: Stream Real-Time Data")
    try:
        payload = {
            "dataset_name": "test_metrics",
            "data": {"value": 100, "timestamp": "2024-01-15T10:00:00"}
        }
        r = requests.post(f"{BASE_URL}/realtime-data", json=payload)
        assert r.status_code == 200, f"Status: {r.status_code}"
        result = r.json()
        assert result["status"] == "success", f"Status: {result.get('status')}"
        print("✓ Real-time data ingested")
        print(f"  Dataset: {result['dataset']}")
        print(f"  Timestamp: {result['timestamp']}")
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False

def test_predict():
    """Test 5: Run Prediction"""
    print_header("TEST 5: Run Real-Time Prediction")
    try:
        payload = {
            "analysis_dataset": "customer_churn_cleaned.csv",
            "forecast_dataset": "customer_churn_cleaned.csv",
            "target_column": "tenure",
            "forecast_periods": 12,
            "question": "What is the churn pattern?",
            "date_columns": ["month"]
        }
        r = requests.post(f"{BASE_URL}/predict", json=payload, timeout=30)
        assert r.status_code == 200, f"Status: {r.status_code}"
        result = r.json()
        assert result.get("status") == "success", f"Status: {result.get('status')}"
        
        # Check components
        assert "analysis" in result, "Missing analysis"
        assert "forecast" in result, "Missing forecast"
        
        print("✓ Prediction completed successfully")
        analysis = result['analysis']
        print(f"  Analysis: {len(analysis)} fields")
        print(f"  Dataset: {analysis.get('dataset_name')}")
        print(f"  Rows: {analysis['basic_statistics']['rows']}")
        
        forecast = result['forecast']
        print(f"  Forecast model: {forecast.get('model', 'N/A')}")
        print(f"  Forecast accuracy: {forecast.get('forecast_accuracy', 'N/A')}%")
        
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False

def test_chat():
    """Test 6: Chat/Q&A"""
    print_header("TEST 6: Ask Questions")
    try:
        payload = {
            "question": "What patterns do you see in customer churn?",
            "context": "Customer retention analysis"
        }
        r = requests.post(f"{BASE_URL}/chat", json=payload, timeout=30)
        assert r.status_code == 200, f"Status: {r.status_code}"
        result = r.json()
        assert result.get("status") == "success", f"Status: {result.get('status')}"
        
        print("✓ Question answered")
        print(f"  Question: {result['question']}")
        print(f"  Answer preview: {result['answer'][:100]}...")
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False

def test_quick_ask():
    """Test 7: Quick Ask"""
    print_header("TEST 7: Quick Ask Endpoint")
    try:
        payload = {
            "question": "What are the key metrics?"
        }
        r = requests.post(f"{BASE_URL}/ask", json=payload, timeout=30)
        assert r.status_code == 200, f"Status: {r.status_code}"
        result = r.json()
        assert result.get("status") == "success", f"Status: {result.get('status')}"
        
        print("✓ Quick ask successful")
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("REALTIME DATA INTEGRATION TEST SUITE")
    print("="*70)
    print(f"Testing API at: {BASE_URL}")
    
    # Check if server is running
    try:
        requests.get(f"{BASE_URL}/", timeout=2)
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Cannot connect to API server!")
        print(f"  Make sure the server is running at {BASE_URL}")
        print("\n  Start server with:")
        print("  uvicorn app:app --reload --host 0.0.0.0 --port 8000")
        return
    
    # Run tests
    tests = [
        ("Health Check", test_health),
        ("Upload Dataset", test_upload),
        ("List Datasets", test_list_datasets),
        ("Stream Real-Time", test_realtime_data),
        ("Prediction", test_predict),
        ("Chat", test_chat),
        ("Quick Ask", test_quick_ask),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Unexpected error in {name}: {e}")
            results.append((name, False))
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nResults: {passed}/{total} tests passed\n")
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {name}")
    
    print("\n" + "="*70)
    
    if passed == total:
        print("\n✓ SUCCESS! All tests passed - System is ready!\n")
        return 0
    else:
        failed = total - passed
        print(f"\n✗ {failed} test(s) failed - Review errors above\n")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
