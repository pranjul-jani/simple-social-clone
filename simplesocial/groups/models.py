from django.db import models
from django.urls import reverse
# get the current user
from django.contrib.auth import get_user_model

# allows us to remove any characters that are not alpha-numeric, '_' or '-' ,
# it is used if we want to use a string that has spaces in it to be used as a part of url,
# slugify will lower case it and convert spaces into dashes so that it can be used as an url
from django.utils.text import slugify

# use markdown text (link embedding) into description
import misaka

# get info from the current user session
User = get_user_model()

# this is how we can use custom template tags
from django import template
register = template.Library()


# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User, through='GroupMember')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('groups:single', kwargs={'slug':self.slug})


    class Meta:
        ordering = ['name']


class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name='memberships', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_groups', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


    class Meta:
        unique_together = ('group', 'user')













