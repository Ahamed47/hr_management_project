from django import forms
from .models import Employee, Visa, EmployeeDocument
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()

class HRRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        if not user.employee_id:
            user.employee_id = f"HR{User.objects.count() + 1}"  # Ensure employee_id is unique
        if commit:
            user.save()
        return user


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_id','name', 'department', 'designation', 'joined_date']
        

class VisaForm(forms.ModelForm):
    class Meta:
        model = Visa
        fields = ['visa_type', 'issue_date', 'expiry_date','visa_issue_country', 'passport_country']
        

class EmployeeDocumentForm(forms.ModelForm):
    class Meta:
        model = EmployeeDocument
        fields = ['document_name', 'uploaded_file'] 


        

