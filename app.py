import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Mock data
restaurants = {
    'rise': {
        'name': 'Rise Coffee Shop',
        'subtitle': 'Your Daily Brew',
        'theme_gradient': 'linear-gradient(135deg, #8B4513, #D2691E)',
        'inventory': [
            {'id': 'rise_espresso', 'name': 'Espresso', 'stock': 80, 'max_stock': 100, 'category': 'drink', 'available': True},
            {'id': 'rise_latte', 'name': 'Latte', 'stock': 70, 'max_stock': 100, 'category': 'drink', 'available': True},
            {'id': 'rise_cappuccino', 'name': 'Cappuccino', 'stock': 60, 'max_stock': 100, 'category': 'drink', 'available': True},
            {'id': 'rise_americano', 'name': 'Americano', 'stock': 90, 'max_stock': 100, 'category': 'drink', 'available': True},
            {'id': 'rise_mocha', 'name': 'Mocha', 'stock': 50, 'max_stock': 100, 'category': 'drink', 'available': True},
            {'id': 'rise_croissant', 'name': 'Croissant', 'stock': 40, 'max_stock': 80, 'category': 'snack', 'available': True},
            {'id': 'rise_muffin', 'name': 'Blueberry Muffin', 'stock': 30, 'max_stock': 80, 'category': 'snack', 'available': True},
            {'id': 'rise_cookie', 'name': 'Chocolate Cookie', 'stock': 60, 'max_stock': 80, 'category': 'snack', 'available': True},
            {'id': 'rise_sandwich', 'name': 'Ham Sandwich', 'stock': 50, 'max_stock': 80, 'category': 'meal', 'available': True},
            {'id': 'rise_wrap', 'name': 'Veggie Wrap', 'stock': 40, 'max_stock': 80, 'category': 'meal', 'available': True},
            {'id': 'rise_brownie', 'name': 'Chocolate Brownie', 'stock': 70, 'max_stock': 100, 'category': 'dessert', 'available': True},
            {'id': 'rise_cake', 'name': 'Carrot Cake', 'stock': 60, 'max_stock': 100, 'category': 'dessert', 'available': True},
        ],
        'sales_data': [
            {'item_id': 'rise_latte', 'quantity': 156, 'revenue': 546},
            {'item_id': 'rise_sandwich', 'quantity': 98, 'revenue': 490},
            {'item_id': 'rise_cookie', 'quantity': 87, 'revenue': 130.5},
        ],
        'ratings': [
            {'item_id': 'rise_latte', 'rating': 5, 'comment': 'Amazing flavor!'},
            {'item_id': 'rise_latte', 'rating': 4, 'comment': 'Good as always'},
            {'item_id': 'rise_latte', 'rating': 5, 'comment': 'Perfect'},
            {'item_id': 'rise_espresso', 'rating': 4, 'comment': 'Strong and bold'},
            {'item_id': 'rise_espresso', 'rating': 5, 'comment': 'Best espresso'},
            {'item_id': 'rise_sandwich', 'rating': 4, 'comment': 'Tasty'},
            {'item_id': 'rise_sandwich', 'rating': 3, 'comment': 'Okay'},
            {'item_id': 'rise_cookie', 'rating': 5, 'comment': 'Delicious'},
            {'item_id': 'rise_cookie', 'rating': 5, 'comment': 'Love it'},
            {'item_id': 'rise_brownie', 'rating': 4, 'comment': 'Rich chocolate'},
        ],
        'suggestions': [
            {'item_name': 'Berry Smoothie', 'category': 'drink', 'description': 'Fresh berry smoothie for summer', 'price_range': 4.50, 'dietary_info': 'vegan'},
            {'item_name': 'Vegan Muffin', 'category': 'snack', 'description': 'Gluten-free vegan option', 'price_range': 2.50, 'dietary_info': 'vegan,gluten-free'},
            {'item_name': 'Iced Matcha', 'category': 'drink', 'description': 'Healthy green tea latte', 'price_range': 3.75, 'dietary_info': 'vegetarian'},
        ]
    },
    'embers': {
        'name': 'Blu Embers Restaurant',
        'subtitle': 'University Dining',
        'theme_gradient': 'linear-gradient(135deg, #1e3c72, #2a5298)',
        'inventory': [
            {'id': 'embers_biryani', 'name': 'Chicken Biryani', 'stock': 90, 'max_stock': 120, 'category': 'meal', 'available': True},
            {'id': 'embers_dal', 'name': 'Dal Rice', 'stock': 100, 'max_stock': 150, 'category': 'meal', 'available': True},
            {'id': 'embers_samosa', 'name': 'Vegetable Samosa', 'stock': 80, 'max_stock': 100, 'category': 'snack', 'available': True},
            {'id': 'embers_curry', 'name': 'Butter Chicken Curry', 'stock': 70, 'max_stock': 100, 'category': 'meal', 'available': True},
            {'id': 'embers_naan', 'name': 'Garlic Naan', 'stock': 110, 'max_stock': 150, 'category': 'snack', 'available': True},
            {'id': 'embers_gulab', 'name': 'Gulab Jamun', 'stock': 60, 'max_stock': 100, 'category': 'dessert', 'available': True},
        ],
        'sales_data': [
            {'item_id': 'embers_biryani', 'quantity': 234, 'revenue': 1872},
            {'item_id': 'embers_dal', 'quantity': 187, 'revenue': 748},
            {'item_id': 'embers_samosa', 'quantity': 165, 'revenue': 247.5},
        ],
        'ratings': [
            {'item_id': 'embers_biryani', 'rating': 5, 'comment': 'Authentic taste'},
            {'item_id': 'embers_biryani', 'rating': 5, 'comment': 'Must try'},
            {'item_id': 'embers_biryani', 'rating': 4, 'comment': 'Good portion'},
            {'item_id': 'embers_dal', 'rating': 4, 'comment': 'Comfort food'},
            {'item_id': 'embers_dal', 'rating': 5, 'comment': 'Perfect spice'},
            {'item_id': 'embers_samosa', 'rating': 5, 'comment': 'Crispy'},
            {'item_id': 'embers_samosa', 'rating': 4, 'comment': 'Spicy good'},
            {'item_id': 'embers_gulab', 'rating': 5, 'comment': 'Sweet heaven'},
            {'item_id': 'embers_gulab', 'rating': 5, 'comment': 'Best dessert'},
            {'item_id': 'embers_lassi', 'rating': 4, 'comment': 'Refreshing'},
        ],
        'suggestions': [
            {'item_name': 'Tandoori Pizza', 'category': 'meal', 'description': 'Fusion Indian pizza', 'price_range': 6.00, 'dietary_info': 'vegetarian'},
            {'item_name': 'Mango Kulfi', 'category': 'dessert', 'description': 'Traditional ice cream', 'price_range': 3.50, 'dietary_info': ''},
        ]
    }
}

# Streamlit app
st.set_page_config(page_title="Restaurant Management Dashboard", layout="wide")

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

# Apply theme
theme_gradient = restaurants[st.session_state.active_restaurant]['theme_gradient']
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
        df_inv = pd.DataFrame(restaurants[st.session_state.active_restaurant]['inventory'])
        df_inv['stock_pct'] = (df_inv['stock'] / df_inv['max_stock'] * 100).round(1)
        
        for _, row in df_inv.iterrows():
            color = 'normal' if row['stock_pct'] > 70 else 'warning' if row['stock_pct'] > 30 else 'inverse'
            st.metric(
                label=row['name'],
                value=f"{row['stock']}/{row['max_stock']}",
                delta=f"{row['stock_pct']}%",
                delta_color='normal' if row['stock_pct'] > 70 else 'warning' if row['stock_pct'] > 30 else 'inverse'
            )
            st.progress(row['stock_pct'] / 100)
            st.caption(f"Category: {row['category']} | Available: {'Yes' if row['available'] else 'No'}")
    
    with col2:
        st.subheader("Sales Analytics")
        df_sales = pd.DataFrame(restaurants[st.session_state.active_restaurant]['sales_data'])
        df_sales = df_sales.merge(pd.DataFrame(restaurants[st.session_state.active_restaurant]['inventory'])[['id', 'name']], left_on='item_id', right_on='id', how='left')
        df_sales = df_sales[['name', 'quantity', 'revenue']].head(5)
        
        if not df_sales.empty:
            fig_bar = px.bar(df_sales, x='name', y='quantity', title='Top Sellers by Sales Volume',
                             color='revenue', color_continuous_scale='Viridis')
            st.plotly_chart(fig_bar, use_container_width=True)
            
            fig_pie = px.pie(df_sales, values='revenue', names='name', title='Revenue Distribution')
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No sales data available.")
    
    with col3:
        st.subheader("Average Ratings")
        df_ratings = pd.DataFrame(restaurants[st.session_state.active_restaurant]['ratings'])
        df_ratings = df_ratings.groupby('item_id').agg({'rating': 'mean', 'comment': 'count'}).reset_index()
        df_ratings = df_ratings.merge(pd.DataFrame(restaurants[st.session_state.active_restaurant]['inventory'])[['id', 'name']], left_on='item_id', right_on='id', how='left')
        
        for _, row in df_ratings.iterrows():
            st.metric(
                label=row['name'],
                value=f"{row['rating']:.1f} ⭐",
                delta=f"{row['comment']} reviews"
            )
    
    # Suggestions Panel
    st.subheader("Customer Suggestions")
    df_sugg = pd.DataFrame(restaurants[st.session_state.active_restaurant]['suggestions'])
    st.dataframe(df_sugg, use_container_width=True)

elif st.session_state.active_view == 'student':
    # Student Dashboard
    tab1, tab2, tab3 = st.tabs(["Top Items", "Rate an Item", "Suggest New Item"])
    
    with tab1:
        st.subheader("Top Items")
        df_inv = pd.DataFrame(restaurants[st.session_state.active_restaurant]['inventory'])
        df_ratings = pd.DataFrame(restaurants[st.session_state.active_restaurant]['ratings'])
        df_top = df_ratings.groupby('item_id').agg({'rating': 'mean', 'comment': 'count'}).reset_index()
        df_top = df_top.merge(df_inv[['id', 'name']], left_on='item_id', right_on='id', how='left')
        df_top = df_top.sort_values('rating', ascending=False).head(10)
        
        if not df_top.empty:
            fig = px.bar(df_top, x='name', y='rating', title='Top Rated Items',
                         color='comment', hover_data=['comment'])
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(df_top, use_container_width=True)
        else:
            st.info("No items available.")
    
    with tab2:
        st.subheader("Rate an Item")
        df_items = pd.DataFrame(restaurants[st.session_state.active_restaurant]['inventory'])
        item_names = df_items[df_items['available']]['name'].tolist()
        
        if item_names:
            item_name = st.selectbox("Select an Item to Rate", item_names)
            selected_item_id = df_items[df_items['name'] == item_name]['id'].iloc[0]
            
            rating = st.slider("Your Rating", 1, 5, 3, help="1-5 stars")
            comment = st.text_area("Comments (optional)", placeholder="Tell us about your experience...")
            
            if st.button("Submit Rating", type="primary"):
                new_rating = {'item_id': selected_item_id, 'rating': rating, 'comment': comment}
                if 'ratings' not in st.session_state:
                    st.session_state.ratings = restaurants[st.session_state.active_restaurant]['ratings'].copy()
                st.session_state.ratings.append(new_rating)
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
                    new_suggestion = {
                        'item_name': item_name,
                        'category': category,
                        'description': description,
                        'price_range': price_range,
                        'dietary_info': dietary_str
                    }
                    if 'suggestions' not in st.session_state:
                        st.session_state.suggestions = restaurants[st.session_state.active_restaurant]['suggestions'].copy()
                    st.session_state.suggestions.append(new_suggestion)
                    st.success("Your suggestion has been submitted! We'll review it soon.")
                else:
                    st.error("Please provide at least an item name and description.")
