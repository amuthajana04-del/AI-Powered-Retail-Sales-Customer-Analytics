# 🤖 AI-Powered Retail Sales & Customer Analytics

An interactive AI-powered retail analytics project built using Python, Machine Learning, Pandas, Plotly, and Streamlit.

This project analyzes retail sales data and provides insights into sales performance, customer segments, product performance, and future sales prediction.

---

## 📊 Project Overview

The **AI-Powered Retail Sales & Customer Analytics** system is designed to help businesses understand their sales and customer data through interactive dashboards and machine learning.

The project includes:

- 📊 Sales Analytics
- 📈 Sales Trend Analysis
- 🔮 Sales Prediction
- 👥 Customer Segmentation
- 🛍️ Product Recommendation
- 🌍 Regional Analysis
- 📦 Category Analysis
- 💰 Profit Analysis
- 📥 Downloadable Reports

---

## 🚀 Key Features

### 1. 📊 Sales Analytics

The dashboard provides important business KPIs such as:

- Total Sales
- Total Profit
- Total Orders
- Total Customers

It also provides interactive visualizations for:

- Sales by Category
- Sales by Region
- Monthly Sales Trends

---

### 2. 🔮 Sales Prediction

A Machine Learning model is used to predict next month's sales.

**Algorithm:**

- Linear Regression

The model evaluates performance using:

- MAE
- MSE
- RMSE
- R² Score

The trained model is saved as a `.pkl` file and used by the Streamlit application for prediction.

---

### 3. 👥 Customer Segmentation

Customer segmentation is performed using:

**Algorithm:**

- K-Means Clustering

Customers are grouped into three segments:

- 🟢 Premium
- 🔵 Regular
- 🔴 Budget

The segmentation uses customer-level:

- Sales
- Profit
- Quantity

The trained clustering model is saved for future use.

---

### 4. 🛍️ Product Recommendation

The product recommendation module analyzes:

- Sales
- Profit
- Quantity

Products are ranked using a recommendation score.

The system provides:

- Top recommended products
- Product comparison
- Recommendation reasons
- Category-based recommendations

---

## 🎛️ Interactive Dashboard

The Streamlit dashboard includes filters for:

- Region
- Category
- Segment

Users can interactively filter the dataset and analyze business performance.

---

## 🧰 Technologies Used

### Programming Language

- Python

### Data Analysis

- Pandas
- NumPy

### Data Visualization

- Matplotlib
- Plotly

### Machine Learning

- Scikit-learn
- Linear Regression
- K-Means Clustering

### Model Management

- Joblib

### Dashboard

- Streamlit

### Development Tools

- Visual Studio Code
- Git
- GitHub

---

## 📁 Project Structure

```text
AI-Powered-Retail-Sales-Customer-Analytics/
│
├── Dataset/
│   ├── Cleaned_Superstore.csv
│   ├── customer_segments.csv
│   ├── top_selling_products.csv
│   ├── top_profitable_products.csv
│   ├── category_analysis.csv
│   └── region_wise_analysis.csv
│
├── Models/
│   ├── sales_prediction.py
│   ├── customer_segmentation.py
│   ├── product_recommendation.py
│   └── trained_models/
│
├── Streamlit_App/
│   └── dashboard.py
│
├── Python/
│   ├── data_cleaning.py
│   └── mysql_import.py
│
├── Screenshots/
│
├── Documentation/
│
├── Report/
│
├── PPT/
│
├── README.md
├── requirements.txt
└── .gitignore