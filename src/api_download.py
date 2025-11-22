import requests
import pandas as pd
import streamlit as st

class AirQualityFetcher:
    """
    Class responsible for fetching air quality data from Open-Meteo API.
    API Documentation: https://open-meteo.com/
    """
    
    def __init__(self, lat=19.4326, lon=-99.1332):
        # Default coordinates: Mexico City (Zocalo)
        self.base_url = "https://air-quality-api.open-meteo.com/v1/air-quality"
        self.lat = lat
        self.lon = lon

    def fetch_data(self, days_past=90):
        """
        Downloads data for the last 'days_past' days.
        """
        # 'dust' parameter removed as requested
        params = {
            "latitude": self.lat,
            "longitude": self.lon,
            "hourly": ["pm10", "pm2_5", "carbon_monoxide", "nitrogen_dioxide", "ozone"],
            "timezone": "auto",
            "past_days": days_past
        }

        try:
            # Increased timeout for slow connections
            response = requests.get(self.base_url, params=params, timeout=15)
            response.raise_for_status() # Raises error if status is not 200
            
            data = response.json()
            
            if 'hourly' not in data:
                raise ValueError("Unexpected API response format")

            # Process JSON response to DataFrame
            df = pd.DataFrame(data['hourly'])
            return df
            
        except requests.exceptions.RequestException as e:
            st.error(f"Critical error connecting to API: {e}")
            return None
        except Exception as e:
            st.error(f"Error processing data: {e}")
            return None

if __name__ == "__main__":
    # Simple unit test
    fetcher = AirQualityFetcher()
    df = fetcher.fetch_data(days_past=10)
    if df is not None:
        print(f"Data downloaded successfully. Shape: {df.shape}")