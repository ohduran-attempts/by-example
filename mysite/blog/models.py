from django.conf import settings
from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone


class PublishedManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES_TPL = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    objects = models.Manager()
    published = PublishedManager()

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES_TPL,
                              default='draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('blog:post_detail',
                            args=[self.publish.year,
                                  self.publish.month,
                                  self.publish.day,
                                  self.slug])
