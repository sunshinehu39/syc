# -*- coding:utf-8 -*-
from django import forms
from django.forms import Textarea,TextInput,RadioSelect,FileInput,URLInput,DateTimeInput

from django.contrib.auth.forms import UserCreationForm
from .models import User,GoldenWords,Member

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

class GoldenWordsForm(forms.ModelForm):
    class Meta:
        model = GoldenWords
        fields = ['publisher', 'copyright','content','photo','application']
        widgets = {
            'content':Textarea(attrs={'class':"content"}),
            'application': TextInput(attrs={'class': "application"}),
            'copyright': RadioSelect(attrs={'class': "copyright"}),
            'photo': FileInput(attrs={'class': "photo",
                                      'value': "配图",
                                      'accept':"image/*",
                                      }),
        }
