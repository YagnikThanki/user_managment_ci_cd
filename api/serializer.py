from rest_framework import serializers
from .models import CustomUser
# from django.contrib.auth.models import User       
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
# User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField(write_only=True,required=True)
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50,min_length=8,write_only=True, required=True) 
    class Meta:
        model = CustomUser
        field = ['first_name','last_name','email','username','password']
    
    
    def validate(self,data):        
        username = data['username']
        try:
            user = CustomUser.objects.filter(username=username) 
        except:
            user = None
        if user:
            raise serializers.ValidationError('user is taken')    
        return data

    def create(self,validate_data):
        user = CustomUser.objects.create(first_name = validate_data['first_name'],last_name=validate_data['last_name'],
                                       email =validate_data['email'],username=validate_data['username'])   
        user.set_password(validate_data.get('password'))
        user.save()
        return user       
 
class loginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True,required=True)
    password = serializers.CharField(write_only=True, required=True) 

    class Meta:
        model = CustomUser
        field = ['email','password']


class passwordserializer(serializers.Serializer):
    password = serializers.CharField(max_length=50,min_length=8,write_only=True, required=True) 
    new_password = serializers.CharField(max_length=50,min_length=8,write_only=True, required=True) 
    conf_password = serializers.CharField(max_length=50,min_length=8,write_only=True, required=True) 

    class Meta:
        model = CustomUser
        field = ['password','new_password','conf_password']     
     
        
class send_otp_serializers(serializers.Serializer):
    email = serializers.EmailField(write_only=True,required=True)   
    
    class Meta:
        model = CustomUser
        field = ['email']         

class confirmation_otp_serializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True,required=True)
    otp = serializers.IntegerField()

    class Meta:
        model = CustomUser
        field = ['email','otp']

class forgot_password_serializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True,required=True)
    new_password = serializers.CharField(max_length=50,min_length=8,write_only=True, required=True)

    class Meta:
        model = CustomUser
        field = ['email','new_password']



        

   