from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from add_road_user.models import create_roadUser


    


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2',"is_customer", 'mobile']

class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', "first_name", "last_name", "is_employee","is_admin", 'mobile', ]

class AddRoadUserForm(forms.ModelForm):  
    class Meta:  
        model = create_roadUser  
        fields = "__all__"  