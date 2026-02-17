"""
Settings Component
Configure compensation, benefits, and security settings
"""

import streamlit as st


def show_settings():
    """Show settings page"""
    st.markdown('<h1 class="main-header">⚙️ Settings</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["💰 Compensation", "🏥 Benefits", "🔒 Security"])
    
    with tab1:
        st.subheader("Compensation Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            hourly_rate = st.number_input(
                "Hourly Rate ($)",
                min_value=0.0,
                value=st.session_state.settings['hourly_rate'],
                step=0.50,
                format="%.2f"
            )
        
        with col2:
            overtime_threshold = st.number_input(
                "Overtime Threshold (hours/week)",
                min_value=0.0,
                value=st.session_state.settings['overtime_threshold'],
                step=1.0,
                format="%.1f"
            )
        
        overtime_multiplier = st.slider(
            "Overtime Multiplier",
            min_value=1.0,
            max_value=3.0,
            value=st.session_state.settings['overtime_multiplier'],
            step=0.1,
            format="%.1fx"
        )
        
        if st.button("💾 Save Compensation Settings", type="primary"):
            st.session_state.settings['hourly_rate'] = hourly_rate
            st.session_state.settings['overtime_threshold'] = overtime_threshold
            st.session_state.settings['overtime_multiplier'] = overtime_multiplier
            st.success("✅ Compensation settings saved!")
    
    with tab2:
        st.subheader("Benefits Settings")
        
        st.markdown("#### Health Insurance")
        col1, col2 = st.columns(2)
        
        with col1:
            health_employee = st.number_input(
                "Employee Contribution ($/week)",
                min_value=0.0,
                value=st.session_state.settings['health_insurance_employee'],
                step=5.0,
                format="%.2f"
            )
        
        with col2:
            health_employer = st.number_input(
                "Employer Contribution ($/week)",
                min_value=0.0,
                value=st.session_state.settings['health_insurance_employer'],
                step=5.0,
                format="%.2f"
            )
        
        st.markdown("#### Other Insurance")
        col1, col2 = st.columns(2)
        
        with col1:
            dental = st.number_input(
                "Dental Insurance ($/week)",
                min_value=0.0,
                value=st.session_state.settings['dental_insurance'],
                step=5.0,
                format="%.2f"
            )
        
        with col2:
            vision = st.number_input(
                "Vision Insurance ($/week)",
                min_value=0.0,
                value=st.session_state.settings['vision_insurance'],
                step=5.0,
                format="%.2f"
            )
        
        st.markdown("#### 401(k) Retirement")
        
        retirement_type = st.radio(
            "Contribution Type",
            options=['percentage', 'fixed'],
            format_func=lambda x: "Percentage of Gross Pay" if x == 'percentage' else "Fixed Amount",
            horizontal=True,
            index=0 if st.session_state.settings['retirement_401k_type'] == 'percentage' else 1
        )
        
        if retirement_type == 'percentage':
            retirement_amount = st.slider(
                "Contribution Percentage",
                min_value=0.0,
                max_value=100.0,
                value=st.session_state.settings['retirement_401k_amount'],
                step=0.5,
                format="%.1f%%"
            )
        else:
            retirement_amount = st.number_input(
                "Fixed Contribution ($/week)",
                min_value=0.0,
                value=st.session_state.settings['retirement_401k_amount'],
                step=5.0,
                format="%.2f"
            )
        
        if st.button("💾 Save Benefits Settings", type="primary"):
            st.session_state.settings['health_insurance_employee'] = health_employee
            st.session_state.settings['health_insurance_employer'] = health_employer
            st.session_state.settings['dental_insurance'] = dental
            st.session_state.settings['vision_insurance'] = vision
            st.session_state.settings['retirement_401k_type'] = retirement_type
            st.session_state.settings['retirement_401k_amount'] = retirement_amount
            st.success("✅ Benefits settings saved!")
    
    with tab3:
        st.subheader("Security Settings")
        
        biometric = st.checkbox(
            "🔐 Enable Biometric Authentication",
            value=st.session_state.settings['biometric_enabled']
        )
        
        two_factor = st.checkbox(
            "📱 Enable Two-Factor Authentication",
            value=st.session_state.settings['two_factor_enabled']
        )
        
        st.markdown("---")
        
        st.markdown("#### Data Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Clear All Data", type="secondary", use_container_width=True):
                if st.session_state.get('confirm_clear', False):
                    st.session_state.time_entries = []
                    st.session_state.confirm_clear = False
                    st.success("✅ All data cleared!")
                    st.rerun()
                else:
                    st.session_state.confirm_clear = True
                    st.warning("⚠️ Click again to confirm deletion")
        
        with col2:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.rerun()
        
        if st.button("💾 Save Security Settings", type="primary"):
            st.session_state.settings['biometric_enabled'] = biometric
            st.session_state.settings['two_factor_enabled'] = two_factor
            st.success("✅ Security settings saved!")
