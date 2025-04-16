from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

from datetime import datetime
import pandas as pd
import os

# Default arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

# Path CSV
CSV_PATH = os.path.join(os.path.dirname(__file__), 'data', 'retail_sales_dataset.csv')

# SQL for create table
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS sales (
    transaction_id INT PRIMARY KEY,
    date DATE,
    customer_id VARCHAR,
    gender VARCHAR,
    age INT,
    product_category VARCHAR,
    quantity INT,
    price_per_unit NUMERIC,
    total_amount NUMERIC
);
"""

# Step 1: Reading CSV file
def read_csv():
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"CSV file tidak ditemukan di path: {CSV_PATH}")
    df = pd.read_csv(CSV_PATH)
    # Rename columns according to table structure in PostgreSQL
    df.rename(columns={
        'Transaction ID': 'transaction_id',
        'Date': 'date',
        'Customer ID': 'customer_id',
        'Gender': 'gender',
        'Age': 'age',
        'Product Category': 'product_category',
        'Quantity': 'quantity',
        'Price per Unit': 'price_per_unit',
        'Total Amount': 'total_amount'
    }, inplace=True)
    df.to_csv('/tmp/retail_sales_cleaned.csv', index=False)  # save for use in next task

# Step 2: Create tabel di PostgreSQL
def create_table():
    pg_hook = PostgresHook(postgres_conn_id='postgres')
    pg_hook.run(CREATE_TABLE_SQL)

# Step 3: Load data to Postgres
def load_data():
    df = pd.read_csv('/tmp/retail_sales_cleaned.csv')  # take from temporary file
    pg_hook = PostgresHook(postgres_conn_id='postgres')
    engine = pg_hook.get_sqlalchemy_engine()
    df.to_sql('sales', engine, if_exists='append', index=False, method='multi')

# DAG
with DAG(
    dag_id='retail_sales_csv_to_postgres',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['retail', 'postgres']
) as dag:

    task_read_csv = PythonOperator(
        task_id='read_csv_file',
        python_callable=read_csv
    )

    task_create_table = PythonOperator(
        task_id='create_postgres_table',
        python_callable=create_table
    )

    task_load_data = PythonOperator(
        task_id='load_data_to_postgres',
        python_callable=load_data
    )

    # Task
    task_read_csv >> task_create_table >> task_load_data
