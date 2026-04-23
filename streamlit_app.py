import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(
    page_title="Blinkit Data Analysis",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #FF6B6B;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess the data"""
    try:
        df = pd.read_csv('blinkit_data.csv')
        # Convert date columns to datetime
        df['order_date'] = pd.to_datetime(df['order_date'])
        df['order_datetime'] = pd.to_datetime(df['order_datetime'])
        return df
    except FileNotFoundError:
        st.error("Data file not found. Please run data_generator.py first.")
        return None

def main():
    # Header
    st.markdown('<h1 class="main-header">🛒 Blinkit Data Analysis Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Date range filter
    min_date = df['order_date'].min()
    max_date = df['order_date'].max()
    date_range = st.sidebar.date_input(
        "Select Date Range",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    # Category filter
    categories = st.sidebar.multiselect(
        "Select Categories",
        options=df['category'].unique(),
        default=df['category'].unique()
    )
    
    # City filter
    cities = st.sidebar.multiselect(
        "Select Cities",
        options=df['city'].unique(),
        default=df['city'].unique()
    )
    
    # Apply filters
    filtered_df = df[
        (df['order_date'] >= pd.to_datetime(date_range[0])) &
        (df['order_date'] <= pd.to_datetime(date_range[1])) &
        (df['category'].isin(categories)) &
        (df['city'].isin(cities))
    ]
    
    # Key Metrics
    st.subheader("📊 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Revenue", f"₹{filtered_df['final_amount'].sum():,.0f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Orders", f"{len(filtered_df):,}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Avg Order Value", f"₹{filtered_df['final_amount'].mean():.0f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Avg Delivery Time", f"{filtered_df['delivery_time_minutes'].mean():.1f} min")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts and Visualizations
    st.subheader("📈 Sales Analysis")
    
    # Row 1: Revenue Trends and Category Performance
    col1, col2 = st.columns(2)
    
    with col1:
        # Monthly Revenue Trend
        monthly_revenue = filtered_df.groupby(filtered_df['order_datetime'].dt.to_period('M'))['final_amount'].sum().reset_index()
        monthly_revenue['order_datetime'] = monthly_revenue['order_datetime'].dt.to_timestamp()
        
        fig = px.line(monthly_revenue, x='order_datetime', y='final_amount',
                     title='📅 Monthly Revenue Trend',
                     labels={'order_datetime': 'Month', 'final_amount': 'Revenue (₹)'})
        fig.update_traces(line=dict(color='#FF6B6B', width=3))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Revenue by Category
        category_revenue = filtered_df.groupby('category')['final_amount'].sum().sort_values(ascending=False)
        
        fig = px.bar(category_revenue, x=category_revenue.values, y=category_revenue.index,
                    orientation='h', title='📦 Revenue by Category',
                    labels={'x': 'Revenue (₹)', 'y': 'Category'})
        fig.update_traces(marker_color='#4ECDC4')
        st.plotly_chart(fig, use_container_width=True)
    
    # Row 2: City Performance and Delivery Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue by City
        city_revenue = filtered_df.groupby('city')['final_amount'].sum().sort_values(ascending=False)
        
        fig = px.pie(city_revenue, values=city_revenue.values, names=city_revenue.index,
                    title='🏙️ Revenue Distribution by City')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Delivery Time Analysis
        fig = px.box(filtered_df, x='city', y='delivery_time_minutes',
                    title='⏱️ Delivery Time Analysis by City',
                    labels={'city': 'City', 'delivery_time_minutes': 'Delivery Time (minutes)'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Row 3: Customer Ratings and Hourly Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Customer Rating Distribution
        rating_dist = filtered_df['customer_rating'].value_counts().sort_index()
        
        fig = px.bar(rating_dist, x=rating_dist.index, y=rating_dist.values,
                    title='⭐ Customer Rating Distribution',
                    labels={'x': 'Rating', 'y': 'Number of Orders'})
        fig.update_traces(marker_color='#FFE66D')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Orders by Hour of Day
        filtered_df['hour'] = filtered_df['order_datetime'].dt.hour
        hourly_orders = filtered_df['hour'].value_counts().sort_index()
        
        fig = px.line(hourly_orders, x=hourly_orders.index, y=hourly_orders.values,
                     title='🕒 Orders by Hour of Day',
                     labels={'x': 'Hour of Day', 'y': 'Number of Orders'})
        fig.update_traces(line=dict(color='#6A0572', width=3))
        st.plotly_chart(fig, use_container_width=True)
    
    # Row 4: Discount Analysis and Weekend vs Weekday
    col1, col2 = st.columns(2)
    
    with col1:
        # Discount Impact on Orders
        discount_orders = filtered_df[filtered_df['discount_percent'] > 0]
        if len(discount_orders) > 0:
            fig = px.scatter(discount_orders, x='discount_percent', y='final_amount',
                           color='category', title='💰 Discount vs Order Value',
                           labels={'discount_percent': 'Discount %', 'final_amount': 'Order Value (₹)'})
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Weekend vs Weekday Performance
        weekend_analysis = filtered_df.groupby('is_weekend').agg({
            'final_amount': 'mean',
            'order_id': 'count',
            'delivery_time_minutes': 'mean'
        }).reset_index()
        weekend_analysis['day_type'] = weekend_analysis['is_weekend'].map({True: 'Weekend', False: 'Weekday'})
        
        fig = make_subplots(rows=1, cols=3, subplot_titles=('Avg Order Value', 'Total Orders', 'Avg Delivery Time'))
        
        fig.add_trace(go.Bar(x=weekend_analysis['day_type'], y=weekend_analysis['final_amount'],
                            name='Avg Order Value', marker_color='#1A535C'), 1, 1)
        fig.add_trace(go.Bar(x=weekend_analysis['day_type'], y=weekend_analysis['order_id'],
                            name='Total Orders', marker_color='#4ECDC4'), 1, 2)
        fig.add_trace(go.Bar(x=weekend_analysis['day_type'], y=weekend_analysis['delivery_time_minutes'],
                            name='Avg Delivery Time', marker_color='#FF6B6B'), 1, 3)
        
        fig.update_layout(title_text='📊 Weekend vs Weekday Performance', showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Raw Data Section
    st.subheader("📋 Raw Data")
    
    with st.expander("View Filtered Data"):
        st.dataframe(filtered_df, use_container_width=True)
        
        # Download button for filtered data
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name=f"blinkit_filtered_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    # Insights Section
    st.subheader("💡 Key Insights")
    
    insights_col1, insights_col2 = st.columns(2)
    
    with insights_col1:
        st.info("""
        **Top Performing Categories:**
        - Highest revenue generating categories
        - Most popular products
        - Seasonal trends
        """)
        
        st.info("""
        **Delivery Performance:**
        - Cities with fastest/slowest delivery
        - Peak hour impacts
        - Weekend vs weekday efficiency
        """)
    
    with insights_col2:
        st.info("""
        **Customer Behavior:**
        - Preferred order times
        - Discount sensitivity
        - Rating patterns
        """)
        
        st.info("""
        **Business Opportunities:**
        - Underperforming categories
        - Cities for expansion
        - Optimal discount strategies
        """)

if __name__ == "__main__":
    main()

