"""
Dashboard Component
Main dashboard with time tracking and weekly summary
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from services.calc_service import CalcService


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
