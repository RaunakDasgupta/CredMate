# Generated by Django 4.2.5 on 2023-09-20 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0003_alter_loanapplication_loan_type_delete_loantypes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanapplication',
            name='loan_type',
            field=models.CharField(choices=[('Home', 'Home'), ('Car', 'Car'), ('Personal', 'Personal'), ('Education', 'Education')], max_length=10),
        ),
    ]