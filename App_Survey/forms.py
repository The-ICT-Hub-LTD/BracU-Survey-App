from django import forms
from .models import Complain

class ComplainForm(forms.ModelForm):
    class Meta:
        model = Complain
        fields = ['student_name', 'student_id', 'problem_details', 'complain_image']

class ResolveForm(forms.ModelForm):
    class Meta:
        model = Complain
        fields = ['resolved_image', 'solution_details']
