import pandas as pd
from datetime import datetime

class DataCleaner:
    """
    Class to clean, normalize, and enrich the air quality dataset.
    """
    
    def __init__(self, df):
        self.df = df.copy() if df is not None else pd.DataFrame()

    def preprocess(self):
        """
        Executes the complete cleaning pipeline.
        """
        if self.df.empty:
            return pd.DataFrame()

        # 1. Convert dates to datetime
        if 'time' in self.df.columns:
            self.df['time'] = pd.to_datetime(self.df['time'])
        
        # --- FIX 1: REMOVE FUTURE DATA ---
        now = pd.Timestamp.now()
        self.df = self.df[self.df['time'] <= now]

        # --- FIX 2: SCIENTIFIC IMPUTATION ---
        cols_numericas = self.df.select_dtypes(include=['float64', 'int64']).columns
        self.df[cols_numericas] = self.df[cols_numericas].interpolate(method='linear', limit=2, limit_direction='both')
        
        # 3. Feature Engineering
        self.df['Hour'] = self.df['time'].dt.hour
        self.df['Date'] = self.df['time'].dt.date
        
        # --- FIX 3: CATEGORICAL ORDERING (ENGLISH) ---
        # We no longer map to Spanish. We keep English names naturally.
        self.df['Day_Week'] = self.df['time'].dt.day_name()
        
        ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.df['Day_Week'] = pd.Categorical(
            self.df['Day_Week'], 
            categories=ordered_days, 
            ordered=True
        )

        # 4. Rename columns for UX (ENGLISH)
        # 'dust' removed completely
        friendly_names = {
            'pm10': 'PM10 (Urban Dust)',
            'pm2_5': 'PM2.5 (Fine Particles)',
            'carbon_monoxide': 'CO',
            'nitrogen_dioxide': 'NO2',
            'ozone': 'Ozone'
        }
        self.df.rename(columns=friendly_names, inplace=True)

        return self.df