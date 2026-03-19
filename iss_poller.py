#!/usr/bin/env python3
import requests
import psycopg2
import os
from datetime import datetime

# Database connection
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'issdb')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'postgres')

# ISS API endpoint
ISS_API_URL = 'http://api.open-notify.org/iss-now.json'

def get_iss_location():
    """Fetch current ISS location from API"""
    try:
        response = requests.get(ISS_API_URL, timeout=30)
        response.raise_for_status()
        data = response.json()
        return {
            'latitude': float(data['iss_position']['latitude']),
            'longitude': float(data['iss_position']['longitude']),
            'timestamp': int(data['timestamp'])
        }
    except requests.exceptions.Timeout:
        print("Error: Request to ISS API timed out after 30 seconds")
        raise
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to fetch ISS location: {e}")
        raise

def store_location(location):
    """Store ISS location in PostgreSQL database"""
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    
    try:
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS iss_locations (
                id SERIAL PRIMARY KEY,
                latitude DECIMAL(10, 6) NOT NULL,
                longitude DECIMAL(10, 6) NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                recorded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        
        # Create indexes if they don't exist
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_timestamp ON iss_locations(timestamp)
            """
        )
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_recorded_at ON iss_locations(recorded_at)
            """
        )
        
        # Insert the location data
        cursor.execute(
            """
            INSERT INTO iss_locations (latitude, longitude, timestamp, recorded_at)
            VALUES (%s, %s, to_timestamp(%s), %s)
            """,
            (location['latitude'], location['longitude'], location['timestamp'], datetime.utcnow())
        )
        conn.commit()
        print(f"Stored ISS location: {location['latitude']}, {location['longitude']}")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    try:
        location = get_iss_location()
        store_location(location)
    except Exception as e:
        print(f"Fatal error: {e}")
        exit(1)
