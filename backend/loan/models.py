from django.db import models
from user.models import User
from .utils import calculate_emi, calculate_emi_due_dates, calculate_total_amount_payable
from django.db import models


class LoanApplication(models.Model):
    LOAN_TYPES = (
        ('Home', 'Home'),
        ('Car', 'Car'),
        ('Personal', 'Personal'),
        ('Education', 'Education'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=10, choices=LOAN_TYPES)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_period = models.PositiveIntegerField()
    emi_disbursed_date = models.DateField(auto_now=True)

    @property
    def emi(self):
        return calculate_emi(self.loan_amount, self.interest_rate, self.term_period)

    @property
    def emi_due_dates(self):
        return calculate_emi_due_dates(self.emi_disbursed_date, self.term_period)

    @property
    def total_payable(self):
        return calculate_total_amount_payable(self.loan_amount, self.interest_rate, self.term_period)

    @property
    def amount_due(self):
        queryset = self.loan.all()
        amounts_paid = queryset.values_list('amount_paid', flat=True)
        total_amount_paid = sum(amounts_paid)  
        return round(float(self.total_payable)-float(total_amount_paid), 2)

    @property
    def tenure_left(self):
        return self.term_period-len(self.loan.all())

    @property
    def emi_amount(self):
        return round(calculate_emi(self.interest_rate, self.principal_due, self.tenure_left), 2)

    @property
    def principal_due(self):
        queryset = self.loan.all()
        amounts_paid = queryset.values_list('amount_paid', flat=True)
        total_emi_paid = sum(amounts_paid)
        months_paid = len(queryset)
        monthly_interest = (self.interest_rate/100)/12
        total_interest_paid = months_paid*monthly_interest

        principal_due = self.loan_amount-(total_emi_paid-(total_interest_paid))

        return round(principal_due, 2)

    @property
    def interest_due(self):
        queryset = self.loan.all()
        months_paid = len(queryset)
        monthly_interest = (self.interest_rate/100)/12
        total_interest_paid = months_paid*monthly_interest

        interest_due = float(self.total_payable) - \
            float(self.loan_amount)-float(total_interest_paid)

        return round(interest_due, 2)
    
    def __str__(self):
        return f"{self.user.name}'s {self.get_loan_type_display()} Loan Application"


class EMI(models.Model):
    loan = models.ForeignKey(
        'LoanApplication', related_name='loan', on_delete=models.CASCADE)
    emi_date = models.DateField()
    amount_paid = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)

    def get_interest(self):
        return self.loan.interest_rate
