# serializers.py
from rest_framework import serializers
from .models import VirtualMachineClass, Student

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
