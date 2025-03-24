import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------- #
# 👤 ADMIN AUTHORIZATION #
# -------------------- #
def admin_dashboard():
    """Admin Dashboard with Restricted Access"""
    
    # Verify admin credentials
    if "username" in st.session_state and st.session_state["username"] == "Shrinjita Paul":
        
        # Display the Admin Dashboard
        st.title("📊 Admin Dashboard")
        st.markdown("**Real-time waste segregation statistics**")

        # Sample Data
        data = {
            "Date": pd.date_range(start="2025-03-01", periods=10, freq="D"),
            "Plastic Waste (kg)": [10, 15, 18, 12, 14, 20, 17, 19, 13, 11],
            "Organic Waste (kg)": [30, 35, 32, 28, 26, 34, 31, 36, 29, 27],
            "Metal Waste (kg)": [5, 8, 7, 6, 4, 7, 9, 10, 5, 6]
        }

        df = pd.DataFrame(data)

        # Line Chart
        fig = px.line(
            df, x="Date", 
            y=["Plastic Waste (kg)", "Organic Waste (kg)", "Metal Waste (kg)"],
            labels={"value": "Waste (kg)", "variable": "Waste Type"},
            title="Daily Waste Segregation"
        )
        st.plotly_chart(fig)

        # Data Table
        st.subheader("Detailed Waste Data")
        st.dataframe(df)

        # Waste Summary Metrics
        st.metric("Plastic Waste (kg)", f"{df['Plastic Waste (kg)'].sum()} kg")
        st.metric("Organic Waste (kg)", f"{df['Organic Waste (kg)'].sum()} kg")
        st.metric("Metal Waste (kg)", f"{df['Metal Waste (kg)'].sum()} kg")

    else:
        # Restricted Access Message
        st.error("🚫 Admin Access Only! You are not authorized to view this page.")
