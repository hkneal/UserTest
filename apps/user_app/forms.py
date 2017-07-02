from django import forms
from .models import UserName, Message, Comment
from django.core.exceptions import ValidationError
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

def validateName(strInput):
    if not strInput.isalpha():
        return False
    return True

def hasNumbers(strInput):
    return any(char.isdigit() for char in strInput)

def hasUpper(strInput):
    return any(char.isupper() for char in strInput)

ADMIN_CHOICES = [
    ('Normal', 'Normal'),
    ('Admin', 'Admin'),
    ]

class add_message_form(forms.Form):
    message = forms.CharField(label="", widget=forms.Textarea(attrs={'rows': 4, 'cols': 80}), required=True)

class add_comment_form(forms.Form):
    comment = forms.CharField(label="", widget=forms.Textarea(attrs={'rows': 4, 'cols': 70}), initial='write a message', required=True)

class change_password_form(forms.Form):
    password = forms.CharField(label='Password:', max_length=255, min_length=8, required=True, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password:', max_length=255, min_length=8, required=True, widget=forms.PasswordInput)

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise ValidationError('Passwords must contain as least 8 characters/numbers')
        elif not hasNumbers(password):
            raise ValidationError('Password should contain at least 1 number!')
        elif not hasUpper(password):
            raise ValidationError('Passwords require at least 1 uppercase letter!')
        return password

    def clean_confirm_password(self):
        form_data = self.cleaned_data
        password = form_data.get('password')
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('Password and Confirm Password must match')
        return confirm_password

class update_info_form(forms.Form):
    email = forms.EmailField(label='Email:', max_length=45, min_length=7, required=True, widget=forms.EmailInput)
    first_name = forms.CharField(label='First Name:', max_length=45, min_length=2, required=True)
    last_name = forms.CharField(label='Last Name:', max_length=45, min_length=2, required=True)
    admin_level = forms.ChoiceField(choices=(ADMIN_CHOICES))

    def clean_email(self):
        thisEmail = self.cleaned_data['email']
        if not EMAIL_REGEX.match(thisEmail):
            raise ValidationError('Please enter a valid email address')
        return thisEmail

    def clean_first_name(self):
        firstName = self.cleaned_data['first_name']
        if not validateName(firstName):
            raise ValidationError('First name should be greater than 2 characters and less than 45 characters and should not contain numbers or symbols')
        return firstName

    def clean_last_name(self):
        lastName = self.cleaned_data['last_name']
        if not validateName(lastName):
            raise ValidationError('Last name should be greater than 2 characters and less than 45 characters and should not contain numbers or symbols')
        return lastName

class signin_form(forms.Form):
    email = forms.EmailField(label='Email Address:', max_length=45, min_length=7, required=True, widget=forms.EmailInput)
    password = forms.CharField(label='Password:', max_length=255, min_length=8, required=True, widget=forms.PasswordInput)

    def clean_email(self):
        thisEmail = self.cleaned_data['email']
        if not UserName.objects.filter(email=thisEmail).exists():
            raise ValidationError('You Must Register First!')
        return thisEmail

    def clean_password(self):
        form_data = self.cleaned_data
        password = self.cleaned_data['password']
        email = form_data.get('email')
        try:
            user = UserName.objects.get(email = email)
        except:
            raise ValidationError('You Must Register First!')
        hashed_pw = user.password
        if bcrypt.hashpw(password.encode(encoding="utf-8", errors="strict"), hashed_pw.encode(encoding="utf-8", errors="strict")) != hashed_pw:
            raise ValidationError('Incorrect password!')
        return password

class register_form(forms.Form):
    email = forms.EmailField(label='Email:', max_length=45, min_length=7, required=True, widget=forms.EmailInput)
    first_name = forms.CharField(label='First Name:', max_length=45, min_length=2, required=True)
    last_name = forms.CharField(label='Last Name:', max_length=45, min_length=2, required=True)
    password = forms.CharField(label='Password:', max_length=255, min_length=8, required=True, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password:', max_length=255, min_length=8, required=True, widget=forms.PasswordInput)

    def clean_email(self):
        thisEmail = self.cleaned_data['email']
        if UserName.objects.filter(email=thisEmail).exists():
            raise ValidationError('Email already exists!')
        elif not EMAIL_REGEX.match(thisEmail):
            raise ValidationError('Please enter a valid email address')
        return thisEmail

    def clean_first_name(self):
        firstName = self.cleaned_data['first_name']
        if not validateName(firstName):
            raise ValidationError('First name should be greater than 2 characters and less than 45 characters and should not contain numbers or symbols')
        return firstName

    def clean_last_name(self):
        lastName = self.cleaned_data['last_name']
        if not validateName(lastName):
            raise ValidationError('Last name should be greater than 2 characters and less than 45 characters and should not contain numbers or symbols')
        return lastName

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise ValidationError('Passwords must contain as least 8 characters/numbers')
        elif not hasNumbers(password):
            raise ValidationError('Password should contain at least 1 number!')
        elif not hasUpper(password):
            raise ValidationError('Passwords require at least 1 uppercase letter!')
        return password

    def clean_confirm_password(self):
        form_data = self.cleaned_data
        password = form_data.get('password')
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('Password and Confirm Password must match')
        return confirm_password
