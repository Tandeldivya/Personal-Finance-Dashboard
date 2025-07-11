import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Personel Finance Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded")

# Load Data and do required transformations
DF = pd.read_csv("final_data.csv")

# Sidebar
with st.sidebar:
    st.header("Filters")
    year_list = list(DF['Year'].unique())
    st.write("Select Year")
    selected_year = st.selectbox("Year", year_list, index=year_list.index(2018))
    st.write("Select Month")
    month_list = list(DF['Month'].unique())
    selected_month = st.selectbox("Month", month_list, index=month_list.index("Jan"))

# Function to format numbers for display
def fmt_income(n):
    return f"₹{n/1_000_000:.2f}M" if n >= 1_000_000 else f"₹{n/1_000:.2f}K"

def fmt_percentage(n,i):
    return f"{round(n / i * 100,2)} %" if i != 0 else  f"0 %"

# Yearly functions
def Income_for_specific_year():
    """Calculate total income for the selected year and month."""
    filtered_df = DF[(DF['Year'] == selected_year) & (DF['Month'] == selected_month)]
    total_yearly_income = filtered_df[filtered_df["Type"] == "Income"]["Value"].sum()
    return total_yearly_income
def Expense_for_specific_year():
    """Calculate total expense for the selected year and month."""
    filtered_df = DF[(DF['Year'] == selected_year) & (DF['Month'] == selected_month)]
    total_yearly_expense = filtered_df[filtered_df["Type"] == "Expense"]["Value"].sum()
    return total_yearly_expense
def Savings_for_specific_year():
    """Calculate total savings for the selected year and month."""
    filtered_df = DF[(DF['Year'] == selected_year) & (DF['Month'] == selected_month)]
    total_yearly_savings = filtered_df[filtered_df["Type"] == "Savings"]["Value"].sum()
    return total_yearly_savings


# All time functions
def Total_income():
    total_lifetime_income = DF[DF["Type"] == "Income"]["Value"].sum()
    return total_lifetime_income
def Total_expense():
    total_lifetime_expense = DF[DF["Type"] == "Expense"]["Value"].sum()
    return total_lifetime_expense
def Total_savings():
    total_lifetime_savings = DF[DF["Type"] == "Savings"]["Value"].sum()
    return total_lifetime_savings

# Yearly section
yearly_income = fmt_income(Income_for_specific_year())
yearly_expense = fmt_percentage(Expense_for_specific_year(), Income_for_specific_year())
yearly_savings = fmt_percentage(Savings_for_specific_year(), Income_for_specific_year())
# All time section
total_income = fmt_income(Total_income())
total_expense = fmt_percentage(Total_expense(), Total_income())
total_savings = fmt_percentage(Total_savings(), Total_income())

st.header("Cummulative Summary")
c2, c4, c6, c8 = st.columns(4)
c2.metric(label=" Total Income", value=total_income)
c4.metric(label=" Total expense %", value=total_expense)
c6.metric(label=" Total expense %", value=total_savings)
c8.metric(label=" Total expense %", value=fmt_income(Total_savings()))

st.header("Yearly Summary for " + selected_month + " - " + str(selected_year))
c1, c3, c5, c7 = st.columns(4)
c1.metric(label=" Yearly Income", value=yearly_income)
c3.metric(label=" Yearly expense %", value=yearly_expense)
c5.metric(label=" Yearly savings %", value=yearly_savings)
c7.metric(label=" Yearly savings %", value=fmt_income(Savings_for_specific_year()))

# Income Growth line chart
st.header("Income Growth ")
def income_growth_chart():
    """Create a line chart showing income growth over the years."""
    income_data = DF[DF["Type"] == "Income"].groupby("Year")["Value"].sum().reset_index()
    income_data['Year'] = income_data['Year'].astype(str)  # Convert Year to string for better x-axis labels

    chart = alt.Chart(income_data).mark_line(point=True).encode(
        x=alt.X("Year", title="Year"),
        y=alt.Y("Value", title="Total Income"),
        tooltip=["Year", "Value"]
    ).properties(
        title="Income Growth Over the Years"
    )
    return chart
st.altair_chart(income_growth_chart(), use_container_width=True)

# Spending Chart
st.header("Spending Chart")
def spending_chart():
    """Create a bar chart showing spending by category for the selected year and month."""
    filtered_df = DF[(DF['Year'] == selected_year) & (DF['Month'] == selected_month)]
    spending_data = filtered_df[filtered_df["Type"] == "Expense"].groupby("Component")["Value"].sum().reset_index()
    spending_data = spending_data.sort_values(by="Value", ascending=False)

    chart = alt.Chart(spending_data).mark_bar().encode(
        y=alt.X("Component", sort="-y"),
        x="Value",
        color="Component"
    ).properties(
        title=f"Spending by Category for {selected_month} {selected_year}"    
    )
    return chart
st.altair_chart(spending_chart(), use_container_width=True)

# Savings Chart
st.header("Savings Chart")
def savings_chart():
    """Create a bar chart showing savings by category for the selected year and month."""
    filtered_df = DF[(DF['Year'] == selected_year) & (DF['Month'] == selected_month)]
    savings_data = filtered_df[filtered_df["Type"] == "Savings"].groupby("Component")["Value"].sum().reset_index()
    savings_data = savings_data.sort_values(by="Value", ascending=False)

    chart = alt.Chart(savings_data).mark_bar().encode(
        y=alt.X("Component", sort="-y"),
        x="Value",
        color="Component"
    ).properties(
        title=f"Savings by Category for {selected_month} {selected_year}"    
    )
    return chart
st.altair_chart(savings_chart(), use_container_width=True)