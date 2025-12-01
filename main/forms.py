from django import forms
from django.db import models
from .models import Comment, Blog, Product

class FeedbackForm(forms.Form):
    name = forms.CharField(label="Ваше имя", required=True)
    email = forms.EmailField(label="Ваш Email", required=True)
    rating = forms.ChoiceField(
        label="Оцените сайт",
        choices=[("1", "1 - Плохо"), ("2", "2 - Средне"), ("3", "3 - Хорошо"), ("4", "4 - Отлично"), ("5", "5 - Великолепно")],
        widget=forms.RadioSelect,
        required=True
    )

    usability = forms.BooleanField(label="Удобство использования", required=False)
    design = forms.BooleanField(label="Дизайн", required=False)
    functionality = forms.BooleanField(label="Функциональность", required=False)
    message = forms.CharField(
        label="Ваш отзыв",
        widget=forms.Textarea(attrs={"rows": 5, "cols": 40}),
        required=True
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  
        fields = ('text',)  
        labels = {'text': "Комментарий"}  


class BlogForm(forms.ModelForm):  # Форма для добавления статьи
    class Meta:
        model = Blog
        fields = ['title', 'short_content', 'full_content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Введите заголовок'}),
            'short_content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Введите краткое содержание'}),
            'full_content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Введите полное содержание'}),
        }
        labels = {
            'title': 'Заголовок',
            'short_content': 'Краткое содержание',
            'full_content': 'Полное содержание',
            'image': 'Изображение',
        }


class ProductForm(forms.ModelForm):  # Форма для добавления товара
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Введите название товара'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Введите описание товара'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Введите цену', 'step': '0.01'}),
            'category': forms.Select(),
        }
        labels = {
            'title': 'Название товара',
            'description': 'Описание',
            'price': 'Цена',
            'category': 'Категория',
            'image': 'Изображение',
        }