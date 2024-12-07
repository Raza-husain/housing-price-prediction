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
    st.title("House Price Prediction & Data Analysis App")
    
    # Add tabs for different functionalities
    tab1, tab2 = st.tabs(["Price Prediction", "Data Analysis"])
    
    with tab1:
        st.subheader("Predict House Price")
        model = load_model()
        
        # Optionally display expected features (for debugging)
        # st.write("Model features:", model.model.feature_names_in_)
        
        with st.form("prediction_form"):
            st.write("Enter House Details:")
            
            col1, col2 = st.columns(2)
            
            with col1:
                med_inc = st.number_input("Median Income (in tens of thousands)", min_value=0.0, value=5.0)
                house_age = st.number_input("House Age (years)", min_value=0, value=20)
                ave_rooms = st.number_input("Average Rooms", min_value=1.0, value=5.0)
                ave_bedrms = st.number_input("Average Bedrooms", min_value=1.0, value=2.0)
            
            with col2:
                population = st.number_input("Population", min_value=1, value=1000)
                ave_occup = st.number_input("Average Occupancy", min_value=1.0, value=2.0)
                latitude = st.number_input("Latitude", min_value=30.0, max_value=50.0, value=37.0)
                longitude = st.number_input("Longitude", min_value=-125.0, max_value=-110.0, value=-119.0)
            
            predict_button = st.form_submit_button("Predict Price")
            
            if predict_button:
                try:
                    # Create input as a pandas DataFrame
                    input_data = pd.DataFrame({
                        'MedInc': [med_inc],
                        'HouseAge': [house_age],
                        'AveRooms': [ave_rooms],
                        'AveBedrms': [ave_bedrms],
                        'Population': [population],
                        'AveOccup': [ave_occup],
                        'Latitude': [latitude],
                        'Longitude': [longitude]
                    })
                    
                    # Make prediction
                    prediction = model.predict(input_data)
                    
                    # Display prediction
                    st.success(f"Predicted House Price: ${float(prediction):,.2f}")
                    
                    # Show additional information
                    st.info("Note: This is an estimated price based on historical data.")
                    
                except Exception as e:
                    st.error(f"Error making prediction: {str(e)}")
                    # Add debugging information
                    st.write("Input data:", input_data)
                    st.write("Input columns:", input_data.columns)
    
    with tab2:
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