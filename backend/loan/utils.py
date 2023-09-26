from datetime import datetime, timedelta

def calculate_monthly_income(annual_income):
    monthly_income= annual_income // 12
    return monthly_income

def calculate_emi(interest_rate, loan_amount, tenure):
    monthly_rate =(int(interest_rate) / 100) / 12

    emi= (int(loan_amount)* monthly_rate* ((1+monthly_rate)**int(tenure)))/(((1+monthly_rate)**int(tenure))-1)
    return emi

def calculate_total_interest_earned(emi, tenure, loan_amount):
    total_interest_earned=(emi*int(tenure))-int(loan_amount)
    return total_interest_earned

def calculate_total_amount_payable(emi, tenure):
    total_amount_payable=emi*int(tenure)
    return total_amount_payable

def calculate_emi_due_dates(emi_start_date, tenure):
    emi_due_dates=[]
    emi_due_dates.append(emi_start_date)
    for i in range(1, int(tenure)):
        emi_due_dates.append(emi_due_dates[i-1]+timedelta(days=30))
    return emi_due_dates