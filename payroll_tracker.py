import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta, date
from typing import Dict, List, Optional
import hashlib
import base64

# Page configuration
st.set_page_config(
    page_title="Secure Pay & Benefits Tracker",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
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


# Initialize session state
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


# Calculation Service
class CalcService:
    """Handles all salary and benefits calculations"""
    
    @staticmethod
    def calculate_hours(clock_in: datetime, clock_out: datetime) -> float:
        """Calculate hours worked"""
        delta = clock_out - clock_in
        return round(delta.total_seconds() / 3600, 2)
    
    @staticmethod
    def calculate_weekly_hours(entries: List[Dict]) -> Dict:
        """Calculate weekly hours breakdown"""
        total_hours = sum(entry['hours'] for entry in entries)
        overtime_threshold = st.session_state.settings['overtime_threshold']
        
        regular_hours = min(total_hours, overtime_threshold)
        overtime_hours = max(0, total_hours - overtime_threshold)
        
        return {
            'total': round(total_hours, 2),
            'regular': round(regular_hours, 2),
            'overtime': round(overtime_hours, 2)
        }
    
    @staticmethod
    def calculate_gross_pay(hours: Dict) -> Dict:
        """Calculate gross pay breakdown"""
        settings = st.session_state.settings
        hourly_rate = settings['hourly_rate']
        overtime_multiplier = settings['overtime_multiplier']
        
        regular_pay = hours['regular'] * hourly_rate
        overtime_pay = hours['overtime'] * hourly_rate * overtime_multiplier
        total_gross = regular_pay + overtime_pay
        
        return {
            'regular': round(regular_pay, 2),
            'overtime': round(overtime_pay, 2),
            'total': round(total_gross, 2)
        }
    
    @staticmethod
    def calculate_deductions() -> Dict:
        """Calculate all deductions"""
        settings = st.session_state.settings
        
        # Get gross pay for the week
        weekly_entries = CalcService.get_current_week_entries()
        hours = CalcService.calculate_weekly_hours(weekly_entries)
        gross_pay = CalcService.calculate_gross_pay(hours)
        
        # Health insurance
        health_insurance = settings['health_insurance_employee']
        
        # Dental insurance
        dental_insurance = settings['dental_insurance']
        
        # Vision insurance
        vision_insurance = settings['vision_insurance']
        
        # 401(k) contribution
        if settings['retirement_401k_type'] == 'percentage':
            retirement_401k = gross_pay['total'] * (settings['retirement_401k_amount'] / 100)
        else:
            retirement_401k = settings['retirement_401k_amount']
        
        # Federal tax (simplified - 15% for demo)
        federal_tax = gross_pay['total'] * 0.15
        
        # State tax (simplified - 5% for demo)
        state_tax = gross_pay['total'] * 0.05
        
        # Social Security (6.2%)
        social_security = gross_pay['total'] * 0.062
        
        # Medicare (1.45%)
        medicare = gross_pay['total'] * 0.0145
        
        total_deductions = (
            health_insurance + dental_insurance + vision_insurance +
            retirement_401k + federal_tax + state_tax +
            social_security + medicare
        )
        
        return {
            'health_insurance': round(health_insurance, 2),
            'dental_insurance': round(dental_insurance, 2),
            'vision_insurance': round(vision_insurance, 2),
            'retirement_401k': round(retirement_401k, 2),
            'federal_tax': round(federal_tax, 2),
            'state_tax': round(state_tax, 2),
            'social_security': round(social_security, 2),
            'medicare': round(medicare, 2),
            'total': round(total_deductions, 2)
        }
    
    @staticmethod
    def calculate_net_pay() -> float:
        """Calculate net pay"""
        weekly_entries = CalcService.get_current_week_entries()
        hours = CalcService.calculate_weekly_hours(weekly_entries)
        gross_pay = CalcService.calculate_gross_pay(hours)
        deductions = CalcService.calculate_deductions()
        
        return round(gross_pay['total'] - deductions['total'], 2)
    
    @staticmethod
    def get_current_week_entries() -> List[Dict]:
        """Get entries for current week (Monday to Sunday)"""
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=6)  # Sunday
        
        weekly_entries = []
        for entry in st.session_state.time_entries:
            entry_date = datetime.fromisoformat(entry['clock_in']).date()
            if start_of_week <= entry_date <= end_of_week:
                weekly_entries.append(entry)
        
        return weekly_entries


# Authentication Component
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


# Dashboard Component
def show_dashboard():
    """Show main dashboard"""
    st.markdown('<h1 class="main-header">💼 Dashboard</h1>', unsafe_allow_html=True)
    
    # Clock In/Out Section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("⏱️ Time Tracking")
        
        if not st.session_state.clocked_in:
            if st.button("🟢 Clock In", type="primary", use_container_width=True):
                st.session_state.clocked_in = True
                st.session_state.clock_in_time = datetime.now()
                st.success(f"✅ Clocked in at {st.session_state.clock_in_time.strftime('%I:%M %p')}")
                st.rerun()
        else:
            st.markdown(f"""
            <div class="success-box">
                <h4>⏰ Currently Clocked In</h4>
                <p><strong>Started:</strong> {st.session_state.clock_in_time.strftime('%I:%M %p')}</p>
                <p><strong>Elapsed:</strong> {str(datetime.now() - st.session_state.clock_in_time).split('.')[0]}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🔴 Clock Out", type="secondary", use_container_width=True):
                clock_out_time = datetime.now()
                hours_worked = CalcService.calculate_hours(st.session_state.clock_in_time, clock_out_time)
                
                # Add entry
                entry = {
                    'id': len(st.session_state.time_entries) + 1,
                    'clock_in': st.session_state.clock_in_time.isoformat(),
                    'clock_out': clock_out_time.isoformat(),
                    'hours': hours_worked,
                    'date': st.session_state.clock_in_time.date().isoformat()
                }
                st.session_state.time_entries.append(entry)
                
                # Reset clock state
                st.session_state.clocked_in = False
                st.session_state.clock_in_time = None
                
                st.success(f"✅ Clocked out! Worked {hours_worked} hours")
                st.rerun()
    
    with col2:
        st.subheader("📅 Current Week")
        weekly_entries = CalcService.get_current_week_entries()
        hours = CalcService.calculate_weekly_hours(weekly_entries)
        
        st.metric("Total Hours", f"{hours['total']} hrs")
        st.metric("Regular Hours", f"{hours['regular']} hrs")
        st.metric("Overtime Hours", f"{hours['overtime']} hrs")
    
    st.markdown("---")
    
    # Weekly Summary
    st.subheader("📊 Weekly Pay Summary")
    
    weekly_entries = CalcService.get_current_week_entries()
    
    if len(weekly_entries) > 0:
        hours = CalcService.calculate_weekly_hours(weekly_entries)
        gross_pay = CalcService.calculate_gross_pay(hours)
        deductions = CalcService.calculate_deductions()
        net_pay = CalcService.calculate_net_pay()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 💵 Gross Pay")
            st.metric("Regular Pay", f"${gross_pay['regular']:,.2f}")
            st.metric("Overtime Pay", f"${gross_pay['overtime']:,.2f}")
            st.metric("Total Gross", f"${gross_pay['total']:,.2f}", delta=None)
        
        with col2:
            st.markdown("### 📉 Deductions")
            st.metric("Health Insurance", f"${deductions['health_insurance']:,.2f}")
            st.metric("Dental Insurance", f"${deductions['dental_insurance']:,.2f}")
            st.metric("Vision Insurance", f"${deductions['vision_insurance']:,.2f}")
            st.metric("401(k)", f"${deductions['retirement_401k']:,.2f}")
            st.metric("Federal Tax", f"${deductions['federal_tax']:,.2f}")
            st.metric("State Tax", f"${deductions['state_tax']:,.2f}")
            st.metric("Social Security", f"${deductions['social_security']:,.2f}")
            st.metric("Medicare", f"${deductions['medicare']:,.2f}")
            st.metric("Total Deductions", f"${deductions['total']:,.2f}")
        
        with col3:
            st.markdown("### 💰 Net Pay")
            st.markdown(f"""
            <div style="background-color: #10b981; color: white; padding: 2rem; border-radius: 0.5rem; text-align: center;">
                <h2 style="margin: 0; font-size: 3rem;">${net_pay:,.2f}</h2>
                <p style="margin: 0.5rem 0 0 0;">Take Home Pay</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            st.metric("Hours Worked", f"{hours['total']} hrs")
            st.metric("Effective Rate", f"${(net_pay / hours['total'] if hours['total'] > 0 else 0):,.2f}/hr")
    else:
        st.info("📝 No time entries for this week yet. Clock in to start tracking!")
    
    st.markdown("---")
    
    # Recent Entries
    st.subheader("🕐 Recent Entries")
    if len(weekly_entries) > 0:
        df = pd.DataFrame(weekly_entries)
        df['clock_in'] = pd.to_datetime(df['clock_in']).dt.strftime('%Y-%m-%d %I:%M %p')
        df['clock_out'] = pd.to_datetime(df['clock_out']).dt.strftime('%Y-%m-%d %I:%M %p')
        df = df[['date', 'clock_in', 'clock_out', 'hours']]
        df.columns = ['Date', 'Clock In', 'Clock Out', 'Hours']
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No entries yet")


# History Component
def show_history():
    """Show time entry history"""
    st.markdown('<h1 class="main-header">📅 History & Reports</h1>', unsafe_allow_html=True)
    
    if len(st.session_state.time_entries) == 0:
        st.info("📝 No time entries yet. Start tracking time from the Dashboard!")
        return
    
    # Date range filter
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        start_date = st.date_input("Start Date", 
                                   value=date.today() - timedelta(days=30),
                                   max_value=date.today())
    
    with col2:
        end_date = st.date_input("End Date", 
                                 value=date.today(),
                                 max_value=date.today())
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔍 Filter", use_container_width=True):
            st.rerun()
    
    # Filter entries
    filtered_entries = [
        entry for entry in st.session_state.time_entries
        if start_date <= datetime.fromisoformat(entry['clock_in']).date() <= end_date
    ]
    
    if len(filtered_entries) == 0:
        st.warning("No entries found for the selected date range")
        return
    
    # Summary Statistics
    st.subheader("📊 Summary Statistics")
    
    total_hours = sum(entry['hours'] for entry in filtered_entries)
    total_days = len(set(entry['date'] for entry in filtered_entries))
    avg_hours_per_day = total_hours / total_days if total_days > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Entries", len(filtered_entries))
    
    with col2:
        st.metric("Total Hours", f"{total_hours:.2f} hrs")
    
    with col3:
        st.metric("Days Worked", total_days)
    
    with col4:
        st.metric("Avg Hours/Day", f"{avg_hours_per_day:.2f} hrs")
    
    st.markdown("---")
    
    # Entries Table
    st.subheader("📋 Time Entries")
    
    df = pd.DataFrame(filtered_entries)
    df['clock_in_dt'] = pd.to_datetime(df['clock_in'])
    df['clock_out_dt'] = pd.to_datetime(df['clock_out'])
    
    display_df = df.copy()
    display_df['Date'] = display_df['clock_in_dt'].dt.strftime('%Y-%m-%d')
    display_df['Clock In'] = display_df['clock_in_dt'].dt.strftime('%I:%M %p')
    display_df['Clock Out'] = display_df['clock_out_dt'].dt.strftime('%I:%M %p')
    display_df['Hours'] = display_df['hours']
    
    display_df = display_df[['Date', 'Clock In', 'Clock Out', 'Hours']]
    display_df = display_df.sort_values('Date', ascending=False)
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Export Options
    st.markdown("---")
    st.subheader("📤 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv_data = display_df.to_csv(index=False)
        st.download_button(
            label="📊 Download CSV",
            data=csv_data,
            file_name=f"time_entries_{start_date}_{end_date}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        json_data = json.dumps(filtered_entries, indent=2)
        st.download_button(
            label="📄 Download JSON",
            data=json_data,
            file_name=f"time_entries_{start_date}_{end_date}.json",
            mime="application/json",
            use_container_width=True
        )


# Settings Component
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


# Main App
def main():
    """Main application"""
    initialize_session_state()
    
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
