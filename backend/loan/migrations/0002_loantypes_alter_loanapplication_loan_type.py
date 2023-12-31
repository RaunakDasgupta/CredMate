# Generated by Django 4.2.5 on 2023-09-20 06:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_type', models.IntegerField(choices=[(1, 'Car'), (2, 'Home'), (3, 'Education'), (4, 'Personal')])),
            ],
        ),
        migrations.AlterField(
            model_name='loanapplication',
            name='loan_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loan.loantypes'),
        ),
    ]
