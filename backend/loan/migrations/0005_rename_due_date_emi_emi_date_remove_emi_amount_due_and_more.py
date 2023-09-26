# Generated by Django 4.2.5 on 2023-09-26 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0004_alter_loanapplication_loan_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emi',
            old_name='due_date',
            new_name='emi_date',
        ),
        migrations.RemoveField(
            model_name='emi',
            name='amount_due',
        ),
        migrations.RemoveField(
            model_name='emi',
            name='emi_amount',
        ),
        migrations.RemoveField(
            model_name='emi',
            name='paid',
        ),
        migrations.AlterField(
            model_name='emi',
            name='loan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loan', to='loan.loanapplication'),
        ),
    ]
