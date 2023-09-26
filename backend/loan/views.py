from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.response import Response
from datetime import timedelta
from rest_framework.decorators import api_view
from user.models import User, CreditScore
from .models import LoanApplication, EMI
from .serializers import ListEmiSerializer, LoanSerializer, EMISerializer, PayEMISerializer


class LoanApplicationAPIView(generics.CreateAPIView):
    queryset = LoanApplication.objects.all()
    serializer_class = LoanSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            res = serializer.save()
            current_date = res.emi_disbursed_date
            loan_id = res.id
            loan_due_dates = []
            amount_due = round(res.emi, 2)
            for i in range(int(res.term_period)):
                due_date = (current_date+timedelta(days=32)).replace(day=1)
                loan_due_dates.append(
                    {'date': due_date, 'amount_due': amount_due})
                current_date = due_date

            return Response({
                'loan_id': loan_id,
                'loan_due_dates': loan_due_dates
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


loan_application_api_view = LoanApplicationAPIView.as_view()

class PayEMIApiView(generics.CreateAPIView):
    serializer_class = PayEMISerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        
emi_payment_api_view = PayEMIApiView.as_view()

class EMIRetrieveApiView(generics.ListAPIView):
    serializer_class = ListEmiSerializer

    def list(self, request, *args, **kwargs):

        loan_id = self.kwargs['loan_id']

        # IF loan exists then return the list of EMIs
        # else return an error message
        loan = get_object_or_404(LoanApplication, id=loan_id)

        # Get past paid EMI list
        past_emi_list = EMI.objects.filter(loan_id=loan_id)
        past_dues = self.get_serializer(past_emi_list, many=True)

        # Create the list of upcoming dues
        upcoming_dues = []
        tenure_left = loan.tenure_left

        last_emi_paid = EMI.objects.filter(loan_id=loan_id).last().emi_date
        current_date = last_emi_paid

        for i in range(tenure_left):
            next_emi_date = (current_date+timedelta(days=32)).replace(day=1)
            emi_amount = loan.emi_amount
            upcoming_dues.append(
                {"date": next_emi_date, "amount_due": round(emi_amount, 2)})
            current_date = next_emi_date

        return Response({"past_transactions": past_dues.data, "upcoming_emi_list": upcoming_dues}, status=status.HTTP_200_OK)

emi_retrieve_api_view = EMIRetrieveApiView.as_view()
