from django import forms
from django.contrib.auth import authenticate
from .models import User

class RegisterForm(forms.ModelForm):
    pin = forms.CharField(
        max_length=4,
        min_length=4,
        widget=forms.PasswordInput,
        label="4-digit PIN"
    )
    confirm_pin = forms.CharField(
        max_length=4,
        min_length=4,
        widget=forms.PasswordInput,
        label="Confirm PIN"
    )

    class Meta:
        model = User
        fields = ['phone_number']

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError("This phone number is already registered.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        pin = cleaned_data.get('pin')
        confirm_pin = cleaned_data.get('confirm_pin')
        if pin and confirm_pin and pin != confirm_pin:
            raise forms.ValidationError("PINs do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # PIN is stored as a hashed password
        user.set_password(self.cleaned_data['pin'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    phone_number = forms.CharField(max_length=15, label="Phone Number")
    pin = forms.CharField(max_length=4, widget=forms.PasswordInput, label="4-digit PIN")

    def clean(self):
        phone = self.cleaned_data.get('phone_number')
        pin = self.cleaned_data.get('pin')
        if phone and pin:
            user = authenticate(phone_number=phone, pin=pin)
            if user is None:
                raise forms.ValidationError("Invalid phone number or PIN.")
            self.user = user
        return self.cleaned_data
