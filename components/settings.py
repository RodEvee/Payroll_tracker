"""
Settings Component
Configure compensation, benefits, and security settings
"""

import streamlit as st
from services.database import get_user_settings, update_user_settings


def show_settings():
    """Show settings page"""
    st.markdown('<h1 class="main-header">⚙️ Settings</h1>', unsafe_allow_html=True)
    
    user_id = st.session_state.current_user_id
    settings = get_user_settings(user_id)
    
    tab1, tab2, tab3 = st.tabs(["💰 Compensation", "🏥 Benefits", "🔒 Security"])
    
    with tab1:
        st.subheader("Compensation Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            hourly_rate = st.number_input(
                "Hourly Rate ($)",
                min_value=0.0,
                value=float(settings['hourly_rate']),
                step=0.50,
                format="%.2f"
            )
        
        with col2:
            overtime_threshold = st.number_input(
                "Overtime Threshold (hours/week)",
                min_value=0.0,
                value=float(settings['overtime_threshold']),
                step=1.0,
                format="%.1f"
            )
        
        overtime_multiplier = st.slider(
            "Overtime Multiplier",
            min_value=1.0,
            max_value=3.0,
            value=float(settings['overtime_multiplier']),
            step=0.1,
            format="%.1fx"
        )
        
        if st.button("💾 Save Compensation Settings", type="primary"):
            settings['hourly_rate'] = hourly_rate
            settings['overtime_threshold'] = overtime_threshold
            settings['overtime_multiplier'] = overtime_multiplier
            update_user_settings(user_id, settings)
            st.success("✅ Compensation settings saved!")
    
    with tab2:
        st.subheader("Benefits Settings")
        
        st.markdown("#### Health Insurance")
        col1, col2 = st.columns(2)
        
        with col1:
            health_employee = st.number_input(
                "Employee Contribution ($/week)",
                min_value=0.0,
                value=float(settings['health_insurance_employee']),
                step=5.0,
                format="%.2f"
            )
        
        with col2:
            health_employer = st.number_input(
                "Employer Contribution ($/week)",
                min_value=0.0,
                value=float(settings['health_insurance_employer']),
                step=5.0,
                format="%.2f"
            )
        
        st.markdown("#### Other Insurance")
        col1, col2 = st.columns(2)
        
        with col1:
            dental = st.number_input(
                "Dental Insurance ($/week)",
                min_value=0.0,
                value=float(settings['dental_insurance']),
                step=5.0,
                format="%.2f"
            )
        
        with col2:
            vision = st.number_input(
                "Vision Insurance ($/week)",
                min_value=0.0,
                value=float(settings['vision_insurance']),
                step=5.0,
                format="%.2f"
            )
        
        st.markdown("#### 401(k) Retirement")
        
        retirement_type = st.radio(
            "Contribution Type",
            options=['percentage', 'fixed'],
            format_func=lambda x: "Percentage of Gross Pay" if x == 'percentage' else "Fixed Amount",
            horizontal=True,
            index=0 if settings['retirement_401k_type'] == 'percentage' else 1
        )
        
        if retirement_type == 'percentage':
            retirement_amount = st.slider(
                "Contribution Percentage",
                min_value=0.0,
                max_value=100.0,
                value=float(settings['retirement_401k_amount']),
                step=0.5,
                format="%.1f%%"
            )
        else:
            retirement_amount = st.number_input(
                "Fixed Contribution ($/week)",
                min_value=0.0,
                value=float(settings['retirement_401k_amount']),
                step=5.0,
                format="%.2f"
            )
        
        if st.button("💾 Save Benefits Settings", type="primary"):
            settings['health_insurance_employee'] = health_employee
            settings['health_insurance_employer'] = health_employer
            settings['dental_insurance'] = dental
            settings['vision_insurance'] = vision
            settings['retirement_401k_type'] = retirement_type
            settings['retirement_401k_amount'] = retirement_amount
            update_user_settings(user_id, settings)
            st.success("✅ Benefits settings saved!")
    
    with tab3:
        st.subheader("Security Settings")
        
        biometric = st.checkbox(
            "🔐 Enable Biometric Authentication",
            value=bool(settings['biometric_enabled'])
        )
        
        st.markdown("---")
        
        st.markdown("#### Data Management")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.current_user_id = None
            st.rerun()
        
        if st.button("💾 Save Security Settings", type="primary"):
            settings['biometric_enabled'] = biometric
            update_user_settings(user_id, settings)
            st.success("✅ Security settings saved!")
