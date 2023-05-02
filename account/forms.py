from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
from .models import User,UserManager

#회원가입에서 사용되는 UserCreateForm을 수정
class UserCreateForm(forms.ModelForm):
    #회원가입(회원아이디, 이메일, 비밀번호
    user_id=forms.CharField(
        label=('User ID'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder':_('User ID'),
                'required': 'True',
            }
        )
    )
    email = forms.EmailField(
        label=('Email'),
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder':_('Email address'),
                'required': 'True',
            }
        )
    )
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Password'),
                'required': 'True',
            }
        )
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Password confirmation'),
                'required': 'True',
            }
        )
    )

    class Meta:
        model = User
        fields = ('login_id', 'email')

        def clean_password2(self):
            #프론트가 두 비밀번호 입력 일치 확인
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError("Passwords don't match")
            return password2

        def save(self, commit=True):
            # Save the provided password in hashed format
            user = super(UserCreateForm, self).save(commit=False)
            user.user_id = UserManager.normalize_email(self.cleaned_data['login_id'])
            user.set_password(self.cleaned_data["password1"])
            if commit:
                user.save()
            return user