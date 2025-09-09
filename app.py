import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Configure page
st.set_page_config(
    page_title="Restaurant Dashboard",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    
    .restaurant-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        color: white;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    
    .coffee-theme {
        background: linear-gradient(135deg, #8B4513 0%, #D2691E 100%);
    }
    
    .embers-theme {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    }
</style>
""", unsafe_allow_html=True)

# Sample data
@st.cache_data
def load_restaurant_data():
    return {
        "rise": {
            "name": "Rise - Ready to serve",
            "subtitle": "Inventory & Suggestions System",
            "inventory": [
                {"name": "Espresso", "stock": 45, "max_stock": 60, "category": "drink", "available": True},
                {"name": "Croissant", "stock": 12, "max_stock": 50, "category": "pastry", "available": True},
                {"name": "Sandwich", "stock": 8, "max_stock": 40, "category": "meal", "available": False},
                {"name": "Cookies", "stock": 25, "max_stock": 80, "category": "snack", "available": True},
            ],
            "top_selling": [
                {"name": "Latte", "sales": 156},
                {"name": "Sandwich", "sales": 98},
                {"name": "Cookies", "sales": 87},
                {"name": "Espresso", "sales": 76},
                {"name": "Muffin", "sales": 54}
            ],
            "daily_revenue": [4200, 3850, 4650, 5200, 4850, 5800, 4450],
            "top_items": [
                {"name": "Caramel Latte", "rating": 4.8, "sales": 89, "badge": "Most Popular"},
                {"name": "Club Sandwich", "rating": 4.6, "sales": 67, "badge": "Staff Pick"},
                {"name": "Chocolate Cookies", "rating": 4.5, "sales": 45, "badge": "Best Value"}
            ],
            "rated_items": [
                {"name": "Cappuccino", "rating": 4.7, "reviews": 23, "comment": "Perfect foam and great taste!", "date": "2 days ago"},
                {"name": "Panini", "rating": 4.3, "reviews": 15, "comment": "Fresh ingredients and crispy bread.", "date": "1 week ago"}
            ]
        },
        "embers": {
            "name": "Blu Embers",
            "subtitle": "Woxsen University Restaurant",
            "inventory": [
                {"name": "Biryani", "stock": 25, "max_stock": 40, "category": "meal", "available": True},
                {"name": "Masala Chai", "stock": 60, "max_stock": 80, "category": "drink", "available": True},
                {"name": "Samosa", "stock": 15, "max_stock": 50, "category": "snack", "available": True},
                {"name": "Gulab Jamun", "stock": 8, "max_stock": 30, "category": "dessert", "available": False},
            ],
            "top_selling": [
                {"name": "Biryani", "sales": 234},
                {"name": "Dal Rice", "sales": 187},
                {"name": "Samosa", "sales": 165},
                {"name": "Chai", "sales": 143},
                {"name": "Paratha", "sales": 98}
            ],
            "daily_revenue": [8200, 7850, 9150, 10200, 9850, 11800, 8950],
            "top_items": [
                {"name": "Chicken Biryani", "rating": 4.9, "sales": 156, "badge": "Chef's Special"},
                {"name": "Butter Chicken", "rating": 4.7, "sales": 98, "badge": "Most Popular"},
                {"name": "Masala Dosa", "rating": 4.6, "sales": 87, "badge": "Traditional"}
            ],
            "rated_items": [
                {"name": "Hyderabadi Biryani", "rating": 4.8, "reviews": 45, "comment": "Authentic taste and perfect spices!", "date": "1 day ago"},
                {"name": "Paneer Curry", "rating": 4.4, "reviews": 28, "comment": "Rich and creamy, loved it!", "date": "3 days ago"}
            ]
        }
    }

# Initialize session state
if 'restaurant' not in st.session_state:
    st.session_state.restaurant = 'rise'
if 'view' not in st.session_state:
    st.session_state.view = 'admin'

# Load data
data = load_restaurant_data()
current_restaurant = data[st.session_state.restaurant]

# Header
st.markdown(f"""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1>🍽️ {current_restaurant['name']}</h1>
            <p style="margin: 0; opacity: 0.9;">{current_restaurant['subtitle']}</p>
        </div>
        <div style="font-size: 3rem; opacity: 0.3;">
            {'☕' if st.session_state.restaurant == 'rise' else '🍽️'}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Control buttons
col1, col2, col3, col4 = st.columns([2, 2, 2, 2])

with col1:
    if st.button("☕ Rise", key="rise_btn", use_container_width=True):
        st.session_state.restaurant = 'rise'
        st.rerun()

with col2:
    if st.button("🍽️ Blu Embers", key="embers_btn", use_container_width=True):
        st.session_state.restaurant = 'embers'
        st.rerun()

with col3:
    if st.button("🛠️ Admin View", key="admin_btn", use_container_width=True):
        st.session_state.view = 'admin'
        st.rerun()

with col4:
    if st.button("👥 Student View", key="student_btn", use_container_width=True):
        st.session_state.view = 'student'
        st.rerun()

st.markdown("---")

# Admin Dashboard
if st.session_state.view == 'admin':
    st.header("🛠️ Admin Dashboard")
    
    # Inventory Overview
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📦 Inventory Overview")
        inventory_df = pd.DataFrame(current_restaurant['inventory'])
        
        for _, item in inventory_df.iterrows():
            stock_percentage = (item['stock'] / item['max_stock']) * 100
            color = "🟢" if stock_percentage > 50 else "🟡" if stock_percentage > 20 else "🔴"
            status = "✅" if item['available'] else "❌"
            
            st.markdown(f"""
            <div style="background: white; padding: 1rem; margin: 0.5rem 0; border-radius: 8px; border-left: 4px solid {'#28a745' if item['available'] else '#dc3545'};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{item['name']}</strong> {status}
                        <br><small>{item['category'].title()}</small>
                    </div>
                    <div>
                        {color} {item['stock']}/{item['max_stock']}
                        <br><small>{stock_percentage:.0f}%</small>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("📊 Sales Analytics")
        
        # Top Selling Items Chart
        selling_df = pd.DataFrame(current_restaurant['top_selling'])
        fig_bar = px.bar(
            selling_df, 
            x='name', 
            y='sales',
            title="Top 5 Selling Items",
            color_discrete_sequence=['#667eea']
        )
        fig_bar.update_layout(height=300)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Daily Revenue Chart
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    revenue_df = pd.DataFrame({
        'Day': days,
        'Revenue': current_restaurant['daily_revenue']
    })
    
    fig_line = px.line(
        revenue_df, 
        x='Day', 
        y='Revenue',
        title="Weekly Revenue Trend (₹)",
        color_discrete_sequence=['#28a745']
    )
    fig_line.update_traces(line=dict(width=3), marker=dict(size=8))
    fig_line.update_layout(height=300)
    st.plotly_chart(fig_line, use_container_width=True)
    
    # Ratings Panel
    st.subheader("⭐ Item Ratings & Reviews")
    for item in current_restaurant['rated_items']:
        stars = "⭐" * int(item['rating']) + "☆" * (5 - int(item['rating']))
        st.markdown(f"""
        <div style="background: white; padding: 1rem; margin: 0.5rem 0; border-radius: 8px; border-left: 4px solid #ffc107;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <strong>{item['name']}</strong>
                <span style="background: #f8f9fa; padding: 0.2rem 0.5rem; border-radius: 12px; font-size: 0.8rem;">
                    {item['reviews']} reviews
                </span>
            </div>
            <div style="margin: 0.5rem 0;">
                {stars} <strong>{item['rating']}</strong>
            </div>
            <div style="background: #f8f9fa; padding: 0.5rem; border-radius: 4px; border-left: 3px solid #17a2b8;">
                💬 "{item['comment']}"
                <br><small style="color: #6c757d;">{item['date']}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Student Dashboard
else:
    st.header("👥 Student Dashboard")
    
    # Welcome Section
    st.markdown(f"""
    <div class="restaurant-card">
        <h2>Welcome to {current_restaurant['name']}!</h2>
        <p>Help us improve by suggesting new items and rating your favorites.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Suggestion Form
        st.subheader("➕ Suggest a New Item")
        with st.form("suggestion_form"):
            item_name = st.text_input("Item Name", placeholder="e.g., Matcha Latte")
            category = st.selectbox("Category", ["drink", "snack", "meal", "dessert"])
            description = st.text_area("Description", placeholder="Describe the item and why it would be a great addition...")
            
            if st.form_submit_button("Submit Suggestion", use_container_width=True):
                if item_name and category and description:
                    st.success(f"Thank you for suggesting '{item_name}'! We'll review it soon.")
                else:
                    st.error("Please fill in all fields before submitting.")
        
        # Item Rating
        st.subheader("⭐ Rate Items")
        with st.form("rating_form"):
            available_items = [item['name'] for item in current_restaurant['inventory'] if item['available']]
            selected_item = st.selectbox("Select Item to Rate", available_items)
            rating = st.slider("Rating", 1, 5, 3)
            comment = st.text_area("Comment (optional)", placeholder="Share your experience...")
            
            if st.form_submit_button("Submit Rating", use_container_width=True):
                st.success(f"Thank you for rating {selected_item}! Rating: {rating} stars")
    
    with col2:
        # Top Items
        st.subheader("🏆 Top Items")
        for item in current_restaurant['top_items']:
            stars = "⭐" * int(item['rating']) + "☆" * (5 - int(item['rating']))
            st.markdown(f"""
            <div style="background: white; padding: 1rem; margin: 0.5rem 0; border-radius: 8px; border: 1px solid #e9ecef;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <strong>{item['name']}</strong>
                    <span style="background: #28a745; color: white; padding: 0.2rem 0.5rem; border-radius: 12px; font-size: 0.8rem;">
                        {item['badge']}
                    </span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>{stars} {item['rating']}</div>
                    <div style="color: #6c757d; font-size: 0.9rem;">📈 {item['sales']} sold this week</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick Stats
        st.subheader("📊 Your Impact")
        st.markdown("""
        <div style="background: white; padding: 1rem; border-radius: 8px; border: 1px solid #e9ecef;">
            <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                <span>Suggestions Submitted</span>
                <span style="background: #6c757d; color: white; padding: 0.2rem 0.5rem; border-radius: 12px; font-size: 0.8rem;">12</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                <span>Items Rated</span>
                <span style="background: #6c757d; color: white; padding: 0.2rem 0.5rem; border-radius: 12px; font-size: 0.8rem;">28</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                <span>Suggestions Approved</span>
                <span style="background: #28a745; color: white; padding: 0.2rem 0.5rem; border-radius: 12px; font-size: 0.8rem;">3</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 1rem;">
    <p>Restaurant Management Dashboard - Built with Streamlit</p>
    <p><strong>Why these items are popular:</strong></p>
    <ul style="list-style: none; padding: 0;">
        <li>• High student ratings and positive feedback</li>
        <li>• Consistent quality and taste</li>
        <li>• Great value for money</li>
    </ul>
</div>
""", unsafe_allow_html=True)