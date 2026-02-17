"""
Custom CSS Styles
"""

import streamlit as st


def apply_custom_styles():
    """Apply custom CSS styling to the app"""
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1f2937;
            margin-bottom: 1rem;
        }
        .metric-card {
            background-color: #f9fafb;
            padding: 1.5rem;
            border-radius: 0.5rem;
            border: 1px solid #e5e7eb;
        }
        .success-box {
            background-color: #d1fae5;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #10b981;
            margin: 1rem 0;
        }
        .warning-box {
            background-color: #fef3c7;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #f59e0b;
            margin: 1rem 0;
        }
        .info-box {
            background-color: #dbeafe;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #3b82f6;
            margin: 1rem 0;
        }
        .stButton>button {
            width: 100%;
            border-radius: 0.5rem;
            height: 3rem;
            font-weight: 600;
        }
    </style>
    """, unsafe_allow_html=True)
