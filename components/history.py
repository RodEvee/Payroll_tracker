"""
History Component
View and export time entry history
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta, date
from services.database import get_user_entries


def show_history():
    """Show time entry history"""
    st.markdown('<h1 class="main-header">📅 History & Reports</h1>', unsafe_allow_html=True)
    
    user_id = st.session_state.current_user_id
    all_entries = get_user_entries(user_id)
    
    if len(all_entries) == 0:
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
            pass # Rerun happens automatically
    
    # Filter entries
    filtered_entries = [
        entry for entry in all_entries
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
