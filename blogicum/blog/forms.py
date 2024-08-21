from django import forms

from .models import Post, Comment, User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'pub_date', 'location', 'category', 'image')
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        help_texts = {
            'email': 'Введите корректный адрес электронной почты.'
        }
        error_messages = {
            'first_name': {
                'required': 'Пожалуйста, введите своё имя.'
            }
        }
        widgets = {
            'email': forms.EmailInput()
        }
