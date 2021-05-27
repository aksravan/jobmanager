from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import StudentData, Company, CompanyStudents

class StudentForm(ModelForm):
    class Meta:
        model = StudentData
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

class CompanyStudentForm(ModelForm):
    class Meta:
        model = CompanyStudents
        fields = '__all__'