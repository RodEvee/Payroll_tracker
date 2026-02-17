"""
Authentication Component
Handles user authentication
"""

import streamlit as st


def show_authentication():
    """Show biometric authentication simulation"""
    st.markdown('<h1 class="main-header">🔐 Secure Authentication</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h3>Biometric Authentication Simulation</h3>
            <p>This is a demo application. In production, this would use actual biometric authentication.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.image("https://via.placeholder.com/300x300/3b82f6/ffffff?text=Face+Recognition", 
                 caption="Biometric Simulation", use_container_width=True)
        
        st.markdown("---")
        
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("🔓 Login", type="primary", use_container_width=True):
                if username and password:
                    st.session_state.authenticated = True
                    st.success("✅ Authentication successful!")
                    st.rerun()
                else:
                    st.error("❌ Please enter both username and password")
        
        with col_btn2:
            if st.button("📷 Biometric Login", use_container_width=True):
                st.session_state.authenticated = True
                st.success("✅ Biometric authentication successful!")
                st.rerun()
