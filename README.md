Air Quality Monitor – CDMX

Interactive dashboard built with Python and Streamlit to monitor, visualize, and analyze historical and real-time air quality data in Mexico City.
It uses the Open-Meteo API to retrieve accurate meteorological and air-quality information.

Features
Modular Architecture (ETL)

Extraction (API): Robust connection to the Open-Meteo API.

Transformation: Data cleaning, feature engineering, and time-series manipulation with Pandas.

Visualization: Dynamic, high-quality charts built with Plotly.

Advanced Visualizations

Interactive time series with WHO reference thresholds.

Heatmaps revealing hourly pollution trends.

Boxplots showing weekly pollutant distribution.

Automated Insights

Simple algorithms that generate descriptive text about:

Best hours for outdoor activities.

Worst pollution periods.

Optimization

Caching system to reduce API calls and significantly improve loading speed.

Technologies Used

-Python 3.8+

-Streamlit — UI and application state

-Pandas — Data cleaning and manipulation

-Plotly — Interactive charting

Requests — Robust HTTP communication:

📦 Installation & Usage
# Clone the repository
git clone https://github.com/your-user/air-quality-monitor.git
cd air-quality-monitor

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run dashboard.py

📂 Project Structure
├── api_download.py     # Open-Meteo API connection and data fetching  
├── cleaning.py         # Data cleaning and feature engineering  
├── visualization.py    # Plot generation using Plotly  
├── dashboard.py        # Main Streamlit app  
├── requirements.txt    # Project dependencies  
└── README.md           # Documentation  

📊 Data Sources

Data is fetched from the Open-Meteo Air Quality API.
The dashboard defaults to the coordinates of Mexico City’s Zócalo, but you can easily modify the location inside api_download.py.

Contributions

Contributions are welcome!
Please open an issue before submitting a pull request to discuss your proposal.

Author

Developed by Heriberto Ganesha Cortés Valdez, using Streamlit.
l25121393@morelia.tecnm.mx