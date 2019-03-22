
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django.contrib.contenttypes.models import ContentType
# Create your models here.



class Category(models.Model):
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, editable=False, max_length=60)

    def __str__(self):
        return self.category_name


    def get_absolute_url(self):
        return reverse('article_from_category', args=[str(self.slug)])


    def get_unique_slug(self):
        slug = slugify(self.category_name.replace('ı', 'i').replace('ə', 'e').replace('ö', 'o').replace('ğ', 'g').replace('ç', 'c').replace('ş', 's'))
        unique_slug = slug
        counter = 1
        while Article.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()

        return super(Category, self).save(*args, **kwargs)


    class Meta:
        verbose_name_plural = 'Kateqoriyalar'
        verbose_name = 'Kateqoriya'




class Article(models.Model):

    title = models.CharField(max_length=100, verbose_name='Başlıq')
    article_category = models.ForeignKey(Category, null=False, on_delete=models.DO_NOTHING,  verbose_name='Kateqoriya')
    content = RichTextField(verbose_name='Məzmun')
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name='Paylaşım tarixi')
    update_date = models.DateTimeField(auto_now=True, verbose_name='Yenilənmə tarixi')
    draft = models.BooleanField(default=False, verbose_name='Qaralama yaradılsın?')
    article_image = models.ImageField(null=True, blank=True, verbose_name='Rəsim')
    article_author = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, verbose_name='Yazar', related_name='articles')
    slug = models.SlugField(unique=True, editable=False, max_length=120)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.slug)])

    def get_update_url(self):
        return reverse('article_update', args=[str(self.slug)])

    def get_delete_url(self):
        return reverse('article_delete', args=[str(self.slug)])

    def get_unique_slug(self):
        slug = slugify(self.title.replace('ı', 'i').replace('ə', 'e').replace('ö', 'o').replace('ğ', 'g').replace('ç', 'c').replace('ş', 's'))
        unique_slug = slug
        counter = 1
        while Article.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, counter)
            counter += 1
        return unique_slug


    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()

        return super(Article, self).save(*args, **kwargs)


    class Meta:
        verbose_name_plural = 'Məqalələr'
        verbose_name = 'Məqalə'
        ordering = ['-publish_date']


class Comment(models.Model):
    #article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    commenter_name = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Ad')
    contenttype = models.ForeignKey(to=ContentType, null=True, on_delete=models.CASCADE)
    is_parent = models.BooleanField(default=False)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('contenttype', 'object_id')
    comment_content = models.TextField(verbose_name='Rəy')
    comment_date = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = 'Şərhlər'
        verbose_name = 'Şərh'
        ordering = ['-comment_date']



class Reply(models.Model):
    parent = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    replier_name = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Ad')
    reply_content = models.TextField(verbose_name='Cavab')
    reply_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Cavablar'
        verbose_name = 'Cavab'
        ordering = ['-reply_date']

