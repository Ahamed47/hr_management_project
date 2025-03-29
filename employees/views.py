from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import login, get_user_model
from .models import Employee, Visa, EmployeeDocument, Notification
from .forms import EmployeeForm, VisaForm, EmployeeDocumentForm, HRRegistrationForm
from django.conf import settings
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from datetime import timedelta
from django.utils import timezone


# Get the custom user model dynamically
User = get_user_model()

# Check if the logged-in user is HR (superuser)
def is_hr(user):
    return user.is_staff  

# HR Registration View
def hr_register(request):
    if request.method == "POST":
        form = HRRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True  
            if not user.employee_id:
                user.employee_id = f"HR{User.objects.count() + 1}" 
            user.save()
            login(request, user)  # Log in the new user
            return redirect("employee_list")  
    else:
        form = HRRegistrationForm()

    return render(request, "employees/hr_register.html", {"form": form})

# Employee List View (Only HR can see employees)
@user_passes_test(is_hr)
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees})

# Employee Detail View (Shows an employee's details including visas)
@user_passes_test(is_hr)
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    visas = Visa.objects.filter(employee=employee)  
    documents = EmployeeDocument.objects.filter(employee=employee)
    return render(request, 'employees/employee_detail.html', {'employee': employee, 'visas': visas, 'documents': documents})

# AWS SNS Configuration
AWS_REGION = "eu-west-1"  
SNS_TOPIC_ARN = "arn:aws:sns:eu-west-1:050752637269:VisaNotificationTopic"  

def send_sns_notification(entity, entity_type, action, message):
    """Send an email notification using AWS SNS when an Employee is created, updated, or deleted."""
    sns_client = boto3.client(
        "sns",
        region_name=AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    
    if entity_type == "employee":
        subject = f"Employee {action}: {entity.name} ({entity.employee_id})"
    elif entity_type == "visa":
        subject = f"Visa {action} for {entity.employee.name} ({entity.employee.employee_id})"
    else:
        subject = f"{entity_type.capitalize()} {action}"


    response = sns_client.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=message,
        Subject=subject,
    )

    print(f"SNS Notification Sent: {response}")

# Create Employee (Only HR can add employees)
@user_passes_test(is_hr)
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            
            message = f"""
            A new employee has been added:
            -----------------------------
            Name: {employee.name}
            Employee ID: {employee.employee_id}
            Department: {employee.department}
            Added By: HR
            
            Please review the visa details.
            """
            send_sns_notification(employee, "employee" ,"Created", message)

            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form})

# Update Employee (Only HR can update)
@user_passes_test(is_hr)
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            employee = form.save()

            message = f"""
            Employee details have been updated:
            ----------------------------------
            Name: {employee.name}
            Employee ID: {employee.employee_id}
            Department: {employee.department}
            Updated By: HR
            
            Please review the visa details.
            """
            send_sns_notification(employee, "employee" , "Updated", message)

            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/employee_form.html', {'form': form})

# Delete Employee (Only HR can delete)
@user_passes_test(is_hr)
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    
    employee_name = employee.name
    employee_id = employee.employee_id
    employee_department = employee.department

    employee.delete()

    message = f"""
    An employee has been deleted:
    ----------------------------
    Name: {employee_name}
    Employee ID: {employee_id}
    Department: {employee_department}
    Deleted By: HR
           
    Please review the visa details.
    """
    send_sns_notification(employee, "employee" , "Deleted", message)

    return redirect('employee_list')

# Create Visa for an Employee (Only HR can add visas)
@user_passes_test(is_hr)
def visa_create(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == "POST":
        form = VisaForm(request.POST)
        if form.is_valid():
            visa = form.save(commit=False)
            visa.employee = employee
            visa.save()

            message = f"""
            New Visa Added for Employee:
            ---------------------------
            Name: {employee.name}
            Employee ID: {employee.employee_id}
            Visa Type: {visa.visa_type}
            Issue Date: {visa.issue_date}
            Expiry Date: {visa.expiry_date}
            Visa Issue Country: {visa.visa_issue_country}
            Passport Country: {visa.passport_country}
            Added By: HR
            
            Please review the visa details.
            """
            send_sns_notification(visa,"visa", "Added", message)

            return redirect("employee_detail", pk=employee.id)
    else:
        form = VisaForm()

    return render(request, "employees/visa_form.html", {"form": form, "employee": employee})

# Update Visa (Only HR can update visas)
@user_passes_test(is_hr)
def visa_update(request, pk):
    visa = get_object_or_404(Visa, pk=pk)
    
    if request.method == 'POST':
        form = VisaForm(request.POST, instance=visa)
        if form.is_valid():
            form.save()

            message = (f"Visa updated for {visa.employee.name}.\n"
                       f"Employee ID: {visa.employee.employee_id}\n"
                       f"Visa Type: {visa.visa_type}\n"
                       f"New Expiry Date: {visa.expiry_date}\n"
                       f"Updated By: HR\n\n"

                       f"Please review the visa details.")
            send_sns_notification(visa ,"visa", "Updated", message)
            
            return redirect('employee_detail', pk=visa.employee.id)
    else:
        form = VisaForm(instance=visa)
    
    return render(request, 'employees/visa_form.html', {'form': form, 'employee': visa.employee})

# Delete Visa (Only HR can delete visas)
@user_passes_test(is_hr)
def visa_delete(request, pk):
    visa = get_object_or_404(Visa, pk=pk)
    employee = visa.employee

    visa_type = visa.visa_type
    
    visa.delete()

    message = (f"Visa deleted for {employee.name}.\n"
               f"Employee ID: {employee.employee_id}\n"
               f"Deleted Visa Type: {visa_type}\n"
               f"Deleted By: HR\n\n"
               

               f"Please review the visa details.")
    send_sns_notification(visa,"visa", "Deleted", message)

    return redirect('employee_detail', pk=employee.id)




@user_passes_test(is_hr)
def upload_employee_document(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == "POST":
        form = EmployeeDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.employee = employee

            try:
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_S3_REGION_NAME
                )
                
                file = request.FILES['uploaded_file']
                file_name = file.name
                
            
                s3.upload_fileobj(
                    file,
                    settings.AWS_STORAGE_BUCKET_NAME,
                    f'{settings.AWS_LOCATION}/{file_name}',  
                    ExtraArgs={'ContentType': file.content_type}
                )

                
                document.uploaded_file = file_name
                document.save()
                
                print(f"Document uploaded to S3 with URL: {settings.MEDIA_URL}{file.name}")
                return redirect('employee_detail', pk=employee.id)
            
            except NoCredentialsError:
                print("AWS credentials not provided or invalid.")
            except PartialCredentialsError:
                print("Incomplete AWS credentials provided.")
            except Exception as e:
                print(f"An error occurred while uploading: {str(e)}")
    else:
        form = EmployeeDocumentForm()

    return render(request, 'employees/document_upload_form.html', {'form': form, 'employee': employee})



@user_passes_test(is_hr)
def delete_employee_document(request, document_id, employee_id):
    document = get_object_or_404(EmployeeDocument, id=document_id, employee_id=employee_id)

    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        
        file_key = f"{settings.AWS_LOCATION}/{document.uploaded_file}"
        
        s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file_key)
        
        print(f"File {file_key} successfully deleted from S3.")

    except NoCredentialsError:
        print("AWS credentials not provided or invalid.")
    except PartialCredentialsError:
        print("Incomplete AWS credentials provided.")
    except Exception as e:
        print(f"An error occurred while deleting from S3: {str(e)}")

    document.delete()
    print("Document record successfully deleted from the database.")

    return redirect('employee_detail', pk=employee_id)



def employee_list(request):
    employees = Employee.objects.all()

    notification_message = None
    today = timezone.now().date()
    expiry_threshold = today + timedelta(days=30)
    expiring_visas = Visa.objects.filter(expiry_date__lte=expiry_threshold)

    if expiring_visas.exists():
        expiring_visa = expiring_visas.first()
        employee = expiring_visa.employee
        notification_message = f"The visa of {employee.name} (ID: {employee.employee_id}) is going to expire in less than 30 days."

    return render(request, 'employees/employee_list.html', {'employees': employees, 'notification_message': notification_message})



