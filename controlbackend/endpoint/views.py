from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import VirtualMachineClassSerializer
from .models import VirtualMachineClass

@api_view(['POST'])
def create_class(request):
    serializer = VirtualMachineClassSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
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
