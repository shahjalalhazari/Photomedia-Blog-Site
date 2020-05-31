from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from .utils import generate_unique_slug

# CATEGORY MODEL
class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Category Name', unique=True)
    image = models.ImageField(upload_to='category_images')

    def __str__(self):
        return self.name


# BLOG MODEL
class Blog(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blog_category')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_author')
    title = models.CharField(max_length=264, verbose_name='Put your title')
    slug = models.SlugField(unique=True, max_length=300, blank=True)
    body = models.TextField(verbose_name="What's in your mind?")
    image = models.ImageField(upload_to='blog_images', verbose_name='Image')
    publish = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publish']

    def save(self, *args, **kwargs):
        if self.slug:
            if slugify(self.title) != self.slug:
                self.slug = generate_unique_slug(Blog, self.title)
        else:
            self.slug = generate_unique_slug(Blog, self.title)
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


# COMMENT MODEL
class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    comment = models.TextField(verbose_name='Comment')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.comment


# BLOG LIKE MODEL
class Like(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_like')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')

    def __str__(self):
        return "{} likes {}".format(self.user.username, self.blog)