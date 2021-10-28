from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse


def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slug + get_random_string(length=5)
    return unique_slug


class Topic(models.Model):
    title = models.CharField(max_length=250, unique=True)
    about = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        )
    title = models.CharField(max_length=250)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,
                              related_name='posts')
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='draft')

    class Meta:
        ordering = ['-published']

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.title))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    blog = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.user} on {self.blog}'
