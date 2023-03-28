from rest_framework.response import Response
from .serializer import RegisterSerializer,loginSerializer,passwordserializer,send_otp_serializers,confirmation_otp_serializer,forgot_password_serializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from .models import CustomUser
from rest_framework.decorators import api_view,authentication_classes,permission_classes
import traceback
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.core.mail import send_mail  
import random


class Registerview(APIView):
    """_summary_

    Args:
        APIView (_type_): _description_
    """
    def post(self,request):
        try:
            data = request.data
            serializer = RegisterSerializer(data=data)
            
            if not serializer.is_valid():
                return Response({
                    'data':serializer.errors,
                    'message':'something went wrong'
                },status = status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                    'data':{},
                    'message':'your account is created'
                },status = status.HTTP_201_CREATED)
        
        except Exception as e:   
            return Response({
                    'data':{
                        'error': str(e)
                    },
                    'message':'something went wrong'
                },status = status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request,*args,**kwargs):
    if request.method == "POST":
        try:
            data = request.data
            serializer = RegisterSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'data':serializer.errors,
                    'message':'something went wrong'
                },status = status.HTTP_400_BAD_REQUEST)

            serializer.save() 
            user =CustomUser.objects.get(username=serializer.validated_data['username'])  
            token_obj,_ = Token.objects.get_or_create(user=user)                                                                                                        
            return Response({
                'data':serializer.validated_data,
                'message':'your account is created',
                'token':str(token_obj)
                },status = status.HTTP_201_CREATED)
        except Exception as e:
            traceback.print_exc()
            return Response({
                    'data':{
                        'error': str(e)
                    },
                    'message':'something went wrong'
                },status = status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
def login_view(request,*args,**kwargs):
    if request.method == "POST":
        try:
            data = request.data
            serializer = loginSerializer(data=data)
            
            if serializer.is_valid():
                email1 = data['email'] 
                password1= data['password']  
                try:
                    user = CustomUser.objects.get(email=email1)
                    token,created = Token.objects.get_or_create(user=user)
                    if user:
                        return Response({
                                'data':serializer.validated_data,
                                'Token':token.key,                                  
                                'message':'login success',
                                },status = status.HTTP_201_CREATED)
                    else:
                        return Response({
                            'data':{},
                            'message':'login failed'
                            },status = status.HTTP_400_BAD_REQUEST)
                except:
                    return Response({
                            'data':{},
                            'message':'login failed'
                            },status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'data':serializer.errors,
                    'message':'something went wrong'
                    },status = status.HTTP_400_BAD_REQUEST)
    
        except Exception as e:
            traceback.print_exc()       
            return Response({       
                    'data':{
                        'error': str(e)
                    },
                    'message':'something went wrong'
                    },status = status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def logout_view(request,*args,**kwargs):
    if request.method == 'DELETE':
        try:
            request.user.auth_token.delete()
            return Response({       
                        'data':{},
                        'message':'user log_out success'
                        },status = status.HTTP_200_OK) 
        except Exception as e:
            traceback.print_exc()       
            return Response({       
                    'data':{
                        'error': str(e)
                    },
                    'message':'something went wrong'
                    },status = status.HTTP_400_BAD_REQUEST)

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def change_password(request,*args,**kwargs):
    if request.method == 'PATCH':
        try:
            data = request.data
            serializer = passwordserializer(data=data)
            if serializer.is_valid():
                password = data['password']
                email = request.user.email
                user = CustomUser.objects.get(email=email)
                if user:
                    if user.check_password(password):
                        if (data['new_password']) != (data['password']):
                            if (data['new_password']) == (data['conf_password']):
                                user.set_password(data['new_password'])
                                user.save()
                                return Response({       
                                            'data':{},
                                            'message':'successfully change password'
                                            },status = status.HTTP_200_OK) 
                            else:
                                return Response({       
                                'data':{},
                                'message':'The password and confirmation password do not match'
                                },status = status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({       
                                'data':{},
                                'message':'It Seems You Have Entered Same Password As Old Password!!!'
                                },status = status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({       
                    'data':{},
                    'message':'current password does not match' 
                    },status = status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'data':{},
                    'message':'current password does not match' 
                    },status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            traceback.print_exc()       
            return Response({       
                    'data':{
                        'error': str(e)
                    },
                    'message':'something went wrong'
                    },status = status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_otp(request,*args,**kwargs):
    if request.method == 'POST':
        data = request.data
        serializer = send_otp_serializers(data=data)
        if serializer.is_valid():
            try:
                user = CustomUser.objects.get(email=data['email'])
                otp_number = random.randint(100000,999999)
                email = data['email']
                subject = 'OTP for password reset'
                message = f'Your OTP for password reset is {otp_number}'
                from_email = 'nakaraniuttam8@gmail.com'
                recipient_list = [email]
                send_mail(subject, message, from_email, recipient_list)
                user.otp = f"{otp_number}"
                user.save()
                return Response({'message': 'OTP sent to email.'},status=status.HTTP_200_OK)
            except:
                return Response({'data':{},
                'message':'email is not valid' 
                },status = status.HTTP_400_BAD_REQUEST)   
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirmation_otp(request,*args,**kwargs):
    if request.method =='POST':
        try:
            data = request.data
            serializer = confirmation_otp_serializer(data=data)
            if serializer.is_valid():
                try:
                    user = CustomUser.objects.get(email=data['email'])
                    store_otp = user.otp
                    if str(store_otp) == str(data['otp']):
                        user.otp = None
                        user.save()
                        return Response({
                            "message": "OTP verified successfully",
                            "verified": True   
                        },status=status.HTTP_200_OK)
                    else:
                        return Response({
                            "message": "OTP verification failed",
                            "verified": False   
                        },status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response({
                        'message':'email is not valid' 
                        },status = status.HTTP_400_BAD_REQUEST)   
            else:
                return Response({
                    "data":serializer.errors    
                },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            traceback.print_exc()       
            return Response({       
                    'data':{
                        'error': str(e)
                    },
                    'message':'something went wrong'
                    },status = status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def forgot_password(request,*args,**kwargs):
    if request.method == 'POST':
        try:
            data = request.data
            serializers = forgot_password_serializer(data=data)
            if serializers.is_valid():
                try: 
                    user = CustomUser.objects.get(email=data['email'])
                    user.password = data['new_password']
                    user.save()
                    return Response({
                        'data':{},
                        'message':'Changed password successfully'
                    },status=status.HTTP_200_OK)
                except:
                    return Response({
                        'message':'email is not valid' 
                        },status = status.HTTP_400_BAD_REQUEST) 
            else:
                return Response({
                    'data':serializers.errors
                },status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            traceback.print_exc()
            return Response({
                'data':{
                'error':str(e)
                },
                'message':'something went wrong'
            },status=status.HTTP_400_BAD_REQUEST)



class registerlistAPIview(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer       
register_list_view = registerlistAPIview



