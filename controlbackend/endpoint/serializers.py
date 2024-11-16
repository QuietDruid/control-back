from rest_framework import serializers
from .models import VirtualMachineClass, Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'email']

class VirtualMachineClassSerializer(serializers.ModelSerializer):
    roster = StudentSerializer(many=True, source='students')

    class Meta:
        model = VirtualMachineClass
        fields = ['id', 'class_name', 'ubuntu_version', 'vm_type', 'roster']

    def create(self, validated_data):
        students_data = validated_data.pop('students')
        vm_class = VirtualMachineClass.objects.create(**validated_data)
        
        for student_data in students_data:
            Student.objects.create(vm_class=vm_class, **student_data)
        
        return vm_class
