# TEST-PYTHON-9h30-27.02.25-BUI-MINH-Triet

## Introduction

This repository contains a Python application that processes sales data from a CSV file and stores it in a PostgreSQL
database. The application provides an API to upload the CSV file, retrieve sales data based on filters, and perform
pagination.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/TEST-PYTHON-9h30-27.02.25-BUI-MINH-Triet.git
cd TEST-PYTHON-9h30-27.02.25-BUI-MINH-Triet
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
   pip install -r requirements.txt 
```
4.
- Set up the PostgreSQL database:
- Install PostgreSQL (if not already installed)
- Create a new database named sales_db
- Update the DATABASE_URL in the connection string (e.g., postgresql://username:password@localhost/sales_db)

## Usage
- Use post man file : 
- REST API basics- CRUD, test & variable.postman_collection.json
- Or use :
```bash 
curl -X POST -F "file=@data.csv" http://127.0.0.1:8000/upload/ 

curl http://127.0.0.1:8000/sales/?start_date=2024-01-01&end_date=2024-12-31&region=USA&page=2&per_page=10
```