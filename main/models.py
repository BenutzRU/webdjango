from django.db import models
from django.contrib import admin
from django.urls import reverse
from datetime import datetime

class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    short_content = models.TextField(verbose_name="Краткое содержание")
    full_content = models.TextField(verbose_name="Полное содержание")
    posted = models.DateTimeField(default=datetime.now, db_index=True, verbose_name="Опубликована")

    def get_absolute_url(self):
        return reverse('blog_detail', args=[str(self.id)])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статья блога"
        verbose_name_plural = "Статьи блога"
        ordering = ['-posted']

admin.site.register(Blog)