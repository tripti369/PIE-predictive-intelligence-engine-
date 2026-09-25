# Real-Time Data Integration Configuration Guide

## Quick Start: 3 Ways to Connect Real-Time Data

### Method 1: Upload CSV/Excel Files (Fastest)
```bash
curl -X POST "http://localhost:8000/upload-dataset" \
  -F "file=@Q1_2024_sales.csv"
```

Then use in predictions:
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "analysis_dataset": "Q1_2024_sales.csv",
    "forecast_dataset": "Q1_2024_sales.csv",
    "target_column": "revenue",
    "forecast_periods": 12,
    "question": "Forecast next quarter revenue?"
  }'
```

---

### Method 2: Real-Time Data Streaming (Live Updates)
For IoT sensors, trading data, or live metrics:

```python
import requests

# Stream a single data point
requests.post("http://localhost:8000/realtime-data", json={
    "dataset_name": "daily_sales",
    "data": {
        "date": "2024-01-15",
        "revenue": 45000,
        "units_sold": 320
    }
})
```

---

### Method 3: Connect to Company Database (Production)

#### PostgreSQL
```bash
curl -X POST "http://localhost:8000/database-query" \
  -H "Content-Type: application/json" \
  -d '{
    "db_type": "postgresql",
    "host": "analytics.company.com",
    "port": 5432,
    "username": "analytics_user",
    "password": "secure_password",
    "database": "production",
    "query": "SELECT date, revenue, region, product FROM sales_fact WHERE date >= CURRENT_DATE - 90"
  }'
```

#### MySQL
```bash
curl -X POST "http://localhost:8000/database-query" \
  -H "Content-Type: application/json" \
  -d '{
    "db_type": "mysql",
    "host": "db.company.local",
    "port": 3306,
    "username": "analytics",
    "password": "your_password",
    "database": "warehouse",
    "query": "SELECT * FROM daily_metrics WHERE date >= DATE_SUB(NOW(), INTERVAL 30 DAY)"
  }'
```

#### Microsoft SQL Server
```bash
curl -X POST "http://localhost:8000/database-query" \
  -H "Content-Type: application/json" \
  -d '{
    "db_type": "mssql",
    "host": "sql-server.company.com",
    "port": 1433,
    "username": "analytics_user",
    "password": "password",
    "database": "DW_Production",
    "query": "SELECT TOP 1000 * FROM [Sales].[Facts] WHERE TransactionDate >= DATEADD(day, -30, CAST(GETDATE() AS DATE))"
  }'
```

#### SQLite
```bash
curl -X POST "http://localhost:8000/database-query" \
  -H "Content-Type: application/json" \
  -d '{
    "db_type": "sqlite",
    "host": "localhost",
    "port": 0,
    "username": "",
    "password": "",
    "database": "/path/to/company_data.db",
    "query": "SELECT * FROM sales WHERE date >= date(\"now\", \"-30 days\")"
  }'
```

---

## Data Source Priority (How Files are Located)

When you request a dataset, the system searches in this order:

1. **Direct Path** - If you provide a full file path
   ```json
   {"analysis_dataset": "C:\\data\\sales_2024.csv"}
   ```

2. **Uploaded Directory** - Files you uploaded via `/upload-dataset`
   ```
   data/uploaded/Q1_sales.csv
   ```

3. **Cleaned Directory** - Pre-cleaned company datasets
   ```
   data/cleaned/customer_churn_cleaned.csv
   ```

4. **Real-Time Directory** - Streamed data via `/realtime-data`
   ```
   data/realtime/daily_metrics_realtime.jsonl
   ```

---

## Common Company Use Cases

### E-Commerce: Daily Sales Analysis
```bash
# Day 1: Upload sales data
curl -F "file=@2024-01-15_sales.csv" http://localhost:8000/upload-dataset

# Day 2: Query and predict
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "analysis_dataset": "2024-01-15_sales.csv",
    "forecast_dataset": "2024-01-15_sales.csv",
    "target_column": "daily_revenue",
    "forecast_periods": 7,
    "question": "Forecast revenue for next week?"
  }'
```

### Manufacturing: Real-Time Metrics
```python
import requests
import time

# Stream metrics every hour
metrics = {
    "timestamp": "2024-01-15T14:00:00",
    "production_rate": 1250,
    "defect_rate": 0.02,
    "downtime_minutes": 5
}

requests.post("http://localhost:8000/realtime-data", json={
    "dataset_name": "factory_metrics",
    "data": metrics
})
```

### Finance: Quarterly Reports
```bash
# Connect directly to finance database
curl -X POST http://localhost:8000/database-query \
  -H "Content-Type: application/json" \
  -d '{
    "db_type": "postgresql",
    "host": "finance-db.company.com",
    "port": 5432,
    "username": "finance_analyst",
    "password": "password",
    "database": "general_ledger",
    "query": "SELECT period, revenue, expenses, profit FROM financial_summary WHERE fiscal_year = 2024"
  }'
```

### HR Analytics: Employee Data
```bash
# Upload HR data from Workday/SAP export
curl -F "file=@employee_data_jan2024.xlsx" http://localhost:8000/upload-dataset

# Then analyze patterns
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the turnover rate by department?"
  }'
```

---

## Security Best Practices

### ⚠️ Never Hardcode Credentials

**❌ DON'T DO THIS:**
```python
payload = {
    "password": "SecurePassword123"  # Exposed in code!
}
```

**✅ DO THIS INSTEAD:**
```python
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file

payload = {
    "password": os.getenv("DB_PASSWORD")
}
```

### Create `.env` File
```
DB_HOST=analytics.company.com
DB_USERNAME=analytics_user
DB_PASSWORD=your_secure_password
DB_NAME=production
API_KEY=your_api_key
```

### Use Environment Variables
```bash
export DB_PASSWORD="your_password"
export DB_HOST="your_host"
```

---

## Troubleshooting Real-Time Data Issues

### Issue: "Dataset not found"
**Solution:** Check the file is in one of these locations:
- `data/uploaded/your_file.csv`
- `data/cleaned/your_file.csv`
- Use `/datasets` endpoint to list available files

### Issue: Database Connection Failed
**Solution:** 
1. Verify host/port are correct
2. Check firewall allows connection
3. Verify username/password
4. Test connection separately: `psql -h host -U user -d database`

### Issue: "Column not found"
**Solution:**
1. Check column names match your data exactly (case-sensitive)
2. Verify date column exists
3. Use `/datasets` to see actual column names

### Issue: Slow predictions
**Solution:**
1. Upload smaller datasets first (test with 1000 rows)
2. Check forecast_periods isn't too large
3. Verify your computer has sufficient RAM

---

## Performance Tips

### Optimize File Size
```bash
# Good: 10-100MB files
# Acceptable: 100-500MB
# Too large: >1GB (may timeout)
```

### Use Efficient Data Types
```python
# When creating your export
df.to_csv('data.csv', 
    dtype={
        'revenue': 'float32',  # Instead of float64
        'date': 'string',      # Instead of object
    }
)
```

### Batch Processing
```bash
# Instead of one huge file, use multiple smaller files:
# - day1_sales.csv (100MB)
# - day2_sales.csv (100MB)
# - day3_sales.csv (100MB)
# Process each separately for faster results
```

---

## API Response Format

All endpoints return consistent JSON:

```json
{
  "status": "success",
  "message": "Operation completed",
  "data": {
    "rows": 5000,
    "columns": ["date", "revenue"],
    "uploaded_at": "2024-01-15T10:30:45"
  },
  "timestamp": "2024-01-15T10:30:45"
}
```

---

## Next Steps

1. **Test Upload**: Upload a sample CSV file
2. **Check Datasets**: List available datasets via `/datasets`
3. **Run Prediction**: Execute `/predict` with your data
4. **Ask Questions**: Use `/chat` endpoint for insights
5. **Monitor Results**: Check timestamps and accuracy scores

See `REALTIME_EXAMPLES.py` for working code examples!
