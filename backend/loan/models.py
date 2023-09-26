from django.db import models
from user.models import User
from .utils import calculate_emi, calculate_emi_due_dates
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

class EMI(models.Model):
    loan = models.ForeignKey(LoanApplication, on_delete=models.CASCADE)
    due_date = models.DateField()
    emi_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2,default=0)

    def get_interest(self):
        return self.loan.interest_rate