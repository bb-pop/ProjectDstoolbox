from typing import Any
from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class XLSXImportForm(forms.Form):
    xlsx_file = forms.FileField()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['StudentID', 'first_name', 'last_name', 'email']