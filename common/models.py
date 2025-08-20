from django.db import models
from django.contrib.auth import get_user_model
from markdown import markdown

User = get_user_model()
MD_EXTENSIONS = [
    "fenced_code",   # ```кодовые блоки```
    "tables",        # таблицы
    "toc",           # оглавление (если нужно)
    "sane_lists",    # списки
    "smarty",        # типографика
    "codehilite",    # подсветка кода (нужен CSS)
]
class Draft(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content_md = models.TextField(blank=True)  # Markdown
    content_html = models.TextField(blank=True)  # Rendered HTML
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.content_html = markdown(self.content_md or "", extensions=MD_EXTENSIONS)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Draft by {self.author} ({self.updated_at})"


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content_md = models.TextField()
    content_html = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def publish_from_draft(cls, draft, title):
        return cls.objects.create(
            author=draft.author,
            title=title,
            content_md=draft.content_md,
            content_html=markdown(draft.content_md or "", extensions=MD_EXTENSIONS),
        )

    def __str__(self):
        return self.title
