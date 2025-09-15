import streamlit as st
import plotly.express as px
import pandas as pd
import mysql.connector
from datetime import datetime, date, timedelta
import numpy as np

# Database configuration
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'Dhruv500049@',
    'database': 'restaurant_db'
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS restaurant_db")
    conn.commit()
    cursor.close()
    conn.close()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    tables_sql = [
        """
        USE restaurant_db;
        CREATE TABLE IF NOT EXISTS restaurants (
            id VARCHAR(10) PRIMARY KEY,
            name VARCHAR(100),
            subtitle VARCHAR(100),
            theme_primary VARCHAR(20),
            theme_secondary VARCHAR(20),
            theme_accent VARCHAR(20),
            theme_gradient VARCHAR(100)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS inventory (
            id VARCHAR(50) PRIMARY KEY,
            restaurant_id VARCHAR(10),
            name VARCHAR(100),
            stock INT,
            max_stock INT,
            category ENUM('drink', 'snack', 'meal', 'dessert'),
            available BOOLEAN DEFAULT TRUE,
            last_restocked DATE,
            supplier VARCHAR(100),
            cost_per_unit DECIMAL(10,2),
            FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS sales_records (
            id INT AUTO_INCREMENT PRIMARY KEY,
            restaurant_id VARCHAR(10),
            item_id VARCHAR(50),
            sale_date DATE,
            quantity INT,
            revenue DECIMAL(10,2),
            FOREIGN KEY (restaurant_id) REFERENCES restaurants(id),
            FOREIGN KEY (item_id) REFERENCES inventory(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS ratings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            restaurant_id VARCHAR(10),
            item_id VARCHAR(50),
            rating INT CHECK (rating >=1 AND rating <=5),
            comment TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (restaurant_id) REFERENCES restaurants(id),
            FOREIGN KEY (item_id) REFERENCES inventory(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS suggestions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            restaurant_id VARCHAR(10),
            item_name VARCHAR(100),
            category ENUM('drink', 'snack', 'meal', 'dessert'),
            description TEXT,
            price_range DECIMAL(10,2),
            dietary_info VARCHAR(100),
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
        )
        """
    ]
    
    for sql in tables_sql:
        cursor.execute(sql)
    
    conn.commit()
    cursor.close()
    conn.close()

def has_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("USE restaurant_db; SELECT COUNT(*) FROM restaurants")
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0

def insert_sample_data():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Insert restaurants
    cursor.execute("""
        INSERT IGNORE INTO restaurants (id, name, subtitle, theme_primary, theme_secondary, theme_accent, theme_gradient)
        VALUES 
        ('rise', 'Rise Coffee Shop', 'Your Daily Brew', '#8B4513', '#D2691E', '#F4A460', 'linear-gradient(135deg, #8B4513, #D2691E)'),
        ('embers', 'Blu Embers Restaurant', 'University Dining', '#1e3c72', '#2a5298', '#87CEEB', 'linear-gradient(135deg, #1e3c72, #2a5298)')
    """)
    
    # Rise inventory
    rise_items = [
        ('rise_espresso', 'rise', 'Espresso', 80, 100, 'drink', '2025-09-01', 'Local Roaster', 2.50),
        ('rise_latte', 'rise', 'Latte', 70, 100, 'drink', '2025-09-01', 'Local Roaster', 3.50),
        ('rise_cappuccino', 'rise', 'Cappuccino', 60, 100, 'drink', '2025-09-02', 'Local Roaster', 3.00),
        ('rise_americano', 'rise', 'Americano', 90, 100, 'drink', '2025-09-01', 'Local Roaster', 2.00),
        ('rise_mocha', 'rise', 'Mocha', 50, 100, 'drink', '2025-09-03', 'Local Roaster', 4.00),
        ('rise_croissant', 'rise', 'Croissant', 40, 80, 'snack', '2025-09-02', 'Bakery', 2.50),
        ('rise_muffin', 'rise', 'Blueberry Muffin', 30, 80, 'snack', '2025-09-02', 'Bakery', 2.00),
        ('rise_cookie', 'rise', 'Chocolate Cookie', 60, 80, 'snack', '2025-09-01', 'Bakery', 1.50),
        ('rise_sandwich', 'rise', 'Ham Sandwich', 50, 80, 'meal', '2025-09-02', 'Deli', 5.00),
        ('rise_wrap', 'rise', 'Veggie Wrap', 40, 80, 'meal', '2025-09-03', 'Deli', 4.50),
        ('rise_brownie', 'rise', 'Chocolate Brownie', 70, 100, 'dessert', '2025-09-01', 'Bakery', 3.00),
        ('rise_cake', 'rise', 'Carrot Cake', 60, 100, 'dessert', '2025-09-01', 'Bakery', 4.00),
        ('rise_pastry1', 'rise', 'Danish Pastry', 55, 80, 'snack', '2025-09-02', 'Bakery', 2.75),
        ('rise_pastry2', 'rise', 'Apple Turnover', 45, 80, 'snack', '2025-09-03', 'Bakery', 2.25),
        ('rise_tea', 'rise', 'Green Tea', 85, 100, 'drink', '2025-09-01', 'Tea Supplier', 1.50)
    ]
    
    cursor.executemany("""
        INSERT IGNORE INTO inventory (id, restaurant_id, name, stock, max_stock, category, last_restocked, supplier, cost_per_unit)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, rise_items)
    
    # Embers inventory
    embers_items = [
        ('embers_biryani', 'embers', 'Chicken Biryani', 90, 120, 'meal', '2025-09-01', 'Spice Supplier', 8.00),
        ('embers_dal', 'embers', 'Dal Rice', 100, 150, 'meal', '2025-09-01', 'Spice Supplier', 4.00),
        ('embers_samosa', 'embers', 'Vegetable Samosa', 80, 100, 'snack', '2025-09-02', 'Street Vendor', 1.50),
        ('embers_curry', 'embers', 'Butter Chicken Curry', 70, 100, 'meal', '2025-09-01', 'Spice Supplier', 7.00),
        ('embers_naan', 'embers', 'Garlic Naan', 110, 150, 'snack', '2025-09-01', 'Bakery', 2.00),
        ('embers_gulab', 'embers', 'Gulab Jamun', 60, 100, 'dessert', '2025-09-03', 'Sweet Shop', 3.50),
        ('embers_roti', 'embers', 'Plain Roti', 120, 150, 'snack', '2025-09-01', 'Bakery', 1.00),
        ('embers_paneer', 'embers', 'Paneer Tikka', 50, 80, 'meal', '2025-09-02', 'Dairy Supplier', 6.50),
        ('embers_rice', 'embers', 'Jeera Rice', 95, 120, 'meal', '2025-09-01', 'Rice Supplier', 3.00),
        ('embers_salad', 'embers', 'Cucumber Raita', 75, 100, 'snack', '2025-09-02', 'Veggie Supplier', 2.50),
        ('embers_kabab', 'embers', 'Seekh Kabab', 65, 100, 'meal', '2025-09-03', 'Meat Supplier', 7.50),
        ('embers_lassi', 'embers', 'Mango Lassi', 85, 120, 'drink', '2025-09-01', 'Dairy Supplier', 3.00),
        ('embers_idli', 'embers', 'Idli Sambhar', 55, 80, 'meal', '2025-09-02', 'South Indian', 4.50),
        ('embers_dosa', 'embers', 'Masala Dosa', 45, 80, 'meal', '2025-09-03', 'South Indian', 5.00),
        ('embers_chaat', 'embers', 'Pani Puri', 40, 80, 'snack', '2025-09-02', 'Street Vendor', 2.00),
        ('embers_vada', 'embers', 'Medu Vada', 35, 60, 'snack', '2025-09-03', 'South Indian', 2.50),
        ('embers_rasmalai', 'embers', 'Rasmalai', 50, 80, 'dessert', '2025-09-01', 'Sweet Shop', 4.00),
        ('embers_chutney', 'embers', 'Coconut Chutney', 90, 100, 'snack', '2025-09-01', 'Spice Supplier', 1.00),
        ('embers_chai', 'embers', 'Masala Chai', 105, 150, 'drink', '2025-09-01', 'Tea Supplier', 1.50),
        ('embers_falooda', 'embers', 'Falooda', 30, 60, 'dessert', '2025-09-04', 'Sweet Shop', 4.50)
    ]
    
    cursor.executemany("""
        INSERT IGNORE INTO inventory (id, restaurant_id, name, stock, max_stock, category, last_restocked, supplier, cost_per_unit)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, embers_items)
    
    # Generate sample sales for rise
    rise_item_ids = [item[0] for item in rise_items]
    start_date = date(2025, 9, 1)
    for i in range(15):
        day = start_date + timedelta(days=i)
        for item_id in rise_item_ids:
            qty = np.random.randint(5, 20)
            price = 3.5  # average
            rev = qty * price
            cursor.execute("""
                INSERT IGNORE INTO sales_records (restaurant_id, item_id, sale_date, quantity, revenue)
                VALUES (%s, %s, %s, %s, %s)
            """, ('rise', item_id, day, qty, round(rev, 2)))
    
    # Generate sample sales for embers
    embers_item_ids = [item[0] for item in embers_items]
    for i in range(15):
        day = start_date + timedelta(days=i)
        for item_id in embers_item_ids:
            qty = np.random.randint(10, 30)
            price = 5.0  # average
            rev = qty * price
            cursor.execute("""
                INSERT IGNORE INTO sales_records (restaurant_id, item_id, sale_date, quantity, revenue)
                VALUES (%s, %s, %s, %s, %s)
            """, ('embers', item_id, day, qty, round(rev, 2)))
    
    # Sample ratings for rise
    rise_ratings = [
        ('rise', 'rise_latte', 5, 'Amazing flavor!'),
        ('rise', 'rise_latte', 4, 'Good as always'),
        ('rise', 'rise_latte', 5, 'Perfect'),
        ('rise', 'rise_espresso', 4, 'Strong and bold'),
        ('rise', 'rise_espresso', 5, 'Best espresso'),
        ('rise', 'rise_sandwich', 4, 'Tasty'),
        ('rise', 'rise_sandwich', 3, 'Okay'),
        ('rise', 'rise_cookie', 5, 'Delicious'),
        ('rise', 'rise_cookie', 5, 'Love it'),
        ('rise', 'rise_brownie', 4, 'Rich chocolate')
    ]
    
    cursor.executemany("""
        INSERT INTO ratings (restaurant_id, item_id, rating, comment)
        VALUES (%s, %s, %s, %s)
    """, rise_ratings)
    
    # Sample ratings for embers
    embers_ratings = [
        ('embers', 'embers_biryani', 5, 'Authentic taste'),
        ('embers', 'embers_biryani', 5, 'Must try'),
        ('embers', 'embers_biryani', 4, 'Good portion'),
        ('embers', 'embers_dal', 4, 'Comfort food'),
        ('embers', 'embers_dal', 5, 'Perfect spice'),
        ('embers', 'embers_samosa', 5, 'Crispy'),
        ('embers', 'embers_samosa', 4, 'Spicy good'),
        ('embers', 'embers_gulab', 5, 'Sweet heaven'),
        ('embers', 'embers_gulab', 5, 'Best dessert'),
        ('embers', 'embers_lassi', 4, 'Refreshing')
    ]
    
    cursor.executemany("""
        INSERT INTO ratings (restaurant_id, item_id, rating, comment)
        VALUES (%s, %s, %s, %s)
    """, embers_ratings)
    
    # Sample suggestions
    suggestions_data = [
        ('rise', 'Berry Smoothie', 'drink', 'Fresh berry smoothie for summer', 4.50, 'vegan'),
        ('rise', 'Vegan Muffin', 'snack', 'Gluten-free vegan option', 2.50, 'vegan,gluten-free'),
        ('embers', 'Tandoori Pizza', 'meal', 'Fusion Indian pizza', 6.00, 'vegetarian'),
        ('embers', 'Mango Kulfi', 'dessert', 'Traditional ice cream', 3.50, ''),
        ('rise', 'Iced Matcha', 'drink', 'Healthy green tea latte', 3.75, 'vegetarian')
    ]
    
    cursor.executemany("""
        INSERT INTO suggestions (restaurant_id, item_name, category, description, price_range, dietary_info)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, suggestions_data)
    
    conn.commit()
    cursor.close()
    conn.close()

# Streamlit app
st.set_page_config(page_title="Restaurant Management Dashboard", layout="wide")

init_db()
if not has_data():
    insert_sample_data()

if 'active_view' not in st.session_state:
    st.session_state.active_view = 'admin'
if 'active_restaurant' not in st.session_state:
    st.session_state.active_restaurant = 'rise'

# Sidebar
with st.sidebar:
    st.title("Dashboard Controls")
    selected_view = st.selectbox("Select View", ['admin', 'student'], index=0 if st.session_state.active_view == 'admin' else 1)
    if selected_view != st.session_state.active_view:
        st.session_state.active_view = selected_view
    
    selected_rest = st.selectbox("Select Restaurant", ['rise', 'embers'], index=0 if st.session_state.active_restaurant == 'rise' else 1)
    if selected_rest != st.session_state.active_restaurant:
        st.session_state.active_restaurant = selected_rest

# Fetch theme for CSS
conn = get_connection()
theme_df = pd.read_sql(f"SELECT theme_gradient FROM restaurants WHERE id = '{st.session_state.active_restaurant}'", conn)
conn.close()
theme_gradient = theme_df['theme_gradient'].iloc[0] if not theme_df.empty else 'linear-gradient(135deg, #f0f0f0, #ffffff)'

st.markdown(f"""
<style>
    .main {{
        background: {theme_gradient};
        background-attachment: fixed;
    }}
    .stApp {{
        background: {theme_gradient};
    }}
</style>
""", unsafe_allow_html=True)

st.title(f"{st.session_state.active_restaurant.upper()} - {st.session_state.active_view.capitalize()} Dashboard")

if st.session_state.active_view == 'admin':
    # Admin Dashboard
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Inventory Overview")
        conn = get_connection()
        df_inv = pd.read_sql(f"""
            SELECT name, stock, max_stock, category, available,
            ROUND((stock / max_stock * 100), 1) as stock_pct
            FROM inventory WHERE restaurant_id = '{st.session_state.active_restaurant}'
        """, conn)
        conn.close()
        
        for _, row in df_inv.iterrows():
            color = 'normal' if row['stock_pct'] > 70 else 'warning' if row['stock_pct'] > 30 else 'warning' if row['stock_pct'] > 10 else 'inverse'
            st.metric(
                label=row['name'],
                value=f"{row['stock']}/{row['max_stock']}",
                delta=f"{row['stock_pct']}%",
                delta_color='normal' if row['stock_pct'] > 70 else 'warning' if row['stock_pct'] > 30 else 'inverse'
            )
            with st.container():
                progress_bar = st.progress(row['stock_pct'] / 100)
                progress_bar.progress(row['stock_pct'] / 100)
            st.caption(f"Category: {row['category']} | Available: {'Yes' if row['available'] else 'No'}")
    
    with col2:
        st.subheader("Sales Analytics")
        conn = get_connection()
        df_sales = pd.read_sql(f"""
            SELECT i.name, SUM(s.quantity) as total_sales, SUM(s.revenue) as total_revenue,
            ROUND(AVG(s.revenue / s.quantity), 2) as avg_price
            FROM sales_records s
            JOIN inventory i ON s.item_id = i.id
            WHERE s.restaurant_id = '{st.session_state.active_restaurant}'
            GROUP BY i.id, i.name
            ORDER BY total_sales DESC
            LIMIT 5
        """, conn)
        conn.close()
        
        if not df_sales.empty:
            fig_bar = px.bar(df_sales, x='name', y='total_sales', title='Top Sellers by Sales Volume',
                             color='total_revenue', color_continuous_scale='Viridis')
            st.plotly_chart(fig_bar, use_container_width=True)
            
            fig_pie = px.pie(df_sales, values='total_revenue', names='name', title='Revenue Distribution')
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No sales data available.")
    
    with col3:
        st.subheader("Average Ratings")
        conn = get_connection()
        df_ratings = pd.read_sql(f"""
            SELECT i.name, ROUND(AVG(r.rating), 1) as avg_rating, COUNT(r.id) as review_count
            FROM inventory i
            LEFT JOIN ratings r ON i.id = r.item_id AND r.restaurant_id = i.restaurant_id
            WHERE i.restaurant_id = '{st.session_state.active_restaurant}'
            GROUP BY i.id, i.name
            ORDER BY avg_rating DESC
        """, conn)
        conn.close()
        
        for _, row in df_ratings.iterrows():
            st.metric(
                label=row['name'],
                value=f"{row['avg_rating']} ⭐",
                delta=f"{row['review_count']} reviews"
            )
    
    # Suggestions Panel
    st.subheader("Customer Suggestions")
    conn = get_connection()
    df_sugg = pd.read_sql(f"""
        SELECT item_name, category, description, price_range, dietary_info, timestamp
        FROM suggestions WHERE restaurant_id = '{st.session_state.active_restaurant}'
        ORDER BY timestamp DESC
    """, conn)
    conn.close()
    st.dataframe(df_sugg, use_container_width=True)

elif st.session_state.active_view == 'student':
    # Student Dashboard
    tab1, tab2, tab3 = st.tabs(["Top Items", "Rate an Item", "Suggest New Item"])
    
    with tab1:
        st.subheader("Top Items")
        conn = get_connection()
        df_top = pd.read_sql(f"""
            SELECT i.name, 
                   COALESCE(ROUND(AVG(r.rating), 1), 0) as avg_rating,
                   COALESCE(COUNT(r.id), 0) as reviews,
                   COALESCE(SUM(s.quantity), 0) as total_sales
            FROM inventory i
            LEFT JOIN ratings r ON i.id = r.item_id AND r.restaurant_id = i.restaurant_id
            LEFT JOIN sales_records s ON i.id = s.item_id AND s.restaurant_id = i.restaurant_id
            WHERE i.restaurant_id = '{st.session_state.active_restaurant}' AND i.available = TRUE
            GROUP BY i.id, i.name
            ORDER BY avg_rating DESC, total_sales DESC
            LIMIT 10
        """, conn)
        conn.close()
        
        if not df_top.empty:
            fig = px.bar(df_top, x='name', y='avg_rating', title='Top Rated Items',
                         color='total_sales', hover_data=['reviews'])
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(df_top, use_container_width=True)
        else:
            st.info("No items available.")
    
    with tab2:
        st.subheader("Rate an Item")
        conn = get_connection()
        df_items = pd.read_sql(f"""
            SELECT id, name FROM inventory 
            WHERE restaurant_id = '{st.session_state.active_restaurant}' AND available = TRUE
        """, conn)
        conn.close()
        
        if not df_items.empty:
            item_name = st.selectbox("Select an Item to Rate", df_items['name'].tolist())
            selected_item_id = df_items[df_items['name'] == item_name]['id'].iloc[0]
            
            rating = st.slider("Your Rating", 1, 5, 3, help="1-5 stars")
            comment = st.text_area("Comments (optional)", placeholder="Tell us about your experience...")
            
            if st.button("Submit Rating", type="primary"):
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO ratings (restaurant_id, item_id, rating, comment)
                    VALUES (%s, %s, %s, %s)
                """, (st.session_state.active_restaurant, selected_item_id, rating, comment))
                conn.commit()
                cursor.close()
                conn.close()
                st.success("Thank you for your rating! It has been submitted.")
        else:
            st.warning("No available items to rate.")
    
    with tab3:
        st.subheader("Suggest a New Item")
        with st.form("suggestion_form", clear_on_submit=True):
            item_name = st.text_input("Item Name", placeholder="e.g., Vegan Burger")
            category = st.selectbox("Category", ['drink', 'snack', 'meal', 'dessert'])
            description = st.text_area("Description", placeholder="Describe the item...", max_chars=500)
            price_range = st.number_input("Expected Price (₹)", min_value=0.0, format="%.2f")
            dietary = st.multiselect("Dietary Preferences", ['vegetarian', 'vegan', 'gluten-free'], help="Select all that apply")
            dietary_str = ", ".join(dietary) if dietary else ""
            
            submitted = st.form_submit_button("Submit Suggestion", type="primary")
            
            if submitted:
                if item_name and description:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO suggestions (restaurant_id, item_name, category, description, price_range, dietary_info)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (st.session_state.active_restaurant, item_name, category, description, price_range, dietary_str))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    st.success("Your suggestion has been submitted! We'll review it soon.")
                else:
                    st.error("Please provide at least an item name and description.")
