from django.db import models


# Create your models here.
class BlogEntry(models.Model):
    """Модель для блоговой записи"""

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержимое")
    preview = models.ImageField(
        upload_to="blog", null=True, blank=True, verbose_name="Превью"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(verbose_name="Отметьте для публикации")
    view_count = models.PositiveIntegerField(
        default=0, verbose_name="Количество просмотров"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        ordering = [
            "created_at",
        ]
        permissions = [
            ("can_unpublish_blogentry", "Can unpublish blogentry"),
        ]
