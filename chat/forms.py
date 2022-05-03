from django import forms
from .models import ChatUser, ChatModel


class RegisterForm(forms.ModelForm):
    '''
    Класс формы регистрации новых пользователей
    (потом как-нибудь дополнить все окмменты чем то осмысленным)
    '''
    password1 = forms.CharField(label='Придумайте пароль',
                                max_length=30,
                                widget=forms.PasswordInput,
                                required=True)
    password2 = forms.CharField(label='Повторите пароль',
                                max_length=30,
                                widget=forms.PasswordInput,
                                required=True)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    class Meta:
        model = ChatUser
        fields = ('username', 'photo')
        labels = {'username': 'Ваше имя пользователя', 'photo': 'Фото профиля'}

class AddChatForm(forms.ModelForm):
    '''
    Форма добавления чата
    '''
    class Meta:
        model = ChatModel
        fields = ('chat_name', 'slug')
        labels = {'chat_name': 'Название чата', 'slug': 'вид url до чата'}

