"""
Calculation Service
Handles all salary and benefits calculations
"""

from datetime import datetime, timedelta, date
from typing import Dict, List
import streamlit as st


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
