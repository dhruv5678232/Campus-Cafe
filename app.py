import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
from datetime import datetime, timedelta

# Configure page
st.set_page_config(
    page_title="Campus Café Pulse",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for coffee-themed styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #8B4513 0%, #D2691E 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    
    .cafe-card {
        background: linear-gradient(135deg, #A0522D 0%, #CD853F 100%);
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
        border-left: 4px solid #8B4513;
    }
    
    .feedback-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #D2691E;
        margin: 0.5rem 0;
    }
    
    .menu-item {
        background: white;
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 1px solid #e9ecef;
        color: black; /* Changed font color to black for readability */
    }
</style>
""", unsafe_allow_html=True)

# Sample data
@st.cache_data
def load_cafe_data():
    return {
        "rise_campus_cafe": {
            "name": "Rise Campus Café",
            "subtitle": "Campus Coffee Hub",
            "inventory": [
                {"name": "Espresso", "stock": 50, "max_stock": 70, "category": "drink", "available": True, "price": 2.5},
                {"name": "Croissant", "stock": 15, "max_stock": 50, "category": "pastry", "available": True, "price": 3.0},
                {"name": "Bagel", "stock": 10, "max_stock": 40, "category": "meal", "available": False, "price": 4.0},
                {"name": "Muffin", "stock": 20, "max_stock": 60, "category": "snack", "available": True, "price": 2.8},
            ],
            "top_selling": [
                {"name": "Latte", "sales": 120},
                {"name": "Croissant", "sales": 85},
                {"name": "Muffin", "sales": 70},
                {"name": "Espresso", "sales": 60},
            ],
            "daily_revenue": [3500, 4000, 4200, 3800, 4500, 5000, 4100],
            "top_items": [
                {"name": "Caramel Latte", "rating": 4.7, "sales": 80, "badge": "Student Favorite"},
                {"name": "Blueberry Muffin", "rating": 4.5, "sales": 50, "badge": "Best Seller"},
            ]
        },
        "embers": {
            "name": "Embers",
            "subtitle": "Campus Coffee Corner",
            "inventory": [
                {"name": "Cappuccino", "stock": 40, "max_stock": 60, "category": "drink", "available": True, "price": 2.7},
                {"name": "Scone", "stock": 12, "max_stock": 40, "category": "pastry", "available": True, "price": 2.5},
                {"name": "Sandwich", "stock": 8, "max_stock": 30, "category": "meal", "available": False, "price": 4.5},
                {"name": "Cookie", "stock": 25, "max_stock": 50, "category": "snack", "available": True, "price": 2.0},
            ],
            "top_selling": [
                {"name": "Cappuccino", "sales": 150},
                {"name": "Sandwich", "sales": 100},
                {"name": "Cookie", "sales": 90},
                {"name": "Scone", "sales": 70},
            ],
            "daily_revenue": [4000, 4500, 4800, 4200, 5000, 5500, 4300],
            "top_items": [
                {"name": "Vanilla Cappuccino", "rating": 4.9, "sales": 100, "badge": "Top Pick"},
                {"name": "Chocolate Cookie", "rating": 4.6, "sales": 60, "badge": "Sweet Deal"},
            ]
        }
    }

# Load or initialize feedback data
FEEDBACK_FILE = "feedback.json"

def load_feedback():
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, 'r') as f:
            return json.load(f)
    return {"rise_campus_cafe": [], "embers": []}

def save_feedback(feedback_data):
    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(feedback_data, f, indent=2)

# Load data and feedback at the start
data = load_cafe_data()
feedback_data = load_feedback()

# Initialize session state
if 'cafe' not in st.session_state:
    st.session_state.cafe = 'rise_campus_cafe'
if 'view' not in st.session_state:
    st.session_state.view = 'student'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = 'student'

# Simulated login
if not st.session_state.logged_in:
    st.markdown("<h2>Login to Campus Café Pulse</h2>", unsafe_allow_html=True)
    with st.form("login_form"):
        username = st.text_input("Username")
        role = st.selectbox("Role", ["Student", "Admin"])
        if st.form_submit_button("Login"):
            if username:
                st.session_state.logged_in = True
                st.session_state.user_role = role.lower()
                st.success(f"Logged in as {username} ({role})")
                st.rerun()
            else:
                st.error("Please enter a username.")
else:
    # Ensure current_cafe is defined
    current_cafe = data.get(st.session_state.cafe, data['rise_campus_cafe'])

    # Header
    st.markdown(f"""
    <div class="main-header">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1>☕ Campus Café Pulse</h1>
                <p style="margin: 0; opacity: 0.9;">{current_cafe['name']} - {current_cafe['subtitle']}</p>
            </div>
            <div style="font-size: 3rem; opacity: 0.3;">☕</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Control buttons
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])
    with col1:
        if st.button("☕ Rise Campus Café", key="rise_campus_cafe_btn", use_container_width=True):
            st.session_state.cafe = 'rise_campus_cafe'
            st.rerun()
    with col2:
        if st.button("☕ Embers", key="embers_btn", use_container_width=True):
            st.session_state.cafe = 'embers'
            st.rerun()
    with col3:
        if st.session_state.user_role == 'admin' and st.button("🛠️ Admin View", key="admin_btn", use_container_width=True):
            st.session_state.view = 'admin'
            st.rerun()
    with col4:
        if st.button("👩‍🎓 Student View", key="student_btn", use_container_width=True):
            st.session_state.view = 'student'
            st.rerun()
    with col5:
        if st.button("🚪 Logout", key="logout_btn", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_role = 'student'
            st.rerun()

    st.markdown("---")

    # Admin Dashboard
    if st.session_state.view == 'admin' and st.session_state.user_role == 'admin':
        st.header("🛠️ Admin Dashboard")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📦 Inventory Overview")
            inventory_df = pd.DataFrame(current_cafe['inventory'])
            for _, item in inventory_df.iterrows():
                stock_percentage = (item['stock'] / item['max_stock']) * 100
                color = "🟢" if stock_percentage > 50 else "🟡" if stock_percentage > 20 else "🔴"
                status = "✅" if item['available'] else "❌"
                st.markdown(f"""
                <div class="metric-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>{item['name']}</strong> {status}
                            <br><small>{item['category'].title()} - ${item['price']:.2f}</small>
                        </div>
                        <div>
                            {color} {item['stock']}/{item['max_stock']}
                            <br><small>{stock_percentage:.0f}%</small>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.subheader("📊 Feedback Analytics")
            feedback_df = pd.DataFrame(feedback_data[st.session_state.cafe])
            if not feedback_df.empty:
                avg_rating = feedback_df['rating'].mean()
                st.markdown(f"""
                <div class="metric-card">
                    <strong>Average Rating:</strong> {avg_rating:.1f} ⭐
                    <br><strong>Total Feedback:</strong> {len(feedback_df)}
                    <br><strong>Feedback Trend:</strong>
                </div>
                """, unsafe_allow_html=True)
                feedback_df['date'] = pd.to_datetime(feedback_df['date'])
                trend_df = feedback_df.groupby(feedback_df['date'].dt.date)['rating'].mean().reset_index()
                fig_trend = px.line(trend_df, x='date', y='rating', title="Feedback Rating Trend")
                fig_trend.update_layout(height=300, yaxis_range=[1, 5])
                st.plotly_chart(fig_trend, use_container_width=True)
            else:
                st.write("No feedback available.")
        
        st.subheader("📈 Sales Overview")
        revenue_df = pd.DataFrame({
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'Revenue': current_cafe['daily_revenue']
        })
        fig_line = px.line(revenue_df, x='Day', y='Revenue', title="Weekly Revenue Trend ($)")
        fig_line.update_traces(line=dict(width=3), marker=dict(size=8))
        fig_line.update_layout(height=300)
        st.plotly_chart(fig_line, use_container_width=True)

    # Student Dashboard
    else:
        st.header("👩‍🎓 Student Dashboard")
        
        st.markdown(f"""
        <div class="cafe-card">
            <h2>Welcome to {current_cafe['name']}!</h2>
            <p>Your feedback shapes our café! Share your thoughts and explore our menu.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📝 Submit Feedback")
            with st.form("feedback_form"):
                item_name = st.selectbox("Select Item", [item['name'] for item in current_cafe['inventory'] if item['available']])
                rating = st.slider("Rating (1-5)", 1, 5, 3)
                comment = st.text_area("Comment", placeholder="Share your experience...")
                submit_button = st.form_submit_button("Submit Feedback")
                if submit_button:
                    if item_name and comment:
                        feedback = {
                            "name": item_name,
                            "rating": rating,
                            "comment": comment,
                            "date": datetime.now().strftime("%Y-%m-%d")
                        }
                        feedback_data[st.session_state.cafe].append(feedback)
                        save_feedback(feedback_data)
                        st.success(f"Thank you for your feedback on {item_name}!")
                    else:
                        st.error("Please select an item and provide a comment.")
            
            st.subheader("➕ Suggest a Menu Item")
            with st.form("suggestion_form"):
                item_name = st.text_input("Item Name", placeholder="e.g., Iced Mocha")
                category = st.selectbox("Category", ["drink", "pastry", "meal", "snack"])
                description = st.text_area("Description", placeholder="Why should we add this item?")
                if st.form_submit_button("Submit Suggestion"):
                    if item_name and description:
                        st.success(f"Thank you for suggesting '{item_name}'!")
                    else:
                        st.error("Please fill in all fields.")
        
        with col2:
            st.subheader("📋 Menu Preview")
            for item in current_cafe['inventory']:
                status = "Available" if item['available'] else "Out of Stock"
                status_color = "#28a745" if item['available'] else "#dc3545"
                st.markdown(f"""
                <div class="menu-item">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>{item['name']}</strong>
                            <br><small>{item['category'].title()} - ${item['price']:.2f}</small>
                        </div>
                        <div style="color: {status_color};">
                            {status}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.subheader("📣 Recent Feedback")
            for item in feedback_data[st.session_state.cafe][:5]:  # Limit to 5 for brevity
                stars = "⭐" * int(item['rating']) + "☆" * (5 - int(item['rating']))
                st.markdown(f"""
                <div class="feedback-card">
                    <strong>{item['name']}</strong>
                    <div>{stars} {item['rating']}</div>
                    <p>💬 "{item['comment']}"</p>
                    <small style="color: #6c757d;">{item['date']}</small>
                </div>
                """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; padding: 1rem;">
        <p>Campus Café Pulse - Powered by Streamlit</p>
        <p><strong>Why we value your feedback:</strong></p>
        <ul style="list-style: none; padding: 0;">
            <li>• Helps us improve our menu</li>
            <li>• Ensures your favorite items stay in stock</li>
            <li>• Creates a better café experience</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
