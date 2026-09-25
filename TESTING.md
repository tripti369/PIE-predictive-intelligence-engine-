










# ✅ Testing Real-Time Data Integration

This file contains step-by-step tests to verify the real-time data system is working correctly.

## Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The API should be running at: `http://localhost:8000`

---

## Test 1: API Health Check

**Verify the API is running:**

```bash
curl http://localhost:8000/
```

**Expected Response:**
```json
{
  "message": "Predictive Intelligence Engine Running",
  "version": "2.0",
  "features": ["Real-time Analysis", "Live Forecasting", "Data Upload", "Database Integration"]
}
```

---

## Test 2: Create Sample Data

**Create a test CSV file:**

```python
import pandas as pd
import os

# Create sample data
data = {
    'date': pd.date_range('2023-01-01', periods=24, freq='MS'),
    'revenue': [50000, 52000, 51500, 54000, 56000, 55800, 
                58000, 60000, 59500, 62000, 64000, 66000,
                68000, 67500, 70000, 72000, 71500, 74000,
                76000, 78000, 77500, 80000, 82000, 84000],
    'units_sold': [1500, 1620, 1580, 1700, 1800, 1780,
                   1900, 2000, 1950, 2100, 2200, 2300,
                   2400, 2350, 2500, 2600, 2550, 2700,
                   2800, 2900, 2850, 3000, 3100, 3200],
    'region': ['North America'] * 24
}

df = pd.DataFrame(data)
df['date'] = df['date'].dt.strftime('%Y-%m-%d')

# Save to CSV
os.makedirs('test_data', exist_ok=True)
df.to_csv('test_data/sample_sales.csv', index=False)

print("✓ Sample data created: test_data/sample_sales.csv")
print(f"  - Rows: {len(df)}")
print(f"  - Columns: {list(df.columns)}")
```

**Output:**
```
✓ Sample data created: test_data/sample_sales.csv
  - Rows: 24
  - Columns: ['date', 'revenue', 'units_sold', 'region']
```

---

## Test 3: Upload Dataset

**Upload the CSV file:**

```bash
curl -X POST "http://localhost:8000/upload-dataset" \
  -F "file=@test_data/sample_sales.csv" | python -m json.tool
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Dataset uploaded successfully",
  "data": {
    "filename": "sample_sales.csv",
    "rows": 24,
    "columns": ["date", "revenue", "units_sold", "region"],
    "uploaded_at": "2024-01-15T10:30:45.123456",
    "file_path": "data/uploaded/sample_sales.csv"
  }
}
```

**Verify file was saved:**
```bash
ls -la data/uploaded/
```

Should show: `sample_sales.csv`

---

## Test 4: List Available Datasets

**View all datasets:**

```bash
curl "http://localhost:8000/datasets" | python -m json.tool
```

**Expected Response:**
```json
{
  "status": "success",
  "datasets": [
    {
      "name": "sample_sales.csv",
      "type": "uploaded",
      "rows": 24,
      "columns": ["date", "revenue", "units_sold", "region"],
      "path": "data/uploaded/sample_sales.csv"
    },
    {
      "name": "Annual_P_L_1_final_cleaned.csv",
      "type": "cleaned",
      "rows": 365,
      "columns": [...],
      "path": "data/cleaned/Annual_P_L_1_final_cleaned.csv"
    }
  ]
}
```

---

## Test 5: Run Real-Time Prediction

**Execute full analysis pipeline on uploaded data:**

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "analysis_dataset": "sample_sales.csv",
    "forecast_dataset": "sample_sales.csv",
    "target_column": "revenue",
    "forecast_periods": 12,
    "question": "What will be the revenue trend for next year?",
    "date_columns": ["date"]
  }' | python -m json.tool
```

**Expected Response Structure:**
```json
{
  "status": "success",
  "analysis": {
    "dataset_name": "sample_sales.csv",
    "basic_statistics": {
      "rows": 24,
      "columns": 4,
      "missing_values": {...},
      "duplicate_rows": 0,
      "data_types": {...}
    },
    "descriptive_statistics": {...},
    "correlation": {...},
    "outlier_report": {...}
  },
  "forecast": {
    "model": "ExponentialSmoothing",
    "forecast": [85000, 87000, ...],
    "forecast_accuracy": 92
  },
  "scenario": {
    "best_case": [...],
    "base_case": [...],
    "worst_case": [...]
  },
  "rag": {
    "answer": "Based on the data..."
  },
  "decision": {
    "risk": "Low",
    "confidence": 0.92,
    "recommendation": "..."
  },
  "data_sources": {
    "analysis_dataset": "data/uploaded/sample_sales.csv",
    "forecast_dataset": "data/uploaded/sample_sales.csv"
  },
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

✅ **Success Indicators:**
- status is "success"
- All 5 components present (analysis, forecast, scenario, rag, decision)
- Forecast has actual values
- Timestamp is recent

---

## Test 6: Ask Questions

**Query about the data:**

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the average revenue per region?",
    "context": "2024 sales data"
  }' | python -m json.tool
```

**Expected Response:**
```json
{
  "status": "success",
  "question": "What is the average revenue per region?",
  "answer": "Based on the data, North America shows an average revenue of $68,500 per month...",
  "context": "2024 sales data",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

---

## Test 7: Stream Real-Time Data

**Send live data point:**

```bash
curl -X POST "http://localhost:8000/realtime-data" \
  -H "Content-Type: application/json" \
  -d '{
    "dataset_name": "hourly_sales",
    "data": {
      "timestamp": "2024-01-15T14:30:00",
      "revenue": 25000,
      "units": 320,
      "region": "North America"
    }
  }' | python -m json.tool
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Real-time data ingested",
  "dataset": "hourly_sales",
  "timestamp": "2024-01-15T14:30:00"
}
```

**Verify data was saved:**
```bash
cat data/realtime/hourly_sales_realtime.jsonl
```

Should show the JSON line you just sent.

---

## Test 8: Database Connection (Optional)

**Test PostgreSQL connection:**

```bash
curl -X POST "http://localhost:8000/database-query" \
  -H "Content-Type: application/json" \
  -d '{
    "db_type": "postgresql",
    "host": "your-db-host",
    "port": 5432,
    "username": "your-username",
    "password": "your-password",
    "database": "your-database",
    "query": "SELECT * FROM your_table LIMIT 5"
  }' | python -m json.tool
```

**Expected Response (if connection succeeds):**
```json
{
  "status": "success",
  "message": "Data fetched from database",
  "rows": 5,
  "columns": ["col1", "col2", "col3"],
  "file_path": "data/uploaded/db_query_1705318245.csv"
}
```

---

## Test 9: Full Python Test Script

**Save as `test_realtime.py` and run:**

```python
#!/usr/bin/env python
"""
Comprehensive test of real-time data integration
"""
import requests
import json
import pandas as pd
import os

BASE_URL = "http://localhost:8000"

def test_health():
    """Test 1: API Health"""
    print("\n" + "="*70)
    print("TEST 1: API Health Check")
    print("="*70)
    try:
        r = requests.get(f"{BASE_URL}/")
        assert r.status_code == 200
        assert r.json()["message"] == "Predictive Intelligence Engine Running"
        print("✅ PASS: API is running")
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False

def test_upload():
    """Test 2: Upload Dataset"""
    print("\n" + "="*70)
    print("TEST 2: Upload Dataset")
    print("="*70)
    try:
        # Create sample file
        data = {
            'date': pd.date_range('2023-01-01', periods=12, freq='MS'),
            'revenue': range(50000, 62000, 1000),
            'units': range(1000, 1120, 10)
        }
        df = pd.DataFrame(data)
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        
        csv_path = 'test_upload.csv'
        df.to_csv(csv_path, index=False)
        
        # Upload
        with open(csv_path, 'rb') as f:
            r = requests.post(f"{BASE_URL}/upload-dataset", files={'file': f})
        
        assert r.status_code == 200
        assert r.json()["status"] == "success"
        assert r.json()["data"]["rows"] == 12
        
        os.remove(csv_path)
        print("✅ PASS: File uploaded successfully")
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False

def test_list_datasets():
    """Test 3: List Datasets"""
    print("\n" + "="*70)
    print("TEST 3: List Available Datasets")
    print("="*70)
    try:
        r = requests.get(f"{BASE_URL}/datasets")
        assert r.status_code == 200
        datasets = r.json()["datasets"]
        print(f"✅ PASS: Found {len(datasets)} dataset(s)")
        for ds in datasets:
            print(f"  - {ds['name']} ({ds['type']}, {ds['rows']} rows)")
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False

def test_realtime_data():
    """Test 4: Stream Real-Time Data"""
    print("\n" + "="*70)
    print("TEST 4: Stream Real-Time Data")
    print("="*70)
    try:
        payload = {
            "dataset_name": "test_metrics",
            "data": {"value": 100, "timestamp": "2024-01-15T10:00:00"}
        }
        r = requests.post(f"{BASE_URL}/realtime-data", json=payload)
        assert r.status_code == 200
        assert r.json()["status"] == "success"
        print("✅ PASS: Real-time data ingested")
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False

def test_predict():
    """Test 5: Run Prediction"""
    print("\n" + "="*70)
    print("TEST 5: Run Real-Time Prediction")
    print("="*70)
    try:
        # Use a cleaned dataset
        payload = {
            "analysis_dataset": "customer_churn_cleaned.csv",
            "forecast_dataset": "customer_churn_cleaned.csv",
            "target_column": "tenure",
            "forecast_periods": 12,
            "question": "What is the churn pattern?",
            "date_columns": ["month"]
        }
        r = requests.post(f"{BASE_URL}/predict", json=payload)
        assert r.status_code == 200
        result = r.json()
        assert result["status"] == "success"
        assert "analysis" in result
        assert "forecast" in result
        print("✅ PASS: Prediction completed successfully")
        print(f"  - Analysis: {len(result['analysis'])} fields")
        print(f"  - Forecast accuracy: {result['forecast'].get('forecast_accuracy')}%")
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False

def test_chat():
    """Test 6: Chat/Q&A"""
    print("\n" + "="*70)
    print("TEST 6: Ask Questions")
    print("="*70)
    try:
        payload = {
            "question": "What patterns do you see in the data?"
        }
        r = requests.post(f"{BASE_URL}/chat", json=payload)
        assert r.status_code == 200
        assert r.json()["status"] == "success"
        print("✅ PASS: Question answered")
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False

def main():
    print("\n" + "="*70)
    print("REALTIME DATA INTEGRATION TEST SUITE")
    print("="*70)
    
    tests = [
        test_health,
        test_upload,
        test_list_datasets,
        test_realtime_data,
        test_predict,
        test_chat
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"Error running test: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED - System is ready for production!")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed - Review errors above")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
```

**Run the test:**
```bash
python test_realtime.py
```

---

## Test 10: Interactive API Documentation

**Open your browser and visit:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

You can:
- See all endpoints
- Try requests directly
- View response schemas
- Download API specification

---

## Troubleshooting Failed Tests

### If Test 1 Fails: API Not Running
```bash
# Check if server is running
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Start server
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### If Test 2 Fails: Upload Issue
```bash
# Check upload directory exists
ls -la data/uploaded/

# Check file permissions
chmod 755 data/uploaded/
```

### If Test 5 Fails: Dataset Not Found
```bash
# List available datasets first
curl http://localhost:8000/datasets

# Use actual filename from response
```

### If Any Test Has "Connection Refused"
- Server is not running
- Wrong port (default is 8000)
- Firewall blocking port

---

## Continuous Testing

**Run tests periodically:**

```bash
# Every hour
watch -n 3600 python test_realtime.py

# Every day at 8 AM
0 8 * * * python test_realtime.py >> test_results.log
```

---

## Success Criteria

Your real-time data integration is working when:

✅ All 6 tests pass
✅ Data uploads successfully
✅ Predictions complete without errors
✅ Questions receive answers
✅ Real-time data is ingested
✅ Datasets are listed correctly

---

## Next Steps

1. ✅ Run all tests
2. ✅ Verify everything passes
3. 📤 Upload your actual company data
4. 🔄 Test with real-time streaming
5. 🔗 Connect to your database
6. 🚀 Deploy to production

Good luck! 🎉
