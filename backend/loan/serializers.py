from  rest_framework import serializers
from .models import LoanApplication, EMI
from .utils import calculate_monthly_income, calculate_emi, calculate_total_interest_earned, calculate_total_amount_payable, calculate_emi_due_dates

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = '__all__'

        def validate(self, attrs):
            loan_amount = attrs.get('loan_amount')
            loan_type=attrs.get('loan_type')
            annual_income=attrs.get('user').annual_income  
            interest_rate=attrs.get('interest_rate')
            emi_start_date=attrs.get('emi_start_date')
            tenure=attrs.get('term_period')

            credit_score=None
            try:
                credit_score=attrs.get('user').credit_score
            except:
                raise serializers.ValidationError("Loan cannot be disbursed without a credit score")
            
            credit_score=credit_score.get_credit_score()

            if int(credit_score) < 450:
                raise serializers.ValidationError("Loan cannot be disbursed for credit score less than 450")
            if not loan_amount:
                raise serializers.ValidationError("Loan must have a loan amount")
            if loan_amount < 0:
                raise serializers.ValidationError("Loan amount must be positive")
            if not loan_type:
                raise serializers.ValidationError("Loan must have a loan type")
            if loan_type not in ['Car', 'Home', 'Education', 'Personal']:
                raise serializers.ValidationError("Loan type must be one of Car, Home, Education, Personal")
            if not interest_rate:
                raise serializers.ValidationError("Loan must have an interest rate")
            if interest_rate < 14:
                raise serializers.ValidationError("Interest rate must be higher than 14%")
            if not tenure:
                raise serializers.ValidationError("Loan must have a term period")
            if tenure < 1:
                raise serializers.ValidationError("Term period must be positive")
            if not emi_start_date:
                raise serializers.ValidationError("Loan must have an EMI start date")
            if annual_income < 150000:
                raise serializers.ValidationError("Annual income must be greater than 150000 to apply for a loan")
            
            if loan_type == 'Car' and loan_amount > 750000:
                raise serializers.ValidationError("Car loan amount cannot be greater than 750000")
            if loan_type == 'Home' and loan_amount > 8500000:
                raise serializers.ValidationError("Home loan amount cannot be greater than 8500000")
            if loan_type == 'Education' and loan_amount > 5000000:
                raise serializers.ValidationError("Education loan amount cannot be greater than 5000000")
            if loan_type == 'Personal' and loan_amount > 1000000:
                raise serializers.ValidationError("Personal loan amount cannot be greater than 1000000")

            monthly_income=calculate_monthly_income(annual_income)
            emi=calculate_emi(interest_rate, loan_amount, tenure)
            max_emi=monthly_income*0.6
            if emi > max_emi:
                raise serializers.ValidationError("EMI cannot be greater than 60% of monthly income")
            total_interest=calculate_total_interest_earned(emi, tenure, loan_amount)
            if total_interest<10000:
                raise serializers.ValidationError("Total interest earned must be greater than 10000")
            return attrs
        
        def create(self, validated_data):
            return super().create(validated_data)

class EMISerializer(serializers.ModelSerializer):
    class Meta:
        model = EMI
        fields = '__all__'