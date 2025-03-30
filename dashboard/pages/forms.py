from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    group_name = forms.CharField(max_length=100, required=True)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'group_name', 'password1', 'password2')
    
    def clean_group_name(self):
        group_name = self.cleaned_data.get('group_name')
        if CustomUser.objects.filter(group_name=group_name).exists():
            raise forms.ValidationError('This group name is already taken.')
        return group_name
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email 