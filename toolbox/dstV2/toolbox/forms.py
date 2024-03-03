from django import forms
from .models import MyUser, ValidStudentID

class MyUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    student_id = forms.CharField(max_length=11)  # Add the student_id field

    class Meta:
        model = MyUser
        fields = ('student_id', 'level')  # Include student_id in the fields

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_student_id(self):
        student_id = self.cleaned_data['student_id']
        # Check if the student_id is in the list of valid IDs
        if not ValidStudentID.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError("Invalid Student ID.")
        # Check if the student_id is already used
        if MyUser.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError("This Student ID is already registered.")
        return student_id

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.student_id = self.cleaned_data['student_id']  # Set the student_id for the user
        if commit:
            user.save()
        return user
    
class CSVUploadForm(forms.Form):
    file = forms.FileField()
