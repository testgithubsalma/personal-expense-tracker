import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# CSV File Name
FILE_NAME = "expenses.csv"

# Create CSV File if not exists
if not os.path.exists(FILE_NAME):

    df = pd.DataFrame(columns=[
        "Type",
        "Category",
        "Amount",
        "Date",
        "Description"
    ])

    df.to_csv(FILE_NAME, index=False)

# Load Data
df = pd.read_csv(FILE_NAME)

# Sidebar Navigation
st.sidebar.title("💰 Navigation")

page = st.sidebar.radio(
    "Go To",
    [
        "Home",
        "Add Transaction",
        "View Transactions",
        "Summary"
    ]
)

# =========================
# HOME PAGE
# =========================

if page == "Home":

    st.title("💰 Personal Expense Tracker")

    st.write(
        "This application helps users manage their income and expenses easily."
    )

    st.markdown("## 🎯 Features")

    st.markdown("""
- Add Income
- Add Expenses
- View Transactions
- Calculate Balance
- Category-wise Expense Summary
""")

# =========================
# ADD TRANSACTION PAGE
# =========================

elif page == "Add Transaction":

    st.title("➕ Add Transaction")

    transaction_type = st.selectbox(
        "Select Transaction Type",
        ["Income", "Expense"]
    )

    # Income Source
    if transaction_type == "Income":

        category = st.text_input(
            "Income Source"
        )

    # Expense Category
    else:

        category = st.selectbox(
            "Expense Category",
            [
                "Food",
                "Travel",
                "Shopping",
                "Bills",
                "Education",
                "Medical",
                "Others"
            ]
        )

    # Amount
    amount = st.number_input(
        "Enter Amount",
        min_value=0.0
    )

    # Date
    transaction_date = st.date_input(
        "Select Date"
    )

    # Description
    description = st.text_area(
        "Description"
    )

    # Save Button
    if st.button("Save Transaction"):

        new_transaction = {
            "Type": transaction_type,
            "Category": category,
            "Amount": amount,
            "Date": transaction_date,
            "Description": description
        }

        # Add New Data
        new_df = pd.DataFrame([new_transaction])

        df = pd.concat(
            [df, new_df],
            ignore_index=True
        )

        # Save CSV
        df.to_csv(FILE_NAME, index=False)

        st.success("Transaction Added Successfully!")

# =========================
# VIEW TRANSACTIONS PAGE
# =========================

elif page == "View Transactions":

    st.title("📋 Transaction History")

    if df.empty:

        st.warning("No Transactions Found")

    else:

        st.dataframe(df)

        # Download CSV
        csv = df.to_csv(index=False)

        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="transactions.csv",
            mime="text/csv"
        )

# =========================
# SUMMARY PAGE
# =========================

elif page == "Summary":

    st.title("📊 Financial Summary")

    if df.empty:

        st.warning("No Data Available")

    else:

        # Income Data
        income_df = df[
            df["Type"] == "Income"
        ]

        # Expense Data
        expense_df = df[
            df["Type"] == "Expense"
        ]

        # Calculations
        total_income = income_df["Amount"].sum()

        total_expense = expense_df["Amount"].sum()

        balance = total_income - total_expense

        # Metrics
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Income",
            f"₹ {total_income}"
        )

        col2.metric(
            "Total Expense",
            f"₹ {total_expense}"
        )

        col3.metric(
            "Balance",
            f"₹ {balance}"
        )

        # Category Summary
        st.subheader("Category-wise Expense Summary")

        category_summary = (
            expense_df.groupby("Category")["Amount"]
            .sum()
            .reset_index()
        )

        st.dataframe(category_summary)

        # Bar Chart
        st.bar_chart(
            category_summary.set_index("Category")
        )

        # Pie Chart
        fig, ax = plt.subplots()

        ax.pie(
            category_summary["Amount"],
            labels=category_summary["Category"],
            autopct="%1.1f%%"
        )

        st.pyplot(fig)