from django import forms
from .models import Complain, Profile
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.forms import AuthenticationForm

class ComplainForm(forms.ModelForm):
    class Meta:
        model = Complain
        fields = ['student_name', 'student_id', 'problem_details', 'complain_image']

    def clean_student_id(self):
        student_id = self.cleaned_data['student_id']
        if not re.match(r'^\d{8}$', student_id):  # 8 digits validation
            raise forms.ValidationError("Student ID must be exactly 8 digits.")
        if student_id == '12345678':  # Avoid serial number
            raise forms.ValidationError("Student ID cannot be 12345678.")
        return student_id

class ResolveForm(forms.ModelForm):
    class Meta:
        model = Complain
        fields = ['solution_details', 'feedback_status', 'resolved_image']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)

# class AdminLoginForm(forms.Form):
#     email = forms.EmailField(label='Email', max_length=255)
#     password = forms.CharField(widget=forms.PasswordInput, label='Password')

#     def clean(self):
#         cleaned_data = super().clean()
#         email = cleaned_data.get('email')
#         password = cleaned_data.get('password')
#         return cleaned_data



class AdminLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email',
        'required': 'required',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'required': 'required',
    }))

    class Meta:
        fields = ['username', 'password']