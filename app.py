"""
Secure Pay & Benefits Tracker - Streamlit Version
Main application entry point
"""

import streamlit as st
from utils.session import initialize_session_state
from utils.styles import apply_custom_styles
from components.auth import show_authentication
from components.dashboard import show_dashboard
from components.history import show_history
from components.settings import show_settings


# Page configuration
st.set_page_config(
    page_title="Secure Pay & Benefits Tracker",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    """Main application"""
    # Initialize session and styles
    initialize_session_state()
    apply_custom_styles()
    
    if not st.session_state.authenticated:
        show_authentication()
    else:
        # Sidebar navigation
        with st.sidebar:
            st.markdown("### 💼 Payroll Tracker")
            st.markdown("---")
            
            page = st.radio(
                "Navigation",
                options=["Dashboard", "History", "Settings"],
                label_visibility="collapsed"
            )
            
            st.markdown("---")
            
            # Quick Stats
            st.markdown("### 📊 Quick Stats")
            total_entries = len(st.session_state.time_entries)
            total_hours = sum(entry['hours'] for entry in st.session_state.time_entries)
            
            st.metric("Total Entries", total_entries)
            st.metric("Total Hours", f"{total_hours:.1f} hrs")
            
            st.markdown("---")
            
            st.markdown("""
            <div style="font-size: 0.8rem; color: #6b7280;">
                <p><strong>v1.0.0</strong></p>
                <p>🔒 Data stored locally</p>
                <p>✅ Privacy-first design</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Main content
        if page == "Dashboard":
            show_dashboard()
        elif page == "History":
            show_history()
        elif page == "Settings":
            show_settings()


if __name__ == "__main__":
    main()
