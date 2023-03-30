from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *

class SignUpForm(UserCreationForm):
    password2 = forms.CharField(label='Confirm Password (again)',widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        labels = {'email':'Email'}

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['blood_group','mobile_no','addr','date_of_birth','image']

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['experience','specialist','service','clinic','cl_address','daystiming','timing','gender','biography','mobile_no','addr','date_of_birth','image','price']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['a_date','status','p_status','from_time','to_time']



class MedicalForm(forms.ModelForm):
    class Meta:
        model = Medical
        fields = ['mobile_no','name','foundation_date','timing','days_time','addr','image','experience']

