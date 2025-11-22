import plotly.express as px
import plotly.graph_objects as go

class DashboardPlots:
    """
    Interactive chart generator using Plotly.
    """
    
    # WHO Reference Limits (Approximate 24h mean guideline)
    WHO_LIMITS = {
        'PM2.5': 15,
        'PM10': 45,
        'NO2': 25,
        'Ozone': 100
    }

    @staticmethod
    def plot_time_series(df, col_name):
        """Interactive time series with WHO reference"""
        fig = px.line(df, x='time', y=col_name, 
                      title=f'Trend: {col_name} (µg/m³)',
                      template="plotly_dark",
                      color_discrete_sequence=['#00CC96']) # Soft neon green
        
        # Add reference line if exists
        limit = DashboardPlots.WHO_LIMITS.get(col_name)
        if limit:
            fig.add_hline(y=limit, line_dash="dot", line_color="red", 
                         annotation_text=f"WHO Limit ({limit})", 
                         annotation_position="top right")

        fig.update_layout(
            xaxis_title="Date and Time", 
            yaxis_title="µg/m³",
            margin=dict(l=60, r=20, t=50, b=50),
            hovermode="x unified"
        )
        return fig

    @staticmethod
    def plot_heatmap_day_hour(df, col_name):
        """Heatmap: Day of Week vs Hour of Day"""
        pivot = df.pivot_table(
            index='Day_Week', 
            columns='Hour', 
            values=col_name, 
            aggfunc='mean'
        )
        
        # Scale Spectral_r: Blue (low) -> Red (high)
        fig = px.imshow(pivot, 
                        labels=dict(x="Hour", y="Day", color="Level"),
                        color_continuous_scale='Spectral_r',
                        title=f"Hourly Intensity: {col_name}",
                        template="plotly_dark")
        
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))
        return fig

    @staticmethod
    def plot_boxplot_distribution(df, col_name):
        """Distribution by day of week (Ordered by DataCleaner)"""
        fig = px.box(df, x='Day_Week', y=col_name, 
                     color='Day_Week',
                     title=f"Weekly Distribution: {col_name}",
                     template="plotly_dark",
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        
        fig.update_layout(
            xaxis_title="",
            yaxis_title="µg/m³",
            showlegend=False,
            margin=dict(l=40, r=20, t=40, b=40)
        )
        return fig