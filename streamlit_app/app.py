import streamlit as st
import pandas as pd
import psycopg2

st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")

@st.cache_data
def get_data():
    conn = psycopg2.connect(
        host="postgres",   # use "localhost" if running outside Docker
        dbname="retail",
        user="airflow",
        password="airflow"
    )
    df = pd.read_sql("SELECT * FROM sales", conn)
    conn.close()
    return df

df = get_data()
df['date'] = pd.to_datetime(df['date'])

st.title("🛍️ Retail Sales Dashboard")

# --- Sidebar filters ---
st.sidebar.header("📌 Filter Data")
gender_filter = st.sidebar.multiselect("Select Gender", options=df['gender'].unique(), default=df['gender'].unique())
category_filter = st.sidebar.multiselect("Select Product Category", options=df['product_category'].unique(), default=df['product_category'].unique())

df_filtered = df[
    (df['gender'].isin(gender_filter)) &
    (df['product_category'].isin(category_filter))
]

# --- KPIs ---
total_sales = df_filtered['total_amount'].sum()
total_transactions = df_filtered['transaction_id'].nunique()
unique_customers = df_filtered['customer_id'].nunique()

st.markdown("### 🔢 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("💵 Total Sales", f"${total_sales:,.2f}")
col2.metric("🧾 Transactions", total_transactions)
col3.metric("👥 Unique Customers", unique_customers)

# --- Sales Over Time ---
st.markdown("### 📈 Sales Over Time")
sales_by_date = df_filtered.groupby('date')['total_amount'].sum().reset_index()
st.line_chart(sales_by_date.set_index('date'))

# --- Sales by Product Category ---
st.markdown("### 🧺 Sales by Product Category")
sales_by_category = df_filtered.groupby('product_category')['total_amount'].sum().sort_values(ascending=False)
st.bar_chart(sales_by_category)

# --- Sales by Gender ---
st.markdown("### 🧍‍♂️🧍‍♀️ Sales by Gender")
sales_by_gender = df_filtered.groupby('gender')['total_amount'].sum()
st.bar_chart(sales_by_gender)

# --- Table Preview ---
st.markdown("### 🔍 Raw Data Preview")
st.dataframe(df_filtered.sort_values(by='date', ascending=False))