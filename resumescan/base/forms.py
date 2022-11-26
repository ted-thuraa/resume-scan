from dataclasses import fields
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Cvuploads

class CvUploadsform(ModelForm):
    class Meta:
        model = Cvuploads
        fields = '__all__'
        exclude = ['user']

    #def __init__(self, *args, **kwargs):
    #        super(CvUploadsform, self).__init__(*args, **kwargs)
    #        for field_name, field in self.fields.items():
    #            field.widget.attrs['class'] = 'form-control'