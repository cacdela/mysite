from django import forms
from .models import Post, Category


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['user']
        fields = ['title', 'content', 'image', 'category', 'status', 'comment', 'image_after']
        widgets = {
            'status': forms.Select(attrs={'class': 'custom-select'}),
            'category': forms.Select(attrs={'class': 'custom-select'}),
        }
        labels = {
            "status": "Статус",
            "title": "Название",
            "content": "Содержание",
            "image": "Изображение",
            "category": "Категория",
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["title"]