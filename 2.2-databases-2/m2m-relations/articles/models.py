from django.db import models
from django.core.exceptions import ValidationError

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    tags = models.ManyToManyField(
        Tag,
        through='Scope',
        related_name='articles'
    )
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def main_scope(self):
        """Возвращает основной тег статьи"""
        return self.scopes.filter(is_main=True).first()


class Scope(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='scopes'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='scopes'
    )
    is_main = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Связь статьи с разделом'
        verbose_name_plural = 'Связи статей с разделами'
        unique_together = ('article', 'tag')
        ordering = ['-is_main', 'tag__name']

    def __str__(self):
        return f'{self.article} — {self.tag}{" (Основной)" if self.is_main else ""}'

    def clean(self):
        """Проверка, что только один основной тег на статью"""
        if self.is_main:
            existing_main = Scope.objects.filter(article=self.article, is_main=True)
            if self.pk:
                existing_main = existing_main.exclude(pk=self.pk)
            if existing_main.exists():
                raise ValidationError('У статьи может быть только один основной тег')