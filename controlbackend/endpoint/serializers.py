# serializers.py
from rest_framework import serializers
from .models import VirtualMachineClass, Student
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'email']  # Added id for clarity

class VirtualMachineClassSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)
    
    class Meta:
        model = VirtualMachineClass
        fields = ['id', 'class_name', 'ubuntu_version', 'vm_type', 'created_at', 'students']

    def create(self, validated_data):
        # Optional: Handle nested creation if needed
        students_data = self.context.get('view').request.data.get('students', [])
        vm_class = VirtualMachineClass.objects.create(**validated_data)
        
        for student_data in students_data:
            Student.objects.create(vm_class=vm_class, **student_data)
        
        return vm_class

class UserSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True}
        }

    def validate(self, attrs):
        # Check if passwords match
        if attrs['password'] != attrs.pop('confirm_password'):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        
        # Check if username already exists
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "A user with this username already exists."})
        
        # Check if email already exists
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})
        
        return attrs

    def create(self, validated_data):
        # Create user with the validated data
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user