from django import forms
from .models import UserData

class UserDataForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ('name', 'country', 'phone', 'email', 'source')
        widgets = {
            'name': forms.TextInput(attrs={'required': False}),
            'country': forms.TextInput(attrs={'required': False}),
            'phone': forms.TextInput(attrs={'required': False}),
            'email': forms.EmailInput(attrs={'required': False}),
            'source': forms.TextInput(attrs={'required': False}),
        }