"""
Session Management
Initialize and manage session state
"""

import streamlit as st


def initialize_session_state():
    """Initialize all session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        
    if 'current_user_id' not in st.session_state:
        st.session_state.current_user_id = None
    
    if 'clocked_in' not in st.session_state:
        st.session_state.clocked_in = False
    
    if 'clock_in_time' not in st.session_state:
        st.session_state.clock_in_time = None
