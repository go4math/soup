from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import ObjectDoesNotExist

from .models import User

class loginForm(forms.Form):
    identifier = forms.CharField(label="登录名",max_length=150, required=True)
    password = forms.CharField(label="密码",max_length=16, 
        widget=forms.PasswordInput, required=True)

class registryForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=150, required=True)
    email = forms.EmailField(label='邮箱',required=True, validators=[EmailValidator])
    password = forms.CharField(label='密码',max_length=16, 
        widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(label='确认密码',max_length=16, 
        widget=forms.PasswordInput, required=True)

    def clean_username(self):
        data = self.cleaned_data['username']
        try:
            User.objects.get(username=data)
            self.add_error('username','用户名已被使用.')
        except ObjectDoesNotExist:
            return data

    def clean_email(self):
        data = self.cleaned_data['email']
        try:
            User.objects.get(email=data)
            self.add_error('email','邮箱已被使用.')
        except ObjectDoesNotExist:
            return data

    def clean(self):
        cleaned_data = super().clean()
        pw1 = cleaned_data.get('password')
        pw2 = cleaned_data.get('confirm_password')

        if pw1 != pw2: 
            self.add_error('password', '密码不一致.')

class profileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name','bio','gender','birthday']
        labels = {
            'name':'昵称',
            'bio':'介绍自己',
            'gender': '性别',
            'birthday':'生日',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'class': "materialize-textarea"}),
            'gender': forms.RadioSelect,
            'birthday': #forms.SelectDateWidget(years=list(range(1970,2005,1)), 
                #empty_label=('请选择年','请选择月','请选择日'))
                forms.DateInput(attrs={'class':'datepicker'}),
        }

class commentForm(forms.Form):
    content = forms.CharField(max_length=200, required=True, widget=forms.Textarea)
