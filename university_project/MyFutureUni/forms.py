from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, ProfileUser


class LoginForm(AuthenticationForm):
    username = UsernameField(label='Логин', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    error_messages = {
        'invalid_login': (
            'Не верный логин или пароль'
        )
    }



class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label='Ваше имя', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    last_name = forms.CharField(label='Ваше фамилия', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    email = forms.EmailField(label='Ваша почта', widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))

    username = UsernameField(label='Придумайте логин', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    password1 = forms.CharField(label='Придумайте пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')



class CommentForm(forms.ModelForm):
    text = forms.CharField(label='Оставить комментарий', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'style': 'height: 150px; width: 1000px',
    }))

    class Meta:
        model = Comment
        fields = ('text',)




class EditAccountForm(forms.ModelForm):
    first_name = forms.CharField(label='Ваше имя', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    last_name = forms.CharField(label='Ваша фамилия', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    email = forms.EmailField(label='Ваша почта', widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))

    username = UsernameField(label='Придумайте логин', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    old_password = forms.CharField(required=False, label='Текущий пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    new_password = forms.CharField(required=False, min_length=8, label='Новый пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    new_password2 = forms.CharField(required=False, min_length=8, label='Подтвердить пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username',
                  'old_password', 'new_password', 'new_password2')




class EditProfileUserForm(forms.ModelForm):
    about = forms.CharField(label='О себе', required=False, max_length=300, widget=forms.Textarea(attrs={
        'class': 'form-control'
    }))

    photo = forms.ImageField(label='Фото', required=False, widget=forms.FileInput(attrs={
        'class': 'form-control'
    }))


    class Meta:
        model = ProfileUser
        fields = ('photo', 'about')




