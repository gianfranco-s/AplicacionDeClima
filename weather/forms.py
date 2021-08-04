from typing import Text
from django.forms import ModelForm, TextInput
from .models import City

class CityForm (ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {'name' : TextInput(attrs={'class' : 'input','placeholder':'Escribí acá una ciudad'})}