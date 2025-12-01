from django.db import models
from django.contrib import admin
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.models import User

class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    short_content = models.TextField(verbose_name="Краткое содержание")
    full_content = models.TextField(verbose_name="Полное содержание")
    posted = models.DateTimeField(default=datetime.now, db_index=True, verbose_name="Опубликована")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True, verbose_name="Изображение")  
    

    def get_absolute_url(self):
        return reverse('blog_detail', args=[str(self.id)])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статья блога"
        verbose_name_plural = "Статьи блога"
        ordering = ['-posted']
        

class Comment(models.Model):
    text = models.TextField(verbose_name="Комментарий")
    date = models.DateTimeField(default=datetime.now, verbose_name="Дата добавления")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="Статья")

    def __str__(self):
        return f"Комментарий от {self.author} к {self.post}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-date']


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('mountain', 'Горные велосипеды'),
        ('road', 'Шоссейные велосипеды'),
        ('city', 'Городские и прогулочные велосипеды'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Название товара")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="Категория")
    image = models.ImageField(upload_to='shop_images/', null=True, blank=True, verbose_name="Изображение")
    created = models.DateTimeField(default=datetime.now, verbose_name="Дата добавления")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created']


admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Product)