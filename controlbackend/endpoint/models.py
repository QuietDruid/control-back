from django.db import models

class VirtualMachineClass(models.Model):
    created_by = models.ForeignKey(
        'auth.User',
        related_name='vm_classes',
        on_delete=models.CASCADE
    )
    class_name = models.CharField(max_length=255)
    ubuntu_version = models.CharField(max_length=10)
    vm_type = models.CharField(max_length=10)  # m1, m2, m3, m4
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.class_name} - Ubuntu {self.ubuntu_version}"

class Student(models.Model):
    vm_class = models.ForeignKey(VirtualMachineClass, related_name='students', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} ({self.email})"

# Create your models here.
