# 🛍️ Retail Sales Data Engineering Project

## 📌 1. Summary

This project is a beginner-friendly data engineering pipeline built using **Python**, **Apache Airflow**, **PostgreSQL**, and **Streamlit**. The goal is to simulate a real-world ETL (Extract, Transform, Load) workflow using a public retail dataset.

Data is ingested into a PostgreSQL database using Airflow, and then visualized through an interactive Streamlit dashboard for business insights such as sales trends, customer demographics, and product category performance.

---

1. Streamlit View
   ![Retail sales](https://github.com/user-attachments/assets/6e831cfa-4f97-4788-86dd-7b6b13e479f3)
2. DAG Vew
   ![dag](https://github.com/user-attachments/assets/b9ebfe0f-69b2-48ef-9627-3654712aaa55)
3. Postgres View
   ![db](https://github.com/user-attachments/assets/1fbdb124-461a-44af-b9a4-1e8880550a06)

## 🎯 2. Objectives

- Build an end-to-end ETL pipeline with modern data tools.
- Transform and store sales transaction data into a structured database (PostgreSQL).
- Automate ingestion using Airflow DAGs.
- Create a user-friendly data visualization interface with Streamlit.
- Practice containerized development with Docker.

---

## 🔄 3. System Flow


1. Airflow triggers a DAG that extracts data from a CSV.
2. The data is cleaned and loaded into a PostgreSQL database.
3. Streamlit reads from PostgreSQL and visualizes sales insights in real time.

---

## 🧰 4. Technologies Used

- **Python** – Core scripting language.
- **Apache Airflow** – Workflow orchestration.
- **PostgreSQL** – Data warehouse to store transactional data.
- **Streamlit** – Dashboard for data exploration and visualization.
- **Docker** – Containerization and environment management.
- **Pandas** – Data manipulation during transformation.

---

## 🛠️ 5. How to Run This Project

### 📁 Prerequisites

- Docker & Docker Compose installed
- Internet connection to pull Docker images

### 🚀 Steps

1. **Clone the repository:**

```bash
git clone https://github.com/rulnin/retail-data-engineering-project.git
cd retail-data-engineering-project
```

2. **Place the dataset inside the /dags/data/ folder:**
- Download from: Retail Sales Dataset
- File name: retail_sales_dataset.csv

3. **Start all services:**
docker-compose up -d

4. **Access the tools:**
- Airflow: http://localhost:8080
    * Username: airflow
    * Password: airflow
- Streamlit Dashboard: http://localhost:8501
- PostgreSQL DB: localhost:5432 (user: airflow, password: airflow)

5 **Trigger the DAG in Airflow:**
- Open Airflow UI → Unpause retail_etl_dag → Trigger it manually

## 6. Conclusion
This project demonstrates how to build a scalable, containerized data pipeline from ingestion to visualization. It provides foundational experience in orchestrating ETL workflows, storing structured data, and creating interactive dashboards. Perfect for showcasing your skills in a data engineering portfolio.
