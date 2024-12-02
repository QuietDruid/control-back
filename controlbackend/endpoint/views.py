from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework import serializers
from .serializers import UserSignupSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError

from .serializers import VirtualMachineClassSerializer
from .models import VirtualMachineClass

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_classes(request):
    classes = VirtualMachineClass.objects.all()
    serializer = VirtualMachineClassSerializer(classes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def index(request):
    """API root endpoint"""
    return Response({
        "message": "Welcome to the Virtual Machine Class API!",
        "endpoints": {
            "POST /api/classes/": "Create a new virtual machine class.",
            "GET /api/classes/list": "Retrieve all virtual machine classes.",
        }
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_class(request):
    serializer = VirtualMachineClassSerializer(data=request.data)
    if serializer.is_valid():
        # Associate the class with the authenticated user
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def signup_view(request):
#     serializer = UserSignupSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save()
#         return Response({
#             'message': 'User created successfully',
#             'username': user.username,
#             'email': user.email
#         }, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """
    User registration endpoint
    """
    try:
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        # Validate input
        if not username or not email or not password:
            raise ValidationError({
                'error': 'Username, email, and password are required'
            })

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            raise ValidationError({
                'username': 'Username is already taken'
            })

        if User.objects.filter(email=email).exists():
            raise ValidationError({
                'email': 'Email is already registered'
            })
        if password != confirm_password:
            raise ValidationError({
                'password': 'Passwords do not match'
            })

        # Create user
        user = User.objects.create_user(
            username=username, 
            email=email, 
            password=password
        )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'token': {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        }, status=status.HTTP_201_CREATED)

    except ValidationError as e:
        return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': 'An unexpected error occurred'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    User login endpoint
    """
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        # Find user by email
        user = User.objects.get(email=email)
        
        # Check password
        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'user_id': user.id,
                'email': user.email,
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
            })
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    except User.DoesNotExist:
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([AllowAny])
def test(request):
    return Response({"message": "This is a test endpoint."})