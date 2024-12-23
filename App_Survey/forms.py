from django import forms
from .models import Complain, Profile, UserProfile
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

class ComplainForm(forms.ModelForm):
    class Meta:
        model = Complain
        fields = ['student_name', 'student_id', 'category', 'problem_details', 'invoice_no', 'invoice_image', 'complain_image']

    def clean_student_id(self):
        student_id = self.cleaned_data['student_id']
        if not re.match(r'^\d{8}$', student_id):  # 8 digits validation
            raise forms.ValidationError("Student ID must be exactly 8 digits.")
        if student_id == '12345678':  # Avoid serial number
            raise forms.ValidationError("Student ID cannot be 12345678.")
        return student_id
    
    def clean_invoice_no(self):
        invoice_no = self.cleaned_data['invoice_no']
        if not re.match(r'^\d{6}$', invoice_no):  # 6 digits validation
            raise forms.ValidationError("Invoive No must be exactly 6 digits.")
        if invoice_no == '123456':  # Avoid serial number
            raise forms.ValidationError("Invoive No cannot be 123456.")
        
        # Check if invoice_no already exists
        if Complain.objects.filter(invoice_no=invoice_no).exists():
            raise ValidationError("A complaint with this Invoice No already exists. Please provide a different Invoice No.")
        
        return invoice_no
    
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Complain
        fields = ['student_name', 'student_id', 'problem_details']

    def clean_student_id(self):
        student_id = self.cleaned_data['student_id']
        if not re.match(r'^\d{8}$', student_id):
            raise forms.ValidationError("Student ID must be exactly 8 digits.")
        return student_id

class ResolveForm(forms.ModelForm):
    class Meta:
        model = Complain
        fields = ['solution_details', 'feedback_status', 'is_feedback', 'resolved_image', 'resolved_at']
        widgets = {
            'solution_details': forms.Textarea(attrs={'class': 'form-control styled-textarea'}),
            'is_feedback': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'feedback_status': forms.Select(attrs={'class': 'form-control custom-select'}),
            'resolved_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'resolved_at': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                },
                format='%Y-%m-%dT%H:%M'
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.resolved_at:
            self.fields['resolved_at'].initial = self.instance.resolved_at.strftime('%Y-%m-%dT%H:%M')

    def clean_resolved_at(self):
        resolved_at = self.cleaned_data['resolved_at']
        if resolved_at:
            return resolved_at
        else:
            return None 

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
        widgets = {
            'address1': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'joined_date': forms.DateInput(attrs={'class': 'form-control'}),
        }

class UserProfileCreationForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ['email', 'name',  'is_superuser', 'is_staff', 'is_active']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

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

