"""
Accounts forms
Mostafa Rasouli
mostafarasooli54@gmail.com
feb 2024
"""

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from accounts.models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='رمز عبور')
    password2 = forms.CharField(widget=forms.PasswordInput, label='تکرار رمز عبور')

    class Meta:
        model = User
        fields = ('email', 'phone', 'first_name', 'last_name', 'gender', 'age', 'marital')

    def clean(self):
        cd = super().clean()
        passwd1 = cd.get('password1')
        passwd2 = cd.get('password2')

        if passwd1 and passwd2 and passwd1 != passwd2:
            raise ValidationError('رمز های عبور باهم مطابقت ندارند!')
        elif len(passwd2) < 8:
            raise ValidationError('رمز عبور حداقل باید 8 حرف باشد!')
        elif not any(i.isalpha() for i in passwd2):
            raise ValidationError('رمز عبور باید شامل حداقل 1 حرف باشد!')
        elif not any(i.isupper() for i in passwd2):
            raise ValidationError('رمز عبور باید شامل حداقل یک حرف بزرگ باشد!')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text='برای تغییر رمز عبور <a href="../password/">کلیک کنید</a>',
                                         label='رمز عبور')

    class Meta:
        model = User
        fields = '__all__'


class UserLoginForm(forms.Form):
    phone = forms.CharField()

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if len(phone) != 11 or phone[:2] != '09':
            raise ValidationError('شماره وارد شده اشتباه است!')

        return phone


class OtpForm(forms.Form):
    otp = forms.CharField()
