import pytest
from datetime import datetime, timedelta
from services.calc_service import CalcService

def test_calculate_hours():
    clock_in = datetime(2023, 10, 1, 9, 0)
    clock_out = datetime(2023, 10, 1, 17, 30)
    hours = CalcService.calculate_hours(clock_in, clock_out)
    assert hours == 8.5

def test_calculate_weekly_hours():
    entries = [
        {'hours': 8.0},
        {'hours': 8.0},
        {'hours': 10.0},
        {'hours': 10.0},
        {'hours': 8.0}
    ]
    # Total = 44 hours
    res = CalcService.calculate_weekly_hours(entries, overtime_threshold=40.0)
    assert res['total'] == 44.0
    assert res['regular'] == 40.0
    assert res['overtime'] == 4.0

def test_calculate_gross_pay():
    hours = {'regular': 40.0, 'overtime': 4.0, 'total': 44.0}
    res = CalcService.calculate_gross_pay(hours, hourly_rate=25.0, overtime_multiplier=1.5)
    
    assert res['regular'] == 1000.0  # 40 * 25
    assert res['overtime'] == 150.0  # 4 * 25 * 1.5
    assert res['total'] == 1150.0

def test_calculate_deductions():
    gross_pay = 1150.0
    settings = {
        'health_insurance_employee': 150.00,
        'dental_insurance': 25.00,
        'vision_insurance': 15.00,
        'retirement_401k_type': 'percentage',
        'retirement_401k_amount': 5.0
    }
    
    res = CalcService.calculate_deductions(gross_pay, settings)
    
    # 401k = 1150 * 0.05 = 57.5
    assert res['retirement_401k'] == 57.5
    # taxes: fed (15%)=172.5, state (5%)=57.5, SS (6.2%)=71.3, Med (1.45%)=16.68
    assert res['federal_tax'] == 172.5
    assert res['state_tax'] == 57.5
    assert res['social_security'] == 71.3
    assert res['medicare'] == 16.68
    
    # total deductions = 150 + 25 + 15 + 57.5 + 172.5 + 57.5 + 71.3 + 16.68
    assert res['total'] == 565.47

def test_calculate_net_pay():
    net = CalcService.calculate_net_pay(1150.0, 565.47)
    assert net == 584.53
