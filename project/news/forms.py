from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
    description = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = ['header',
                  'text',
                  'category',
                  'author']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        description = cleaned_data.get("description")
        if name == description:
            raise ValidationError({
                "description": "Описание должно отличаться от названия."
            })
        return cleaned_data


class LetterForm(forms.Form):
    theme = forms.CharField(label='Тема')
    text = forms.CharField(label='Текст')
