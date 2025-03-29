from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone


class CustomUser(AbstractUser):
    employee_id = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username

class Employee(models.Model):
    employee_id = models.CharField(max_length=20, unique=True) 
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    joined_date = models.DateField()

    def __str__(self):
        return f"{self.employee_id} - {self.name}"


class Visa(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    visa_type = models.CharField(max_length=100)
    issue_date = models.DateField() 
    expiry_date = models.DateField()
    visa_issue_country = models.CharField(max_length=100)
    passport_country = models.CharField(max_length=100) 

    def __str__(self):
        return f"{self.visa_type} - {self.employee.name}"
    

class EmployeeDocument(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="documents")
    document_name = models.CharField(max_length=255)
    uploaded_file = models.FileField(upload_to="")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_name} - {self.employee.name}"
    
    


class Notification(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message
 