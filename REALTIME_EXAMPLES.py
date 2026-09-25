"""
REAL-TIME DATA INTEGRATION EXAMPLES
Predictive Intelligence Engine

This file shows practical examples of using the API with real-time company data.
"""

import requests
import json
import pandas as pd

BASE_URL = "http://localhost:8000"

# =============================================================================
# EXAMPLE 1: Upload Company Data and Run Analysis
# =============================================================================
def example_upload_and_analyze():
    """Upload a CSV file from your company system and run analysis"""
    
    print("\n" + "="*70)
    print("EXAMPLE 1: Upload Company Data")
    print("="*70)
    
    # Upload a CSV file
    with open("your_company_data.csv", "rb") as f:
        files = {"file": f}
        response = requests.post(f"{BASE_URL}/upload-dataset", files=files)
    
    print("Upload Response:", json.dumps(response.json(), indent=2))
    uploaded_file = response.json()["data"]["filename"]
    
    # Now run prediction on the uploaded data
    predict_payload = {
        "analysis_dataset": uploaded_file,
        "forecast_dataset": uploaded_file,
        "target_column": "revenue",
        "forecast_periods": 12,
        "question": "What is the trend for next quarter?",
        "date_columns": ["date"]
    }
    
    response = requests.post(f"{BASE_URL}/predict", json=predict_payload)
    print("\nPrediction Response:", json.dumps(response.json(), indent=2))


# =============================================================================
# EXAMPLE 2: Connect to Company Database and Get Real-Time Data
# =============================================================================
def example_database_connection():
    """Connect to your company database and fetch live data"""
    
    print("\n" + "="*70)
    print("EXAMPLE 2: Real-Time Database Integration")
    print("="*70)
    
    # PostgreSQL Example
    db_payload = {
        "db_type": "postgresql",
        "host": "your-db-server.company.com",
        "port": 5432,
        "username": "analyst",
        "password": "your_secure_password",
        "database": "production",
        "query": "SELECT date, revenue, region FROM sales WHERE date >= NOW() - INTERVAL '30 days' ORDER BY date"
    }
    
    response = requests.post(f"{BASE_URL}/database-query", json=db_payload)
    print("Database Query Response:", json.dumps(response.json(), indent=2))
    
    db_file_path = response.json()["file_path"]
    
    # Use the fetched data for prediction
    predict_payload = {
        "analysis_dataset": db_file_path,
        "forecast_dataset": db_file_path,
        "target_column": "revenue",
        "forecast_periods": 30,
        "question": "What will revenue be next month?",
        "date_columns": ["date"]
    }
    
    response = requests.post(f"{BASE_URL}/predict", json=predict_payload)
    print("\nPrediction from Database:", json.dumps(response.json(), indent=2))


# =============================================================================
# EXAMPLE 3: Stream Real-Time Data Points
# =============================================================================
def example_realtime_streaming():
    """Stream live data points from sensors, APIs, or business systems"""
    
    print("\n" + "="*70)
    print("EXAMPLE 3: Real-Time Data Streaming")
    print("="*70)
    
    # Simulate streaming data from various company sources
    data_points = [
        {
            "timestamp": "2024-01-15T10:00:00",
            "revenue": 15000,
            "units_sold": 250,
            "region": "North America",
            "customer_count": 45
        },
        {
            "timestamp": "2024-01-15T11:00:00",
            "revenue": 18500,
            "units_sold": 310,
            "region": "North America",
            "customer_count": 52
        },
        {
            "timestamp": "2024-01-15T12:00:00",
            "revenue": 16800,
            "units_sold": 280,
            "region": "North America",
            "customer_count": 48
        }
    ]
    
    for data_point in data_points:
        payload = {
            "dataset_name": "hourly_sales_metrics",
            "data": data_point,
            "timestamp": data_point["timestamp"]
        }
        
        response = requests.post(f"{BASE_URL}/realtime-data", json=payload)
        print(f"Ingested: {data_point['timestamp']} - {response.json()['message']}")


# =============================================================================
# EXAMPLE 4: Interactive Questions About Real-Time Data
# =============================================================================
def example_chat_with_data():
    """Ask questions about real-time data using AI"""
    
    print("\n" + "="*70)
    print("EXAMPLE 4: Interactive Q&A with Real-Time Data")
    print("="*70)
    
    questions = [
        "What are the top 3 regions by revenue this month?",
        "What is the churn rate trend?",
        "Which product line is declining?",
        "What are the key risk factors for Q2?"
    ]
    
    for question in questions:
        payload = {
            "question": question,
            "context": "Q1 2024 sales data"
        }
        
        response = requests.post(f"{BASE_URL}/chat", json=payload)
        result = response.json()
        
        print(f"\nQ: {question}")
        print(f"A: {result.get('answer', 'No answer available')}")


# =============================================================================
# EXAMPLE 5: List All Available Datasets
# =============================================================================
def example_list_datasets():
    """View all available datasets (uploaded, cleaned, from database)"""
    
    print("\n" + "="*70)
    print("EXAMPLE 5: Available Datasets")
    print("="*70)
    
    response = requests.get(f"{BASE_URL}/datasets")
    datasets = response.json().get("datasets", [])
    
    print(f"\nTotal Datasets: {len(datasets)}\n")
    
    for dataset in datasets:
        print(f"Name: {dataset['name']}")
        print(f"Type: {dataset['type']}")
        print(f"Rows: {dataset['rows']}")
        print(f"Columns: {', '.join(dataset['columns'][:5])}{'...' if len(dataset['columns']) > 5 else ''}")
        print(f"Path: {dataset['path']}")
        print("-" * 50)


# =============================================================================
# EXAMPLE 6: Full Workflow - From Data to Decision
# =============================================================================
def example_complete_workflow():
    """Complete workflow: Upload → Analyze → Forecast → Decide"""
    
    print("\n" + "="*70)
    print("EXAMPLE 6: Complete Real-Time Workflow")
    print("="*70)
    
    # Step 1: Create sample data
    print("\n[Step 1] Creating sample company data...")
    data = {
        "date": pd.date_range("2024-01-01", periods=12, freq="MS"),
        "revenue": [50000, 52000, 51500, 54000, 56000, 55800, 58000, 60000, 59500, 62000, 64000, 66000],
        "expenses": [30000, 31000, 30800, 32000, 33000, 32900, 34000, 35000, 34700, 36000, 37000, 38000]
    }
    df = pd.DataFrame(data)
    df.to_csv("sample_company_data.csv", index=False)
    print("✓ Sample data created")
    
    # Step 2: Upload data
    print("\n[Step 2] Uploading data to system...")
    with open("sample_company_data.csv", "rb") as f:
        files = {"file": f}
        response = requests.post(f"{BASE_URL}/upload-dataset", files=files)
    
    if response.json()["status"] == "success":
        filename = response.json()["data"]["filename"]
        print(f"✓ Data uploaded: {filename}")
    else:
        print("✗ Upload failed")
        return
    
    # Step 3: Run complete analysis
    print("\n[Step 3] Running real-time analysis...")
    predict_payload = {
        "analysis_dataset": filename,
        "forecast_dataset": filename,
        "target_column": "revenue",
        "forecast_periods": 12,
        "question": "What is the revenue forecast for next year?",
        "date_columns": ["date"]
    }
    
    response = requests.post(f"{BASE_URL}/predict", json=predict_payload)
    result = response.json()
    
    if result["status"] == "success":
        print("✓ Analysis complete")
        
        # Display key results
        analysis = result["analysis"]
        print(f"\n  Dataset Stats:")
        print(f"    - Rows: {analysis['basic_statistics']['rows']}")
        print(f"    - Columns: {analysis['basic_statistics']['columns']}")
        print(f"    - Missing Values: {analysis['basic_statistics']['missing_values']}")
        
        print(f"\n  Forecast:")
        forecast = result["forecast"]
        print(f"    - Model: {forecast.get('model', 'N/A')}")
        print(f"    - Accuracy: {forecast.get('forecast_accuracy', 'N/A')}%")
        
        print(f"\n  Decision:")
        decision = result["decision"]
        print(f"    - Risk Level: {decision.get('risk', 'N/A')}")
        print(f"    - Recommendation: {decision.get('recommendation', 'N/A')}")
        
    else:
        print(f"✗ Analysis failed: {result['message']}")


# =============================================================================
# USAGE
# =============================================================================
if __name__ == "__main__":
    print("\n" + "="*70)
    print("PREDICTIVE INTELLIGENCE ENGINE - REAL-TIME DATA EXAMPLES")
    print("="*70)
    
    # Uncomment the examples you want to run
    
    # example_list_datasets()
    # example_upload_and_analyze()
    # example_database_connection()
    # example_realtime_streaming()
    # example_chat_with_data()
    example_complete_workflow()
    
    print("\n" + "="*70)
    print("Examples completed!")
    print("="*70)
