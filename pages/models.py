from django.db import models

# Create your models here.


class NewsLetter(models.Model):
    email = models.EmailField()

    class Meta:
        app_label = 'blog'

    def __str__(self):
        return self.email