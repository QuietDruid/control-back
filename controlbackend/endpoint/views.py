from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
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
            "POST /create-class/": "Create a new virtual machine class.",
            "GET /get-classes/": "Retrieve all virtual machine classes.",
        }
    })
# Create your views here.
