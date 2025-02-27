from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import io
from datetime import datetime

app = Flask(__name__)
# URI database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123300@localhost/sales_db'
db = SQLAlchemy(app)


# Create data table sale
class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    region = db.Column(db.String(50))
    product = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    sales = db.Column(db.Float)

    def __init__(self, date, region, product, quantity, price):
        self.date = date
        self.region = region
        self.product = product
        self.quantity = quantity
        self.price = price
        self.sales = quantity * price


# Create a new instance of the sales table
with app.app_context():
    db.create_all()


# Upload CSV File (POST /upload/)
@app.route('/upload/', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    # Accepts CSV file upload.
    if file:
        try:
            # Read CSV data into a Pandas DataFrame
            df = pd.read_csv(io.StringIO(file.stream.read().decode("UTF8")), parse_dates=['date'])
            df['date'] = pd.to_datetime(df['date'])
            sales_list = []
            for _, row in df.iterrows():
                sale = Sale(row['date'], row['region'], row['product'], row['quantity'], row['price'])
                sales_list.append(sale)
            with app.app_context():
                # Store data in PostgreSQL instead of in-memory
                db.session.add_all(sales_list)
                db.session.commit()
            return jsonify({'message': 'File uploaded and data stored in PostgreSQL successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500


# Get Filtered Sales Data (GET /sales/?start_date=2024-01-01&end_date=2024-02-01&region=USA)
@app.route('/sales/', methods=['GET'])
def get_sales_data():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    region = request.args.get('region')

    if not all([start_date, end_date, region]):
        return jsonify({'error': 'Missing query parameters'}), 400

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        filtered_data = Sale.query.filter(
            Sale.date >= start_date,
            Sale.date <= end_date,
            Sale.region == region
        ).all()

        total_sales = sum(sale.sales for sale in filtered_data)
        average_sales = total_sales / len(filtered_data) if filtered_data else 0
        transaction_count = len(filtered_data)
        # Returns total sales, average sales, and count of transactions for the given date range and region.
        return jsonify({
            'total_sales': total_sales,
            'average_sales': average_sales,
            'transaction_count': transaction_count
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
