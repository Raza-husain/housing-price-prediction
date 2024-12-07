import streamlit as st
import pandas as pd
import numpy as np
import joblib
from model import HousePriceModel
import plotly.express as px
from model import create_connection

# Load the trained model
@st.cache_resource
def load_model():
    model = HousePriceModel()
    model.model = joblib.load('house_price_model.joblib')
    return model

def main():
    st.title("Data Analysis App")
    
    # Add a form for data input
    with st.form("data_input_form"):
        st.subheader("Add New Data")
        
        # Simple input fields
        date = st.date_input("Date")
        value = st.number_input("Value", min_value=0.0)
        category = st.selectbox("Category", ["Sales", "Expenses", "Revenue", "Other"])
        notes = st.text_area("Notes (optional)")
        
        # Submit button
        submit_button = st.form_submit_button("Add Data")
        
        if submit_button:
            try:
                # Create new data entry
                new_data = {
                    'date': date,
                    'value': value,
                    'category': category,
                    'notes': notes
                }
                
                # Add to database using your existing model
                add_data_to_db(new_data)
                st.success("Data added successfully!")
            except Exception as e:
                st.error(f"Error adding data: {str(e)}")
    
    # Show existing data
    st.subheader("Existing Data")
    display_data()

def add_data_to_db(data):
    # Implement your database insertion logic here
    pass

def display_data():
    """Display and analyze the stored data"""
    conn = create_connection()
    df = pd.read_sql_query("SELECT * FROM data_table", conn)
    conn.close()
    
    if len(df) == 0:
        st.info("No data available yet")
        return
        
    # Display raw data with date sorting
    st.write("Raw Data:")
    st.dataframe(df.sort_values('date', ascending=False))
    
    # Basic statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Summary by Category:")
        summary = df.groupby('category')['value'].agg(['sum', 'mean', 'count'])
        st.dataframe(summary.round(2))
        
    with col2:
        st.write("Trend Over Time:")
        fig = px.line(df, x='date', y='value', color='category')
        st.plotly_chart(fig)

if __name__ == "__main__":
    main() 