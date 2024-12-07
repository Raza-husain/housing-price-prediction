import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import fetch_california_housing
import joblib
from sqlite3 import connect

class HousePriceModel:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.feature_names = None
        
    def train(self):
        # Load California Housing dataset
        california = fetch_california_housing(as_frame=True)
        df = california.frame
        
        # Define features (X) and target variable (y)
        X = df.drop(columns=['MedHouseVal'])
        y = df['MedHouseVal']
        self.feature_names = X.columns.tolist()
        
        # Split the dataset
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train the model
        self.model.fit(X_train, y_train)
        
        # Save the model
        joblib.dump(self.model, 'house_price_model.joblib')
        
    def predict(self, features):
        return self.model.predict(features)[0]
    
    def get_feature_names(self):
        return self.feature_names

def create_connection():
    """Create a database connection to SQLite database"""
    return connect('data.sqlite')

def init_db():
    conn = create_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS data_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,
            value FLOAT,
            category TEXT,
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_data_to_db(data):
    """
    Add new data entry to the database
    
    Args:
        data (dict): Dictionary containing date, value, category, and notes
    """
    # Your database connection logic here
    try:
        # Example using SQLite
        conn = create_connection()
        cursor = conn.cursor()
        
        query = """
        INSERT INTO data_table (date, value, category, notes)
        VALUES (?, ?, ?, ?)
        """
        
        cursor.execute(query, (
            data['date'],
            data['value'],
            data['category'],
            data['notes']
        ))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        raise Exception(f"Database error: {str(e)}")

if __name__ == "__main__":
    model = HousePriceModel()
    model.train()
    init_db()

