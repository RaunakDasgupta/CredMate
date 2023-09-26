from rest_framework import status, generics
from rest_framework.response import Response
from datetime import timedelta
from rest_framework.decorators import api_view
from user.models import User, CreditScore
from .models import LoanApplication, EMI
from .serializers import LoanSerializer, EMISerializer


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
