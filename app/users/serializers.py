from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')  
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5
        }} 


    def create(self,validate_data):
        """create new user"""
        return get_user_model().objects.create_user(**validate_data)
            

class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace=False)

    def validate(self, attrs):
        """validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request= self.context.get('request'),
        username=email,
        password=password)

        if not user:
            msg = 'unable to authenticate the user'
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user']= user
        return attrs