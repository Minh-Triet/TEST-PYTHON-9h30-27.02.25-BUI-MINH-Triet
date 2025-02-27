import pytest
import io
import pandas as pd
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def create_test_csv():
    data = {
        'date': ['2024-05-05', '2024-02-21', '2024-12-30', '2024-08-27'],
        'region': ['USA', 'USA', 'Canada', 'Canada'],
        'product': ['Keyboard', 'Table', 'Mouse', 'Phone'],
        'quantity': [5, 6, 1, 13],
        'price': [100, 600, 50, 1000]
    }
    df = pd.DataFrame(data)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    return csv_buffer


def test_upload_csv(client):
    csv_buffer = create_test_csv()
    response = client.post('/upload/', data={'file': (io.BytesIO(csv_buffer.getvalue().encode('utf-8')), 'test.csv')})
    assert response.status_code == 200
    assert response.json['message'] == 'File uploaded and data stored in PostgreSQL successfully'


def test_get_sales_data(client):
    # Upload CSV first
    csv_buffer = create_test_csv()
    client.post('/upload/', data={'file': (io.BytesIO(csv_buffer.getvalue().encode('utf-8')), 'test.csv')})

    response = client.get('/sales/?start_date=2024-01-01&end_date=2024-12-31&region=USA')
    assert response.status_code == 200
    data = response.json
    assert data['total_sales'] == 3100
    assert data['average_sales'] == 1550
    assert data['transaction_count'] == 2


def test_get_sales_data_invalid_date_format(client):
    # Upload CSV first
    csv_buffer = create_test_csv()
    client.post('/upload/', data={'file': (io.BytesIO(csv_buffer.getvalue().encode('utf-8')), 'test.csv')})

    response = client.get('/sales/?start_date=2024/01/01&end_date=2024-12-31&region=Canada')
    assert response.status_code == 400
    assert response.json['message'] == 'Invalid date format. Please use YYYY-MM-DD.'


def test_get_sales_data_invalid_region(client):
    # Upload CSV first
    csv_buffer = create_test_csv()
    client.post('/upload/', data={'file': (io.BytesIO(csv_buffer.getvalue().encode('utf-8')), 'test.csv')})

    response = client.get('/sales/?start_date=2024-01-01&end_date=2024-12-31&region=Unknown')
    assert response.status_code == 400
    assert response.json['message'] == 'Invalid region. Please choose from available regions.'


def test_get_sales_data_pagination(client):
    # Upload CSV first
    csv_buffer = create_test_csv()
    client.post('/upload/', data={'file': (io.BytesIO(csv_buffer.getvalue().encode('utf-8')), 'test.csv')})

    response = client.get('/sales/?start_date=2025-01-01&end_date=2025-12-31&region=USA')
    assert response.status_code == 200
    data = response.json
    assert data['total_sales'] == 0
    assert data['average_sales'] == 0
    assert data['transaction_count'] == 0
