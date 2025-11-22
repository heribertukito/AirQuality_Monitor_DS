import streamlit as st
import pandas as pd

# Import local modules
from api_download import AirQualityFetcher
from cleaning import DataCleaner
from visualization import DashboardPlots

# ==========================================
# PAGE CONFIGURATION & STYLES
# ==========================================
st.set_page_config(
    page_title="Air Quality Monitor",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for metrics and chart appearance
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    .stMetric {
        background-color: #1E212B;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #333;
    }
    /* Adjust chart toolbar modebar */
    .js-plotly-plot .plotly .modebar {
        orientation: h;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# DATA LOADING FUNCTION (Cached)
# ==========================================
@st.cache_data(ttl=3600) # 1-hour cache
def load_data(days):
    """
    Orchestrates data fetching and cleaning.
    """
    # 1. Instantiate and fetch
    fetcher = AirQualityFetcher() 
    raw_df = fetcher.fetch_data(days_past=days)
    
    # 2. Instantiate and clean
    cleaner = DataCleaner(raw_df)
    return cleaner.preprocess()

# ==========================================
# MAIN DASHBOARD LOGIC
# ==========================================
def main():
    # --- SIDEBAR ---
    st.sidebar.title("⚙️ Settings")
    st.sidebar.info("Real-time data from Open-Meteo API")
    
    # History days selector
    days_selection = st.sidebar.slider("History to analyze (days):", 7, 90, 30)
    
    # Data loading with spinner
    with st.spinner('Connecting to satellites and stations...'):
        df = load_data(days_selection)

    if df.empty:
        st.error("⚠️ Could not load data. Please check your internet connection.")
        return

    # Dynamic detection of available pollutants (excluding time/text columns)
    excluded_cols = ['time', 'Hour', 'Date', 'Day_Week']
    pollutant_cols = [c for c in df.columns if c not in excluded_cols]
    
    # Pollutant selector
    selected_pollutant = st.sidebar.selectbox(
        "Select Pollutant:", 
        pollutant_cols,
        index=1 if 'PM2.5 (Fine Particles)' in pollutant_cols else 0
    )

    # Date Filter (Zoom)
    min_date, max_date = df['Date'].min(), df['Date'].max()
    date_range = st.sidebar.date_input(
        "Filter by Date:", 
        [min_date, max_date],
        min_value=min_date, 
        max_value=max_date
    )

    # Apply date mask if valid range selected
    if len(date_range) == 2:
        start_date, end_date = date_range
        mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
        filtered_df = df.loc[mask]
    else:
        filtered_df = df

    # --- MAIN SECTION (HEADER & KPIs) ---
    st.title("🌍 Air Quality Monitor")
    st.markdown(f"Detailed analysis for **{selected_pollutant}** in CDMX.")

    # Calculate metrics
    if not filtered_df.empty:
        last_val = filtered_df[selected_pollutant].iloc[-1]
        avg_val = filtered_df[selected_pollutant].mean()
        max_val = filtered_df[selected_pollutant].max()
        
        # Color logic based on WHO limits
        # We need to map the friendly name back to the key in WHO_LIMITS (simple substring match)
        limit_val = 9999
        for key, val in DashboardPlots.WHO_LIMITS.items():
            if key in selected_pollutant:
                limit_val = val
                break
        
        is_safe = last_val < limit_val
        delta_msg = "Within WHO Norm" if is_safe else "⚠️ Above WHO Norm"
        delta_col = "normal" if is_safe else "inverse"

        # Show KPIs
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Current Level", f"{last_val:.1f} µg/m³", delta=delta_msg, delta_color=delta_col)
        k2.metric("Period Average", f"{avg_val:.1f} µg/m³")
        k3.metric("Max Peak", f"{max_val:.1f} µg/m³")
        k4.metric("Total Records", f"{len(filtered_df)}")
    
    st.divider()

    # --- VISUALIZATIONS ---
    
    # 1. Time Series
    st.subheader("Temporal Trend")
    st.plotly_chart(
        DashboardPlots.plot_time_series(filtered_df, selected_pollutant), 
        use_container_width=True
    )

    # 2. Secondary Charts
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Hourly Heatmap")
        st.caption("Identify critical hours of the day.")
        st.plotly_chart(
            DashboardPlots.plot_heatmap_day_hour(filtered_df, selected_pollutant), 
            use_container_width=True
        )
        
    with c2:
        st.subheader("Weekly Distribution")
        st.caption("Pollution variability by day of the week.")
        st.plotly_chart(
            DashboardPlots.plot_boxplot_distribution(filtered_df, selected_pollutant), 
            use_container_width=True
        )

    # --- AUTOMATED INSIGHTS ---
    st.subheader("Automated Insights")
    
    if not filtered_df.empty:
        # Simple calculations for text generation
        worst_hour = filtered_df.groupby('Hour')[selected_pollutant].mean().idxmax()
        best_hour = filtered_df.groupby('Hour')[selected_pollutant].mean().idxmin()
        worst_day = filtered_df.groupby('Day_Week', observed=True)[selected_pollutant].mean().idxmax()
        
        st.info(f"""
        **Smart Summary:**
        - 🏃 **Recommendation:** The best time for outdoor activities is around **{best_hour}:00 hrs**.
        - ⚠️ **Caution:** Pollution levels tend to peak at **{worst_hour}:00 hrs**.
        - 📅 **Weekly Trend:** **{worst_day}s** have recorded the highest average of {selected_pollutant} in this period.
        """)

if __name__ == "__main__":
    main()