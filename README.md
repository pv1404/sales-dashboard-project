Interactive Sales Performance & Forecasting Dashboard
Live Demo Link (https://sales-dashboard-project-m7erjuxko7n6zagngx8ion.streamlit.app/)
This project analyzes historical sales data to identify key performance trends and builds a forecasting model to predict future sales. The goal is to provide actionable insights for business leaders through an interactive, easy-to-use dashboard built with Streamlit.

This project is designed to showcase skills in data analysis, data visualization, and predictive modeling, directly aligning with the requirements for a strategy and operations role.

Dashboard Preview:
<img width="1919" height="968" alt="image" src="https://github.com/user-attachments/assets/d5deb19b-8718-484a-8be4-ea1cbf534e30" />

A snapshot of the main dashboard, showing key KPIs and interactive charts.

Key Features
KPI Dashboard: At-a-glance view of critical metrics like Total Revenue, Total Units Sold, and Average Sale Price.

Interactive Filtering: Dynamically filter sales data by Region and Product to drill down into specific performance areas.

Visual Trend Analysis: Interactive charts powered by Plotly to visualize:

Monthly revenue trends over time.

Sales distribution by region.

Top-performing products.

Sales Forecasting: A predictive model that forecasts future monthly sales based on historical data, helping with strategic planning and inventory management.

Actionable Insights: The dashboard automatically surfaces a key business insight based on the data analysis, such as identifying the top-performing region or the month with the highest sales growth.

Key Business Insight Example
Based on the analysis, the "East" region is the top-performing market, contributing over 35% of the total revenue. This suggests that strategic initiatives and marketing budgets could be focused on replicating the success of the East region in other markets, or further investing in the East to maximize growth.

Technical Stack
Language: Python

Libraries:

Streamlit: For building the interactive web application.

Pandas: For data manipulation and analysis.

Plotly: For creating interactive data visualizations.

Scikit-learn: For building the sales forecasting model (Linear Regression).

How to Run This Project Locally
Clone the repository:

git clone [https://github.com/your-username/sales-dashboard.git]([https://github.com/your-username/sales-dashboard.git](https://github.com/pv1404/sales-dashboard-project/blob/main/README.md))
cd sales-dashboard

Create a virtual environment (recommended):

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install the required libraries:

pip install -r requirements.txt

Run the Streamlit app:

streamlit run app.py

The application will open in your web browser at http://localhost:8501.
