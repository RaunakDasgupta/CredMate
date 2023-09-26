from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'annual_income', 'aadhar_id'] 

    def validate(self, attrs):
        email = attrs.get('email')
        name = attrs.get('name')
        annual_income = attrs.get('annual_income')
        aadhar_id = attrs.get('aadhar_id')
        if not email:
            raise serializers.ValidationError("User must have an email address")
        if not name:
            raise serializers.ValidationError("User must have a name")
        if not annual_income:
            raise serializers.ValidationError("User must have an annual income")
        if not aadhar_id:
            raise serializers.ValidationError("User must have an aadhar id")
        return attrs
    
    def create(self, validated_data):
        return super().create(validated_data)