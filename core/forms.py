from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from core.models import News, Section, Authors, Post, Profile
from django.contrib.auth.models import User


class NewsForm(ModelForm):
    title = forms.CharField(label="Название новости", required=True)
    topic = forms.ModelMultipleChoiceField(label="Раздел(ы) новости", queryset=Section.objects.all())
    summary = forms.CharField(widget=forms.Textarea, label="Содержание новости", required=True)
    picture = forms.FileField(label="Картинка для новости", required=False)
    auth_opinion = forms.CharField(widget=forms.Textarea, label="Мнение автора новости", required=False)
    authors = forms.ModelChoiceField(label="Автор новости", queryset=Authors.objects.all())
    source = forms.URLField(label="Источник новости", required=False)
    active = forms.BooleanField(label="Активна ли новость?")

    def clean_title(self):
        name = self.cleaned_data['title']
        if name.isdigit():
            raise forms.ValidationError('Название не должно являться числом!')
        return name

    class Meta:
        model = News
        fields = "__all__"


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=255)
    username = forms.CharField(label="Никнейм на сайте")
    first_name = forms.CharField(label="Имя пользователя (нигде не используется)")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2',)


class DiscussionForm(UserCreationForm):
    title = forms.CharField(label="Название обсуждения")
    topic = forms.ModelMultipleChoiceField(label="Раздел(ы) обсуждения", queryset=Section.objects.all())
    caption = forms.CharField(widget=forms.Textarea, label="Содержание новости", required=True)
    image = forms.FileField(label="Картинка для обсуждения", required=False)

    class Meta:
        model = Post
        fields = ['title', 'topic', 'caption', 'image']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(max_length=255)
    username = forms.CharField(label="Никнейм на сайте")
    first_name = forms.CharField(label="Имя пользователя (нигде не используется)")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image']
