# Generated by Django 4.2.5 on 2023-09-20 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0002_loantypes_alter_loanapplication_loan_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanapplication',
            name='loan_type',
            field=models.CharField(choices=[('HOME', 'Home Loan'), ('CAR', 'Car Loan'), ('PERSONAL', 'Personal Loan'), ('EDUCATION', 'Education Loan')], max_length=10),
        ),
        migrations.DeleteModel(
            name='LoanTypes',
        ),
    ]
