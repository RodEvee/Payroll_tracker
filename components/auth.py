"""
Authentication Component
Handles user authentication
"""

import streamlit as st
from services.database import verify_user, create_user

def show_authentication():
    """Show authentication screens"""
    st.markdown('<h1 class="main-header">🔐 Secure Authentication</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["🔒 Login", "📝 Register"])
        
        with tab1:
            st.markdown("### Log in to your account")
            login_username = st.text_input("Username", key="login_username")
            login_password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("🔓 Login", type="primary", use_container_width=True):
                if login_username and login_password:
                    success, user_id = verify_user(login_username, login_password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.current_user_id = user_id
                        st.success("✅ Authentication successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
                else:
                    st.warning("Please enter both username and password")
                    
        with tab2:
            st.markdown("### Create a new account")
            reg_username = st.text_input("New Username", key="reg_username")
            reg_password = st.text_input("New Password", type="password", key="reg_password")
            reg_password_confirm = st.text_input("Confirm Password", type="password", key="reg_password_confirm")
            
            if st.button("📝 Register Account", type="primary", use_container_width=True):
                if not reg_username or not reg_password:
                    st.warning("Please fill out all fields")
                elif reg_password != reg_password_confirm:
                    st.error("Passwords do not match")
                elif len(reg_password) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    success, message = create_user(reg_username, reg_password)
                    if success:
                        st.success("✅ Account created successfully! You can now log in.")
                    else:
                        st.error(f"❌ Error: {message}")
