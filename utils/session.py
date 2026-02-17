"""
Session Management
Initialize and manage session state
"""

import streamlit as st


def initialize_session_state():
    """Initialize all session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'time_entries' not in st.session_state:
        st.session_state.time_entries = []
    
    if 'clocked_in' not in st.session_state:
        st.session_state.clocked_in = False
    
    if 'clock_in_time' not in st.session_state:
        st.session_state.clock_in_time = None
    
    if 'settings' not in st.session_state:
        st.session_state.settings = {
            'hourly_rate': 25.00,
            'overtime_threshold': 40.0,
            'overtime_multiplier': 1.5,
            'health_insurance_employee': 150.00,
            'health_insurance_employer': 300.00,
            'dental_insurance': 25.00,
            'vision_insurance': 15.00,
            'retirement_401k_type': 'percentage',  # 'fixed' or 'percentage'
            'retirement_401k_amount': 5.0,  # percentage or fixed amount
            'biometric_enabled': True,
            'two_factor_enabled': False
        }
