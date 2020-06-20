from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm

from django.apps import apps
Chapter = apps.get_model('theoryTag', 'Chapter')
Subject = apps.get_model('theoryTag', 'Subject')
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    username = forms.CharField(max_length=254, required=True)
    chapter = forms.ModelChoiceField(queryset=Chapter.objects.all())
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'subject', 'chapter')

class SignInForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
        