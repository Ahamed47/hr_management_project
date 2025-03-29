from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Employee, Visa

# Register CustomUser with UserAdmin to use Django's built-in user management features
admin.site.register(CustomUser, UserAdmin)

# Register Employee and Visa models
admin.site.register(Employee)
admin.site.register(Visa)



