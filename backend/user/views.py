from rest_framework.response import Response
from django.shortcuts import render
from .models import User
from .serializers import UserSerializer
from rest_framework import generics, status
from .tasks import calculate_credit_score
class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer= self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            calculate_credit_score.delay(serializer.data['aadhar_id'])
            return Response({'id':serializer.data.get('aadhar_id')}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


register_user_api_view = UserRegisterAPIView.as_view()