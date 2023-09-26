import os
import csv
import logging

from celery import Celery, shared_task

from django.conf import settings

from .models import User, CreditScore

logger = logging.getLogger(__name__)


@shared_task
def calculate_credit_score(uuid):
    try:
        csv_file_path = os.path.join(
            settings.BASE_DIR, 'transactions_data Backend.csv')
        max_credit_score = 900
        min_credit_score = 300

        max_amount_balance = 1000000
        min_amount_balance = 100000

        total_credit = 0
        total_debit = 0

        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if (row[0] == uuid):
                    if row[2] == 'CREDIT':
                        total_credit += int(row[3])
                    elif row[2] == 'DEBIT':
                        total_debit += int(row[3])
                    sum = abs(total_credit-total_debit)
                    if sum > max_amount_balance:
                        credit_score = max_credit_score
                    elif sum < min_amount_balance:
                        credit_score = min_credit_score
                    else:
                        new_credit = sum//15000
                        credit_score = new_credit*10 + min_credit_score
                    print(credit_score)
            current_user = User.objects.get(aadhar_id=uuid)
            credit_score_instance = CreditScore.objects.create(
                aadhar_id=current_user, credit_score=credit_score)
            credit_score_instance.save()
            logger.info(
                f"Credit score for given UUID {current_user} is {credit_score}")
            return credit_score
    except Exception as e:
        logger.error(e)
        logger.error("Error in processing CSV file")
        return None
