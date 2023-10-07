from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from PIL import Image
import os


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'pk': self.pk})


class Post(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Принято в работу'),
        ('completed', 'Выполнено'),
    ]

    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    comment = models.TextField(null=True, blank=True)
    image_after = models.ImageField(upload_to='images', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and image.size > 2 * 1024 * 1024:
            raise ValidationError("Размер изображения не должен превышать 2 МБ")

        ext = os.path.splitext(image.name)[1]
        valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']

        if not ext.lower() in valid_extensions:
            raise ValidationError("Неподдерживаемый формат изображения. Поддерживаемые форматы: JPG, JPEG, PNG, BMP")
        try:
            with Image.open(image) as img:
                pass
        except:
            raise ValidationError("Невозможно открыть изображение. Проверьте, что файл является изображением")

        return image