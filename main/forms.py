from django import forms
from .models import CustomUser, Profile, Role, Ad
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.forms import ImageField, FileInput

class ProfileForm(forms.ModelForm):
    image_link=ImageField(widget=FileInput)
    class Meta:
        model = Profile
        fields = ['phone_number', 'role','image_link']

        widgets = {
            'phone_number': forms.TextInput(
            attrs={
                'class': 'registration__form__inputs-pair-input',
                'placeholder': 'Введите номер телефона'
            }),
            'role': forms.RadioSelect(attrs={'class': 'registration__form__inputs-pair-input-radio'}),
        }

class ProfileEditForm(ProfileForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ProfileEditForm, self).__init__(*args, **kwargs)



class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'surname',  'email', 'password']
        
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'registration__form__inputs-pair-input',
                    'placeholder': 'Введите имя'
                }),
            'surname': forms.TextInput(
                attrs={
                    'class': 'registration__form__inputs-pair-input',
                    'placeholder': 'Введите фамилию'
                }),
            'email': forms.EmailInput(
                attrs={
                    'class': 'registration__form__inputs-pair-input',
                    'placeholder': 'Введите почту'
                }),
            'password': forms.PasswordInput(
                attrs={
                    'class': 'registration__form__inputs-pair-input',
                    'placeholder': 'Введите пароль'
                }),
        }

    def init(self, *args, **kwargs):
        super().init(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-class'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()
        return user
    
class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'surname',  'email']
        
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'registration__form__inputs-pair-input',
                    'placeholder': 'Введите имя'
                }),
            'surname': forms.TextInput(
                attrs={
                    'class': 'registration__form__inputs-pair-input',
                    'placeholder': 'Введите фамилию'
                }),
            'email': forms.EmailInput(
                attrs={
                    'class': 'registration__form__inputs-pair-input',
                    'placeholder': 'Введите почту'
                }),
        }


class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['password']
        exclude = ['email']
    
class AdCreateForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['user', 'title', 'company_name', 'image_link', 'description', 'cost']

        widgets = {
            'user': forms.HiddenInput(),
            'title': forms.TextInput(
                attrs={
                    'class': 'text-field__input',
                    'placeholder': "Введите название"
                }
            ),
            'company_name': forms.TextInput(
                attrs={
                    'class': 'text-field__input',
                    'placeholder': "Введите название компании"
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': "Опишите свой товар/услугу (максимум 200 символов)"
                }
            ),
            'cost': forms.NumberInput(
                attrs={
                    'class': 'text-field__input',
                    'placeholder': "Введите цену",
                    'style': "width:50%;"
                }
            ),
        }
